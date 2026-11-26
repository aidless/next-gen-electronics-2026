#!/usr/bin/env python3
"""数字闸与机构闸的反向自测：注入违规必须 exit 1；缺底物必须 exit 3。"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

BASE = Path(__file__).resolve().parent
PROJECT = BASE.parent


def run(script, env):
    return subprocess.run([sys.executable, str(BASE / script)], env={**os.environ, **env},
                          capture_output=True, text=True).returncode


with tempfile.TemporaryDirectory() as td:
    root = Path(td)
    # 数字闸：合法副本 -> 0；注入冲突值 -> 1；删指定文件 -> 1
    ledger = json.loads((PROJECT / "analyses" / "numeric_consistency_ledger.json").read_text(encoding="utf-8"))
    e = ledger["entries"][0]
    target = root / e["required_files"][0]
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("口径：" + e["canonical"] + " — " + e["caliber"], encoding="utf-8")
    other = root / e["required_files"][1]
    other.parent.mkdir(parents=True, exist_ok=True)
    other.write_text(e["canonical"], encoding="utf-8")
    led = root / "ledger.json"
    led.write_text(json.dumps({"entries": [e]}, ensure_ascii=False), encoding="utf-8")
    env = {"NUMERIC_BASE": str(root), "NUMERIC_LEDGER": str(led)}
    rc_ok = run("check_numeric_consistency.py", env)
    target.write_text("口径：$1.656T — " + e["caliber"], encoding="utf-8")
    rc_red = run("check_numeric_consistency.py", env)
    target.unlink()
    rc_missing = run("check_numeric_consistency.py", env)
    # 机构闸：合法文档 -> 0；注入未在披露表的新机构单例高频 -> 1；空目录 -> 3
    docs = root / "docs"
    docs.mkdir()
    (docs / "专题99-测试.md").write_text("TrendForce 出现三次。", encoding="utf-8")
    env2 = {"INST_FREQ_DOCS": str(docs), "INST_FREQ_OUT": str(root / "freq.json")}
    rc_freq_ok = run("check_institution_freq.py", env2)
    (docs / "专题99-测试.md").write_text("TechInsights " * 12, encoding="utf-8")
    rc_freq_red = run("check_institution_freq.py", env2)
    empty = root / "empty"
    empty.mkdir()
    env3 = {"INST_FREQ_DOCS": str(empty), "INST_FREQ_OUT": str(root / "freq2.json")}
    rc_freq_empty = run("check_institution_freq.py", env3)

checks = {
    "numeric_green": rc_ok == 0,
    "numeric_red_on_value_drift": rc_red == 1,
    "numeric_red_on_missing_file": rc_missing == 1,
    "institution_green": rc_freq_ok == 0,
    "institution_red_on_undisclosed_single_source": rc_freq_red == 1,
    "institution_not_run_on_empty": rc_freq_empty == 3,
}
print(json.dumps(checks, ensure_ascii=False))
print("PASS selftest" if all(checks.values()) else "FAIL selftest")
sys.exit(0 if all(checks.values()) else 1)
