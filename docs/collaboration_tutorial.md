# 参与开发

感谢你对 UltraFlow 项目的关注！无论你是想修复 bug、添加新功能、改进文档，还是只是提出建议，我们都非常欢迎你的贡献。

## 为什么参与贡献？

参与开源项目贡献能让你：

- 🌟 **提升技能**：通过实际项目学习最佳实践
- 🤝 **结识伙伴**：与全球开发者交流协作
- 📈 **积累经验**：为你的简历增添亮点
- 💡 **影响产品**：让工具更符合你的需求
- ❤️ **回馈社区**：帮助其他开发者解决问题

## 贡献方式

你可以通过以下方式参与项目：

### 🐛 报告 Bug

在使用过程中遇到问题？请在 [GitHub Issues](https://github.com/enthusa/UltraFlow/issues) 提交 bug 报告。

**好的 bug 报告应包括**：

- 问题的简洁描述
- 复现步骤 (越详细越好)
- 预期行为 vs 实际行为
- 运行环境 (OS、Python 版本、UltraFlow 版本)
- 相关的错误信息或截图

### 💡 提出建议

有新功能想法或改进建议？欢迎在 GitHub Issues 中提出！

**好的功能建议应包括**：

- 功能的用途和使用场景
- 具体的实现思路 (如果有)
- 可能的替代方案
- 是否愿意自己实现

### 📝 改进文档

文档是项目的重要组成部分。如果你发现：

- 文档有错误或不清楚的地方
- 缺少某些说明或示例
- 有更好的表述方式

请直接提交 Pull Request 或在 Issues 中指出。

### 🔧 贡献代码

想要修复 bug 或实现新功能？太好了！请查看下面的开发流程。

### 🌐 翻译文档

帮助翻译文档到其他语言，让更多人能够使用 UltraFlow。

## 行为准则

参与贡献时，请遵守以下原则：

- ✅ 尊重所有参与者，保持友善和专业
- ✅ 欢迎新手，耐心解答问题
- ✅ 建设性地讨论，专注于改进项目
- ✅ 尊重维护者的决定
- ❌ 禁止骚扰、歧视或攻击性言论

## 开发环境搭建

要参与 UltraFlow 开发，你需要准备以下环境。

### 前置要求

在开始之前，请确保你的系统已安装：

- **Python >= 3.9.2**：推荐使用 miniforge 或 Anaconda 管理 Python 环境
- **Git**：用于克隆仓库和版本控制
- **pdm**：项目依赖管理工具 (下面会介绍如何安装)

### 安装 pdm

如果你还没有安装 pdm，建议通过 pipx 安装：

```bash
# 1. 安装 pipx(如果还没有)
python3 -m pip install --user --upgrade pip
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# 验证安装
pipx --version

# 2. 使用 pipx 安装 pdm
pipx install pdm

# 验证安装
pdm --version
```

### 配置 pdm(可选)

为了加快包下载速度和统一管理虚拟环境，可以配置 pdm：

```bash
# 配置 PyPI 镜像 (可选，国内用户推荐)
pdm config pypi.url https://mirrors.aliyun.com/pypi/simple/

# 配置虚拟环境位置 (可选)
pdm config venv.location ~/venv
```

### 1.2 搭建 venv 项目运行虚拟环境

代码 clone 到本地，进入项目，通过 pdm 创建 venv 虚拟环境。

```bash
git clone git@github.com:enthusa/UltraFlow.git
cd UltraFlow
pdm venv create -n venv-py39 /opt/miniforge3/envs/py39/bin/python
pdm use --venv venv-py39
pdm sync
```

如果您想激活虚拟环境，可以使用 `pdm run bash` 或 `pdm run zsh` (类似于 `source` 激活这个虚拟环境)。

### 1.3 初始化配置文件

### 1.4 启动测试

在开发过程中，您应该经常运行测试以确保您的更改没有引入新的问题。UltraFlow 使用 `pytest` 进行单元测试。您可以通过 PDM 运行测试：

```bash
pdm run pytest
```

## 代码规范 {#代码规范}

UltraFlow 使用 `ruff` 进行代码格式化和 Linting，以确保代码风格的统一性。在提交代码之前，请确保您的代码通过 `ruff` 的检查。

### 自动格式化

您可以使用以下命令自动格式化您的代码：

```bash
pdm run format
```

### 代码检查

您可以使用以下命令检查代码是否符合规范：

```bash
pdm run lint
```

我们建议您在提交代码之前，先运行这两个命令。

## 文档更新

UltraFlow 的文档使用 `MkDocs` 编写，并以 Markdown 格式存储在 `docs/` 目录下。如果您对文档进行了更改，请确保重新构建文档并检查其正确性。

### 编辑文档

使用如下命令，启动预览模式，可以一遍编辑文档，一遍预览效果。

```bash
pdm run docs-dev
```

### 文档编写规范

- 使用 Markdown 语法。
- 保持文档清晰、简洁、准确。
- 为新的功能或更改添加相应的文档。
- 确保示例代码可运行且正确。

为了确保文档格式风格统一，我们引入 `markdown-formatter` npm 包进行 Markdown 文档格式化。前提需要 node.js 运行环境，然后执行 `npm install` 安装依赖，之后使用如下命令进行文档格式化

```bash
npm run docs:format
```

## 代码贡献流程

我们遵循标准的 GitHub Flow 贡献流程：

1. **Fork 仓库**：在 GitHub 上 Fork UltraFlow 仓库到您自己的账户。
2. **克隆您的 Fork**：将您 Fork 的仓库克隆到本地。
   ```bash
   git clone git@github.com:enthusa/UltraFlow.git
   cd UltraFlow
   ```
3. **创建新分支**：为您的新功能或 Bug 修复创建一个新的分支。分支名称应具有描述性，例如 `feature/add-new-command` 或 `fix/bug-in-batch-test`。
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **进行更改**：在您的新分支上进行代码更改。请确保您的更改符合代码规范，并编写相应的单元测试。
5. **提交更改**：提交您的更改到本地仓库。提交信息应清晰、简洁，说明本次提交的目的。
   ```bash
   git add .
   git commit -m "feat: add new command for X"
   ```
   (我们推荐使用 Conventional Commits 规范，例如 `feat:`, `fix:`, `docs:`, `chore:` 等前缀)
6. **同步上游**：在提交 PR 之前，请确保您的分支与上游 `main` 分支保持同步，以避免合并冲突。
   ```bash
   git remote add upstream git@github.com:enthusa/UltraFlow.git # 首次添加
   git checkout main
   git pull upstream main
   git checkout feature/your-feature-name
   git rebase main
   ```
7. **推送分支**：将您的分支推送到您的 Fork 仓库。
   ```bash
   git push origin feature/your-feature-name
   ```
8. **提交 Pull Request (PR)**：在 GitHub 上打开您的 Fork 仓库页面，您会看到一个提示，引导您创建 Pull Request。请填写清晰的 PR 描述，说明您的更改内容、目的以及解决了哪些问题。
9. **等待审查**：提交 PR 后，项目维护者将对您的代码进行审查。您可能需要根据审查意见进行修改。
10. **合并**：一旦您的 PR 通过审查并被批准，它将被合并到 `main` 分支。

## Issue 提交规范

在提交 Issue 时，请提供尽可能详细的信息，以便我们更好地理解和解决问题：

- **Bug 报告**：
  - **标题**：简洁明了地描述 Bug，例如 `[Bug] uf run 批量测试结果不准确`。
  - **环境**：提供您的操作系统、Python 版本、UltraFlow 版本等信息。
  - **复现步骤**：详细描述如何复现 Bug，包括您执行的命令、输入的数据等。
  - **预期结果**：描述您期望的正确行为。
  - **实际结果**：描述实际发生的不正确行为。
  - **错误信息**：如果出现错误，请提供完整的错误堆栈信息。
- **功能请求**：
  - **标题**：简洁明了地描述功能请求，例如 `[Feature] 支持更多 LLM 提供商`。
  - **描述**：详细说明您希望添加的功能，以及它能解决什么问题或带来什么好处。
  - **用例**：提供一些使用该功能的具体场景。

## 联系我们

如果您有任何疑问或需要帮助，可以通过以下方式联系我们：

- 在 GitHub 上提交 Issue。
- (待定) 加入我们的社区讨论群 (例如 Discord, Slack 等)。

感谢您对 UltraFlow 的贡献！
