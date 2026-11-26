#!/usr/bin/env python3
"""跨专题重复数字口径闸：机读台账登记值须在指定文件出现，禁用变体须缺席。

退出码：0 全过 / 1 口径冲突 / 2 用法错 / 3 闸没执行（不等于通过）。
摘要首行：entries=N occurrences=M conflicts=K problems=P。
"""
import hashlib
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(os.environ.get("NUMERIC_BASE", Path(__file__).resolve().parent.parent))
BASE = ROOT
LEDGER = Path(os.environ.get("NUMERIC_LEDGER", BASE / "analyses" / "numeric_consistency_ledger.json"))


def sha12(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def main() -> int:
    if not LEDGER.exists():
        print("exit3: 台账缺失，闸没执行，不等于通过")
        return 3
    try:
        data = json.loads(LEDGER.read_text(encoding="utf-8"))
        entries = data["entries"]
    except Exception as exc:
        print(f"exit2: 台账不可解析: {exc}")
        return 2
    total_occ = 0
    conflicts = []
    for e in entries:
        for field in ("id", "canonical", "caliber", "required_files"):
            if field not in e:
                print(f"exit2: 条目缺字段 {field}")
                return 2
        for rel in e["required_files"]:
            p = BASE / rel
            if not p.exists():
                conflicts.append(f"{e['id']}: 文件缺失 {rel}")
                continue
            txt = p.read_text(encoding="utf-8")
            if e["canonical"] not in txt:
                conflicts.append(f"{e['id']}: {rel} 缺规范值 {e['canonical']}")
            else:
                total_occ += txt.count(e["canonical"])
            for bad in e.get("forbidden_variants", []):
                if bad == e["canonical"]:
                    continue
                # 带数值边界，避免把 0.7% 的子串 7% 误判为冲突
                pat = r"(?<![\d.])" + re.escape(bad) + r"(?!\d)"
                allowed = e.get("allowed_contexts", {}).get(bad, [])
                bad_lines = [ln for ln in txt.splitlines() if re.search(pat, ln)]
                bad_lines = [ln for ln in bad_lines if not any(ctx in ln for ctx in allowed)]
                if bad_lines:
                    conflicts.append(f"{e['id']}: {rel} 出现禁用变体 {bad}（非白名单上下文）")
    first = f"entries={len(entries)} occurrences={total_occ} conflicts={len(conflicts)} problems={len(conflicts)}"
    print(first)
    print(f"ledger_sha12={sha12(LEDGER)}")
    if conflicts:
        for c in conflicts:
            print("FAIL " + c)
        return 1
    print("PASS 全部规范值在指定文件出现且禁用变体缺席")
    return 0


if __name__ == "__main__":
    sys.exit(main())
