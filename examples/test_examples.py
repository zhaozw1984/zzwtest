"""
测试示例
展示不同类型指令的处理效果
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nlp_processor import NLPProcessor
import json

def test_patrol_commands():
    """测试巡检指令"""
    print("="*60)
    print("测试巡检指令")
    print("="*60)
    
    processor = NLPProcessor()
    
    test_cases = [
        "巡检A区2号房主柜温度",
        "检查B区配电室湿度",
        "监测C区UPS电压",
        "查看东侧空调运行状态",
        "巡检3楼变压器温度和电流"
    ]
    
    for text in test_cases:
        print(f"\n输入: {text}")
        result = processor.process_command(text)
        print(f"意图: {result.intent.name} (置信度: {result.intent.confidence:.2f})")
        print(f"实体: {[f'{e.type}={e.value}' for e in result.entities]}")
        print(f"有效性: {'✓' if result.is_valid else '✗'}")
        if result.structured_command:
            print(f"结构化指令: {json.dumps(result.structured_command, ensure_ascii=False)}")

def test_control_commands():
    """测试控制指令"""
    print("\n" + "="*60)
    print("测试设备控制指令")
    print("="*60)
    
    processor = NLPProcessor()
    
    test_cases = [
        "开启A区空调",
        "关闭主柜电源",
        "启动UPS1",
        "设置空调温度为25度",
        "调节风机转速到60%",
        "重启配电柜系统"
    ]
    
    for text in test_cases:
        print(f"\n输入: {text}")
        result = processor.process_command(text)
        print(f"意图: {result.intent.name} (置信度: {result.intent.confidence:.2f})")
        print(f"实体: {[f'{e.type}={e.value}' for e in result.entities]}")
        print(f"有效性: {'✓' if result.is_valid else '✗'}")
        if result.validation_errors:
            print(f"错误: {result.validation_errors}")

def test_query_commands():
    """测试查询指令"""
    print("\n" + "="*60)
    print("测试状态查询指令")
    print("="*60)
    
    processor = NLPProcessor()
    
    test_cases = [
        "查询UPS1状态",
        "显示主柜运行参数",
        "报告B区所有设备状态",
        "查看空调温度设置",
        "获取配电室电压数据"
    ]
    
    for text in test_cases:
        print(f"\n输入: {text}")
        result = processor.process_command(text)
        print(f"意图: {result.intent.name} (置信度: {result.intent.confidence:.2f})")
        print(f"实体: {[f'{e.type}={e.value}' for e in result.entities]}")
        print(f"有效性: {'✓' if result.is_valid else '✗'}")

def test_navigation_commands():
    """测试导航指令"""
    print("\n" + "="*60)
    print("测试导航移动指令")
    print("="*60)
    
    processor = NLPProcessor()
    
    test_cases = [
        "前往A区2号房",
        "移动到配电室",
        "回到充电桩",
        "导航至B区主控室",
        "到达3楼机房"
    ]
    
    for text in test_cases:
        print(f"\n输入: {text}")
        result = processor.process_command(text)
        print(f"意图: {result.intent.name} (置信度: {result.intent.confidence:.2f})")
        print(f"实体: {[f'{e.type}={e.value}' for e in result.entities]}")
        print(f"有效性: {'✓' if result.is_valid else '✗'}")

def test_alarm_commands():
    """测试报警处理指令"""
    print("\n" + "="*60)
    print("测试报警处理指令")
    print("="*60)
    
    processor = NLPProcessor()
    
    test_cases = [
        "确认高温报警",
        "处理过载警报",
        "消除通信故障报警",
        "确认断电报警",
        "处理A区低温警报"
    ]
    
    for text in test_cases:
        print(f"\n输入: {text}")
        result = processor.process_command(text)
        print(f"意图: {result.intent.name} (置信度: {result.intent.confidence:.2f})")
        print(f"实体: {[f'{e.type}={e.value}' for e in result.entities]}")
        print(f"有效性: {'✓' if result.is_valid else '✗'}")

def test_complex_commands():
    """测试复杂指令"""
    print("\n" + "="*60)
    print("测试复杂组合指令")
    print("="*60)
    
    processor = NLPProcessor()
    
    test_cases = [
        "巡检A区2号房主柜和副柜的温度湿度",
        "前往B区3号房开启空调并设置温度为26度",
        "查询C区所有UPS设备的电压电流状态",
        "检查东侧机房1到3号机柜的运行参数",
        "确认配电室高温报警并调节空调温度"
    ]
    
    for text in test_cases:
        print(f"\n输入: {text}")
        result = processor.process_command(text)
        print(f"意图: {result.intent.name} (置信度: {result.intent.confidence:.2f})")
        print(f"实体数量: {len(result.entities)}")
        for entity in result.entities:
            print(f"  - {entity.type}: {entity.value} (置信度: {entity.confidence:.2f})")
        print(f"有效性: {'✓' if result.is_valid else '✗'}")
        if result.structured_command:
            print(f"结构化指令:")
            print(json.dumps(result.structured_command, ensure_ascii=False, indent=2))

def test_edge_cases():
    """测试边界情况"""
    print("\n" + "="*60)
    print("测试边界情况")
    print("="*60)
    
    processor = NLPProcessor()
    
    test_cases = [
        "",  # 空字符串
        "你好",  # 无关指令
        "巡检",  # 缺少参数
        "A区2号房",  # 只有位置信息
        "温度很高",  # 模糊描述
        "帮我看看那个设备怎么样",  # 口语化表达
        "机器人快点过来",  # 非正式指令
    ]
    
    for text in test_cases:
        print(f"\n输入: '{text}'")
        result = processor.process_command(text)
        print(f"意图: {result.intent.name} (置信度: {result.intent.confidence:.2f})")
        print(f"实体: {[f'{e.type}={e.value}' for e in result.entities]}")
        print(f"有效性: {'✓' if result.is_valid else '✗'}")
        if result.validation_errors:
            print(f"错误: {result.validation_errors}")

if __name__ == "__main__":
    print("语音控制机器人NLP系统测试")
    
    # 运行所有测试
    test_patrol_commands()
    test_control_commands()
    test_query_commands()
    test_navigation_commands()
    test_alarm_commands()
    test_complex_commands()
    test_edge_cases()
    
    print("\n" + "="*60)
    print("测试完成")
    print("="*60)