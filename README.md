# UltraFlow

<div align="center">

**一站式的大语言模型提示词工程工具包**

简单 · 强大 · 开源

[![PyPI](https://img.shields.io/pypi/v/ultraflow)](https://pypi.org/project/UltraFlow/)
[![Python](https://img.shields.io/pypi/pyversions/ultraflow)](https://pypi.org/project/UltraFlow/)
[![License](https://img.shields.io/github/license/enthusa/UltraFlow)](https://github.com/enthusa/UltraFlow/blob/master/LICENSE)

[快速开始](https://enthusa.github.io/UltraFlow/get_started/) · [文档](https://enthusa.github.io/UltraFlow/) · [示例](https://enthusa.github.io/UltraFlow/examples/) · [反馈](https://github.com/enthusa/UltraFlow/issues)

</div>

---

## ✨ 特性

- 🎯 **简单易用** - 三个命令完成从配置到运行
- 🚀 **批量处理** - 内置多线程支持，高效处理大规模数据
- 📝 **版本控制** - 纯文本 Prompty 格式，完美支持 Git
- 🔧 **灵活集成** - 命令行工具 + Python API 双接口
- 🔍 **完整追踪** - 记录每次 API 调用的完整信息
- 🛡️ **智能修复** - 自动修复格式错误的 JSON 输出

## 📸 使用截图

![UltraFlow 使用示例](https://pic-gino-prod.oss-cn-qingdao.aliyuncs.com/henry/20251016203242758-_20251016203226_58.png)

## 🚀 快速开始

### 安装

```bash
pip install -U UltraFlow
```

### 三步上手

```bash
# 1. 初始化项目
uf init

# 2. 创建流程模板
uf new hello_world

# 3. 运行流程
uf run hello_world
```

就这么简单！

### Python API

```python
from ultraflow import Prompty

# 加载并执行
flow = Prompty.load('hello_world.prompty')
result = flow(text='你好，世界！')
print(result)
```

## 📚 文档

完整文档请访问：**<https://enthusa.github.io/UltraFlow/>**

- [快速开始](https://enthusa.github.io/UltraFlow/get_started/) - 10 分钟上手指南
- [API 参考](https://enthusa.github.io/UltraFlow/api_reference/) - 完整 API 文档
- [Prompty 格式](https://enthusa.github.io/UltraFlow/prompty_format/) - 文件格式说明
- [实用示例](https://enthusa.github.io/UltraFlow/examples/) - 13 个实战示例
- [常见问题](https://enthusa.github.io/UltraFlow/faq/) - 问题解答

## 💡 使用场景

- 📝 **提示词工程** - 设计、测试、优化 LLM 提示词
- 🔄 **批量处理** - 翻译、摘要、分类等批量任务
- 🧪 **实验迭代** - 快速测试不同的提示词变体
- 🤖 **AI 应用开发** - 将 LLM 集成到应用中
- 📊 **数据标注** - 使用 LLM 进行数据处理

## 🤝 参与贡献

我们欢迎所有形式的贡献！

- 🐛 [报告 Bug](https://github.com/enthusa/UltraFlow/issues/new?template=bug_report.md)
- 💡 [提出建议](https://github.com/enthusa/UltraFlow/issues/new?template=feature_request.md)
- 📝 改进文档
- 🔧 提交代码

查看 [贡献指南](https://enthusa.github.io/UltraFlow/feedback/) 了解更多。

## 📊 项目状态

- ✅ 核心功能已实现
- ✅ 单元测试覆盖
- ✅ 完整文档
- ⏳ Web UI（开发中）
- ⏳ API 服务（计划中）

## 📄 许可证

本项目采用 [MIT License](LICENSE)。

## 🙏 致谢

- 基于 [PromptFlow](https://github.com/microsoft/promptflow) 开发
- 使用 [json-repair](https://github.com/mangiucugna/json_repair) 修复 JSON
- 文档由 [MkDocs](https://www.mkdocs.org/) 生成

## ⭐ Star History

如果这个项目对你有帮助，请给我们一个 Star！

---

<div align="center">

**用 UltraFlow 让 AI 开发更简单**

[开始使用](https://enthusa.github.io/UltraFlow/get_started/) · [GitHub](https://github.com/enthusa/UltraFlow) · [PyPI](https://pypi.org/project/UltraFlow/)

</div>