#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate a standalone model context protocol server from the template.

Examples:
  python apply.py --target H:/work/my-tool/mcp --tool-id my-tool --version 0.1.0
  python apply.py --spec batch.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILES = [("server_template.py", "server.py"), ("README.md", "README.md"), ("example_tool.py", "example_tool.py")]
TOKENS = ("TOOL_ID", "TOOL_VERSION", "TOOL_TITLE", "TOOL_SCRIPT")


def safe_id(value: str) -> str:
    value = value.strip().lower()
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", value):
        raise ValueError("tool-id 只能用 a-z0-9_-，且以字母数字开头")
    return value


def apply_one(target: Path, tool_id: str, version: str, title: str, force: bool = False, dry: bool = False) -> list[Path]:
    tool_id = safe_id(tool_id)
    if not re.fullmatch(r"[0-9A-Za-z._-]+", version):
        raise ValueError("version 不合法")
    target = target.resolve()
    if target.exists() and any(target.iterdir()) and not force:
        raise FileExistsError(f"目标非空：{target}（加 --force 覆盖）")
    script_name = tool_id.replace("-", "_") + "_tool.py"
    values = {"TOOL_ID": tool_id, "TOOL_VERSION": version, "TOOL_TITLE": title, "TOOL_SCRIPT": script_name}
    made = []
    for src_name, out_name in FILES:
        src = HERE / src_name
        text = src.read_text(encoding="utf-8")
        for key in TOKENS:
            text = text.replace("{{" + key + "}}", values[key])
        if "{{" in text:
            raise ValueError(f"{src_name} 仍有未替换占位符")
        out = target / (script_name if out_name == "example_tool.py" else out_name)
        made.append(out)
        if not dry:
            target.mkdir(parents=True, exist_ok=True)
            out.write_text(text, encoding="utf-8")
    return made


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="生成可批量套用的模型上下文协议服务")
    p.add_argument("--target", help="目标服务目录")
    p.add_argument("--tool-id", default="my-tool")
    p.add_argument("--version", default="0.1.0")
    p.add_argument("--title", default="我的工具")
    p.add_argument("--spec", help="JSON 数组，每项 {target, tool_id, version, title}")
    p.add_argument("--force", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args(argv)
    if args.spec:
        jobs = json.loads(Path(args.spec).read_text(encoding="utf-8"))
        if not isinstance(jobs, list):
            raise SystemExit("spec 必须是数组")
    elif args.target:
        jobs = [{"target": args.target, "tool_id": args.tool_id, "version": args.version, "title": args.title}]
    else:
        raise SystemExit("需要 --target 或 --spec")
    for job in jobs:
        made = apply_one(Path(job["target"]), job.get("tool_id", args.tool_id), job.get("version", args.version),
                         job.get("title", args.title), args.force, args.dry_run)
        print(json.dumps({"target": job["target"], "files": [str(p) for p in made], "dry_run": args.dry_run},
                         ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
