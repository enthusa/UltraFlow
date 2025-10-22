# API 参考文档

本文档详细介绍 UltraFlow 提供的 Python API 接口。如果你希望在 Python 代码中直接使用 UltraFlow 的功能，而不仅仅是使用命令行工具，那么这份文档将为你提供完整的 API 使用指南。

## 适用场景

- 需要在 Python 程序中集成 LLM 调用功能
- 需要对流程执行进行精细控制
- 需要批量处理大量数据
- 需要自定义错误处理和日志记录

## 核心类

### Prompty

`Prompty` 是 UltraFlow 的核心类，负责加载和执行 prompty 文件。它封装了以下功能：

- 解析 prompty 文件 (YAML 配置 + Jinja2 模板)
- 查找和加载连接配置
- 调用 LLM API
- 处理响应和 JSON 解析

**主要特点**：

- 支持 Jinja2 模板语法，可以动态生成提示词
- 自动管理 API 连接配置
- 集成 PromptFlow 的追踪功能
- 支持 JSON 格式输出的自动解析和修复

#### 初始化

```python
from ultraflow import Prompty

# 从文件加载
flow = Prompty.load('my_flow.prompty')

# 或者直接实例化
flow = Prompty('my_flow.prompty')
```

**参数：**

- `path` (str | PathLike): prompty 文件路径
- `model` (dict，可选)：模型配置，用于覆盖 prompty 文件中的配置
- `**kwargs`：其他可选参数

#### 执行流程

```python
# 调用流程，传入输入参数
result = flow(text="你好，请介绍一下你自己")
print(result)
```

**参数：**

- `**kwargs`：输入参数，必须与 prompty 文件中定义的 `inputs` 字段匹配

**返回值：**

- 如果 prompty 配置了 JSON 输出格式，返回解析后的字典对象
- 否则返回 LLM 响应的文本内容

#### 属性

- `path`：prompty 文件路径
- `model`：使用的模型名称
- `parameters`：模型参数 (包括 temperature、max_tokens 等)
- `connection`：连接配置 (URL、API Key 等)

#### 方法

##### resolve_inputs(input_values)

解析并验证输入参数。

```python
resolved = flow.resolve_inputs({'text': '你好'})
```

**参数：**

- `input_values` (dict)：输入参数字典

**返回值：**

- dict：解析后的输入参数

### FlowProcessor

`FlowProcessor` 是批量数据处理器，专门用于处理大量数据的场景。它提供了以下能力：

- 自动加载 JSON 格式的数据文件
- 支持单线程和多线程两种处理模式
- 自动切换处理模式 (根据 `max_workers` 参数)
- 实时显示处理进度

**使用场景**：

- 批量翻译大量文本
- 对数据集进行批量分析
- 批量生成内容
- 大规模数据清洗和标注

#### 初始化

```python
from ultraflow import FlowProcessor, Prompty

flow = Prompty.load('my_flow.prompty')
processor = FlowProcessor(
    flow=flow,
    data_path='test_data.json',
    max_workers=4  # 并发线程数
)
```

**参数：**

- `flow` (Prompty): Prompty 实例
- `data_path` (str | PathLike)：输入数据文件路径 (JSON 格式)
- `max_workers` (int，默认=2)：最大并发线程数，小于 2 时使用单线程模式

#### 运行处理器

```python
# 执行批量处理
results = processor.run()

# results 是一个列表，包含所有处理结果
for i, result in enumerate(results):
    print(f"结果 {i+1}: {result}")
```

**返回值：**

- list：处理结果列表，顺序可能与输入顺序不同 (多线程模式下)

#### 数据文件格式

输入数据文件应为 JSON 格式，可以是：

**单个对象：**

```json
{
  "text": "你好，请介绍一下你自己"
}
```

**对象数组：**

```json
[
  {"text": "第一个问题"},
  {"text": "第二个问题"},
  {"text": "第三个问题"}
]
```

## 工具函数

### generate_connection_config()

生成默认的连接配置 JSON 字符串。

```python
from ultraflow import generate_connection_config

config_json = generate_connection_config()
print(config_json)
```

**返回值：**

- str：连接配置的 JSON 字符串

**生成的配置结构：**

```json
{
  "ark_connection": {
    "url": "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
    "api_key": "<your_key>",
    "model_list": [
      "doubao-1-5-pro-32k-250115",
      "doubao-seed-1-6-thinking-250715"
    ]
  },
  "qwen_connection": {
    "url": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
    "api_key": "<your_key>",
    "model_list": [
      "qwen3-coder-plus"
    ]
  }
}
```

### generate_example_prompty()

生成示例 prompty 文件内容和对应的测试数据。

```python
from ultraflow import generate_example_prompty

data_json, prompty_content = generate_example_prompty()

# 保存到文件
with open('my_flow.json', 'w', encoding='utf-8') as f:
    f.write(data_json)

with open('my_flow.prompty', 'w', encoding='utf-8') as f:
    f.write(prompty_content)
```

**返回值：**

- tuple[str, str]: (测试数据 JSON 字符串，prompty 文件内容)

## 完整示例

### 示例 1：基本使用

```python
from ultraflow import Prompty

# 加载流程
flow = Prompty.load('translate.prompty')

# 单次调用
result = flow(text="Hello, how are you?")
print(result)
```

### 示例 2：批量处理

```python
from ultraflow import FlowProcessor, Prompty
from promptflow.tracing import start_trace

# 启动追踪 (可选，用于日志记录)
start_trace(collection='batch_translation')

# 加载流程
flow = Prompty.load('translate.prompty')

# 创建处理器
processor = FlowProcessor(
    flow=flow,
    data_path='test_cases.json',
    max_workers=5
)

# 执行批量处理
results = processor.run()

# 处理结果
for i, result in enumerate(results, 1):
    print(f"结果 {i}: {result}")
```

### 示例 3：自定义模型参数

```python
from ultraflow import Prompty

# 加载流程并覆盖模型参数
flow = Prompty.load('my_flow.prompty', model={
    'parameters': {
        'temperature': 0.7,
        'max_tokens': 2000
    }
})

result = flow(text="你的问题")
print(result)
```

## 异常处理

### 常见异常

#### FileNotFoundError

- **原因**: prompty 文件或数据文件不存在
- **解决**：检查文件路径是否正确

```python
from ultraflow import Prompty

try:
    flow = Prompty.load('non_existent.prompty')
except FileNotFoundError as e:
    print(f"文件未找到： {e}")
```

#### ValueError

- **原因**：模型在连接配置中未找到，或输入参数不匹配
- **解决**：检查 prompty 文件中的模型名称，确保在 connection_config.json 中有对应配置

```python
from ultraflow import Prompty

try:
    flow = Prompty.load('my_flow.prompty')
    result = flow()  # 缺少必需参数
except ValueError as e:
    print(f"参数错误： {e}")
```

#### KeyError

- **原因**：输入参数缺失
- **解决**：确保传入的参数与 prompty 文件中的 inputs 定义匹配

```python
from ultraflow import Prompty

flow = Prompty.load('my_flow.prompty')

try:
    # prompty 定义了 'text' 参数，但这里没有提供
    result = flow(question="你好")
except KeyError as e:
    print(f"缺少必需参数： {e}")
```

## 最佳实践

### 1. 使用追踪功能

PromptFlow 提供了追踪功能，可以记录所有 API 调用的详细信息：

```python
from promptflow.tracing import start_trace
from ultraflow import Prompty

# 启动追踪，指定集合名称
start_trace(collection='my_experiments')

flow = Prompty.load('my_flow.prompty')
result = flow(text="测试输入")

# 追踪数据会自动保存到 .promptflow 目录
```

### 2. 配置管理

建议将连接配置放在项目根目录的 `.ultraflow/connection_config.json` 中，UltraFlow 会自动向上查找配置文件。

### 3. 错误处理

在生产环境中，建议添加完整的错误处理：

```python
from ultraflow import Prompty
import logging

logging.basicConfig(level=logging.INFO)

def safe_run_flow(flow_path, **inputs):
    try:
        flow = Prompty.load(flow_path)
        result = flow(** inputs)
        return result
    except FileNotFoundError:
        logging.error(f"流程文件不存在： {flow_path}")
        return None
    except ValueError as e:
        logging.error(f"参数错误： {e}")
        return None
    except Exception as e:
        logging.error(f"执行失败： {e}")
        return None

result = safe_run_flow('my_flow.prompty', text='测试')
if result:
    print(result)
```

### 4. 性能优化

对于大批量数据处理，建议：

- 使用多线程模式 (设置 `max_workers` > 1)
- 根据 API 限流情况调整 `max_workers`
- 对于非常大的数据集，考虑分批处理

```python
from ultraflow import FlowProcessor, Prompty

flow = Prompty.load('my_flow.prompty')

# 根据 API 限流调整并发数
# 如果 API 限制 10 QPS，可以设置 max_workers=10
processor = FlowProcessor(
    flow=flow,
    data_path='large_dataset.json',
    max_workers=10
)

results = processor.run()
```
