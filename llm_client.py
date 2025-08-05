"""
大模型客户端
用于调用大模型API进行自然语言理解
"""
import json
import requests
from typing import Dict, Any, Optional
from loguru import logger
from openai import OpenAI

from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME, INTENT_TYPES, ENTITY_TYPES
from models import LLMResponse

class LLMClient:
    """大模型客户端"""
    
    def __init__(self):
        self.api_key = OPENAI_API_KEY
        self.base_url = OPENAI_BASE_URL
        self.model_name = MODEL_NAME
        
        if self.api_key:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
        else:
            logger.warning("No OpenAI API key provided, LLM features will be disabled")
            self.client = None
    
    def _build_system_prompt(self) -> str:
        """构建系统提示词"""
        intent_descriptions = []
        for intent_type, config in INTENT_TYPES.items():
            intent_descriptions.append(f"- {intent_type}: {config['name']} - {config['description']}")
        
        entity_descriptions = []
        for entity_type, config in ENTITY_TYPES.items():
            examples = ", ".join(config['examples'][:3])
            entity_descriptions.append(f"- {entity_type}: {config['name']} - 例如: {examples}")
        
        system_prompt = f"""你是一个语音控制机器人的自然语言理解系统。你的任务是分析用户的语音指令，识别意图并提取相关实体。

支持的意图类型：
{chr(10).join(intent_descriptions)}

支持的实体类型：
{chr(10).join(entity_descriptions)}

请分析用户输入的文本，返回JSON格式的结果，包含：
1. intent_type: 识别的意图类型
2. intent_confidence: 意图识别的置信度 (0-1)
3. entities: 提取的实体列表，每个实体包含type、value、start、end
4. reasoning: 分析推理过程
5. structured_command: 结构化的指令参数

示例输入："巡检A区2号房主柜温度"
示例输出：
{{
    "intent_type": "patrol_inspection",
    "intent_confidence": 0.95,
    "entities": [
        {{"type": "location", "value": "A区", "start": 2, "end": 4}},
        {{"type": "location", "value": "2号房", "start": 4, "end": 7}},
        {{"type": "equipment", "value": "主柜", "start": 7, "end": 9}},
        {{"type": "parameter", "value": "温度", "start": 9, "end": 11}}
    ],
    "reasoning": "用户要求巡检A区2号房的主柜温度，这是一个典型的巡检指令",
    "structured_command": {{
        "action": "patrol_inspection",
        "location": {{"zone": "A", "room": "2"}},
        "equipment": "主柜",
        "parameter": "温度"
    }}
}}

请严格按照JSON格式返回结果，不要包含其他内容。"""
        
        return system_prompt
    
    def analyze_command(self, text: str) -> Optional[LLMResponse]:
        """使用大模型分析指令"""
        if not self.client:
            logger.warning("LLM client not initialized, skipping LLM analysis")
            return None
        
        try:
            system_prompt = self._build_system_prompt()
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ],
                temperature=0.1,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content.strip()
            logger.debug(f"LLM response: {content}")
            
            # 解析JSON响应
            try:
                result_data = json.loads(content)
                llm_response = LLMResponse(**result_data)
                return llm_response
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse LLM response as JSON: {e}")
                logger.error(f"Raw response: {content}")
                return None
            except Exception as e:
                logger.error(f"Failed to create LLMResponse: {e}")
                return None
                
        except Exception as e:
            logger.error(f"Error calling LLM API: {e}")
            return None
    
    def enhance_entity_extraction(self, text: str, existing_entities: list) -> Optional[Dict[str, Any]]:
        """使用大模型增强实体抽取"""
        if not self.client:
            return None
        
        try:
            prompt = f"""请分析以下文本中的实体，特别关注可能被遗漏的实体：

文本："{text}"

已识别的实体：{existing_entities}

请补充可能遗漏的实体，返回JSON格式：
{{
    "additional_entities": [
        {{"type": "实体类型", "value": "实体值", "start": 起始位置, "end": 结束位置}}
    ],
    "corrections": [
        {{"original": "原实体值", "corrected": "修正后的值", "reason": "修正原因"}}
    ]
}}"""

            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=500
            )
            
            content = response.choices[0].message.content.strip()
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"Error in entity enhancement: {e}")
            return None