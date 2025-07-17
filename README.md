# UltraFlow

提示词工程开发、测试、部署一站式工具.

## 开发测试

代码 clone 到本地, 进入项目创建 venv 虚拟环境, 需要 >=3.9 的 Python 解释器, 比如我的命令
```bash
/opt/miniconda3/envs/py39/bin/python -m venv .venv
source .venv/bin/activate
pip install -U pip setuptools wheel
pip install -e .
```

## 项目规划

- [ ] uf init 初始化一个提示词工程项目, 配置 connection, apikey
- [ ] uf new 创建一个提示词模版, 即 prompty 文件
- [ ] uf run --flow <xxx.prompty>, 启动 web ui 交互式对话界面, 支持多轮对话, 展示 request/response 详情
- [ ] uf run --flow <xxx.prompty> --data <xxx.json> 批量测试, 支持多线程
- [ ] uf serve 以 API 方式启动微服务
- [ ] uf dag 可视化一个复杂任务

## 项目原则

- 约定优于配置
- 支持代码引用和命令行工具两种方式
- 记录好日志, 方便评估、回溯