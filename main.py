"""
语音控制机器人自然语言处理系统主程序
"""
import sys
import json
from typing import Dict, Any
from loguru import logger
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

from nlp_processor import NLPProcessor
from models import ProcessingContext

# 配置日志
logger.add("logs/nlp_processor.log", rotation="1 day", retention="7 days")

# 初始化处理器
nlp_processor = NLPProcessor()

# FastAPI应用
app = FastAPI(title="语音控制机器人NLP服务", version="1.0.0")

class CommandRequest(BaseModel):
    text: str
    context: Dict[str, Any] = {}

class CommandResponse(BaseModel):
    success: bool
    result: Dict[str, Any] = {}
    error: str = ""

@app.post("/process", response_model=CommandResponse)
async def process_command(request: CommandRequest):
    """处理语音指令API"""
    try:
        # 构建处理上下文
        context = ProcessingContext(**request.context) if request.context else None
        
        # 处理指令
        result = nlp_processor.process_command(request.text, context)
        
        # 转换为字典格式
        result_dict = {
            "original_text": result.original_text,
            "intent": {
                "type": result.intent.type,
                "name": result.intent.name,
                "confidence": result.intent.confidence,
                "description": result.intent.description
            },
            "entities": [
                {
                    "type": entity.type,
                    "value": entity.value,
                    "start": entity.start,
                    "end": entity.end,
                    "confidence": entity.confidence,
                    "normalized_value": entity.normalized_value
                }
                for entity in result.entities
            ],
            "confidence": result.confidence,
            "structured_command": result.structured_command,
            "is_valid": result.is_valid,
            "validation_errors": result.validation_errors,
            "timestamp": result.timestamp.isoformat()
        }
        
        return CommandResponse(success=True, result=result_dict)
        
    except Exception as e:
        logger.error(f"Error processing command: {e}")
        return CommandResponse(success=False, error=str(e))

@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "service": "nlp_processor"}

def process_command_cli(text: str) -> None:
    """命令行处理接口"""
    try:
        result = nlp_processor.process_command(text)
        
        # 打印结果
        print("\n" + "="*50)
        print(f"原始文本: {result.original_text}")
        print(f"识别意图: {result.intent.name} ({result.intent.type})")
        print(f"意图置信度: {result.intent.confidence:.2f}")
        
        if result.entities:
            print("\n提取的实体:")
            for entity in result.entities:
                normalized_info = ""
                if entity.normalized_value:
                    normalized_info = f" -> {entity.normalized_value}"
                print(f"  - {entity.type}: {entity.value} (置信度: {entity.confidence:.2f}){normalized_info}")
        
        if result.structured_command:
            print(f"\n结构化指令:")
            print(json.dumps(result.structured_command, ensure_ascii=False, indent=2))
        
        print(f"\n整体置信度: {result.confidence:.2f}")
        print(f"指令有效性: {'有效' if result.is_valid else '无效'}")
        
        if result.validation_errors:
            print("验证错误:")
            for error in result.validation_errors:
                print(f"  - {error}")
        
        print("="*50)
        
    except Exception as e:
        logger.error(f"Error processing command: {e}")
        print(f"处理指令时出错: {e}")

def main():
    """主函数"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "server":
            # 启动API服务
            print("启动NLP处理服务...")
            uvicorn.run(app, host="0.0.0.0", port=8000)
        elif sys.argv[1] == "test":
            # 运行测试样例
            test_commands = [
                "巡检A区2号房主柜温度",
                "开启B区空调",
                "查询UPS1状态",
                "前往C区3号房",
                "关闭主柜电源",
                "检查配电室湿度",
                "设置空调温度为25度",
                "确认高温报警"
            ]
            
            print("运行测试样例...")
            for cmd in test_commands:
                print(f"\n测试指令: {cmd}")
                process_command_cli(cmd)
        else:
            # 处理单个指令
            command_text = " ".join(sys.argv[1:])
            process_command_cli(command_text)
    else:
        # 交互式模式
        print("语音控制机器人自然语言处理系统")
        print("输入 'quit' 退出程序")
        print("-" * 40)
        
        while True:
            try:
                text = input("\n请输入语音指令: ").strip()
                if text.lower() in ['quit', 'exit', '退出']:
                    break
                if text:
                    process_command_cli(text)
            except KeyboardInterrupt:
                print("\n程序已退出")
                break
            except Exception as e:
                print(f"发生错误: {e}")

if __name__ == "__main__":
    main()