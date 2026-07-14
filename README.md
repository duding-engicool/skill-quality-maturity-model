# 质量成熟度 QMM（quality-maturity-model）

> 主色：`#C8102E`
> 范式：混合式双版（MD + HTML），由 `scripts/build_report.py` 生成。

## 简介

面向质量总监与体系总监的质量管理成熟度诊断助手。基于通用成熟度分级思路（参考 ISO 9004 自我评定方法与 EFQM 卓越模型分级逻辑），从六个维度量化评估企业质量管理水平（1–5 级），并生成分阶段改进路线图。

## 适用角色

- 质量总监：把握整体成熟度水平与改进优先级。
- 体系总监 / 体系负责人：组织自评估、维度打分与路线落地。

## 目录结构

```
quality-maturity-model/
├── SKILL.md                  # 技能定义（10 节结构 + TRACE 自评）
├── README.md                 # 本文件
├── scripts/
│   └── build_report.py       # 双版诊断报告生成器（MD + HTML）
└── references/
    └── qmm_dimensions.md     # 维度定义、等级特征与权重说明
```

## 快速开始

1. 调用技能，提供：企业名称、评估日期、范围、评分方式（自评/专家评）。
2. 对六个维度逐一打 1–5 分并提供证据。
3. 运行脚本产出诊断报告双版：

```bash
python scripts/build_report.py --input sample.json --md-out output/maturity_report.md --html-out output/maturity_report.html
# 或使用内置演示数据：
python scripts/build_report.py
```

## 报告双版说明

- **MD 版**：适合归档、版本管理与评审批注。
- **HTML 版**：适合高管汇报演示，主色 `#C8102E`，含维度雷达式评分卡与改进路线图。

## 注意事项

- 成熟度等级由企业结合战略正式确认，技能仅提供模型测算。
- 框架参考 ISO 9004 / EFQM 通用思路；权重与阈值企业可自定义（标注「待企业补充」）。
- 演示数据为内置小样本，正式使用前请替换为真实评分。
