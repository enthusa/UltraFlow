# 快速开始

欢迎使用 UltraFlow！这份快速入门指南将帮助你在 10 分钟内完成安装、配置并运行你的第一个 AI 提示词流程。

UltraFlow (简称 `uf`) 是一个强大而简洁的命令行工具，让你能够像管理代码一样管理大语言模型的提示词。它的核心是 `.prompty` 文件格式，将配置和提示词模板优雅地组合在一起。

## 为什么选择 UltraFlow？

- ✅ **简单易用**：三个命令完成从配置到运行的全流程
- ✅ **版本管理**：纯文本格式，完美支持 Git 版本控制
- ✅ **批量处理**：内置多线程支持，轻松处理大规模数据
- ✅ **灵活集成**：既可命令行使用，也可作为 Python 库调用
- ✅ **完善追踪**：集成 PromptFlow 追踪功能，记录每次调用详情

## 🧰 安装说明

### 前置要求

- Python 3.9 或更高版本
- pip 包管理工具

### 安装步骤

使用 pip 安装 UltraFlow：

```bash
pip install -U UltraFlow
```

> 💡 **提示**：`-U` 参数确保安装最新版本

### 验证安装

安装完成后，验证 `uf` 命令是否可用：

```bash
uf --version
```

如果显示版本号，说明安装成功！

### 可选：使用虚拟环境 (推荐)

为了避免依赖冲突，建议在虚拟环境中安装：

```bash
# 创建虚拟环境
python -m venv ultraflow-env

# 激活虚拟环境
source ultraflow-env/bin/activate  # macOS/Linux
# 或
ultraflow-env\Scripts\activate  # Windows

# 安装 UltraFlow
pip install -U UltraFlow
```

## 📌 命令概览

| 命令 | 功能 |
| - | - |
| `uf --version` | 查看当前版本号 |
| `uf init [PROJECT_NAME]` | 初始化一个 UltraFlow 项目，生成连接配置文件 |
| `uf new FLOW_NAME` | 创建一个新的示例流程 (包含 `.prompty` 和 `.json` 输入数据) |
| `uf run FLOW_NAME [--data DATA_PATH] [--max_workers N]` | 执行指定名称的流程 |

## 🔧 使用详解

### 1. 初始化项目 (`uf init`)

第一步是创建项目配置。`uf init` 命令会在项目目录下生成 `.ultraflow/connection_config.json` 配置文件，用于存储 LLM 服务的连接信息。

**在当前目录初始化：**

```bash
uf init
```

**在指定目录初始化：**

```bash
uf init my_project
```

> 💡 **提示**：如果未提供项目名，将在当前工作目录创建配置。

**接下来做什么？**

配置文件创建后，你需要：

1. 打开 `.ultraflow/connection_config.json` 文件
2. 将 `<your_key>` 替换为你的实际 API Key
3. 如果需要，添加更多 LLM 服务商的配置

详细的配置说明请参考 [连接配置说明](connection_config.md)。

### 2. 新建流程模板 (`uf new`)

使用 `uf new` 命令快速创建一个流程模板。该命令会生成两个文件：

- `<FLOW_NAME>.prompty`：提示词模板文件 (包含配置和提示词)
- `<FLOW_NAME>.json`：测试数据文件 (JSON 格式)

**创建示例流程：**

```bash
uf new hello_flow
```

这将创建：

- `hello_flow.prompty`：一个可以直接运行的示例流程
- `hello_flow.json`：包含两条示例数据

**自定义流程：**

创建文件后，你可以：

1. 编辑 `.prompty` 文件，定义你的提示词和参数
2. 编辑 `.json` 文件，准备你的测试数据
3. 根据需要调整模型参数 (temperature、max_tokens 等)

> 💡 **提示**：prompty 文件支持 Jinja2 模板语法，可以创建动态提示词。详见 [Prompty 文件格式说明](prompty_format.md)。

### 3. 运行流程 (`uf run`)

准备好流程文件和数据后，就可以运行了！`uf run` 命令会自动加载流程配置、读取数据、调用 LLM API 并返回结果。

#### 基础用法：使用同名数据文件

最简单的方式是让 UltraFlow 自动查找同名的 JSON 文件：

```bash
uf run hello_flow
```

这个命令会：

1. 加载 `hello_flow.prompty` 流程配置
2. 读取 `hello_flow.json` 数据文件
3. 对每条数据调用 LLM API
4. 显示处理进度和结果

#### 进阶用法：指定数据文件

如果你的数据文件名称不同，可以手动指定：

```bash
uf run hello_flow --data ./custom_data.json
# 简写形式
uf run hello_flow -d ./test_cases.json
```

#### 高级用法：调整并发数

对于大批量数据，可以使用多线程加速处理：

```bash
# 使用 4 个并发线程
uf run hello_flow --max_workers 4

# 简写形式
uf run hello_flow -w 4

# 使用单线程 (更稳定，避免限流)
uf run hello_flow -w 1
```

> ⚠️ **注意**：并发数不是越大越好。建议根据 API 的限流策略设置合理的值，避免触发限流。

#### 执行结果

运行时，你会看到：

- 📊 处理进度提示
- ✅ 成功处理的数据条数
- ⚠️ 失败的数据条数 (如果有)
- 📁 追踪日志位置 (保存在 `.promptflow/runs/` 目录)

## 二、Python API 使用

除了命令行，UltraFlow 也支持在 Python 代码中直接调用。这让你可以将 LLM 能力无缝集成到自己的应用中。

### 2.1 基本使用

```python
from ultraflow import Prompty

# 加载 prompty 文件
flow = Prompty.load('my_flow.prompty')

# 调用流程，传入输入参数
result = flow(text="你好，请介绍一下你自己")
print(result)
```

### 2.2 批量处理

```python
from ultraflow import FlowProcessor, Prompty

# 加载流程
flow = Prompty.load('translate.prompty')

# 创建处理器，支持多线程
processor = FlowProcessor(
    flow=flow,
    data_path='test_cases.json',
    max_workers=4  # 并发线程数
)

# 执行批量处理
results = processor.run()

# 处理结果
for i, result in enumerate(results, 1):
    print(f"结果 {i}: {result}")
```

### 2.3 启用追踪

PromptFlow 提供了追踪功能，可以记录所有 API 调用的详细信息：

```python
from promptflow.tracing import start_trace
from ultraflow import Prompty

# 启动追踪，指定集合名称
start_trace(collection='my_experiments')

flow = Prompty.load('my_flow.prompty')
result = flow(text="测试输入")

# 追踪数据会自动保存到 .promptflow 目录
# 可以使用 PromptFlow 工具查看详细的调用记录
```

### 2.4 数据文件格式

输入数据文件应为 JSON 格式：

**单个对象：**

```json
{
  "text": "你好，请介绍一下你自己"
}
```

**对象数组 (批量处理)：**

```json
[
  {"text": "第一个问题"},
  {"text": "第二个问题"},
  {"text": "第三个问题"}
]
```

## 三、下一步

- 阅读 [Prompty 文件格式说明](prompty_format.md) 了解如何编写 prompty 文件
- 阅读 [连接配置说明](connection_config.md) 了解如何配置不同的 LLM 服务
- 阅读 [API 参考文档](api_reference.md) 了解完整的 Python API
- 参与 [项目开发](collaboration_tutorial.md) 贡献代码
