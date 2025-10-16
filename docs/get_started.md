# 快速开始

UltraFlow 已发布到 PyPI，用户可以通过 `pip` 命令一键安装。在安装之前，请确保您的 Python 版本为 3.9 或更高。

```bash
pip install -U UltraFlow
```

## 一、命令行工具

### 1.1 初始化项目

使用 `uf init` 命令初始化一个新的提示词工程项目：

```bash
uf init my_prompt_project
cd my_prompt_project
```

该命令将创建一个新的目录 `my_prompt_project`，并在其中生成项目所需的基本文件和配置。

### 1.2 创建提示词模板

使用 `uf new` 命令创建一个新的提示词模板文件 (例如 `hello_world.prompty`)：

```bash
uf new hello_world
```

打开 `hello_world.prompty` 文件，您可以定义您的提示词内容和变量。

### 1.3 交互式测试

通过 `uf run` 命令启动 Web UI 进行交互式测试：

```bash
uf run hello_world.prompty
```

您的浏览器将自动打开一个界面，您可以在其中输入对话内容，并查看 LLM 的响应以及详细的请求/响应信息。

### 1.4 批量测试

准备一个 JSON 文件 (例如 `test_data.json`)，包含用于批量测试的数据：

```json
[
    {
        "input": "你好，请介绍一下你自己。"
    },
    {
        "input": "请用中文写一首关于春天的诗。"
    }
]
```

然后运行批量测试命令：

```bash
uf run hello_world.prompty --data test_data.json
```

测试结果将输出到控制台，并可配置保存到文件。

## 二、Python API 引入
