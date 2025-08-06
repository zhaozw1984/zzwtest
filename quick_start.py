#!/usr/bin/env python3
"""
快速开始脚本
帮助用户快速体验语音控制机器人NLP系统
"""
import os
import sys
from nlp_processor import NLPProcessor

def quick_demo():
    """快速演示"""
    print("🤖 语音控制机器人NLP系统 - 快速体验")
    print("="*50)
    
    processor = NLPProcessor()
    
    # 示例指令
    demo_commands = [
        "巡检A区2号房主柜温度",
        "开启B区空调", 
        "查询UPS1状态",
        "前往C区3号房",
        "确认高温报警"
    ]
    
    print("正在处理示例指令...")
    print("-" * 30)
    
    for i, cmd in enumerate(demo_commands, 1):
        print(f"\n{i}. 输入: {cmd}")
        
        try:
            result = processor.process_command(cmd)
            print(f"   意图: {result.intent.name}")
            print(f"   实体: {[f'{e.type}={e.value}' for e in result.entities]}")
            print(f"   有效: {'✅' if result.is_valid else '❌'}")
        except Exception as e:
            print(f"   错误: {e}")
    
    print("\n" + "="*50)
    print("✅ 基础功能演示完成！")
    
    # 检查是否配置了硅基流动API
    api_key = os.getenv("SILICONFLOW_API_KEY")
    if api_key:
        print("🚀 已检测到硅基流动API配置，可获得更强的语义理解能力")
    else:
        print("💡 提示：配置硅基流动API可获得更强的语义理解能力")
        print("   1. 访问 https://cloud.siliconflow.cn/ 注册")
        print("   2. 获取API密钥")
        print("   3. 配置环境变量 SILICONFLOW_API_KEY")
        print("   4. 运行 python3 demo_siliconflow.py 查看详细说明")

def interactive_mode():
    """交互模式"""
    print("\n🎯 进入交互模式")
    print("输入语音指令，输入 'quit' 退出")
    print("-" * 30)
    
    processor = NLPProcessor()
    
    while True:
        try:
            text = input("\n请输入指令: ").strip()
            if text.lower() in ['quit', 'exit', '退出', 'q']:
                print("👋 再见！")
                break
            
            if not text:
                continue
                
            result = processor.process_command(text)
            print(f"意图: {result.intent.name} (置信度: {result.intent.confidence:.2f})")
            print(f"实体: {len(result.entities)}个")
            for entity in result.entities:
                print(f"  - {entity.type}: {entity.value}")
            print(f"有效: {'✅' if result.is_valid else '❌'}")
            
            if not result.is_valid:
                print("错误:", result.validation_errors)
                
        except KeyboardInterrupt:
            print("\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 处理错误: {e}")

def main():
    """主函数"""
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        interactive_mode()
    else:
        quick_demo()
        
        # 询问是否进入交互模式
        try:
            choice = input("\n是否进入交互模式？(y/n): ").strip().lower()
            if choice in ['y', 'yes', '是']:
                interactive_mode()
        except KeyboardInterrupt:
            print("\n👋 再见！")

if __name__ == "__main__":
    main()