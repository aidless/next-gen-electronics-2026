# Provenance — research-collection

## v5（2026-11-25，当前）
- 生成脚本：`analyses/build_collection.py`（docs 列表 26 份，汇编描述动态生成"五轮深挖"）
- 自检脚本：`analyses/selfcheck.py`（27 份全 OK，389 锚点/389 链接/缺失 0，退出码 0）
- 源文档：主报告 v6（新增第十三节第五波深挖）+ 5 首轮专题 + 5 第二波 + 5 第三波 + 5 第四波 + 5 第五波（专题 21–25）
- 规模：9555 行 / 736834 字符 / 389 锚点；三格式同步重建：HTML（955712 字符/1153 目录链接）、PDF（11MB/305 页）、EPUB（27 章）
- 第五波五专题一手源：Nature Communications/NIST/上海科技大学/中科院高能所（专题21）；Formal Methods 论文/Siemens/Cadence/Synopsys 一手页（专题22）；NGK/IMAPS/APEC 2026/三井/斯达年报（专题23）；IBM/imec/BAQIS/NIST/中科大/电子科大（专题24）；ClinicalTrials.gov API/Neuralink/Synchron/Paradromics/Nature Medicine/NEO/FDA（专题25）。论文 DOI 逐条 web_fetch 验号；UNVERIFIED 单列不入结论
- 独立性：根目录 research-manifest.json 属另一研究线（长程推理天花板），本项目使用独立目录 `next-gen-electronics-2026/`，未改动共享 manifest
- GitHub：aidless/next-gen-electronics-2026（public；v1 + 产品化产物已 push，v2/v3/v4 本地 commit 于本次一并推送）

## v4（2026-11-25）
- 生成脚本：`analyses/build_collection.py`（docs 列表 21 份，汇编描述动态生成"四轮深挖"）
- 自检脚本：`analyses/selfcheck.py`（22 份全 OK，319 锚点/319 链接/缺失 0，退出码 0）
- 源文档：主报告 v5（新增第十二节第四波深挖）+ 5 首轮专题 + 5 第二波专题 + 5 第三波专题 + 5 第四波专题（专题 16–20）
- 规模：7729 行 / 593988 字符 / 319 锚点
- 第四波五专题一手源：Lightmatter/Nature + 曦智官网 + Q.ANT/NPS（专题16）；Intel Hala Point/SpiNNaker2/BrainScaleS-2/Sony Ace（专题17）；RISC-V ratified 文档树/RVA23 CRD/RISE 看板/OpenTitan/厂商公告（专题18）；VW CEA/NVIDIA/TI/华为/蔚来/地平线/IEEE TSN/中汽协（专题19）；JPL/NASA/TI/Frontgrade/Scientific Reports/JEIT（专题20）。论文 DOI 逐条 web_fetch 验号；UNVERIFIED 单列不入结论
- 独立性：根目录 research-manifest.json 属另一研究线（长程推理天花板），本项目使用独立目录 `next-gen-electronics-2026/`，未改动共享 manifest
- GitHub：aidless/next-gen-electronics-2026（public，2026-11-24 用户明确要求开源；v1 已推送，v2/v3/v4 本地 commit 未 push）

## v3（2026-11-24）
- 生成脚本：`analyses/build_collection.py`（docs 列表 16 份，汇编描述动态生成"三轮深挖"）
- 自检脚本：`analyses/selfcheck.py`（17 份全 OK，242 锚点/242 链接/缺失 0，退出码 0）
- 源文档：主报告 v4（新增第十一节第三波深挖）+ 5 首轮专题 + 5 第二波专题 + 5 第三波专题（专题 11–15）
- 规模：5978 行 / 455124 字符 / 242 锚点
- 第三波五专题一手源：NVIDIA/AMD/Google/AWS 官方架构文档 + UALink 规范 + Cerebras 新闻稿 + 华为 CloudMatrix384 论文（专题11）；索尼/三星/豪威/TI/ST 产品页 + Nature 封面 + 索尼-TSMC 合资公告（专题12）；SEMI/Lam/AMAT/ASM/KLA 设备数据 + BIS 管制原文（专题13）；味之素/ABF 供应链 + 玻璃基板厂商 + JEDEC HBM4 + ECTC/IEEE 论文（专题14）；Sony/Samsung/UBI Research + Lumus/SCHOTT + OLEDoS 产能（专题15）。论文 DOI 逐条 web_fetch 验号；UNVERIFIED 单列不入结论
- 独立性：根目录 research-manifest.json 属另一研究线（长程推理天花板），本项目使用独立目录 `next-gen-electronics-2026/`，未改动共享 manifest
- GitHub：aidless/next-gen-electronics-2026（public，2026-11-24 用户明确要求开源；v1 已推送，v2/v3 本地 commit 未 push）

## v2（2026-11-24）
- 生成脚本：`analyses/build_collection.py`（docs 列表 11 份）
- 自检脚本：`analyses/selfcheck.py`（12 份全 OK，155 锚点/155 链接/缺失 0，退出码 0）
- 源文档：主报告 v3（新增第十节第二波深挖）+ 5 首轮专题（v2）+ 5 第二波专题（专题 6–10，2026-11-24 新取证）
- 规模：4056 行 / 318872 字符 / 155 锚点
- 第二波五专题均带回一手源：ASML/SEC/SEC 20-F、IEEE/Transactions VLSI/EDL、SEC 8-K/EDGAR、Nature/Nature Physics、NVIDIA 官方指南/OCP/IEA 4E/RAND；论文 DOI 逐条 web_fetch 验号；UNVERIFIED 单列不入结论
- 独立性：根目录 research-manifest.json 属另一研究线（长程推理天花板），本项目使用独立目录 `next-gen-electronics-2026/`，未改动共享 manifest
- GitHub：aidless/next-gen-electronics-2026（public，2026-11-24 用户明确要求开源，v1 已推送）

## v1（2026-11-24）
- 6 份文档（1 报告 + 5 专题），2261 行 / 75 锚点 / 159144 字符，已推送 GitHub
- 检索窗口 2024-01 至 2026-11-23（最新对齐 2026-11）
- 证据纪律：结论先行；数字附出处链接与日期；论文 DOI web_fetch 验号；UNVERIFIED 隔离不入结论；冲突口径并列
