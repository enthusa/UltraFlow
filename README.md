# UltraFlow 项目说明文档

## 1. 项目概述

UltraFlow 是一个专为大模型提示词工程项目设计的一站式开源工具包。它旨在简化和加速提示词的创建、开发、测试、发布和部署流程，为开发者提供一个高效、便捷的解决方案。随着大型语言模型（LLMs）在各个领域的广泛应用，提示词工程（Prompt Engineering）已成为一项关键技能。然而，目前市场上缺乏一个集成化的工具来管理提示词的整个生命周期。UltraFlow 的出现正是为了填补这一空白，它将提示词工程从一个艺术性的实践提升为一套系统化、工程化的流程。

UltraFlow 的核心价值在于其“一站式”的理念。它不仅提供命令行工具 `uf` 来快速执行常见任务，还支持通过 Python `import` 语句在代码中灵活调用其功能，满足不同开发者的需求。该工具包采用 Python 编写，兼容 Python 3.9 及以上版本，确保了广泛的适用性。

## 2. 主要功能与特点

UltraFlow 提供了以下核心功能，旨在覆盖提示词工程的各个环节：

### 2.1 命令行工具 `uf`

`uf` 是 UltraFlow 的主要交互界面，提供了一系列子命令来管理提示词工程项目：

*   **`uf init`**: 初始化一个新的提示词工程项目，包括配置连接信息和 API 密钥等。
*   **`uf new`**: 创建一个新的提示词模板，即 `.prompty` 文件，用于定义提示词结构和内容。
*   **`uf run <xxx.prompty>`**: 启动一个交互式 Web UI 界面，支持多轮对话，并详细展示请求和响应的细节，便于调试和优化提示词。
*   **`uf run <xxx.prompty> --data <xxx.json>`**: 支持批量测试提示词，可配置多线程并行执行，提高测试效率。
*   **`uf serve`**: 以 API 方式启动微服务，将提示词工程能力封装为可调用的接口，便于集成到其他应用中。
*   **`uf dag`**: 可视化复杂的提示词任务流程，帮助开发者理解和管理复杂的提示词链。

### 2.2 Python API 接口

除了命令行工具，UltraFlow 还提供了丰富的 Python API，允许开发者在自己的 Python 项目中直接导入和使用其功能，实现更高级的定制和自动化。

### 2.3 项目管理与代码规范

UltraFlow 采用 `pdm` 进行项目管理，确保依赖的清晰和项目的可复现性。代码格式化工具 `ruff` 的使用，保证了代码风格的统一性和可读性，这对于开源项目尤为重要。

### 2.4 单元测试与文档

工具包包含全面的单元测试，确保代码质量和功能的稳定性。项目文档通过 `sphinx` 编写，提供详细的使用指南、API 参考和开发文档，方便用户和贡献者理解和使用 UltraFlow。

## 3. 安装指南

UltraFlow 将发布到 PyPI，用户可以通过 `pip` 命令一键安装。在安装之前，请确保您的 Python 版本为 3.9 或更高。

```bash
pip install -U UltraFlow
```

对于开发和贡献者，可以通过以下步骤从源代码安装：

0. 安装 pdm, 建议通过 pipx 安装, 先激活一个 python 3.9 的环境
```bash
conda activate py39
python3 -m pip uninstall -y pipx
python3 -m pip install --user --upgrade pip
python3 -m pip install --user pipx
python3 -m pipx ensurepath
pipx --version

pipx install pdm
pdm --version
```
1. 克隆仓库：
```bash
git clone git@github.com:enthusa/UltraFlow.git
cd UltraFlow
```
2. 创建并激活虚拟环境：
```bash
pdm sync
source .venv/bin/activate
```
3. 安装依赖：
```bash
pip install -U pip setuptools wheel
pip install -e .
```

## 4. 快速入门

### 4.1 初始化项目

使用 `uf init` 命令初始化一个新的提示词工程项目：

```bash
uf init my_prompt_project
cd my_prompt_project
```

该命令将创建一个新的目录 `my_prompt_project`，并在其中生成项目所需的基本文件和配置。

### 4.2 创建提示词模板

使用 `uf new` 命令创建一个新的提示词模板文件（例如 `hello_world.prompty`）：

```bash
uf new hello_world
```

打开 `hello_world.prompty` 文件，您可以定义您的提示词内容和变量。

### 4.3 交互式测试

通过 `uf run` 命令启动 Web UI 进行交互式测试：

```bash
uf run hello_world.prompty
```

您的浏览器将自动打开一个界面，您可以在其中输入对话内容，并查看 LLM 的响应以及详细的请求/响应信息。

### 4.4 批量测试

准备一个 JSON 文件（例如 `test_data.json`），包含用于批量测试的数据：

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

## 5. 项目架构与技术栈

UltraFlow 的设计遵循“约定优于配置”和“支持代码引用和命令行工具两种方式”的项目原则，其核心架构如下：

*   **核心模块**：提供提示词解析、执行、结果处理等核心功能，支持多种 LLM 提供商的集成。
*   **命令行接口 (CLI)**：基于 `click` 包实现，提供友好的命令行交互。
*   **Web UI**：用于交互式对话和调试，提供可视化的请求/响应详情。
*   **API 服务**：基于轻量级 Web 框架实现，提供 RESTful API 接口。
*   **数据管理**：处理提示词模板、测试数据和日志的存储和管理。

**技术栈**：

*   **Python**: 主要开发语言，版本 >= 3.9。
*   **pdm**: 项目管理和依赖管理工具。
*   **ruff**: 代码格式化和 Linting 工具。
*   **click**: 用于构建命令行接口。
*   **sphinx**: 用于生成项目文档。
*   **（待定）**: Web UI 和 API 服务相关的 Web 框架（例如 FastAPI, Flask 等）。

## 6. 项目原则

*   **约定优于配置**：通过合理的默认设置和规范，减少用户的配置负担，提高开发效率。
*   **支持代码引用和命令行工具两种方式**：兼顾不同开发者的使用习惯和集成需求。
*   **记录好日志，方便评估、回溯**：提供详细的日志记录功能，便于用户分析和优化提示词效果，以及问题排查。

## 7. 贡献与支持

UltraFlow 是一个开源项目，我们欢迎并鼓励社区的贡献。如果您有任何问题、建议或想参与贡献，请访问我们的 GitHub 仓库：[GitHub 仓库链接](https://github.com/enthusa/UltraFlow)

您可以通过以下方式支持我们：

*   在 GitHub 上为项目点赞 (Star)。
*   提交 Bug 报告或功能请求 (Issue)。
*   贡献代码 (Pull Request)。
*   分享 UltraFlow 给更多需要的人。

感谢您的支持！
