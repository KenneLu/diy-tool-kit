# mcp_kit —— 模型上下文协议服务公共层

给工具复用的模型上下文协议服务公共层。协议处理只在 `server.py`；工具只写一个薄适配模块，定义工具、提示词、资源和回调，然后调用 `serve(config)`。

## 工具侧最小适配

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

适配模块放在 `src/`，不要为每个工具复制一份协议循环。

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
