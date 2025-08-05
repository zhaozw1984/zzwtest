"""
实体抽取模块
使用正则表达式和大模型结合的方式提取命名实体
"""
import re
import jieba
from typing import List, Dict, Any, Tuple
from loguru import logger

from models import Entity
from config import ENTITY_TYPES, LOCATION_MAPPING, EQUIPMENT_MAPPING

class EntityExtractor:
    """实体抽取器"""
    
    def __init__(self):
        self.entity_types = ENTITY_TYPES
        self.location_mapping = LOCATION_MAPPING
        self.equipment_mapping = EQUIPMENT_MAPPING
        
        # 编译正则表达式
        self.compiled_patterns = {}
        for entity_type, config in self.entity_types.items():
            patterns = []
            for pattern in config["patterns"]:
                try:
                    patterns.append(re.compile(pattern))
                except re.error as e:
                    logger.warning(f"Invalid regex pattern for {entity_type}: {pattern}, error: {e}")
            self.compiled_patterns[entity_type] = patterns
    
    def extract_entities_regex(self, text: str) -> List[Entity]:
        """使用正则表达式提取实体"""
        entities = []
        
        for entity_type, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                matches = pattern.finditer(text)
                for match in matches:
                    entity = Entity(
                        type=entity_type,
                        value=match.group(),
                        start=match.start(),
                        end=match.end(),
                        confidence=0.9  # 正则匹配的置信度较高
                    )
                    
                    # 标准化实体值
                    normalized_value = self._normalize_entity(entity_type, entity.value)
                    if normalized_value:
                        entity.normalized_value = normalized_value
                    
                    entities.append(entity)
        
        # 去重和合并重叠的实体
        entities = self._deduplicate_entities(entities)
        return entities
    
    def extract_entities_keywords(self, text: str) -> List[Entity]:
        """使用关键词匹配提取实体"""
        entities = []
        
        # 分词
        words = jieba.lcut(text)
        text_lower = text.lower()
        
        # 检查每个实体类型的示例
        for entity_type, config in self.entity_types.items():
            for example in config["examples"]:
                if example in text or example.lower() in text_lower:
                    # 查找在原文中的位置
                    start_pos = text.find(example)
                    if start_pos == -1:
                        start_pos = text_lower.find(example.lower())
                    
                    if start_pos != -1:
                        entity = Entity(
                            type=entity_type,
                            value=example,
                            start=start_pos,
                            end=start_pos + len(example),
                            confidence=0.8
                        )
                        
                        # 标准化实体值
                        normalized_value = self._normalize_entity(entity_type, entity.value)
                        if normalized_value:
                            entity.normalized_value = normalized_value
                        
                        entities.append(entity)
        
        return entities
    
    def _normalize_entity(self, entity_type: str, value: str) -> Dict[str, Any]:
        """标准化实体值"""
        if entity_type == "location":
            if value in self.location_mapping:
                return self.location_mapping[value]
            # 解析复合位置，如"A区2号房"
            zone_match = re.search(r'([A-Z])区', value)
            room_match = re.search(r'(\d+)号房', value)
            result = {}
            if zone_match:
                result["zone"] = zone_match.group(1)
            if room_match:
                result["room"] = room_match.group(1)
            if result:
                result["type"] = "compound"
                return result
                
        elif entity_type == "equipment":
            if value in self.equipment_mapping:
                return self.equipment_mapping[value]
            # 处理带编号的设备
            for base_name, mapping in self.equipment_mapping.items():
                if base_name in value:
                    result = mapping.copy()
                    # 提取编号
                    number_match = re.search(r'\d+', value)
                    if number_match:
                        result["number"] = number_match.group()
                    return result
                    
        elif entity_type == "parameter":
            return {"parameter_type": value, "unit": self._extract_unit(value)}
            
        elif entity_type == "value":
            # 解析数值和单位
            value_match = re.search(r'(\d+\.?\d*)', value)
            unit_match = re.search(r'(°C|%|V|A|Hz)', value)
            if value_match:
                result = {"numeric_value": float(value_match.group(1))}
                if unit_match:
                    result["unit"] = unit_match.group(1)
                return result
        
        return None
    
    def _extract_unit(self, parameter: str) -> str:
        """提取参数单位"""
        unit_mapping = {
            "温度": "°C",
            "湿度": "%",
            "电压": "V", 
            "电流": "A",
            "功率": "W",
            "频率": "Hz",
            "压力": "Pa"
        }
        return unit_mapping.get(parameter, "")
    
    def _deduplicate_entities(self, entities: List[Entity]) -> List[Entity]:
        """去重和合并重叠的实体"""
        if not entities:
            return entities
        
        # 按位置排序
        entities.sort(key=lambda x: (x.start, x.end))
        
        deduplicated = []
        for entity in entities:
            # 检查是否与已有实体重叠
            overlapped = False
            for existing in deduplicated:
                if (entity.start < existing.end and entity.end > existing.start):
                    # 有重叠，保留置信度更高的
                    if entity.confidence > existing.confidence:
                        deduplicated.remove(existing)
                        deduplicated.append(entity)
                    overlapped = True
                    break
            
            if not overlapped:
                deduplicated.append(entity)
        
        return deduplicated
    
    def extract_entities(self, text: str) -> List[Entity]:
        """综合提取实体"""
        # 使用正则表达式提取
        regex_entities = self.extract_entities_regex(text)
        
        # 使用关键词匹配提取
        keyword_entities = self.extract_entities_keywords(text)
        
        # 合并结果
        all_entities = regex_entities + keyword_entities
        
        # 去重
        final_entities = self._deduplicate_entities(all_entities)
        
        logger.info(f"Extracted {len(final_entities)} entities from text: {text}")
        for entity in final_entities:
            logger.debug(f"Entity: {entity.type} = {entity.value} (confidence: {entity.confidence})")
        
        return final_entities