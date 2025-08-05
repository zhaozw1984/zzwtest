#!/usr/bin/env python3
"""
硅基流动API演示脚本
展示如何配置和使用硅基流动API进行语音指令理解
"""
import os
from nlp_processor import NLPProcessor
from llm_client import LLMClient

def demo_without_api():
    """演示不使用API的基础功能"""
    print("="*60)
    print("演示：基础功能（不使用大模型API）")
    print("="*60)
    
    processor = NLPProcessor()
    
    test_commands = [
        "巡检A区2号房主柜温度",
        "开启B区空调",
        "查询UPS1状态",
        "前往C区3号房",
        "确认高温报警"
    ]
    
    for cmd in test_commands:
        print(f"\n输入: {cmd}")
        result = processor.process_command(cmd)
        print(f"意图: {result.intent.name} (置信度: {result.intent.confidence:.2f})")
        print(f"实体: {len(result.entities)}个")
        print(f"有效: {'✓' if result.is_valid else '✗'}")

def demo_with_siliconflow_api():
    """演示使用硅基流动API的增强功能"""
    print("\n" + "="*60)
    print("演示：硅基流动API增强功能")
    print("="*60)
    
    # 检查API配置
    api_key = os.getenv("SILICONFLOW_API_KEY")
    if not api_key:
        print("❌ 未配置硅基流动API密钥")
        print("请设置环境变量 SILICONFLOW_API_KEY")
        print("或在 .env 文件中配置:")
        print("SILICONFLOW_API_KEY=your_api_key_here")
        return
    
    print(f"✓ 已配置硅基流动API密钥: {api_key[:8]}...")
    
    # 创建LLM客户端
    llm_client = LLMClient()
    if not llm_client.client:
        print("❌ 硅基流动客户端初始化失败")
        return
    
    print(f"✓ 使用模型: {llm_client.model_name}")
    
    # 测试复杂指令
    complex_commands = [
        "巡检A区2号房主柜和副柜的温度湿度",
        "前往B区3号房开启空调并设置温度为26度",
        "检查配电室所有设备的运行状态",
        "确认高温报警并调节空调温度"
    ]
    
    processor = NLPProcessor()
    
    for cmd in complex_commands:
        print(f"\n输入: {cmd}")
        try:
            result = processor.process_command(cmd)
            print(f"意图: {result.intent.name} (置信度: {result.intent.confidence:.2f})")
            print(f"实体: {len(result.entities)}个")
            for entity in result.entities:
                print(f"  - {entity.type}: {entity.value}")
            print(f"有效: {'✓' if result.is_valid else '✗'}")
            if result.structured_command:
                print(f"结构化指令: {result.structured_command}")
        except Exception as e:
            print(f"❌ 处理失败: {e}")

def show_model_options():
    """显示可用的模型选项"""
    print("\n" + "="*60)
    print("硅基流动可用模型")
    print("="*60)
    
    models = [
        {
            "name": "Qwen/Qwen2.5-7B-Instruct",
            "type": "免费",
            "description": "轻量级模型，适合开发测试"
        },
        {
            "name": "Qwen/Qwen2.5-72B-Instruct", 
            "type": "免费",
            "description": "高性能模型，推荐生产使用"
        },
        {
            "name": "deepseek-ai/DeepSeek-V2.5",
            "type": "付费",
            "description": "高性能通用模型"
        },
        {
            "name": "Pro/deepseek-ai/DeepSeek-R1",
            "type": "付费",
            "description": "推理专用模型"
        },
        {
            "name": "internlm/internlm2_5-20b-chat",
            "type": "付费", 
            "description": "对话优化模型"
        }
    ]
    
    for model in models:
        status = "🆓" if model["type"] == "免费" else "💰"
        print(f"{status} {model['name']}")
        print(f"    {model['description']}")
    
    print(f"\n当前配置模型: {os.getenv('MODEL_NAME', 'Qwen/Qwen2.5-72B-Instruct')}")

def show_setup_guide():
    """显示配置指南"""
    print("\n" + "="*60)
    print("硅基流动配置指南")
    print("="*60)
    
    print("1. 注册账户：")
    print("   访问 https://cloud.siliconflow.cn/ 注册")
    
    print("\n2. 获取API密钥：")
    print("   - 登录后进入控制台")
    print("   - 点击左侧菜单'API密钥'")
    print("   - 点击'新建API密钥'")
    print("   - 复制生成的密钥")
    
    print("\n3. 配置环境变量：")
    print("   创建 .env 文件，添加以下内容：")
    print("   SILICONFLOW_API_KEY=your_api_key_here")
    print("   MODEL_NAME=Qwen/Qwen2.5-72B-Instruct")
    
    print("\n4. 验证配置：")
    print("   python3 demo_siliconflow.py")

def main():
    """主函数"""
    print("🤖 语音控制机器人 - 硅基流动API演示")
    
    # 显示配置指南
    show_setup_guide()
    
    # 显示模型选项
    show_model_options()
    
    # 演示基础功能
    demo_without_api()
    
    # 演示API增强功能
    demo_with_siliconflow_api()
    
    print("\n" + "="*60)
    print("演示完成")
    print("="*60)
    print("💡 提示：")
    print("- 免费模型足够满足大部分需求")
    print("- 配置API密钥后可获得更强的语义理解能力")
    print("- 查看 SILICONFLOW_SETUP.md 获取详细配置说明")

if __name__ == "__main__":
    main()