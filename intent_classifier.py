"""
意图识别模块
使用关键词匹配和大模型结合的方式识别用户意图
"""
import re
from typing import Dict, List, Tuple, Optional
from loguru import logger

from models import Intent
from config import INTENT_TYPES

class IntentClassifier:
    """意图分类器"""
    
    def __init__(self):
        self.intent_types = INTENT_TYPES
        
    def classify_intent_keywords(self, text: str) -> List[Tuple[str, float]]:
        """基于关键词匹配的意图识别"""
        intent_scores = {}
        
        text_lower = text.lower()
        
        for intent_type, config in self.intent_types.items():
            score = 0.0
            matched_keywords = 0
            
            # 检查关键词匹配
            for keyword in config["keywords"]:
                if keyword in text or keyword in text_lower:
                    score += 1.0
                    matched_keywords += 1
            
            # 根据匹配的关键词数量计算置信度
            if matched_keywords > 0:
                confidence = min(0.9, score / len(config["keywords"]) + 0.3)
                intent_scores[intent_type] = confidence
        
        # 按置信度排序
        sorted_intents = sorted(intent_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_intents
    
    def classify_intent_rules(self, text: str) -> List[Tuple[str, float]]:
        """基于规则的意图识别"""
        intent_scores = {}
        
        # 巡检相关规则
        if re.search(r'巡检|检查|监测|查看.*?(温度|湿度|电压|电流)', text):
            intent_scores["patrol_inspection"] = 0.95
        
        # 设备控制相关规则
        if re.search(r'(开启|关闭|启动|停止|调节|设置).*?(设备|主柜|副柜|UPS|空调)', text):
            intent_scores["equipment_control"] = 0.95
        
        # 状态查询相关规则
        if re.search(r'(查询|状态|显示|报告).*?(设备|主柜|副柜)', text):
            intent_scores["status_query"] = 0.9
        
        # 报警处理相关规则
        if re.search(r'(报警|警报|确认|处理|消除)', text):
            intent_scores["alarm_handling"] = 0.9
        
        # 导航移动相关规则
        if re.search(r'(前往|移动|到达|回到|导航).*?([A-Z]区|\d+号房)', text):
            intent_scores["navigation"] = 0.9
        
        sorted_intents = sorted(intent_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_intents
    
    def classify_intent(self, text: str) -> Intent:
        """综合意图识别"""
        # 基于关键词的识别
        keyword_results = self.classify_intent_keywords(text)
        
        # 基于规则的识别
        rule_results = self.classify_intent_rules(text)
        
        # 合并结果
        combined_scores = {}
        
        # 添加关键词结果
        for intent_type, score in keyword_results:
            combined_scores[intent_type] = score * 0.6  # 关键词权重0.6
        
        # 添加规则结果
        for intent_type, score in rule_results:
            if intent_type in combined_scores:
                combined_scores[intent_type] += score * 0.4  # 规则权重0.4
            else:
                combined_scores[intent_type] = score * 0.4
        
        # 找到最高分的意图
        if combined_scores:
            best_intent_type = max(combined_scores.items(), key=lambda x: x[1])
            intent_type, confidence = best_intent_type
            
            intent = Intent(
                type=intent_type,
                name=self.intent_types[intent_type]["name"],
                confidence=confidence,
                description=self.intent_types[intent_type]["description"]
            )
        else:
            # 默认意图
            intent = Intent(
                type="unknown",
                name="未知意图",
                confidence=0.1,
                description="无法识别的意图"
            )
        
        logger.info(f"Classified intent: {intent.type} ({intent.name}) with confidence {intent.confidence:.2f}")
        return intent
    
    def validate_intent_entities(self, intent_type: str, entities: List[Dict[str, str]]) -> Tuple[bool, List[str]]:
        """验证意图所需的实体是否完整"""
        if intent_type not in self.intent_types:
            return False, [f"未知的意图类型: {intent_type}"]
        
        config = self.intent_types[intent_type]
        required_entities = config.get("required_entities", [])
        
        # 提取实体类型
        entity_types = [entity["type"] for entity in entities]
        
        # 检查必需实体
        missing_entities = []
        for required_entity in required_entities:
            if required_entity not in entity_types:
                missing_entities.append(required_entity)
        
        errors = []
        if missing_entities:
            errors.append(f"缺少必需的实体: {', '.join(missing_entities)}")
        
        is_valid = len(errors) == 0
        return is_valid, errors