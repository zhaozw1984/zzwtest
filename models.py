"""
数据模型定义
定义指令解析结果的数据结构
"""
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime

class Entity(BaseModel):
    """实体信息"""
    type: str = Field(description="实体类型")
    value: str = Field(description="实体值")
    start: int = Field(description="在原文中的起始位置")
    end: int = Field(description="在原文中的结束位置")
    confidence: float = Field(default=1.0, description="置信度")
    normalized_value: Optional[Dict[str, Any]] = Field(default=None, description="标准化后的值")

class Intent(BaseModel):
    """意图信息"""
    type: str = Field(description="意图类型")
    name: str = Field(description="意图名称")
    confidence: float = Field(description="置信度")
    description: Optional[str] = Field(default=None, description="意图描述")

class CommandResult(BaseModel):
    """指令解析结果"""
    original_text: str = Field(description="原始文本")
    intent: Intent = Field(description="识别的意图")
    entities: List[Entity] = Field(default=[], description="提取的实体列表")
    confidence: float = Field(description="整体置信度")
    timestamp: datetime = Field(default_factory=datetime.now, description="处理时间")
    
    # 结构化的指令参数
    structured_command: Optional[Dict[str, Any]] = Field(default=None, description="结构化指令")
    
    # 执行状态
    is_valid: bool = Field(default=True, description="指令是否有效")
    validation_errors: List[str] = Field(default=[], description="验证错误信息")

class ProcessingContext(BaseModel):
    """处理上下文"""
    session_id: Optional[str] = Field(default=None, description="会话ID")
    user_id: Optional[str] = Field(default=None, description="用户ID")
    previous_commands: List[CommandResult] = Field(default=[], description="历史指令")
    current_location: Optional[str] = Field(default=None, description="当前位置")
    current_task: Optional[str] = Field(default=None, description="当前任务")

class LLMResponse(BaseModel):
    """大模型响应"""
    intent_type: str
    intent_confidence: float
    entities: List[Dict[str, Any]]
    reasoning: str
    structured_command: Dict[str, Any]