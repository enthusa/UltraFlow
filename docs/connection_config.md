# 连接配置说明

连接配置文件是 UltraFlow 连接各种大语言模型服务的桥梁。通过统一的配置格式，你可以轻松管理多个 LLM 服务提供商的 API 连接信息，在不同的模型之间自由切换。

## 配置文件的作用

连接配置文件主要解决以下问题：

1. **统一管理**：集中管理所有 LLM 服务的 API 配置
2. **灵活切换**：在不同模型之间快速切换，无需修改代码
3. **安全存储**：将敏感的 API Key 与代码分离
4. **多环境支持**：可以为开发、测试、生产环境配置不同的连接

## 配置文件位置

UltraFlow 按以下顺序查找配置文件：

1. 从当前目录开始，向上递归查找 `.ultraflow/connection_config.json`
2. 如果未找到，查找用户主目录 `~/.ultraflow/connection_config.json`

### 推荐位置

**项目级配置** (推荐)：

```
my_project/
  .ultraflow/
    connection_config.json  # 项目特定的配置
  flows/
    translate.prompty
    summarize.prompty
```

**全局配置**：

```
~/.ultraflow/
  connection_config.json    # 所有项目共享的配置
```

## 配置文件格式

### 基本结构

```json
{
  "连接名称 1": {
    "url": "API 端点 URL",
    "api_key": "API 密钥",
    "model_list": ["模型 1", "模型 2"]
  },
  "连接名称 2": {
    "url": "API 端点 URL",
    "api_key": "API 密钥",
    "model_list": ["模型 3", "模型 4"]
  }
}
```

### 字段说明

- **连接名称**：自定义的连接标识符，用于区分不同的服务提供商
- **url**：LLM API 的端点 URL
- **api_key**：API 访问密钥
- **model_list**：该连接支持的模型列表

## 支持的服务提供商

### 1. 字节跳动豆包 (Doubao)

```json
{
  "doubao_connection": {
    "url": "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
    "api_key": "your_api_key_here",
    "model_list": [
      "doubao-1-5-pro-32k-250115",
      "doubao-seed-1-6-thinking-250715"
    ]
  }
}
```

**获取 API Key：**

1. 访问 [火山引擎控制台](https://console.volcengine.com/)
2. 进入"火山方舟" > "API Key 管理"
3. 创建 API Key

### 2. 阿里云通义千问 (Qwen)

```json
{
  "qwen_connection": {
    "url": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
    "api_key": "your_api_key_here",
    "model_list": [
      "qwen-turbo",
      "qwen-plus",
      "qwen-max",
      "qwen3-coder-plus"
    ]
  }
}
```

**获取 API Key：**

1. 访问 [阿里云控制台](https://www.aliyun.com/)
2. 进入"阿里云百炼" > "应用开发" > "密钥管理"
3. 创建 API Key

### 3. OpenAI

```json
{
  "openai_connection": {
    "url": "https://api.openai.com/v1/chat/completions",
    "api_key": "your_api_key_here",
    "model_list": [
      "gpt-4",
      "gpt-4-turbo",
      "gpt-3.5-turbo"
    ]
  }
}
```

**获取 API Key：**

1. 访问 [OpenAI Platform](https://platform.openai.com/)
2. 进入"API Keys"
3. 创建新的 API Key

### 4. OpenAI 兼容服务

许多服务提供 OpenAI 兼容的 API，例如：

```json
{
  "azure_openai": {
    "url": "https://your-resource.openai.azure.com/openai/deployments/your-deployment/chat/completions?api-version=2024-02-15-preview",
    "api_key": "your_api_key_here",
    "model_list": ["gpt-4", "gpt-35-turbo"]
  },
  "local_llm": {
    "url": "http://localhost:8000/v1/chat/completions",
    "api_key": "dummy_key",
    "model_list": ["llama2-13b", "mistral-7b"]
  }
}
```

## 完整配置示例

```json
{
  "doubao_connection": {
    "url": "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
    "api_key": "0f1234567890abcdef1234567890abcdef",
    "model_list": [
      "doubao-1-5-pro-32k-250115",
      "doubao-seed-1-6-thinking-250715"
    ]
  },
  "qwen_connection": {
    "url": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
    "api_key": "sk-1234567890abcdef1234567890abcdef",
    "model_list": [
      "qwen-turbo",
      "qwen-plus",
      "qwen-max",
      "qwen3-coder-plus"
    ]
  },
  "openai_connection": {
    "url": "https://api.openai.com/v1/chat/completions",
    "api_key": "sk-proj-1234567890abcdef",
    "model_list": [
      "gpt-4",
      "gpt-4-turbo",
      "gpt-3.5-turbo"
    ]
  }
}
```

## 初始化配置

```bash
# 在当前目录初始化
uf init

# 在指定目录初始化
uf init my_project
```

## 配置管理

### 编辑配置

使用文本编辑器打开配置文件：

```bash
# macOS/Linux
vim .ultraflow/connection_config.json

# Windows
notepad .ultraflow\connection_config.json
```

### 添加新连接

在配置文件中添加新的连接对象：

```json
{
  "existing_connection": {
    "url": "...",
    "api_key": "...",
    "model_list": [...]
  },
  "new_connection": {
    "url": "https://api.example.com/v1/chat/completions",
    "api_key": "your_new_api_key",
    "model_list": ["model-1", "model-2"]
  }
}
```

### 更新 API Key

找到对应的连接，修改 `api_key` 字段：

```json
{
  "my_connection": {
    "url": "...",
    "api_key": "new_api_key_here",  # 更新这里
    "model_list": [...]
  }
}
```

### 添加模型

在对应连接的 `model_list` 中添加新模型：

```json
{
  "my_connection": {
    "url": "...",
    "api_key": "...",
    "model_list": [
      "existing-model",
      "new-model"  # 添加新模型
    ]
  }
}
```

## 安全建议

### 1. 保护 API Key

**不要**将包含真实 API Key 的配置文件提交到版本控制系统，或者取消项目中的配置，直接使用用户主目录下的配置：

```bash
# .gitignore
.ultraflow/connection_config.json
```

### 2. 权限设置

在 Linux/macOS 上，限制配置文件的访问权限：

```bash
chmod 600 .ultraflow/connection_config.json
```

## 故障排查

### 错误：Connection config file not found

**原因**：找不到配置文件

**解决方法**：

1. 检查当前目录及父目录是否有 `.ultraflow/connection_config.json`
2. 检查用户主目录是否有 `~/.ultraflow/connection_config.json`
3. 运行 `uf init` 初始化配置

### 错误：Model xxx not found in any connection

**原因**：prompty 文件中指定的模型在配置中找不到

**解决方法**：

1. 检查 prompty 文件中的模型名称
2. 确保配置文件中有对应的 `model_list` 包含该模型
3. 检查模型名称的拼写是否正确

```bash
# 查看配置文件内容
cat .ultraflow/connection_config.json
```

### 错误：API key is invalid

**原因**：API Key 错误或已过期

**解决方法**：

1. 检查 API Key 是否正确
2. 确认 API Key 是否仍然有效
3. 在服务商控制台重新生成 API Key

### JSON 格式错误

**原因**：配置文件不是有效的 JSON 格式

**解决方法**：

1. 使用 JSON 验证工具检查格式
2. 检查是否有缺少的逗号、引号
3. 使用 `uf init` 重新生成配置文件

```bash
# 验证 JSON 格式
python -m json.tool .ultraflow/connection_config.json
```

## 最佳实践

### 1. 使用描述性的连接名称

```json
{
  "doubao_prod": {  // 好：清楚表明用途
    ...
  },
  "conn1": {        // 差：不清楚
    ...
  }
}
```

### 2. 分组相关模型

```json
{
  "doubao_fast": {
    "url": "...",
    "api_key": "...",
    "model_list": ["doubao-lite"]
  },
  "doubao_quality": {
    "url": "...",
    "api_key": "...",
    "model_list": ["doubao-pro", "doubao-thinking"]
  }
}
```

### 3. 注释模型用途

虽然 JSON 不支持注释，但可以在连接名称中体现：

```json
{
  "openai_chat_models": {
    "url": "...",
    "model_list": ["gpt-4", "gpt-3.5-turbo"]
  },
  "openai_embedding_models": {
    "url": "...",
    "model_list": ["text-embedding-3-small"]
  }
}
```

### 4. 定期轮换 API Key

建议定期更新 API Key，特别是在以下情况：

- Key 可能泄露
- 团队成员变动
- 每 3-6 个月例行更新

### 5. 备份配置

定期备份配置文件 (去除敏感信息后)：

```bash
# 创建配置模板
cp .ultraflow/connection_config.json .ultraflow/connection_config.template.json
# 手动删除 template 文件中的 API Key，替换为占位符
```

## 高级配置

### 使用代理

如果需要通过代理访问 API，可以在 Python 代码中设置：

```python
import os

# 设置环境变量
os.environ['HTTP_PROXY'] = 'http://proxy.example.com:8080'
os.environ['HTTPS_PROXY'] = 'https://proxy.example.com:8080'

# 然后正常使用 UltraFlow
from ultraflow import Prompty
flow = Prompty.load('my_flow.prompty')
```

### 自定义 HTTP 请求

如果需要更多控制，可以修改 `Prompty` 类的 `call_chat_api` 方法 (高级用法)。
