#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MCP template server (stdio, newline-delimited JSON-RPC).

This file is a template. Do not edit placeholders by hand for each new tool;
use `apply.py` (or `apply.py --spec batch.json`) to generate a concrete tool.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SERVER_INFO = {"name": "{{TOOL_ID}}", "version": "{{TOOL_VERSION}}"}
PROTOCOL_VERSION = "2024-11-05"
INSTRUCTIONS = "{{TOOL_TITLE}}：通过 MCP 暴露白名单工具与流程说明；本模板默认单机 stdio，不监听端口。"
PERMISSIONS = {
    "local_only": True,
    "read_local": True,
    "write_local": True,
    "network": False,
    "note": "模板默认本地；具体工具按自己的能力修改，并保持白名单。",
}

TOOLS = [
    {
        "name": "{{TOOL_ID}}.version",
        "description": "Return tool name/version.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "{{TOOL_ID}}.run",
        "description": "Run the tool's whitelisted CLI example.",
        "inputSchema": {
            "type": "object",
            "properties": {"args": {"type": "array", "items": {"type": "string"}}},
            "required": ["args"],
        },
    },
]

PROMPTS = [
    {
        "name": "{{TOOL_ID}}-guide",
        "description": "{{TOOL_TITLE}} 的使用说明与边界。",
        "arguments": [{"name": "task", "description": "任务说明", "required": False}],
    },
]

RESOURCE_FILES = {"{{TOOL_ID}}://guide": ROOT / "README.md"}
RESOURCE_NAMES = {"{{TOOL_ID}}://guide": "{{TOOL_ID}}-guide"}
RESOURCES = [
    {"uri": uri, "name": RESOURCE_NAMES[uri], "description": "{{TOOL_TITLE}} 使用说明", "mimeType": "text/markdown"}
    for uri in RESOURCE_FILES
]


def reply(msg_id, result=None, error=None):
    out = {"jsonrpc": "2.0", "id": msg_id}
    if error is None:
        out["result"] = result
    else:
        out["error"] = error
    sys.stdout.write(json.dumps(out, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def run_tool(args):
    proc = subprocess.run([sys.executable, str(ROOT / "{{TOOL_SCRIPT}}"), *args],
                          capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=120)
    return {"content": [{"type": "text", "text": proc.stdout + proc.stderr}],
            "isError": proc.returncode != 0}


def dispatch(name, arguments):
    if name == "{{TOOL_ID}}.version":
        return {"content": [{"type": "text", "text": json.dumps(SERVER_INFO, ensure_ascii=False)}]}
    if name == "{{TOOL_ID}}.run":
        args = arguments.get("args") or []
        if not all(isinstance(a, str) for a in args):
            raise ValueError("args must be string[]")
        return run_tool(args)
    raise ValueError(f"unknown tool: {name}")


def prompt_content(name, args):
    if name != "{{TOOL_ID}}-guide":
        raise ValueError(f"unknown prompt: {name}")
    task = (args or {}).get("task") or "未提供任务"
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    return f"# {{TOOL_TITLE}}\n\n任务：{task}\n\n{text}\n"


def read_resource(uri):
    path = RESOURCE_FILES.get(uri)
    if not path or not path.is_file():
        raise ValueError(f"resource not found: {uri}")
    return path.read_text(encoding="utf-8")


def handle(req):
    method, msg_id = req.get("method"), req.get("id")
    if method == "initialize":
        reply(msg_id, {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {}, "prompts": {}, "resources": {}},
            "serverInfo": SERVER_INFO,
            "instructions": INSTRUCTIONS,
            "permissions": PERMISSIONS,
        })
    elif method in ("notifications/initialized", "initialized"):
        return
    elif method == "tools/list":
        reply(msg_id, {"tools": TOOLS})
    elif method == "tools/call":
        params = req.get("params") or {}
        try:
            reply(msg_id, dispatch(params.get("name", ""), params.get("arguments") or {}))
        except Exception as e:
            reply(msg_id, error={"code": -32602, "message": str(e)})
    elif method == "prompts/list":
        reply(msg_id, {"prompts": PROMPTS})
    elif method == "prompts/get":
        params = req.get("params") or {}
        try:
            text = prompt_content(params.get("name"), params.get("arguments") or {})
            reply(msg_id, {"description": params.get("name"), "messages": [{"role": "user", "content": {"type": "text", "text": text}}]})
        except Exception as e:
            reply(msg_id, error={"code": -32602, "message": str(e)})
    elif method == "resources/list":
        reply(msg_id, {"resources": RESOURCES})
    elif method == "resources/read":
        uri = (req.get("params") or {}).get("uri", "")
        try:
            reply(msg_id, {"contents": [{"uri": uri, "mimeType": "text/markdown", "text": read_resource(uri)}]})
        except Exception as e:
            reply(msg_id, error={"code": -32602, "message": str(e)})
    elif msg_id is not None:
        reply(msg_id, error={"code": -32601, "message": f"method not found: {method}"})


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdin.reconfigure(encoding="utf-8")
    except Exception:
        pass
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(req, dict):
            handle(req)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
