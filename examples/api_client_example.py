"""
API客户端示例
展示如何调用NLP服务的API接口
"""
import requests
import json
from typing import Dict, Any

class NLPClient:
    """NLP服务客户端"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def process_command(self, text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """处理语音指令"""
        url = f"{self.base_url}/process"
        
        payload = {
            "text": text,
            "context": context or {}
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        url = f"{self.base_url}/health"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

def demo_basic_usage():
    """基本使用示例"""
    print("="*50)
    print("基本使用示例")
    print("="*50)
    
    client = NLPClient()
    
    # 健康检查
    health = client.health_check()
    print(f"服务状态: {health}")
    
    # 处理指令
    commands = [
        "巡检A区2号房主柜温度",
        "开启B区空调",
        "查询UPS1状态"
    ]
    
    for cmd in commands:
        print(f"\n处理指令: {cmd}")
        result = client.process_command(cmd)
        
        if result.get("success"):
            data = result["result"]
            print(f"意图: {data['intent']['name']} (置信度: {data['intent']['confidence']:.2f})")
            print(f"实体数量: {len(data['entities'])}")
            print(f"指令有效: {'是' if data['is_valid'] else '否'}")
        else:
            print(f"处理失败: {result.get('error')}")

def demo_with_context():
    """带上下文的使用示例"""
    print("\n" + "="*50)
    print("带上下文的使用示例")
    print("="*50)
    
    client = NLPClient()
    
    # 模拟会话上下文
    context = {
        "session_id": "session_12345",
        "user_id": "operator_001",
        "current_location": "A区1号房",
        "current_task": "daily_inspection"
    }
    
    commands = [
        "巡检这里的主柜温度",  # 使用上下文中的位置
        "然后检查湿度",      # 延续之前的操作
        "前往下一个房间"      # 基于当前位置导航
    ]
    
    for cmd in commands:
        print(f"\n处理指令: {cmd}")
        result = client.process_command(cmd, context)
        
        if result.get("success"):
            data = result["result"]
            print(f"意图: {data['intent']['name']}")
            print(f"结构化指令: {json.dumps(data.get('structured_command', {}), ensure_ascii=False, indent=2)}")
        else:
            print(f"处理失败: {result.get('error')}")

def demo_batch_processing():
    """批量处理示例"""
    print("\n" + "="*50)
    print("批量处理示例")
    print("="*50)
    
    client = NLPClient()
    
    # 模拟一天的巡检任务
    daily_tasks = [
        "开始今日巡检任务",
        "前往A区1号房",
        "巡检主柜温度",
        "检查UPS电压",
        "前往A区2号房",
        "巡检副柜温度湿度",
        "检查空调运行状态",
        "前往B区配电室",
        "查询所有设备状态",
        "完成巡检任务"
    ]
    
    results = []
    for i, task in enumerate(daily_tasks, 1):
        print(f"\n任务 {i}: {task}")
        result = client.process_command(task)
        
        if result.get("success"):
            data = result["result"]
            intent_info = f"{data['intent']['name']} (置信度: {data['intent']['confidence']:.2f})"
            entity_count = len(data['entities'])
            is_valid = "✓" if data['is_valid'] else "✗"
            
            print(f"  意图: {intent_info}")
            print(f"  实体: {entity_count}个")
            print(f"  有效: {is_valid}")
            
            results.append({
                "task": task,
                "intent": data['intent']['type'],
                "confidence": data['intent']['confidence'],
                "valid": data['is_valid']
            })
        else:
            print(f"  错误: {result.get('error')}")
            results.append({
                "task": task,
                "error": result.get('error')
            })
    
    # 统计结果
    print(f"\n批量处理结果统计:")
    print(f"总任务数: {len(daily_tasks)}")
    valid_count = sum(1 for r in results if r.get('valid', False))
    print(f"有效指令: {valid_count}")
    avg_confidence = sum(r.get('confidence', 0) for r in results if 'confidence' in r) / len([r for r in results if 'confidence' in r])
    print(f"平均置信度: {avg_confidence:.2f}")

def demo_error_handling():
    """错误处理示例"""
    print("\n" + "="*50)
    print("错误处理示例")
    print("="*50)
    
    client = NLPClient()
    
    # 测试各种错误情况
    error_cases = [
        "",  # 空字符串
        "这是一个无关的指令",  # 无法识别的指令
        "巡检",  # 缺少必要参数
        "前往",  # 缺少目标位置
    ]
    
    for case in error_cases:
        print(f"\n测试用例: '{case}'")
        result = client.process_command(case)
        
        if result.get("success"):
            data = result["result"]
            if not data['is_valid']:
                print(f"  指令无效: {data['validation_errors']}")
            else:
                print(f"  意图: {data['intent']['name']}")
        else:
            print(f"  API错误: {result.get('error')}")

if __name__ == "__main__":
    print("NLP服务API客户端示例")
    print("请确保NLP服务已启动 (python main.py server)")
    
    try:
        demo_basic_usage()
        demo_with_context()
        demo_batch_processing()
        demo_error_handling()
    except Exception as e:
        print(f"\n运行示例时出错: {e}")
        print("请检查NLP服务是否正在运行")
    
    print("\n示例演示完成")