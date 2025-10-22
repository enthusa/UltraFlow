# 欢迎使用 UltraFlow

![UltraFlow 使用截图](https://pic-gino-prod.oss-cn-qingdao.aliyuncs.com/henry/20251017114825308-_20251017114655_105.png)

UltraFlow 是一个轻量级、易用的开源工具，专为大语言模型 (LLM) 的提示词工程、测试和部署而设计。它让你能够像管理代码一样管理和版本控制你的 AI 提示词。

## 为什么选择 UltraFlow？

### 🎯 简单易用

- **三步上手**：init → new → run，快速开始你的第一个 AI 流程
- **直观的文件格式**：Prompty 格式结合 YAML 配置和 Jinja2 模板
- **命令行友好**：简洁的 CLI 命令，适合脚本自动化

### 🚀 功能强大

- **批量处理**：内置多线程支持，高效处理大规模数据
- **灵活配置**：统一管理多个 LLM 服务商的连接
- **完善追踪**：集成 PromptFlow 追踪，记录每次 API 调用
- **双接口**：支持命令行工具和 Python API 两种使用方式

### 🔧 开发友好

- **版本控制**：纯文本格式，完美融入 Git 工作流
- **易于测试**：独立的数据文件，方便编写测试用例
- **可扩展**：基于 PromptFlow，可轻松扩展功能
- **跨平台**：支持 Windows、macOS、Linux

## 快速开始

准备好了吗？让我们开始吧！

```bash
# 1. 安装 UltraFlow
pip install -U UltraFlow

# 2. 初始化项目
uf init

# 3. 创建第一个流程
uf new hello_world

# 4. 运行流程
uf run hello_world
```

就这么简单！前往 [快速开始](get_started.md) 了解更多详情。

## 文档导航

### 📚 基础教程

- **[快速开始](get_started.md)** - 10 分钟上手指南，从安装到运行你的第一个流程
- **[Prompty 文件格式](prompty_format.md)** - 学习核心文件格式，掌握提示词定义方法
- **[连接配置说明](connection_config.md)** - 配置不同 LLM 服务商的连接信息

### 🔍 深入学习

- **[API 参考文档](api_reference.md)** - Python API 完整文档，适合程序化调用
- **[实用示例](examples.md)** - 13 个精心设计的实战示例，涵盖常见应用场景
- **[常见问题](faq.md)** - 30 个常见问题解答，帮助你快速解决疑惑

### 🤝 参与贡献

- **[反馈与贡献](feedback.md)** - 如何提供反馈和参与项目
- **[参与开发](collaboration_tutorial.md)** - 开发环境搭建和代码贡献流程

## 适用场景

- 📝 **提示词工程** - 设计、测试、优化 LLM 提示词
- 🔄 **批量处理** - 翻译、摘要、分类等批量任务
- 🧪 **实验迭代** - 快速测试不同的提示词变体
- 🤖 **AI 应用开发** - 将 LLM 集成到你的应用中
- 📊 **数据标注** - 使用 LLM 进行数据清洗和标注

---

## 项目背景

### 基于 PromptFlow 的改进

UltraFlow 基于微软开源的 [PromptFlow](https://github.com/microsoft/promptflow) 进行开发。PromptFlow 提供了优秀的基础能力，但在实际使用中也存在一些不足：

**PromptFlow 的优势**：

- 定义了轻量级的 Prompty 文件格式 (YAML + Jinja2)
- 支持版本控制和命令行工具
- 提供追踪和日志功能

**存在的不足**：

- 连接配置加密存储导致部署迁移困难
- 日志缺少 API 调用的原始数据
- JSON 格式输出解析失败时无法查看原始内容

UltraFlow 继承了 PromptFlow 的优势，同时针对这些问题进行了改进：

- 使用 JSON 文件存储连接配置，方便迁移
- 增强了错误处理和日志记录
- 自动修复格式不正确的 JSON 输出
- 简化了配置和使用流程

## 技术架构

UltraFlow 采用模块化设计，确保代码的可维护性和可扩展性。

**核心组件**：

- **Prompty 解析器** - 解析 YAML 配置和 Jinja2 模板
- **连接管理器** - 管理多个 LLM 服务商的 API 连接
- **流程执行器** - 支持单线程和多线程批量处理
- **追踪系统** - 记录完整的 API 调用链路

**技术栈**：

- **Python >= 3.9** - 主要开发语言
- **PromptFlow** - 核心依赖，提供基础能力
- **click** - 命令行接口框架
- **json-repair** - 自动修复格式错误的 JSON
- **pdm** - 项目管理工具
- **ruff** - 代码格式化和检查工具
- **MkDocs** - 文档生成工具

## 开发路线图

**当前已实现**：

- ✅ `uf init` - 项目初始化
- ✅ `uf new` - 创建流程模板
- ✅ `uf run` - 执行流程 (支持批量和多线程)

**计划中的功能**：

- ⏳ `uf run --ui` - 交互式 Web UI
- ⏳ `uf serve` - API 微服务
- ⏳ `uf dag` - 工作流可视化

欢迎查看 [参与开发](collaboration_tutorial.md) 了解如何贡献代码。

## 设计理念

1. **简单优先** - 提供最直接的使用方式，降低学习成本
2. **约定优于配置** - 通过合理的默认设置，减少配置负担
3. **双接口支持** - 兼顾命令行和编程接口两种使用方式
4. **开放兼容** - 兼容 OpenAI API，支持多种 LLM 服务商
5. **详细日志** - 完整记录执行过程，方便评估和回溯

## 项目信息

- **许可证** - MIT License
- **Python 版本** - >= 3.9
- **GitHub** - <https://github.com/enthusa/UltraFlow>
- **文档** - <https://enthusa.github.io/UltraFlow/>
- **PyPI** - <https://pypi.org/project/UltraFlow/>

---

准备好开始了吗？查看 [快速开始](get_started.md) 指南，10 分钟上手 UltraFlow！

## 用户反馈

你的反馈对我们非常重要！

- 💡 **功能建议** - 你希望 UltraFlow 支持什么功能？
- 🐛 **问题报告** - 遇到了 bug 或不符合预期的行为？
- 💬 **使用心得** - 愿意分享你的使用场景和经验吗？
- ⭐ **成功案例** - 用 UltraFlow 解决了什么问题？

**反馈渠道**：

- GitHub Issues - <https://github.com/enthusa/UltraFlow/issues>
- GitHub Discussions - <https://github.com/enthusa/UltraFlow/discussions>

每一条反馈都会被认真对待，你的建议将直接影响 UltraFlow 的发展方向！

## 如何贡献

UltraFlow 是开源项目，欢迎所有形式的贡献！

**代码贡献**：

- 修复 bug、实现新功能
- 优化性能、改进错误处理

**非代码贡献**：

- 改进文档、编写教程
- 回答问题、分享案例

**快速开始**：

1. ⭐ 给项目加星
2. 📖 阅读 [反馈与贡献](feedback.md)
3. 🔍 查看 [Good First Issue](https://github.com/enthusa/UltraFlow/labels/good%20first%20issue)
4. 💬 在 Discussions 介绍自己

即使只是修正一个错别字，也是有价值的贡献！
