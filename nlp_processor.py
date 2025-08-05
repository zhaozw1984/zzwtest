"""
自然语言处理主控制器
整合意图识别、实体抽取和大模型分析功能
"""
from typing import Dict, List, Optional, Any
from loguru import logger

from models import CommandResult, Intent, Entity, ProcessingContext
from intent_classifier import IntentClassifier
from entity_extractor import EntityExtractor
from llm_client import LLMClient
from config import INTENT_TYPES

class NLPProcessor:
    """自然语言处理器"""
    
    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.entity_extractor = EntityExtractor()
        self.llm_client = LLMClient()
        
    def process_command(self, text: str, context: Optional[ProcessingContext] = None) -> CommandResult:
        """处理语音指令"""
        logger.info(f"Processing command: {text}")
        
        # 第一阶段：使用规则和关键词进行初步分析
        rule_based_intent = self.intent_classifier.classify_intent(text)
        rule_based_entities = self.entity_extractor.extract_entities(text)
        
        # 第二阶段：使用大模型进行深度分析
        llm_result = self.llm_client.analyze_command(text)
        
        # 第三阶段：融合结果
        final_intent, final_entities, structured_command = self._merge_results(
            text, rule_based_intent, rule_based_entities, llm_result
        )
        
        # 第四阶段：验证和结构化
        is_valid, validation_errors = self._validate_command(final_intent, final_entities)
        
        # 计算整体置信度
        overall_confidence = self._calculate_confidence(final_intent, final_entities, llm_result)
        
        # 构建结果
        result = CommandResult(
            original_text=text,
            intent=final_intent,
            entities=final_entities,
            confidence=overall_confidence,
            structured_command=structured_command,
            is_valid=is_valid,
            validation_errors=validation_errors
        )
        
        logger.info(f"Command processed: {result.intent.type} with confidence {result.confidence:.2f}")
        return result
    
    def _merge_results(self, text: str, rule_intent: Intent, rule_entities: List[Entity], 
                      llm_result: Optional[Any]) -> tuple:
        """融合规则和大模型的结果"""
        
        # 默认使用规则结果
        final_intent = rule_intent
        final_entities = rule_entities
        structured_command = None
        
        if llm_result:
            # 比较意图识别结果
            if llm_result.intent_confidence > rule_intent.confidence:
                # 使用大模型的意图识别结果
                final_intent = Intent(
                    type=llm_result.intent_type,
                    name=INTENT_TYPES.get(llm_result.intent_type, {}).get("name", "未知"),
                    confidence=llm_result.intent_confidence,
                    description=INTENT_TYPES.get(llm_result.intent_type, {}).get("description", "")
                )
            
            # 合并实体识别结果
            llm_entities = []
            for entity_data in llm_result.entities:
                llm_entity = Entity(
                    type=entity_data["type"],
                    value=entity_data["value"],
                    start=entity_data["start"],
                    end=entity_data["end"],
                    confidence=0.9  # 大模型实体的置信度
                )
                llm_entities.append(llm_entity)
            
            # 合并实体（优先使用大模型结果，补充规则结果）
            final_entities = self._merge_entities(rule_entities, llm_entities)
            
            # 使用大模型的结构化指令
            structured_command = llm_result.structured_command
        
        return final_intent, final_entities, structured_command
    
    def _merge_entities(self, rule_entities: List[Entity], llm_entities: List[Entity]) -> List[Entity]:
        """合并不同来源的实体"""
        merged = []
        
        # 添加大模型实体
        for llm_entity in llm_entities:
            merged.append(llm_entity)
        
        # 添加规则实体（如果不重叠）
        for rule_entity in rule_entities:
            overlapped = False
            for existing in merged:
                if (rule_entity.start < existing.end and rule_entity.end > existing.start):
                    overlapped = True
                    break
            
            if not overlapped:
                merged.append(rule_entity)
        
        # 按位置排序
        merged.sort(key=lambda x: x.start)
        return merged
    
    def _validate_command(self, intent: Intent, entities: List[Entity]) -> tuple:
        """验证指令的完整性"""
        errors = []
        
        if intent.type == "unknown":
            errors.append("无法识别指令意图")
            return False, errors
        
        if intent.type not in INTENT_TYPES:
            errors.append(f"不支持的意图类型: {intent.type}")
            return False, errors
        
        # 检查必需实体
        config = INTENT_TYPES[intent.type]
        required_entities = config.get("required_entities", [])
        entity_types = [entity.type for entity in entities]
        
        missing_entities = []
        for required_entity in required_entities:
            if required_entity not in entity_types:
                missing_entities.append(required_entity)
        
        if missing_entities:
            errors.append(f"缺少必需的实体: {', '.join(missing_entities)}")
        
        is_valid = len(errors) == 0
        return is_valid, errors
    
    def _calculate_confidence(self, intent: Intent, entities: List[Entity], 
                            llm_result: Optional[Any]) -> float:
        """计算整体置信度"""
        # 意图置信度权重0.5
        intent_score = intent.confidence * 0.5
        
        # 实体置信度权重0.3
        if entities:
            entity_score = sum(entity.confidence for entity in entities) / len(entities) * 0.3
        else:
            entity_score = 0.0
        
        # 大模型结果权重0.2
        llm_score = 0.0
        if llm_result:
            llm_score = llm_result.intent_confidence * 0.2
        
        overall_confidence = intent_score + entity_score + llm_score
        return min(1.0, overall_confidence)
    
    def build_structured_command(self, intent: Intent, entities: List[Entity]) -> Dict[str, Any]:
        """构建结构化指令"""
        structured = {
            "action": intent.type,
            "intent_name": intent.name
        }
        
        # 按类型组织实体
        entity_dict = {}
        for entity in entities:
            if entity.type not in entity_dict:
                entity_dict[entity.type] = []
            
            entity_info = {
                "value": entity.value,
                "confidence": entity.confidence
            }
            
            if entity.normalized_value:
                entity_info["normalized"] = entity.normalized_value
            
            entity_dict[entity.type].append(entity_info)
        
        structured["entities"] = entity_dict
        
        # 根据意图类型构建特定结构
        if intent.type == "patrol_inspection":
            structured.update(self._build_patrol_command(entity_dict))
        elif intent.type == "equipment_control":
            structured.update(self._build_control_command(entity_dict))
        elif intent.type == "status_query":
            structured.update(self._build_query_command(entity_dict))
        elif intent.type == "navigation":
            structured.update(self._build_navigation_command(entity_dict))
        
        return structured
    
    def _build_patrol_command(self, entities: Dict[str, List]) -> Dict[str, Any]:
        """构建巡检指令"""
        command = {"command_type": "patrol"}
        
        if "location" in entities:
            locations = entities["location"]
            if locations:
                command["target_location"] = locations[0]["value"]
                if "normalized" in locations[0]:
                    command["location_details"] = locations[0]["normalized"]
        
        if "equipment" in entities:
            equipment = entities["equipment"]
            if equipment:
                command["target_equipment"] = equipment[0]["value"]
        
        if "parameter" in entities:
            parameters = entities["parameter"]
            command["parameters"] = [p["value"] for p in parameters]
        
        return command
    
    def _build_control_command(self, entities: Dict[str, List]) -> Dict[str, Any]:
        """构建控制指令"""
        command = {"command_type": "control"}
        
        if "equipment" in entities:
            equipment = entities["equipment"]
            if equipment:
                command["target_equipment"] = equipment[0]["value"]
        
        if "action" in entities:
            actions = entities["action"]
            if actions:
                command["action"] = actions[0]["value"]
        
        if "value" in entities:
            values = entities["value"]
            if values:
                command["target_value"] = values[0]["value"]
        
        return command
    
    def _build_query_command(self, entities: Dict[str, List]) -> Dict[str, Any]:
        """构建查询指令"""
        command = {"command_type": "query"}
        
        if "equipment" in entities:
            equipment = entities["equipment"]
            if equipment:
                command["target_equipment"] = equipment[0]["value"]
        
        if "parameter" in entities:
            parameters = entities["parameter"]
            command["query_parameters"] = [p["value"] for p in parameters]
        
        return command
    
    def _build_navigation_command(self, entities: Dict[str, List]) -> Dict[str, Any]:
        """构建导航指令"""
        command = {"command_type": "navigation"}
        
        if "location" in entities:
            locations = entities["location"]
            if locations:
                command["destination"] = locations[0]["value"]
                if "normalized" in locations[0]:
                    command["location_details"] = locations[0]["normalized"]
        
        return command