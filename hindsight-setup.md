# Hindsight 配置状态（2026-11-27）

诊断结果（hindsight_diagnose，只读）：
- bank：`coding-agent::F:\deepseek`
- 配置文件 `/home/liuzewen/.hindsight/coding-agent.json` 不存在。
- `api_url = https://api.hindsight.vectorize.io`，`api_token_configured = false`，`disabled = false`。
- 无 `HINDSIGHT_*` / `VECTORIZE_*` 环境变量；诊断日志中出现配置键名 `apiToken`，但未发现可用凭据。
- `hindsight_ingest_document` / `hindsight_search_pages` 返回 401（`no apiToken is configured`）。

结论：Hindsight 云端记忆通道因缺少 apiToken 未启用；不重试、不伪造凭据。临时替代通道已实际使用：
- `scripts/ledger_append.py --series L-ops`（已追加 L-ops-984）
- `MEMORY.md` 项目段落
- `notes/2026-11-26-新一代电子技术研究-六轮迭代启示与记忆.md`

恢复步骤（需凭据由持有者提供后再执行）：
1. 将 apiToken 写入 `/home/liuzewen/.hindsight/coding-agent.json`（键名 `apiToken`），或从 shell 注入对应环境变量；不要在日志、报告或 git 中记录值。
2. 重跑 `hindsight_diagnose`，确认 `api_token_configured = true`。
3. 用 `hindsight_ingest_document` 摄入 `notes/2026-11-26-新一代电子技术研究-六轮迭代启示与记忆.md`，并用 `hindsight_search_pages` 做一次检索验证。
4. 验证通过后在本文件追加「已恢复」与日期；验证失败仍保留 401 记录。
