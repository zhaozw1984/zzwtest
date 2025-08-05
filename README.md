# 语音控制机器人自然语言处理系统

这是一个基于大模型的语音控制机器人自然语言处理系统，能够理解用户的语音指令，识别意图并提取相关参数。

## 功能特性

- **意图识别**：识别用户指令的意图类型（巡检、设备控制、状态查询、报警处理、导航移动）
- **实体抽取**：提取指令中的关键信息（位置、设备、参数、动作等）
- **语义理解**：结合规则匹配和大模型分析，提供准确的语义理解
- **结构化输出**：将自然语言指令转换为结构化的机器可执行指令
- **多种接口**：支持命令行、交互式和API接口

## 支持的指令类型

### 1. 巡检指令 (patrol_inspection)
- 示例：`"巡检A区2号房主柜温度"`
- 提取：位置(A区、2号房)、设备(主柜)、参数(温度)

### 2. 设备控制 (equipment_control)
- 示例：`"开启B区空调"`、`"设置空调温度为25度"`
- 提取：动作(开启/设置)、设备(空调)、位置(B区)、数值(25度)

### 3. 状态查询 (status_query)
- 示例：`"查询UPS1状态"`
- 提取：设备(UPS1)、查询参数

### 4. 报警处理 (alarm_handling)
- 示例：`"确认高温报警"`
- 提取：报警类型(高温报警)

### 5. 导航移动 (navigation)
- 示例：`"前往C区3号房"`
- 提取：目标位置(C区、3号房)

## 安装和配置

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置环境变量
复制 `.env.example` 为 `.env` 并配置：
```bash
cp .env.example .env
```

编辑 `.env` 文件：
```env
# 大模型API配置
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
MODEL_NAME=gpt-3.5-turbo
```

### 3. 创建日志目录
```bash
mkdir logs
```

## 使用方法

### 1. 交互式模式
```bash
python main.py
```
然后输入语音指令进行测试。

### 2. 单条指令处理
```bash
python main.py "巡检A区2号房主柜温度"
```

### 3. 批量测试
```bash
python main.py test
```

### 4. API服务模式
```bash
python main.py server
```
服务将在 `http://localhost:8000` 启动。

#### API接口

**POST /process**
```json
{
    "text": "巡检A区2号房主柜温度",
    "context": {
        "session_id": "session_123",
        "user_id": "user_456"
    }
}
```

**响应示例**：
```json
{
    "success": true,
    "result": {
        "original_text": "巡检A区2号房主柜温度",
        "intent": {
            "type": "patrol_inspection",
            "name": "巡检",
            "confidence": 0.95,
            "description": "巡检相关指令，包括温度、湿度、电压等参数检查"
        },
        "entities": [
            {
                "type": "location",
                "value": "A区",
                "start": 2,
                "end": 4,
                "confidence": 0.9,
                "normalized_value": {"zone": "A", "type": "zone"}
            },
            {
                "type": "location", 
                "value": "2号房",
                "start": 4,
                "end": 7,
                "confidence": 0.9,
                "normalized_value": {"room": "2", "type": "room"}
            },
            {
                "type": "equipment",
                "value": "主柜",
                "start": 7,
                "end": 9,
                "confidence": 0.9,
                "normalized_value": {"type": "cabinet", "subtype": "main"}
            },
            {
                "type": "parameter",
                "value": "温度",
                "start": 9,
                "end": 11,
                "confidence": 0.9,
                "normalized_value": {"parameter_type": "温度", "unit": "°C"}
            }
        ],
        "confidence": 0.92,
        "structured_command": {
            "action": "patrol_inspection",
            "location": {"zone": "A", "room": "2"},
            "equipment": "主柜",
            "parameter": "温度"
        },
        "is_valid": true,
        "validation_errors": [],
        "timestamp": "2024-01-01T12:00:00"
    }
}
```

## 系统架构

```
├── config.py              # 配置文件，定义意图类型和实体类型
├── models.py              # 数据模型定义
├── intent_classifier.py   # 意图识别模块
├── entity_extractor.py    # 实体抽取模块
├── llm_client.py          # 大模型客户端
├── nlp_processor.py       # 主控制器
└── main.py               # 程序入口
```

## 工作流程

1. **文本预处理**：对输入的语音转文本结果进行预处理
2. **规则分析**：使用关键词匹配和正则表达式进行初步分析
3. **大模型分析**：调用大模型API进行深度语义理解
4. **结果融合**：将规则分析和大模型分析结果进行融合
5. **验证和结构化**：验证指令完整性并生成结构化输出

## 扩展指南

### 添加新的意图类型
1. 在 `config.py` 的 `INTENT_TYPES` 中添加新意图定义
2. 在 `intent_classifier.py` 中添加相应的识别规则
3. 在 `nlp_processor.py` 中添加结构化指令构建逻辑

### 添加新的实体类型
1. 在 `config.py` 的 `ENTITY_TYPES` 中添加新实体定义
2. 在 `entity_extractor.py` 中添加标准化逻辑
3. 更新大模型的提示词

### 集成其他大模型
1. 在 `llm_client.py` 中添加新的客户端实现
2. 在 `config.py` 中添加相应的配置选项

## 注意事项

- 确保大模型API密钥配置正确
- 系统支持离线运行（不使用大模型功能）
- 建议在生产环境中配置日志轮转
- 可根据实际场景调整置信度阈值

## 许可证

MIT License