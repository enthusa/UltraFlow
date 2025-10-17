# 快速开始

UltraFlow (简称 `uf`) 是一个基于 [Click](https://click.palletsprojects.com/) 构建的命令行工具，用于管理和执行以 `.prompty` 文件为核心的流程任务。它支持初始化项目、创建示例流程、并行运行流程等功能。

## 🧰 安装说明

确保你已经安装了 `UltraFlow` 包：

```bash
pip install -U UltraFlow
```

然后即可使用命令行工具 `uf`。

## 📌 命令概览

| 命令 | 功能 |
| - | - |
| `uf --version` | 查看当前版本号 |
| `uf init [PROJECT_NAME]` | 初始化一个 UltraFlow 项目，生成连接配置文件 |
| `uf new FLOW_NAME` | 创建一个新的示例流程 (包含 `.prompty` 和 `.json` 输入数据) |
| `uf run FLOW_NAME [--data DATA_PATH] [--max_workers N]` | 执行指定名称的流程 |

## 🔧 使用详解

### 1. 初始化项目 (`uf init`)

在当前目录或指定目录下创建 UltraFlow 的连接配置文件 `.ultraflow/connection_config.json`。

```bash
uf init my_project
```

> 如果未提供项目名，则默认为当前工作目录。

### 2. 新建流程模板 (`uf new`)

创建一个名为 `<FLOW_NAME>.prompty` 的 Prompty 流程文件和对应的输入数据文件 `<FLOW_NAME>.json`。你可以编辑这两个文件来自定义你的流程逻辑与测试数据。

```bash
uf new hello_flow
```

### 3. 运行流程 (`uf run`)

运行一个已有的流程，并可选择性地传入自定义的数据文件。

#### 示例一：自动查找同名 JSON 数据文件

```bash
uf run hello_flow
```

这会尝试加载 `hello_flow.prompty` 和 `hello_flow.json` 并执行流程。

#### 示例二：手动指定数据文件路径

```bash
uf run hello_flow --data ./custom_data.json
```

#### 可选参数：

- `--max_workers INT`：设置最大并发线程数，默认值为 `2`。

例如：

```bash
uf run hello_flow --max_workers 4
```

## 二、Python API 引入
