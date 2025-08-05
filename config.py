"""
语音控制机器人配置文件
定义支持的指令类型、实体类型和相关配置
"""
import os
from typing import Dict, List, Any
from dotenv import load_dotenv

load_dotenv()

# API配置
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")

# 支持的指令类型
INTENT_TYPES = {
    "patrol_inspection": {
        "name": "巡检",
        "description": "巡检相关指令，包括温度、湿度、电压等参数检查",
        "keywords": ["巡检", "检查", "监测", "查看"],
        "required_entities": ["location", "equipment"],
        "optional_entities": ["parameter", "time"]
    },
    "equipment_control": {
        "name": "设备控制",
        "description": "设备开关、调节等控制指令",
        "keywords": ["开启", "关闭", "启动", "停止", "调节", "设置"],
        "required_entities": ["equipment", "action"],
        "optional_entities": ["location", "parameter", "value"]
    },
    "status_query": {
        "name": "状态查询",
        "description": "查询设备状态、参数等信息",
        "keywords": ["查询", "状态", "显示", "报告"],
        "required_entities": ["equipment"],
        "optional_entities": ["location", "parameter"]
    },
    "alarm_handling": {
        "name": "报警处理",
        "description": "报警确认、处理等指令",
        "keywords": ["报警", "警报", "确认", "处理", "消除"],
        "required_entities": ["alarm_type"],
        "optional_entities": ["location", "equipment"]
    },
    "navigation": {
        "name": "导航移动",
        "description": "机器人移动、导航相关指令",
        "keywords": ["前往", "移动", "到达", "回到", "导航"],
        "required_entities": ["location"],
        "optional_entities": ["route", "speed"]
    }
}

# 实体类型定义
ENTITY_TYPES = {
    "location": {
        "name": "位置",
        "description": "区域、房间、位置信息",
        "patterns": [
            r"[A-Z]区",
            r"\d+号房",
            r"\d+楼",
            r"[东西南北]侧",
            r"机房\d*",
            r"配电室\d*"
        ],
        "examples": ["A区", "2号房", "3楼", "东侧", "机房1", "配电室"]
    },
    "equipment": {
        "name": "设备",
        "description": "各类设备名称",
        "patterns": [
            r"主柜",
            r"副柜", 
            r"UPS\d*",
            r"空调\d*",
            r"风机\d*",
            r"变压器\d*",
            r"开关柜\d*",
            r"配电柜\d*"
        ],
        "examples": ["主柜", "副柜", "UPS1", "空调", "风机", "变压器", "开关柜", "配电柜"]
    },
    "parameter": {
        "name": "参数",
        "description": "监测参数类型",
        "patterns": [
            r"温度",
            r"湿度",
            r"电压",
            r"电流",
            r"功率",
            r"频率",
            r"压力"
        ],
        "examples": ["温度", "湿度", "电压", "电流", "功率", "频率", "压力"]
    },
    "action": {
        "name": "动作",
        "description": "控制动作类型",
        "patterns": [
            r"开启|启动|打开",
            r"关闭|停止|关掉",
            r"调节|设置|调整",
            r"重启|复位"
        ],
        "examples": ["开启", "关闭", "调节", "重启"]
    },
    "value": {
        "name": "数值",
        "description": "参数数值",
        "patterns": [
            r"\d+\.?\d*°C",
            r"\d+\.?\d*%",
            r"\d+\.?\d*V",
            r"\d+\.?\d*A",
            r"\d+\.?\d*Hz"
        ],
        "examples": ["25°C", "60%", "220V", "10A", "50Hz"]
    },
    "time": {
        "name": "时间",
        "description": "时间相关信息",
        "patterns": [
            r"\d{1,2}:\d{2}",
            r"\d+分钟",
            r"\d+小时",
            r"现在|立即|马上"
        ],
        "examples": ["14:30", "10分钟", "2小时", "现在"]
    },
    "alarm_type": {
        "name": "报警类型",
        "description": "报警类型",
        "patterns": [
            r"高温报警",
            r"低温报警", 
            r"过载报警",
            r"断电报警",
            r"通信故障"
        ],
        "examples": ["高温报警", "低温报警", "过载报警", "断电报警", "通信故障"]
    }
}

# 常见位置映射
LOCATION_MAPPING = {
    "A区": {"zone": "A", "type": "zone"},
    "B区": {"zone": "B", "type": "zone"},
    "C区": {"zone": "C", "type": "zone"},
    "1号房": {"room": "1", "type": "room"},
    "2号房": {"room": "2", "type": "room"},
    "3号房": {"room": "3", "type": "room"}
}

# 设备映射
EQUIPMENT_MAPPING = {
    "主柜": {"type": "cabinet", "subtype": "main"},
    "副柜": {"type": "cabinet", "subtype": "secondary"},
    "UPS": {"type": "ups", "subtype": "power"},
    "空调": {"type": "air_conditioner", "subtype": "hvac"}
}