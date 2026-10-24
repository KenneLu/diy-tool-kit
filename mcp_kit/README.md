# mcp_kit —— 模型上下文协议服务公共层

给工具复用的模型上下文协议服务公共层。协议处理只在 `server.py`；工具只写一个薄适配模块，定义工具、提示词、资源和回调，然后调用 `serve(config)`。

## 工具侧必须遵守的契约

使用本模板的工具，必须提供且只提供一个平铺适配文件：

```text
<tool>/src/mcp_app.py
```

该文件必须在模块级创建 `ServerConfig` 并调用 `serve(config)`，不得复制 `server.py` 的协议循环，也不得在工具内创建 `mcp/` 或 `mcp_template/` 目录。

`ServerConfig` 必须提供：

| 字段 | 要求 |
|---|---|
| `name` | 服务标识，与工具标识一致 |
| `version` | 与工具参数卡版本一致 |
| `instructions` | 初始化时返回的边界说明 |
| `permissions` | 声明式权限与数据留存说明 |
| `tools` | 白名单工具及其输入结构 |
| `prompts` | 提示词名称、描述与参数 |
| `resources` | 资源 URI、名称、描述、MIME、版本、指纹 |
| `dispatch` | 工具名与参数到结果的回调 |
| `prompt_content` | 提示词名与参数到文本的回调 |
| `read_resource` | 资源 URI 到文本的回调 |

工具侧还必须：

1. 在 `run.bat mcp` 或等价开发入口中启动 `src/mcp_app.py`；
2. 在 README 或使用手册中写明该入口；
3. 让提示词、文档、技能等资源从工具内的固定位置读取，不写死个人绝对路径；
4. 保持名称、资源 URI、初始化字段与工具既有版本一致；
5. 为适配层提供协议测试，至少覆盖初始化、工具列表、提示词列表、资源列表、资源读取和一次工具调用。

## 适配示例

```python
from template.mcp_kit import ServerConfig, serve

config = ServerConfig(
    name="my-tool",
    version="1.0.0",
    instructions="工具边界说明",
    permissions={"local_only": True},
    tools=[...],
    prompts=[...],
    resources=[...],
    dispatch=dispatch,
    prompt_content=prompt_content,
    read_resource=read_resource,
)
serve(config)
```

适配文件放在 `src/`，不要为每个工具复制一份协议循环。

## 两种使用形态

| 形态 | 适用场景 | 文件 |
|---|---|---|
| 共享适配 | 工具已经在 `src/template` 挂载本库，想共用协议层 | 工具 `src/mcp_app.py` + 本库 `server.py` |
| 独立生成 | 工具不挂本库，需要一份独立服务 | `apply.py` 生成的 `server.py` |

两种形态不要混用：共享适配不再生成独立服务；独立生成的服务不依赖本库运行时。

## 生成独立服务

```powershell
python mcp_kit/apply.py --target <目标目录> --tool-id my-tool --version 1.0.0
```

`apply.py` 用 `server_template.py` 生成一个最简独立服务；批量时使用 `--spec batch.json`。

## 边界

- 只通过标准输入输出工作，不监听网络端口；
- 不执行任意命令；工具调用必须是白名单；
- 权限声明是调用约束，不是平台安全边界；
- 工具自己的提示词、文档和脚本资源由适配模块提供。
