#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
质量成熟度 QMM 诊断报告生成器
读入结构化结果 JSON，生成 MD 文档 + 精美网页版 HTML（主色 #C8102E）。

用法：
  python build_report.py --input result.json --md-out report.md --html-out report.html
  python build_report.py                      # 使用内置演示数据，输出到 ./output/

输入 JSON 结构：
{
  "meta": {"company":"示例制造有限公司","date":"2026-04-20","scope":"整体（演示数据，待企业补充）","mode":"自评"},
  "dimensions": [
    {"name":"领导与战略","score":3,"evidence":"有质量方针但未与战略量化挂钩","gap":"缺少质量战略分解"},
    ...
  ],
  "roadmap": [
    {"target_level":"L4 量化管理","action":"建立过程KPI与SPC监控","owner":"质量部","priority":"高"}
  ]
}
"""
import argparse
import json
import os
import sys
import html
from datetime import datetime

MAIN = "#C8102E"  # 主色

LEVELS = {
    1: "L1 初始级（应对式）",
    2: "L2 已管理级（基本流程）",
    3: "L3 已定义级（标准化）",
    4: "L4 量化管理级（数据驱动）",
    5: "L5 优化级（持续改进/卓越）",
}


def esc(s):
    return html.escape(str(s), quote=True)


def load_result(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def level_of(avg):
    # 阈值：≥4.5→L5, ≥3.5→L4, ≥2.5→L3, ≥1.5→L2, 否则 L1（企业可调，待企业补充）
    if avg >= 4.5:
        return 5
    if avg >= 3.5:
        return 4
    if avg >= 2.5:
        return 3
    if avg >= 1.5:
        return 2
    return 1


# ----------------------------- 内置演示数据 -----------------------------
DEMO = {
    "meta": {
        "company": "示例制造有限公司（演示数据，待企业补充）",
        "date": "2026-04-20",
        "scope": "整体质量管理体系",
        "mode": "自评"
    },
    "dimensions": [
        {"name": "领导与战略", "score": 3, "evidence": "有质量方针但未与战略量化挂钩", "gap": "缺少质量战略分解"},
        {"name": "顾客与满意", "score": 3, "evidence": "有投诉处理但满意度未闭环分析", "gap": "顾客声音未系统转化为改进"},
        {"name": "过程管理", "score": 2, "evidence": "关键过程有SOP但执行一致性不足", "gap": "过程绩效监控薄弱"},
        {"name": "测量分析与知识", "score": 2, "evidence": "有检验数据但缺趋势分析与知识沉淀", "gap": "数据未驱动决策"},
        {"name": "改进与创新", "score": 3, "evidence": "有纠正措施但预防与横向展开不足", "gap": "改进多为事后救火"},
        {"name": "结果绩效", "score": 3, "evidence": "合格率达标但成本与效率指标缺失", "gap": "结果维度指标不全"}
    ],
    "roadmap": [
        {"target_level": "L3 已定义级", "action": "统一过程SOP并加强执行一致性与过程监控", "owner": "生产/质量", "priority": "高"},
        {"target_level": "L4 量化管理级", "action": "建立过程KPI看板与SPC趋势分析", "owner": "质量部", "priority": "高"},
        {"target_level": "L4 量化管理级", "action": "顾客满意度闭环分析与改进机制", "owner": "营销/质量", "priority": "中"},
        {"target_level": "L5 优化级", "action": "推行预防型改进与知识库沉淀", "owner": "体系部", "priority": "中"}
    ]
}


# ----------------------------- MD 生成 -----------------------------
def build_md(r):
    L = []
    m = r.get("meta", {})
    dims = r.get("dimensions", []) or []
    avg = sum(d.get("score", 0) for d in dims) / len(dims) if dims else 0
    lvl = level_of(avg)
    L.append("# 质量成熟度诊断报告（QMM）\n")
    L.append("## 一、评估概况\n")
    L.append(f"- 企业名称：{m.get('company','')}")
    L.append(f"- 评估日期：{m.get('date','')}")
    L.append(f"- 评估范围：{m.get('scope','')}")
    L.append(f"- 评分方式：{m.get('mode','')}")
    L.append(f"- 参考框架：ISO 9004 / EFQM 通用成熟度思路（阈值待企业补充）")
    L.append("")
    L.append("## 二、维度评分\n")
    L.append(f"- **整体成熟度：{LEVELS[lvl]}（均分 {avg:.2f}/5）** 〔由企业结合战略确认〕")
    L.append("")
    L.append("| 维度 | 评分(1-5) | 证据 | 差距 |")
    L.append("|------|-----------|------|------|")
    for d in dims:
        L.append(f"| {d.get('name','')} | {d.get('score','')} | {d.get('evidence','')} | {d.get('gap','')} |")
    L.append("")
    L.append("## 三、短板诊断\n")
    weak = sorted(dims, key=lambda x: x.get("score", 0))[:2]
    for d in weak:
        L.append(f"- **{d.get('name','')}（{d.get('score','')}分）**：{d.get('gap','')}")
    L.append("")
    L.append("## 四、改进路线图\n")
    L.append("| 目标等级 | 改进措施 | 责任 | 优先级 |")
    L.append("|----------|----------|------|--------|")
    for rm in r.get("roadmap", []) or []:
        L.append(f"| {rm.get('target_level','')} | {rm.get('action','')} | {rm.get('owner','')} | {rm.get('priority','')} |")
    L.append("")
    L.append(f"> 报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')} ｜ 主色 {MAIN}")
    return "\n".join(L)


# ----------------------------- HTML 生成 -----------------------------
CSS = """
:root{ --main:%s; --bg:#f7f8fa; --card:#fff; --ink:#1f2937; --muted:#6b7280; --line:#e5e7eb; }
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif;background:var(--bg);color:var(--ink);line-height:1.7;padding:32px}
.wrap{max-width:1100px;margin:0 auto}
header{text-align:center;padding:30px 0 20px;border-bottom:3px solid var(--main);margin-bottom:28px}
header h1{font-size:27px;letter-spacing:1px}
header .meta{color:var(--muted);font-size:14px;margin-top:10px}
.sec{background:var(--card);border-radius:14px;padding:24px;box-shadow:0 4px 16px rgba(0,0,0,.06);margin-bottom:26px}
.sec h2{font-size:21px;margin-bottom:16px;border-left:5px solid var(--main);padding-left:12px}
.badge{display:inline-block;background:var(--main);color:#fff;padding:6px 16px;border-radius:8px;font-size:16px;font-weight:700}
table{width:100%%;border-collapse:collapse;font-size:14px}
th,td{border:1px solid var(--line);padding:9px 11px;text-align:left;vertical-align:top}
th{background:#fef2f4;color:var(--main);font-weight:700}
tr:nth-child(even){background:#fafafa}
.score5{color:#15803d;font-weight:700}.score4{color:#65a30d;font-weight:700}
.score3{color:#d97706;font-weight:700}.score2{color:#ea580c;font-weight:700}.score1{color:#b91c1c;font-weight:700}
.rm{background:#fef2f4;border-left:5px solid var(--main);padding:14px 16px;border-radius:8px;margin-bottom:12px;font-size:14px}
footer{text-align:center;color:var(--muted);font-size:12px;margin-top:20px}
""" % MAIN


def build_html(r):
    m = r.get("meta", {})
    dims = r.get("dimensions", []) or []
    avg = sum(d.get("score", 0) for d in dims) / len(dims) if dims else 0
    lvl = level_of(avg)

    def score_cls(s):
        return f"score{s}"

    dim_rows = "".join(
        f"<tr><td>{esc(d.get('name',''))}</td><td class='{score_cls(d.get('score',0))}'>{d.get('score','')}</td>"
        f"<td>{esc(d.get('evidence',''))}</td><td>{esc(d.get('gap',''))}</td></tr>"
        for d in dims)
    weak = sorted(dims, key=lambda x: x.get("score", 0))[:2]
    weak_html = "".join(
        f"<li><b>{esc(d.get('name',''))}</b>（{d.get('score','')}分）：{esc(d.get('gap',''))}</li>"
        for d in weak)
    rm_html = "".join(
        f"<div class='rm'><b>{esc(rm.get('target_level',''))}</b> ｜ {esc(rm.get('action',''))}"
        f" ｜ 责任：{esc(rm.get('owner',''))} ｜ 优先级：{esc(rm.get('priority',''))}</div>"
        for rm in r.get("roadmap", []) or [])

    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>质量成熟度诊断报告 · {esc(m.get('company',''))}</title>
<style>{CSS}</style></head>
<body><div class="wrap">
<header>
  <h1>质量成熟度诊断报告（QMM）</h1>
  <div class="meta">{esc(m.get('company',''))} ｜ {esc(m.get('date',''))} ｜ {esc(m.get('scope',''))} ｜ {esc(m.get('mode',''))}</div>
</header>

<section class="sec" style="text-align:center">
  <span class="badge">整体成熟度：{esc(LEVELS[lvl])}（均分 {avg:.2f}/5）</span>
  <div style="color:var(--muted);font-size:13px;margin-top:8px">〔由企业结合战略确认〕</div>
</section>

<section class="sec">
  <h2>一、维度评分</h2>
  <table><thead><tr><th>维度</th><th>评分(1-5)</th><th>证据</th><th>差距</th></tr></thead>
  <tbody>{dim_rows}</tbody></table>
</section>

<section class="sec">
  <h2>二、短板诊断</h2>
  <ul style="padding-left:20px;line-height:2">{weak_html}</ul>
</section>

<section class="sec">
  <h2>三、改进路线图</h2>
  {rm_html}
</section>

<footer>本报告由 质量成熟度QMM技能 生成 · {datetime.now().strftime('%Y-%m-%d %H:%M')} · 主色 {MAIN} · 参考 ISO9004/EFQM 思路</footer>
</div></body></html>"""


def main():
    ap = argparse.ArgumentParser(description="质量成熟度 QMM 诊断报告生成器")
    ap.add_argument("--input", help="结构化结果 JSON 路径（缺省使用内置演示数据）")
    ap.add_argument("--md-out", help="输出 MD 路径")
    ap.add_argument("--html-out", help="输出 HTML 路径")
    args = ap.parse_args()

    if args.input:
        try:
            r = load_result(args.input)
        except Exception as e:
            sys.stderr.write(f"读取输入失败：{e}\n")
            sys.exit(1)
    else:
        r = DEMO
        sys.stderr.write("未指定 --input，使用内置演示数据。\n")

    if not args.md_out and not args.html_out:
        out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
        os.makedirs(out_dir, exist_ok=True)
        args.md_out = os.path.join(out_dir, "maturity_report.md")
        args.html_out = os.path.join(out_dir, "maturity_report.html")

    if args.md_out:
        with open(args.md_out, "w", encoding="utf-8") as f:
            f.write(build_md(r))
        sys.stderr.write(f"MD 已生成：{args.md_out}\n")
    if args.html_out:
        with open(args.html_out, "w", encoding="utf-8") as f:
            f.write(build_html(r))
        sys.stderr.write(f"HTML 已生成：{args.html_out}\n")


if __name__ == "__main__":
    main()
