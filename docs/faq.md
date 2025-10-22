# 常见问题 (FAQ)

本文档整理了使用 UltraFlow 过程中最常遇到的 30 个问题及其解决方案。问题按类别组织，方便你快速找到答案。

## 问题分类

- **安装相关** (Q1-Q3)：安装和环境配置问题
- **配置相关** (Q4-Q6)：连接配置和模型设置问题
- **文件相关** (Q7-Q9)：文件操作和格式问题
- **执行相关** (Q10-Q13)：流程运行和 API 调用问题
- **Python API 相关** (Q14-Q16)：Python 编程接口使用问题
- **Prompty 文件相关** (Q17-Q20)：Prompty 格式和语法问题
- **性能相关** (Q21-Q22)：性能优化和限流问题
- **调试相关** (Q23-Q25)：调试技巧和问题排查
- **其他问题** (Q26-Q30)：其他常见疑问

💡 **提示**：如果你的问题在这里没有找到答案，欢迎在 [GitHub Issues](https://github.com/enthusa/UltraFlow/issues) 提问。

## 安装相关

### Q1：如何安装 UltraFlow？

**A:** 使用 pip 安装：

```bash
pip install -U UltraFlow
```

如果网络较慢，可以使用国内镜像：

```bash
pip install -U UltraFlow -i https://mirrors.aliyun.com/pypi/simple/
```

### Q2：安装后 `uf` 命令找不到？

**A:** 可能是因为 Python 的 scripts 目录不在 PATH 中。解决方法：

1. 检查 `uf` 是否已安装：
   ```bash
   python -m ultraflow.cli.main --version
   ```

2. 如果可以运行，添加 scripts 目录到 PATH，或者使用别名：
   ```bash
   alias uf='python -m ultraflow.cli.main'
   ```

3. 或者使用 pipx 安装 (推荐)：
   ```bash
   pipx install UltraFlow
   ```

### Q3：安装时出现依赖冲突怎么办？

**A:** 建议使用虚拟环境：

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install UltraFlow
```

## 配置相关

### Q4: Connection config file not found 错误

**A:** 这表示找不到连接配置文件。解决方法：

1. 运行 `uf init` 初始化配置：
   ```bash
   uf init
   ```

2. 或者在用户主目录创建全局配置：
   ```bash
   mkdir -p ~/.ultraflow
   uf init ~
   ```

3. 检查配置文件是否存在：
   ```bash
   ls -la .ultraflow/connection_config.json
   # 或
   ls -la ~/.ultraflow/connection_config.json
   ```

### Q5: Model xxx not found in any connection 错误

**A:** 这表示模型在配置中找不到。解决方法：

1. 检查 prompty 文件中的模型名称：
   ```yaml
   model:
     configuration:
       model: doubao-1-5-pro-32k-250115  # 检查这个名称
   ```

2. 确保配置文件中有对应的模型：
   ```json
   {
     "my_connection": {
       "model_list": ["doubao-1-5-pro-32k-250115"]  # 必须包含
     }
   }
   ```

3. 检查模型名称拼写是否正确。

### Q6：如何配置多个 API Key？

**A:** 在配置文件中添加多个连接：

```json
{
  "doubao_dev": {
    "url": "...",
    "api_key": "dev_key_here",
    "model_list": ["doubao-pro"]
  },
  "doubao_prod": {
    "url": "...",
    "api_key": "prod_key_here",
    "model_list": ["doubao-pro"]
  }
}
```

在 prompty 文件中使用不同的模型名来区分不同的环境。

## 文件相关

### Q7：文件已存在的警告如何处理？

**A:** 有几个选择：

1. 重命名新文件：
   ```bash
   uf new my_flow_v2
   ```

2. 删除旧文件：
   ```bash
   rm my_flow.prompty my_flow.json
   uf new my_flow
   ```

3. 手动编辑现有文件。

### Q8：如何指定不同的数据文件？

**A:** 使用 `--data` 参数：

```bash
uf run my_flow --data custom_data.json
# 或简写
uf run my_flow -d custom_data.json
```

### Q9：数据文件的格式要求是什么？

**A:** 数据文件必须是 JSON 格式，可以是：

1. 单个对象：
   ```json
   {
     "text": "你好"
   }
   ```

2. 对象数组 (批量处理)：
   ```json
   [
     {"text": "第一条"},
     {"text": "第二条"}
   ]
   ```

字段名必须与 prompty 文件中的 `inputs` 定义匹配。

## 执行相关

### Q10：如何调整并发线程数？

**A:** 使用 `--max_workers` 参数：

```bash
uf run my_flow --max_workers 5
# 或简写
uf run my_flow -w 5
```

注意：

- 小于 2 时使用单线程模式
- 建议根据 API 限流设置
- 过多线程可能触发 API 限流

### Q11：如何查看执行的详细日志？

**A:** UltraFlow 使用 PromptFlow 的追踪功能，日志保存在 `.promptflow` 目录。直观地，提供网页查看方式，地址将会直接打印在终端。

### Q12: API 调用失败怎么办？

**A:** 常见原因和解决方法：

1. **API Key 错误**：
   - 检查配置文件中的 API Key 是否正确
   - 确认 Key 未过期

2. **网络问题**：
   - 检查网络连接
   - 尝试使用代理

3. **限流**：
   - 减少并发数：`--max_workers 2`
   - 增加请求间隔

4. **模型不可用**：
   - 检查模型名称是否正确
   - 确认该模型对你的账号可用

### Q13: JSON 输出解析失败

**A:** 当要求 JSON 输出时，可能出现解析错误：

1. 确保在 prompty 中设置了 JSON 格式：
   ```yaml
   model:
     parameters:
       response_format:
         type: json_object
   ```

2. 在提示词中明确输出格式：
   ```
   以 JSON 格式输出，包含以下字段：
   {
     "field1": "value1",
     "field2": "value2"
   }
   ```

3. UltraFlow 使用 `json_repair` 库尝试修复格式错误，但不保证总是成功。

## Python API 相关

### Q14：如何在 Python 代码中使用 UltraFlow？

**A:** 基本使用示例：

```python
from ultraflow import Prompty

# 加载流程
flow = Prompty.load('my_flow.prompty')

# 调用
result = flow(text="你的输入")
print(result)
```

批量处理：

```python
from ultraflow import FlowProcessor, Prompty

flow = Prompty.load('my_flow.prompty')
processor = FlowProcessor(flow, 'data.json', max_workers=4)
results = processor.run()
```

### Q15：如何自定义模型参数？

**A:** 在加载时覆盖参数：

```python
from ultraflow import Prompty

flow = Prompty.load('my_flow.prompty', model={
    'parameters': {
        'temperature': 0.9,
        'max_tokens': 3000
    }
})
```

### Q16：如何处理异常？

**A:** 建议使用 try-except：

```python
from ultraflow import Prompty

try:
    flow = Prompty.load('my_flow.prompty')
    result = flow(text='测试')
except FileNotFoundError:
    print("流程文件不存在")
except ValueError as e:
    print(f"参数错误： {e}")
except KeyError as e:
    print(f"缺少必需参数： {e}")
except Exception as e:
    print(f"执行失败： {e}")
```

## Prompty 文件相关

### Q17: Prompty 文件的基本格式是什么？

**A:** Prompty 文件由两部分组成：

```yaml
---
name：任务名称
model:
  api: chat
  configuration:
    model：模型名称
  parameters:
    temperature: 0.7
inputs:
  text:
    type: string
---
system:
系统提示词

user:
{{ text }}
```

详见 [Prompty 文件格式说明](prompty_format.md)。

### Q18：如何在提示词中使用条件语句？

**A:** 使用 Jinja2 语法：

```
{% if language == "English" %}
Translate to English:
{% else %}
翻译成中文：
{% endif %}

{{ text }}
```

### Q19：如何传递列表参数？

**A:** 在 inputs 中定义数组类型：

```yaml
inputs:
  items:
    type: array
```

在模板中遍历：

```
{% for item in items %}
{{ loop.index }}. {{ item }}
{% endfor %}
```

### Q20：支持多模态输入吗 (如图片)？

**A:** 当前版本主要支持文本输入。对于图片等多模态输入，需要：

1. 将图片转换为 base64 或 URL
2. 在 inputs 中定义相应参数
3. 使用支持多模态的模型

## 性能相关

### Q21：如何提高处理速度？

**A:** 几个建议：

1. **增加并发数**：
   ```bash
   uf run my_flow --max_workers 10
   ```

2. **使用更快的模型**：
   - 例如 `gpt-3.5-turbo` 比 `gpt-4` 快

3. **减少 max_tokens**：
   ```yaml
   parameters:
     max_tokens: 500  # 降低到合理范围
   ```

4. **降低 temperature**：
   ```yaml
   parameters:
     temperature: 0.0  # 最快但最确定
   ```

### Q22：批量处理时如何避免超出限流？

**A:**

1. 控制并发数：
   ```python
   processor = FlowProcessor(flow, 'data.json', max_workers=2)
   ```

2. 添加延迟 (需要修改代码)：
   ```python
   import time
   for item in items:
       result = flow(**item)
       time.sleep(0.5)  # 延迟 0.5 秒
   ```

3. 分批处理：
   ```python
   # 将大数据集分成小批次
   batch_size = 100
   for i in range(0, len(data), batch_size):
       batch = data[i:i+batch_size]
       # 处理 batch
   ```

## 调试相关

### Q23：如何调试 Prompty 模板？

**A:** 几个方法：

1. **使用追踪功能**：
   ```python
   from promptflow.tracing import start_trace
   start_trace(collection='debug')
   ```

2. **打印 resolved inputs**：
   ```python
   flow = Prompty.load('my_flow.prompty')
   inputs = flow.resolve_inputs({'text': '测试'})
   print(inputs)
   ```

3. **单独测试 Jinja2 模板**：
   ```python
   from jinja2 import Template
   template = Template("Hello {{ name }}!")
   print(template.render(name='World'))
   ```

### Q24：如何查看实际发送给 LLM 的消息？

**A:** 使用追踪功能后，查看 trace 网页，一般在 <http://127.0.0.1:23333>，里面包含完整的请求和响应。

### Q25：输出结果不符合预期怎么办？

**A:** 调试步骤：

1. **检查提示词**：
   - 是否清晰明确？
   - 是否提供了足够的上下文？

2. **调整温度**：
   - 降低 temperature 获得更确定的输出
   - 提高 temperature 获得更多样的输出

3. **添加示例**：
   - 使用少样本学习 (few-shot)
   - 提供期望输出的示例

4. **迭代优化**：
   - 逐步调整提示词
   - 测试不同的参数组合

## 其他问题

### Q26：UltraFlow 与 PromptFlow 的关系？

**A:** UltraFlow 基于 PromptFlow，主要区别：

- UltraFlow 简化了配置和部署
- 连接配置使用 JSON 文件 (而非加密存储)
- 更注重命令行工具的易用性
- 保留了 PromptFlow 的追踪和日志功能

### Q27：可以在生产环境使用吗？

**A:** 可以，但建议：

1. 充分测试流程
2. 实现完整的错误处理
3. 监控 API 调用情况
4. 设置合理的超时和重试
5. 考虑成本控制

### Q28：如何贡献代码？

**A:** 欢迎贡献！请查看 [参与开发](collaboration_tutorial.md) 文档。

### Q29：在哪里获取帮助？

**A:** 

1. 查看文档：<https://enthusa.github.io/UltraFlow/>
2. GitHub Issues：<https://github.com/enthusa/UltraFlow/issues>
3. 阅读现有 Issues 和 Discussions

### Q30：支持哪些 LLM 服务商？

**A:** 理论上支持所有提供 OpenAI 兼容 API 的服务商，包括：

- OpenAI
- Azure OpenAI
- 字节跳动豆包 (Doubao)
- 阿里云通义千问 (Qwen)
- 本地部署的 LLM(如 llama.cpp、vLLM)

只需在配置文件中添加相应的 URL 和 API Key。

---

如果你的问题没有在这里找到答案，欢迎在 GitHub 上提 Issue！
