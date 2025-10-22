# Prompty 文件格式说明

Prompty 是 UltraFlow 的核心文件格式，专门用于定义和管理大语言模型 (LLM) 的提示词。它巧妙地将结构化配置 (YAML) 和动态模板 (Jinja2) 结合在一起，让提示词的定义既简洁又强大。

## 为什么使用 Prompty 格式？

**解决的痛点**：

- ❌ 提示词散落在代码中，难以管理
- ❌ 参数和内容分散，不易维护
- ❌ 无法版本控制，改动难以追溯
- ❌ 团队协作时格式不统一

**Prompty 的优势**：

- ✅ **纯文本格式**：可以用任何编辑器打开，完美支持 Git
- ✅ **结构清晰**：配置和内容分离，一目了然
- ✅ **动态生成**：Jinja2 模板让提示词可以根据输入变化
- ✅ **易于调试**：可以独立测试配置和模板

**实际效果**：

```
使用前：提示词硬编码在 Python 代码中，修改需要改代码
使用后：prompty 文件独立管理，修改只需编辑文本文件

使用前：团队成员各自维护提示词，格式混乱
使用后：统一的 prompty 格式，协作更高效

使用前：提示词版本混乱，无法回溯
使用后：Git 管理 prompty 文件，完整版本历史
```

## 文件结构

Prompty 文件由两部分组成，使用 `---` 分隔符分隔：

```
---
YAML 配置部分
---
Jinja2 模板部分
```

## YAML 配置部分

### 基本结构

```yaml
---
name: 任务名称
description: 任务描述 (可选)
model:
  api: chat
  configuration:
    model: 模型名称
  parameters:
    temperature: 0.7
    max_tokens: 2000
inputs:
  参数名:
    type: 参数类型
    default: 默认值 (可选)
---
```

### 配置字段说明

#### name (可选)

任务名称，用于标识这个 prompty 文件的用途。

```yaml
name：英文翻译中文
```

#### description (可选)

任务描述，更详细地说明这个任务的功能。

```yaml
description：将英文文本翻译成中文，保持原文的语气和风格
```

#### model (必需)

模型配置，定义使用哪个 LLM 模型以及相关参数。

##### model.api

API 类型，目前支持：

- `chat`：聊天补全 API

```yaml
model:
  api: chat
```

##### model.configuration

模型基础配置。

- `model`：模型名称，必须在 `connection_config.json` 中有对应的配置

```yaml
model:
  configuration:
    model: doubao-1-5-pro-32k-250115
```

##### model.parameters

模型参数，会传递给 LLM API。

常用参数：

- `temperature` (float)：温度参数，控制输出的随机性，范围 0-2
  - 0：输出最确定
  - 1：平衡创造性和确定性
  - 2：输出最随机

- `max_tokens` (int)：最大输出 token 数

- `top_p` (float): nucleus sampling 参数，范围 0-1

- `presence_penalty` (float)：存在惩罚，范围 -2.0 到 2.0

- `frequency_penalty` (float)：频率惩罚，范围 -2.0 到 2.0

- `response_format` (object)：响应格式
  - `type: json_object`：要求模型输出 JSON 格式

```yaml
model:
  parameters:
    temperature: 0.7
    max_tokens: 2000
    top_p: 0.9
    response_format:
      type: json_object
```

#### inputs (必需)

定义输入参数，这些参数将在 Jinja2 模板中使用。

```yaml
inputs:
  text:
    type: string
  language:
    type: string
    default: "中文"
  style:
    type: string
    default: "正式"
```

支持的类型：

- `string`：字符串
- `number`：数字
- `boolean`：布尔值
- `object`：对象
- `array`：数组

## Jinja2 模板部分

模板部分使用 Jinja2 语法，定义发送给 LLM 的提示词。

### 基本格式

模板使用角色标记来定义对话：

```
system:
系统提示词内容

user:
用户消息内容

assistant:
助手回复内容 (用于少样本学习)
```

### 使用变量

使用 `{{ 变量名 }}` 来引用 inputs 中定义的参数：

```
user:
请将以下文本翻译成{{ language }}：

{{ text }}
```

### Jinja2 语法

#### 条件语句

```
{% if language == "英文" %}
Translate the following text to English:
{% else %}
请将以下文本翻译成{{ language }}：
{% endif %}

{{ text }}
```

#### 循环语句

```yaml
inputs:
  items:
    type: array
```

```
{% for item in items %}
{{ loop.index }}. {{ item }}
{% endfor %}
```

#### 注释

```
{# 这是注释，不会出现在最终的提示词中 #}
```

## 完整示例

### 示例 1：简单翻译

```yaml
---
name: 英文翻译中文
model:
  api: chat
  configuration:
    model: doubao-1-5-pro-32k-250115
  parameters:
    temperature: 0.3
    max_tokens: 4096
inputs:
  text:
    type: string
---
system:
你是一个专业的翻译助手，擅长将英文准确地翻译成中文。

user:
请将以下英文文本翻译成中文，保持原文的语气和风格：

{{ text }}
```

### 示例 2：JSON 格式输出

```yaml
---
name: 文本分析
model:
  api: chat
  configuration:
    model: doubao-1-5-pro-32k-250115
  parameters:
    temperature: 0.0
    max_tokens: 4096
    response_format:
      type: json_object
inputs:
  text:
    type: string
---
system:
你是一个文本分析专家，需要分析文本的情感、主题和关键信息。

## 输出准则

以 JSON 格式输出如下字段：
- `sentiment`: str，情感分析结果 (positive/negative/neutral)
- `topics`: list[str]，文本主题列表
- `keywords`: list[str]，关键词列表
- `summary`: str，文本摘要

user:
请分析以下文本：

{{ text }}
```

### 示例 3：多参数

```yaml
---
name: 邮件生成器
model:
  api: chat
  configuration:
    model: doubao-1-5-pro-32k-250115
  parameters:
    temperature: 0.7
    max_tokens: 2000
inputs:
  recipient:
    type: string
  subject:
    type: string
  content:
    type: string
  tone:
    type: string
    default: "专业"
---
system:
你是一个专业的邮件撰写助手。

user:
请帮我撰写一封邮件：

收件人：{{ recipient }}
主题：{{ subject }}
内容要点：{{ content }}
语气：{{ tone }}

请生成一封完整的邮件内容。
```

### 示例 4：少样本学习

```yaml
---
name: 情感分类
model:
  api: chat
  configuration:
    model: doubao-1-5-pro-32k-250115
  parameters:
    temperature: 0.0
    max_tokens: 100
inputs:
  text:
    type: string
---
system:
你是一个情感分析专家，需要判断文本的情感倾向。

user:
文本：这个产品太棒了，非常喜欢！

assistant:
positive

user:
文本：质量很差，非常失望。

assistant:
negative

user:
文本：还行吧，没什么特别的。

assistant:
neutral

user:
文本：{{ text }}
```

### 示例 5：复杂逻辑

```yaml
---
name: 多语言翻译
model:
  api: chat
  configuration:
    model: doubao-1-5-pro-32k-250115
  parameters:
    temperature: 0.3
    max_tokens: 4096
inputs:
  text:
    type: string
  source_lang:
    type: string
    default: "auto"
  target_lang:
    type: string
  preserve_format:
    type: boolean
    default: true
---
system:
你是一个专业的翻译助手，精通多种语言。

user:
{% if source_lang == "auto" %}
请识别以下文本的语言，并翻译成{{ target_lang }}：
{% else %}
请将以下{{ source_lang }}文本翻译成{{ target_lang }}：
{% endif %}

{% if preserve_format %}
注意：请保持原文的格式 (如段落、列表、加粗等)。
{% endif %}

---
{{ text }}
---
```

## 最佳实践

### 1. 系统提示词

系统提示词应该：

- 清晰定义 AI 的角色
- 说明任务的目标
- 提供必要的背景信息

```
system:
你是一个专业的代码审查助手，擅长发现代码中的问题并提供改进建议。
你的审查应该关注：
1. 代码质量
2. 潜在的 bug
3. 性能问题
4. 最佳实践
```

### 2. 结构化输出

对于需要结构化数据的场景，使用 JSON 格式输出：

```yaml
model:
  parameters:
    response_format:
      type: json_object
```

并在提示词中明确输出格式：

```
## 输出格式

以 JSON 格式输出，包含以下字段：
{
  "field1": "说明",
  "field2": "说明"
}
```

### 3. 参数命名

使用清晰、有意义的参数名：

```yaml
inputs:
  source_text:        # 好：清楚表达参数用途
    type: string
  text:               # 可以：简洁但不够明确
    type: string
  t:                  # 差：太简洁，不清楚含义
    type: string
```

### 4. 温度参数

根据任务类型选择合适的温度：

- `0.0 - 0.3`：事实性任务 (翻译、摘要、问答)
- `0.3 - 0.7`：平衡型任务 (邮件撰写、文章生成)
- `0.7 - 1.0`：创造性任务 (故事创作、头脑风暴)

### 5. 模板复用

对于相似的任务，可以使用条件语句复用模板：

```
{% if task_type == "translate" %}
请翻译以下文本：
{% elif task_type == "summarize" %}
请总结以下文本：
{% else %}
请分析以下文本：
{% endif %}

{{ text }}
```

## 调试技巧

### 1. 查看生成的消息

在开发过程中，可以通过追踪功能查看实际发送给 LLM 的消息：

```python
from promptflow.tracing import start_trace
from ultraflow import Prompty

start_trace(collection='debug')
flow = Prompty.load('my_flow.prompty')
result = flow(text='测试')

# 查看 .promptflow/runs 目录下的追踪日志
```

### 2. 测试变量替换

确保所有变量都能正确替换：

```python
from ultraflow import Prompty

flow = Prompty.load('my_flow.prompty')

# 测试 resolve_inputs
inputs = flow.resolve_inputs({'text': '测试文本'})
print(inputs)
```

### 3. 逐步构建

从简单的提示词开始，逐步添加复杂性：

1. 先测试基本的系统提示词和用户消息
2. 添加变量
3. 添加条件逻辑
4. 添加少样本示例
5. 调整参数优化效果

## 常见问题

### Q：如何在模板中使用引号？

A：直接使用即可，Jinja2 会自动处理：

```
user:
请分析这句话："{{ text }}"的含义。
```

### Q：如何处理多行文本？

A：使用 YAML 的多行语法：

```yaml
inputs:
  text:
    type: string
```

```
user:
请分析以下文本：

"""
{{ text }}
"""
```

### Q：变量为空时怎么办？

A：可以设置默认值：

```
{{ text | default("没有提供文本") }}
```

### Q：如何调试 Jinja2 模板？

A：使用 Python 的 Jinja2 库进行测试：

```python
from jinja2 import Template

template_str = """
user:
Hello {{ name }}!
"""

template = Template(template_str)
result = template.render(name='World')
print(result)
```
