# 硅基流动配置指南

本项目已集成硅基流动API，为语音控制机器人提供强大的大模型支持。

## 🌟 硅基流动优势

- **免费额度**：新用户注册送3亿token，足够开发测试使用
- **多模型支持**：提供Qwen、DeepSeek、InternLM等多种开源大模型
- **高性能**：自研推理加速引擎，响应速度快
- **兼容性好**：完全兼容OpenAI API格式，迁移简单
- **成本低廉**：按量计费，部分模型完全免费

## 🚀 快速开始

### 1. 注册账户

访问 [硅基流动官网](https://cloud.siliconflow.cn/) 注册账户

### 2. 获取API密钥

1. 登录后进入控制台
2. 点击左侧菜单"API密钥"
3. 点击"新建API密钥"按钮
4. 复制生成的API密钥

### 3. 配置环境变量

创建 `.env` 文件：

```env
# 硅基流动API配置
SILICONFLOW_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SILICONFLOW_BASE_URL=https://api.siliconflow.cn/v1
MODEL_NAME=Qwen/Qwen2.5-72B-Instruct
```

## 📋 推荐模型选择

### 免费模型（推荐开发测试）

| 模型名称 | 描述 | 适用场景 |
|---------|------|----------|
| `Qwen/Qwen2.5-7B-Instruct` | 轻量级模型，完全免费 | 开发测试、轻量应用 |
| `Qwen/Qwen2.5-72B-Instruct` | 高性能模型，免费使用 | 生产环境、复杂任务 |

### 付费模型（高级功能）

| 模型名称 | 描述 | 特点 |
|---------|------|------|
| `deepseek-ai/DeepSeek-V2.5` | 高性能通用模型 | 推理能力强，适合复杂NLP任务 |
| `Pro/deepseek-ai/DeepSeek-R1` | 推理专用模型 | 逻辑推理能力突出 |
| `internlm/internlm2_5-20b-chat` | 对话优化模型 | 对话理解能力强 |

## ⚙️ 配置示例

### 基础配置（使用免费模型）

```env
SILICONFLOW_API_KEY=your_api_key_here
MODEL_NAME=Qwen/Qwen2.5-7B-Instruct
```

### 高性能配置（使用大模型）

```env
SILICONFLOW_API_KEY=your_api_key_here
MODEL_NAME=Qwen/Qwen2.5-72B-Instruct
```

### 推理优化配置（使用推理模型）

```env
SILICONFLOW_API_KEY=your_api_key_here
MODEL_NAME=Pro/deepseek-ai/DeepSeek-R1
```

## 🧪 测试配置

配置完成后，运行测试验证：

```bash
# 运行系统测试
python3 test_system.py

# 测试单条指令
python3 main.py "巡检A区2号房主柜温度"

# 运行批量测试
python3 main.py test
```

## 💡 使用建议

### 开发阶段
- 使用 `Qwen/Qwen2.5-7B-Instruct` 免费模型
- 足够满足功能开发和调试需求
- 无需担心token消耗

### 生产环境
- 推荐 `Qwen/Qwen2.5-72B-Instruct` 
- 免费使用，性能优秀
- 适合处理复杂的语音指令

### 特殊需求
- 复杂推理任务：使用 `Pro/deepseek-ai/DeepSeek-R1`
- 对话优化：使用 `internlm/internlm2_5-20b-chat`
- 成本敏感：坚持使用免费模型

## 🔧 故障排除

### 常见问题

1. **API密钥无效**
   - 检查密钥是否正确复制
   - 确认密钥未过期
   - 验证账户状态正常

2. **模型不存在**
   - 检查模型名称拼写
   - 确认模型在硅基流动平台可用
   - 参考官方文档获取最新模型列表

3. **请求失败**
   - 检查网络连接
   - 确认API地址正确
   - 查看错误日志获取详细信息

### 调试方法

启用详细日志：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

查看API调用详情：

```bash
# 查看日志文件
tail -f logs/nlp_processor.log
```

## 📞 技术支持

- 官方文档：https://docs.siliconflow.cn/
- 技术交流群：查看官网获取最新信息
- 问题反馈：通过官网提交工单

## 🎯 最佳实践

1. **模型选择**：根据实际需求选择合适的模型
2. **缓存策略**：对相同指令进行缓存，减少API调用
3. **错误处理**：实现完善的降级机制
4. **监控告警**：监控API调用成功率和响应时间
5. **成本控制**：合理使用付费模型，避免不必要的开销

通过以上配置，你的语音控制机器人将获得强大的自然语言理解能力！