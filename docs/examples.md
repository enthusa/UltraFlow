# 实用示例

本文档提供了 13 个精心设计的实用示例，涵盖从基础到高级的各种应用场景。每个示例都包含完整的代码和详细说明，你可以直接复制使用，或根据自己的需求进行修改。

## 示例导航

**文本处理** (示例 1-3)：

- 翻译、摘要、情感分析

**内容生成** (示例 4-6)：

- 邮件撰写、文章大纲、代码生成

**数据处理** (示例 7-8)：

- 信息提取、数据清洗

**问答系统** (示例 9-10)：

- FAQ 问答、多轮对话

**高级应用** (示例 11-13)：

- 思维链推理、少样本学习、复杂分析

## 如何使用这些示例

1. **复制示例代码**：将 prompty 文件和数据文件保存到本地
2. **配置连接**：确保已运行 `uf init` 初始化配置
3. **修改 API Key**：在配置文件中设置你的 API Key
4. **运行测试**：使用 `uf run` 命令或 Python API 运行示例
5. **根据需求调整**：修改模板内容、参数设置，适配你的场景

## 文本处理示例

### 1. 文本翻译

创建一个英译中的翻译流程：

**translate_en_zh.prompty:**

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
你是一个专业的翻译助手，擅长将英文准确地翻译成中文，保持原文的语气和风格。

user:
请将以下英文文本翻译成中文：

{{ text }}
```

**test_data.json:**

```json
[
  {
    "text": "Hello, how are you today?"
  },
  {
    "text": "Machine learning is a subset of artificial intelligence."
  },
  {
    "text": "The quick brown fox jumps over the lazy dog."
  }
]
```

**运行：**

```bash
uf run translate_en_zh
```

### 2. 文本摘要

创建文本摘要流程：

**summarize.prompty:**

```yaml
---
name: 文本摘要
model:
  api: chat
  configuration:
    model: doubao-1-5-pro-32k-250115
  parameters:
    temperature: 0.5
    max_tokens: 500
inputs:
  text:
    type: string
  max_words:
    type: number
---
system:
你是一个专业的文本摘要助手，能够提炼文章的核心要点。

user:
请将以下文本概括为不超过 {{ max_words }} 字的摘要：

{{ text }}
```

**Python 调用：**

```python
from ultraflow import Prompty

flow = Prompty.load('summarize.prompty')
result = flow(
    text="这是一篇很长的文章...",
    max_words=100
)
print(result)
```

### 3. 情感分析

创建情感分析流程，输出 JSON 格式：

**sentiment_analysis.prompty:**

```yaml
---
name: 情感分析
model:
  api: chat
  configuration:
    model: doubao-1-5-pro-32k-250115
  parameters:
    temperature: 0.0
    max_tokens: 200
    response_format:
      type: json_object
inputs:
  text:
    type: string
---
system:
你是一个情感分析专家，需要分析文本的情感倾向。

## 输出准则

以 JSON 格式输出如下字段：
- `sentiment`: str，情感分类 (positive/negative/neutral)
- `confidence`: float，置信度 (0-1)
- `reason`: str，判断理由

user:
请分析以下文本的情感：

{{ text }}
```

**批量处理：**

```python
from ultraflow import FlowProcessor, Prompty

flow = Prompty.load('sentiment_analysis.prompty')
processor = FlowProcessor(
    flow=flow,
    data_path='reviews.json',
    max_workers=5
)

results = processor.run()

# 统计结果
sentiments = [r['sentiment'] for r in results]
positive_count = sentiments.count('positive')
negative_count = sentiments.count('negative')
neutral_count = sentiments.count('neutral')

print(f"正面： {positive_count}")
print(f"负面： {negative_count}")
print(f"中性： {neutral_count}")
```

## 内容生成示例

### 4. 邮件生成

**email_generator.prompty:**

```yaml
---
name: 邮件生成器
model:
  api: chat
  configuration:
    model: doubao-1-5-pro-32k-250115
  parameters:
    temperature: 0.7
    max_tokens: 1000
inputs:
  recipient:
    type: string
  subject:
    type: string
  key_points:
    type: string
  tone:
    type: string
---
system:
你是一个专业的邮件撰写助手，能够根据要求撰写得体的商务邮件。

user:
请帮我撰写一封邮件：

**收件人：** {{ recipient }}
**主题：** {{ subject }}
**内容要点：** {{ key_points }}
**语气：** {{ tone }}

请生成完整的邮件内容，包括称呼、正文和结尾。
```

### 5. 文章大纲生成

**outline_generator.prompty:**

```yaml
---
name: 文章大纲生成
model:
  api: chat
  configuration:
    model: doubao-1-5-pro-32k-250115
  parameters:
    temperature: 0.8
    max_tokens: 2000
    response_format:
      type: json_object
inputs:
  topic:
    type: string
  word_count:
    type: number
  target_audience:
    type: string
---
system:
你是一个专业的内容策划师，擅长创建结构清晰的文章大纲。

## 输出准则

以 JSON 格式输出如下字段：
- `title`: str，文章标题
- `introduction`: str，引言概要
- `sections`: list[object]，章节列表
  - `section_title`: str，章节标题
  - `key_points`: list[str]，要点列表
- `conclusion`: str，结论概要

user:
请为以下主题创建文章大纲：

**主题：** {{ topic }}
**目标字数：** {{ word_count }}
**目标读者：** {{ target_audience }}
```

### 6. 代码生成

**code_generator.prompty:**

```yaml
---
name: 代码生成器
model:
  api: chat
  configuration:
    model: qwen3-coder-plus
  parameters:
    temperature: 0.2
    max_tokens: 2000
inputs:
  requirement:
    type: string
  language:
    type: string
---
system:
你是一个专业的程序员，精通多种编程语言，能够根据需求编写高质量的代码。

user:
请用 {{ language }} 编写代码实现以下需求：

{{ requirement }}

请提供完整的代码，包含必要的注释。
```

## 数据处理示例

### 7. 结构化信息提取

**extract_info.prompty:**

```yaml
---
name: 信息提取
model:
  api: chat
  configuration:
    model: doubao-1-5-pro-32k-250115
  parameters:
    temperature: 0.0
    max_tokens: 1000
    response_format:
      type: json_object
inputs:
  text:
    type: string
  schema:
    type: string
---
system:
你是一个信息提取专家，能够从文本中提取结构化信息。

user:
请从以下文本中提取信息，按照指定的 schema 格式输出：

**文本：**
{{ text }}

**Schema：**
{{ schema }}
```

**使用示例：**

```python
from ultraflow import Prompty

flow = Prompty.load('extract_info.prompty')

text = """
张三，男，30 岁，软件工程师，毕业于清华大学计算机系。
联系方式：13800138000，邮箱：zhangsan@example.com
"""

schema = """
{
  "name": "姓名",
  "gender": "性别",
  "age": "年龄",
  "occupation": "职业",
  "education": "学历",
  "phone": "电话",
  "email": "邮箱"
}
"""

result = flow(text=text, schema=schema)
print(result)
```

### 8. 批量数据清洗

**data_cleaning.prompty:**

```yaml
---
name: 数据清洗
model:
  api: chat
  configuration:
    model: doubao-1-5-pro-32k-250115
  parameters:
    temperature: 0.0
    max_tokens: 500
    response_format:
      type: json_object
inputs:
  raw_text:
    type: string
---
system:
你是一个数据清洗专家，需要标准化和规范化文本数据。

## 输出准则

以 JSON 格式输出如下字段：
- `cleaned_text`: str，清洗后的文本
- `issues_fixed`: list[str]，修复的问题列表

user:
请清洗以下文本：
- 移除多余的空格和换行
- 统一标点符号
- 修正明显的错别字

{{ raw_text }}
```

## 问答系统示例

### 9. FAQ 问答

**faq_qa.prompty:**

```yaml
---
name: FAQ 问答
model:
  api: chat
  configuration:
    model: doubao-1-5-pro-32k-250115
  parameters:
    temperature: 0.3
    max_tokens: 1000
inputs:
  question:
    type: string
  context:
    type: string
---
system:
你是一个客服助手，需要根据提供的 FAQ 文档回答用户的问题。

user:
**FAQ 文档：**
{{ context }}

**用户问题：**
{{ question }}

请根据 FAQ 文档回答用户的问题。如果 FAQ 中没有相关信息，请礼貌地告知用户。
```

### 10. 多轮对话支持

对于需要上下文的对话，可以在模板中包含历史消息：

**chat_with_history.prompty:**

```yaml
---
name: 多轮对话
model:
  api: chat
  configuration:
    model: doubao-1-5-pro-32k-250115
  parameters:
    temperature: 0.7
    max_tokens: 1000
inputs:
  history:
    type: string
  question:
    type: string
---
system:
你是一个智能助手，能够根据对话历史回答问题。

{{ history }}

user:
{{ question }}
```

**Python 使用：**

```python
from ultraflow import Prompty

flow = Prompty.load('chat_with_history.prompty')

# 维护对话历史
history = ""

while True:
    question = input("你： ")
    if question.lower() in ['exit', 'quit', '退出']:
        break

    # 调用 LLM
    response = flow(history=history, question=question)
    print(f"助手： {response}")

    # 更新历史
    history += f"user:\n{question}\n\nA:\n{response}\n\n"
```

## 高级应用示例

### 11. 思维链提示 (Chain of Thought)

**cot_reasoning.prompty:**

```yaml
---
name: 思维链推理
model:
  api: chat
  configuration:
    model: doubao-seed-1-6-thinking-250715
  parameters:
    temperature: 0.7
    max_tokens: 3000
inputs:
  problem:
    type: string
---
system:
你是一个逻辑推理专家。解决问题时，请先进行逐步推理，然后给出最终答案。

user:
请解决以下问题，要求：
1. 展示你的推理过程 (Think step by step)
2. 给出最终答案

**问题：**
{{ problem }}
```

### 12. 少样本学习 (Few-shot Learning)

**few_shot_classification.prompty:**

```yaml
---
name: 少样本分类
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
你是一个文本分类专家，根据示例进行分类。

user:
文本：iPhone 14 Pro Max 价格降了！

A:
科技

user:
文本：今天天气真不错，适合出去玩。

A:
生活

user:
文本：NBA 总决赛今晚开打。

A:
体育

user:
文本：股市今天大涨，沪指突破 3000 点。

A:
财经

user:
文本：{{ text }}
```

### 13. 复杂 JSON 输出

**complex_analysis.prompty:**

```yaml
---
name: 复杂文本分析
model:
  api: chat
  configuration:
    model: doubao-1-5-pro-32k-250115
  parameters:
    temperature: 0.2
    max_tokens: 2000
    response_format:
      type: json_object
inputs:
  text:
    type: string
---
system:
你是一个高级文本分析专家，需要对文本进行全面分析。

## 输出准则

以 JSON 格式输出，包含以下字段：
- `summary`: str，文本摘要
- `sentiment`: object，情感分析
  - `overall`: str(positive/negative/neutral)
  - `score`: float(0-1)
- `entities`: list[object]，实体识别
  - `text`: str，实体文本
  - `type`: str，实体类型 (PERSON/ORG/LOC/TIME)
- `keywords`: list[str]，关键词列表
- `topics`: list[str]，主题列表
- `language`: str，语言

user:
请全面分析以下文本：

{{ text }}
```

## 最佳实践

### 使用追踪功能记录实验

```python
from promptflow.tracing import start_trace
from ultraflow import Prompty
import time

# 为每次实验创建独立的追踪集合
experiment_name = f"translation_test_{time.strftime('%Y%m%d_%H%M%S')}"
start_trace(collection=experiment_name)

flow = Prompty.load('translate.prompty')

# 运行测试
test_cases = [
    "Hello, world!",
    "How are you?",
    "Good morning!"
]

for text in test_cases:
    result = flow(text=text)
    print(f"{text} -> {result}")

# 追踪数据保存在 .promptflow/runs/{experiment_name}/
```

## 总结

这些示例涵盖了 UltraFlow 的主要应用场景：

1. **文本处理**：翻译、摘要、情感分析
2. **内容生成**：邮件、大纲、代码
3. **数据处理**：信息提取、数据清洗
4. **问答系统**：FAQ、多轮对话
5. **高级应用**：思维链、少样本学习

你可以根据实际需求修改这些模板，创建适合自己场景的提示词流程。
