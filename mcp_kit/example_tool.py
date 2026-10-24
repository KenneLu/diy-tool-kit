#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Example tool used by mcp_template; replace with the tool CLI."""
from __future__ import annotations
import sys


def main() -> int:
    print("example tool:", " ".join(sys.argv[1:]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
