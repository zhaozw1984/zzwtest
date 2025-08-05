#!/usr/bin/env python3
"""
系统测试脚本
验证语音控制机器人NLP系统的基本功能
"""
import sys
import os

def test_imports():
    """测试模块导入"""
    print("测试模块导入...")
    try:
        from config import INTENT_TYPES, ENTITY_TYPES
        from models import CommandResult, Intent, Entity
        from intent_classifier import IntentClassifier
        from entity_extractor import EntityExtractor
        from llm_client import LLMClient
        from nlp_processor import NLPProcessor
        print("✓ 所有模块导入成功")
        return True
    except ImportError as e:
        print(f"✗ 模块导入失败: {e}")
        return False

def test_basic_functionality():
    """测试基本功能"""
    print("\n测试基本功能...")
    try:
        from nlp_processor import NLPProcessor
        
        processor = NLPProcessor()
        
        # 测试示例指令
        test_text = "巡检A区2号房主柜温度"
        result = processor.process_command(test_text)
        
        print(f"✓ 指令处理成功: {test_text}")
        print(f"  意图: {result.intent.name} (置信度: {result.intent.confidence:.2f})")
        print(f"  实体数量: {len(result.entities)}")
        print(f"  指令有效: {'是' if result.is_valid else '否'}")
        
        return True
    except Exception as e:
        print(f"✗ 基本功能测试失败: {e}")
        return False

def test_intent_classification():
    """测试意图识别"""
    print("\n测试意图识别...")
    try:
        from intent_classifier import IntentClassifier
        
        classifier = IntentClassifier()
        
        test_cases = [
            ("巡检A区2号房主柜温度", "patrol_inspection"),
            ("开启B区空调", "equipment_control"),
            ("查询UPS1状态", "status_query"),
            ("前往C区3号房", "navigation"),
            ("确认高温报警", "alarm_handling")
        ]
        
        success_count = 0
        for text, expected_intent in test_cases:
            intent = classifier.classify_intent(text)
            if intent.type == expected_intent:
                print(f"✓ {text} -> {intent.name}")
                success_count += 1
            else:
                print(f"✗ {text} -> {intent.name} (期望: {expected_intent})")
        
        print(f"意图识别准确率: {success_count}/{len(test_cases)} ({success_count/len(test_cases)*100:.1f}%)")
        return success_count == len(test_cases)
        
    except Exception as e:
        print(f"✗ 意图识别测试失败: {e}")
        return False

def test_entity_extraction():
    """测试实体抽取"""
    print("\n测试实体抽取...")
    try:
        from entity_extractor import EntityExtractor
        
        extractor = EntityExtractor()
        
        test_cases = [
            ("巡检A区2号房主柜温度", ["location", "equipment", "parameter"]),
            ("开启B区空调", ["location", "equipment"]),
            ("设置空调温度为25度", ["equipment", "parameter"])
        ]
        
        success_count = 0
        for text, expected_types in test_cases:
            entities = extractor.extract_entities(text)
            extracted_types = [e.type for e in entities]
            
            # 检查是否包含期望的实体类型
            contains_expected = all(et in extracted_types for et in expected_types)
            if contains_expected:
                print(f"✓ {text} -> {extracted_types}")
                success_count += 1
            else:
                print(f"✗ {text} -> {extracted_types} (期望包含: {expected_types})")
        
        print(f"实体抽取成功率: {success_count}/{len(test_cases)} ({success_count/len(test_cases)*100:.1f}%)")
        return success_count >= len(test_cases) * 0.7  # 70%成功率即可
        
    except Exception as e:
        print(f"✗ 实体抽取测试失败: {e}")
        return False

def test_configuration():
    """测试配置"""
    print("\n测试配置...")
    try:
        from config import INTENT_TYPES, ENTITY_TYPES
        
        # 检查意图类型配置
        required_intents = ["patrol_inspection", "equipment_control", "status_query", "navigation", "alarm_handling"]
        for intent_type in required_intents:
            if intent_type not in INTENT_TYPES:
                print(f"✗ 缺少意图类型: {intent_type}")
                return False
        
        # 检查实体类型配置
        required_entities = ["location", "equipment", "parameter", "action"]
        for entity_type in required_entities:
            if entity_type not in ENTITY_TYPES:
                print(f"✗ 缺少实体类型: {entity_type}")
                return False
        
        print(f"✓ 意图类型配置完整 ({len(INTENT_TYPES)}个)")
        print(f"✓ 实体类型配置完整 ({len(ENTITY_TYPES)}个)")
        return True
        
    except Exception as e:
        print(f"✗ 配置测试失败: {e}")
        return False

def test_dependencies():
    """测试依赖包"""
    print("\n测试依赖包...")
    required_packages = [
        'pydantic',
        'loguru', 
        'jieba',
        'fastapi',
        'uvicorn',
        'requests',
        'openai'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} (缺失)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n请安装缺失的包: pip install {' '.join(missing_packages)}")
        return False
    
    return True

def run_all_tests():
    """运行所有测试"""
    print("="*60)
    print("语音控制机器人NLP系统测试")
    print("="*60)
    
    tests = [
        ("依赖包测试", test_dependencies),
        ("模块导入测试", test_imports),
        ("配置测试", test_configuration),
        ("意图识别测试", test_intent_classification),
        ("实体抽取测试", test_entity_extraction),
        ("基本功能测试", test_basic_functionality)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"✗ {test_name} 执行失败: {e}")
    
    print("\n" + "="*60)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统可以正常使用。")
        print("\n使用方法:")
        print("1. 交互式模式: python main.py")
        print("2. 单条指令: python main.py '巡检A区2号房主柜温度'")
        print("3. 批量测试: python main.py test")
        print("4. API服务: python main.py server")
    else:
        print("❌ 部分测试失败，请检查系统配置。")
        return False
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)