# 参与开发

UltraFlow 是一个开源项目，我们非常欢迎并鼓励社区成员参与贡献。本教程将指导您如何参与 UltraFlow 的开发，包括环境搭建、代码贡献流程、代码规范以及文档更新等。如果您有任何问题、建议或想参与贡献，请访问我们的 GitHub 仓库：[GitHub 仓库链接](https://github.com/enthusa/UltraFlow)

您可以通过以下方式支持我们：

- **提交 Issue**：如果您在使用过程中遇到 Bug，或者有新的功能建议，请随时在 GitHub 上提交 Issue。在提交之前，请先搜索现有 Issue，避免重复提交。
- **贡献代码**：如果您希望修复 Bug、实现新功能或改进现有代码，请通过 Pull Request (PR) 的方式提交您的代码。
- **改进文档**：文档是项目的重要组成部分。如果您发现文档有任何不准确、不清晰或遗漏的地方，欢迎提交 PR 进行改进。
- **分享与推广**：将 UltraFlow 推荐给更多需要的人，或者撰写文章、制作教程，帮助更多人了解和使用 UltraFlow。

感谢您的支持！

## 一、开发环境搭建

UltraFlow 需要 `>=3.9.2` 的 Python 开发环境。建议通过 miniforge 安装管理 Python 解释器，通过 pdm 安装管理项目依赖，下面假设你的电脑中以及安装了 python 3.9+，以及 git。

### 1.1 前置条件

安装并配置 pdm，如果你的电脑已经安装了 pdm，可以跳过本小节。安装 pdm，建议通过 pipx 安装，先激活一个 python 3.9 的环境。

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

配置 pdm，主要配置 pip 包安装源，以及 pip 包安装的位置路径。

```bash
pdm config pypi.url https://mirrors.aliyun.com/pypi/simple/
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

## 二、 代码规范

UltraFlow 使用 `ruff` 进行代码格式化和 Linting，以确保代码风格的统一性。在提交代码之前，请确保您的代码通过 `ruff` 的检查。

### 2.1 自动格式化

您可以使用以下命令自动格式化您的代码：

```bash
pdm run format
```

### 2.2 代码检查

您可以使用以下命令检查代码是否符合规范：

```bash
pdm run lint
```

我们建议您在提交代码之前，先运行这两个命令。

## 三、文档更新

UltraFlow 的文档使用 `MkDocs` 编写，并以 Markdown 格式存储在 `docs/` 目录下。如果您对文档进行了更改，请确保重新构建文档并检查其正确性。

### 3.1 编辑文档

使用如下命令，启动预览模式，可以一遍编辑文档，一遍预览效果。

```bash
pdm run docs-dev
```

### 3.2 文档编写规范

- 使用 Markdown 语法。
- 保持文档清晰、简洁、准确。
- 为新的功能或更改添加相应的文档。
- 确保示例代码可运行且正确。

为了确保文档格式风格统一，我们引入 `markdown-formatter` npm 包进行 Markdown 文档格式化。前提需要 node.js 运行环境，然后执行 `npm install` 安装依赖，之后使用如下命令进行文档格式化

```bash
npm run docs:format
```

## 四、代码贡献流程

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

## 五、Issue 提交规范

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

## 六、联系我们

如果您有任何疑问或需要帮助，可以通过以下方式联系我们：

- 在 GitHub 上提交 Issue。
- (待定) 加入我们的社区讨论群 (例如 Discord, Slack 等)。

感谢您对 UltraFlow 的贡献！
