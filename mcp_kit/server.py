# -*- coding: utf-8 -*-
"""Generic model context protocol server (standard input/output, newline JSON).

A tool supplies a ServerConfig; this module owns the protocol loop and common
error handling. It never imports a tool and never executes arbitrary commands.
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from typing import Any, Callable

PROTOCOL_VERSION = "2024-11-05"


@dataclass
class ServerConfig:
    name: str
    version: str
    instructions: str
    permissions: dict[str, Any]
    tools: list[dict[str, Any]]
    prompts: list[dict[str, Any]]
    resources: list[dict[str, Any]]
    dispatch: Callable[[str, dict[str, Any]], dict[str, Any]]
    prompt_content: Callable[[str, dict[str, Any]], str]
    read_resource: Callable[[str], str]


def _reply(out, msg_id, result=None, error=None):
    payload = {"jsonrpc": "2.0", "id": msg_id}
    if error is None:
        payload["result"] = result
    else:
        payload["error"] = error
    out.write(json.dumps(payload, ensure_ascii=False) + "\n")
    out.flush()


def _resource_map(config: ServerConfig) -> dict[str, dict[str, Any]]:
    return {row["uri"]: row for row in config.resources}


def _handle(config: ServerConfig, out, req: dict[str, Any]) -> None:
    method, msg_id = req.get("method"), req.get("id")
    if method == "initialize":
        _reply(out, msg_id, {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {}, "prompts": {}, "resources": {}},
            "serverInfo": {"name": config.name, "version": config.version},
            "instructions": config.instructions,
            "permissions": config.permissions,
        })
    elif method in ("notifications/initialized", "initialized"):
        return
    elif method == "tools/list":
        _reply(out, msg_id, {"tools": config.tools})
    elif method == "tools/call":
        params = req.get("params") or {}
        try:
            _reply(out, msg_id, config.dispatch(params.get("name", ""), params.get("arguments") or {}))
        except Exception as exc:
            _reply(out, msg_id, error={"code": -32602, "message": str(exc)})
    elif method == "prompts/list":
        _reply(out, msg_id, {"prompts": config.prompts})
    elif method == "prompts/get":
        params = req.get("params") or {}
        try:
            text = config.prompt_content(params.get("name", ""), params.get("arguments") or {})
            _reply(out, msg_id, {"description": params.get("name"), "messages": [
                {"role": "user", "content": {"type": "text", "text": text}}
            ]})
        except Exception as exc:
            _reply(out, msg_id, error={"code": -32602, "message": str(exc)})
    elif method == "resources/list":
        _reply(out, msg_id, {"resources": config.resources})
    elif method == "resources/read":
        params = req.get("params") or {}
        uri = params.get("uri", "")
        row = _resource_map(config).get(uri)
        if row is None:
            _reply(out, msg_id, error={"code": -32602, "message": f"resource not found: {uri}"})
            return
        try:
            _reply(out, msg_id, {"contents": [{
                "uri": uri,
                "mimeType": row.get("mimeType") or "text/markdown",
                "text": config.read_resource(uri),
            }]})
        except Exception as exc:
            _reply(out, msg_id, error={"code": -32602, "message": str(exc)})
    elif msg_id is not None:
        _reply(out, msg_id, error={"code": -32601, "message": f"method not found: {method}"})


def serve(config: ServerConfig, stdin=None, stdout=None) -> int:
    stdin = stdin or sys.stdin
    stdout = stdout or sys.stdout
    try:
        stdin.reconfigure(encoding="utf-8")
        stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    for line in stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(req, dict):
            _handle(config, stdout, req)
    return 0
