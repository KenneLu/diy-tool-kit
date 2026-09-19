# -*- coding: utf-8 -*-
"""T5 · i18n 包状态回归（可重复执行；2.1.1）。

钉死的缺陷：包门面若 `from .i18n import *`，`LANG` 会被拷成**静态副本**——
`init('en')` 后子模块真值已变，从**包命名空间**读到却仍是 'zh'，而 `t()` 已切英文。
下游读过期语言的地方（菜单签名等）因此判定"无需重建"。

断言要点：**必须从包命名空间读**（`i18n.LANG`），只读子模块（`i18n.i18n.LANG`）
测不出这个 bug。

用法：python my-diy-tool-template/test_i18n_state.py   （失败退出码 1）
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from modules import i18n  # noqa: E402

FAILS = []


def check(name, ok, detail=""):
    print(("  ok  " if ok else "  FAIL") + " " + name + (("  " + detail) if detail else ""),
          flush=True)
    if not ok:
        FAILS.append(name)


# 前置：状态不得被绑进包命名空间（绑了 __getattr__ 委派就永远不触发）
check("LANG is not a static copy in the package namespace", "LANG" not in vars(i18n))

i18n.init("en")
check("package namespace reports en right after init('en')", i18n.LANG == "en", i18n.LANG)
check("accessor reports en", i18n.current_lang() == "en", i18n.current_lang())
check("submodule agrees", i18n.i18n.LANG == "en", i18n.i18n.LANG)
check("t() follows the language", i18n.t("menu_quit") == "Quit", i18n.t("menu_quit"))

i18n.init("zh")
check("switching back takes effect immediately (package)", i18n.LANG == "zh", i18n.LANG)
check("switching back takes effect immediately (accessor)",
      i18n.current_lang() == "zh", i18n.current_lang())
check("t() follows back", i18n.t("menu_quit") == "退出", i18n.t("menu_quit"))

print("I18N STATE TEST " + ("FAILED: " + ",".join(FAILS) if FAILS else "OK"), flush=True)
sys.exit(1 if FAILS else 0)
