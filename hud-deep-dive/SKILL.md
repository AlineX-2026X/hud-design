---
name: hud-deep-dive
description: |
  按层深潜 HUD 设计：屏幕分区与空间语法、信息分层与数据密度、视觉介质（配色 / 字体 / 发光）、动效编排、三种 HUD 与实拍或引擎内嵌；每个做法都给适用条件与反例。
  何时优先用独立技能：从零设计用 hud-design；诊断已有界面用 hud-audit。
  触发词：HUD布局、屏幕分区、信息层级、数据密度、HUD配色、发光、HUD动效、diegetic、world-space、适用条件。
license: MIT
metadata:
  version: 1.0.0
  source: 公开 HUD / FUI 成品影像的观察归纳（素材无解说、无设计推演）
---

# HUD 分层深潜：分区、层级、视觉、动效与内嵌

## 一、适用与不适用

**适用**：HUD 的某一层怎么做（分区 / 层级 / 视觉 / 动效 / 内嵌），以及想知道某个做法的适用条件与反例。

**不适用**：普通 App / 官网 / SaaS 后台 UI；纯平面海报、Logo、品牌 VI；影视游戏作品版权与素材采购；AE / C4D / UE 的按钮级操作教程；临床、驾驶安全、法规合规等需专业评估的可用性结论。

## 二、核心原则（概览类问题读到这里即可回答）

1. 先定屏上必须回答的三个问题（状态 / 动作 / 风险），再决定画什么。
2. 五功能区切开屏幕：顶栏、左右轨、中央舞台、底栏；中央必须留净空。
3. 信息分三层亮度（环境 / 上下文 / 关键），关键值最大最亮，关键项 ≤5。
4. 单主色相 + 单告警色；告警必须颜色 + 形状 + 文字三重编码。
5. 高密度表列区与低密度净空区并置，密区只在边缘，中央托主体。
6. 动效只做进入 / 状态 / 常态 / 强调四件事，关键动作后必须静止。
7. 可信度来自模式选择与物理痕迹：screen / world / diegetic 三选一，保留反光、倾斜、遮挡、噪点。
8. 屏上文字语言先探测系统：`bash scripts/detect-language.sh` → `zh-CN` 简体、`zh-TW` 繁体、`en` 英文；用户指定优先。支持 macOS、Windows（原生 PowerShell 用 `scripts/detect-language.ps1`）、Linux、WSL、鸿蒙。同一块屏只允许一种自然语言，机器标识与专有名词除外。

## 三、路由（按意图只加载 1 张能力卡）

| 用户意图 | 读这张卡 | 可补读 |
|---|---|---|
| 从零设计 HUD / FUI；游戏运行时 HUD；影视道具屏；工业 / 航天 / 医疗数据大屏；AR 叠加或驾驶舱 | `capabilities/hud-design.md` | 若已装独立技能 `hud-design`，优先直接用，本卡作背景 |
| 评审 HUD 截图或录屏；界面太乱、看不清、太花；上线前走查；要可执行优化清单 | `capabilities/hud-audit.md` | 若已装独立技能 `hud-audit`，优先直接用，本卡作背景 |
| 布局怎么排；屏幕怎么分区；仪表盘太乱怎么摆；数据与 3D 主体怎么对应 | `capabilities/layout-grammar.md` | `information-hierarchy.md` |
| 哪些数据该上屏；层级怎么分；太密怎么办；数值与单位怎么排版 | `capabilities/information-hierarchy.md` | `visual-language.md` |
| 配色；科幻感 / 发光怎么做；字体规范；告警色怎么用 | `capabilities/visual-language.md` | `motion-choreography.md` |
| 动效怎么做；进入节奏；界面太晃 / 太闪；关键帧怎么排 | `capabilities/motion-choreography.md` | `diegetic-integration.md` |
| 怎么和实拍结合；全息 / 投影怎么做才不假；游戏内 UI 放哪；AR 怎么锚定 | `capabilities/diegetic-integration.md` | `layout-grammar.md` |

以上卡片均在 `references/capabilities/` 下。另有三个参考文件：

- 术语与口径（HUD / FUI / 三层亮度 / 介质痕迹 / P0-P2） → `references/glossary.md`
- 七条一句话决策规则 → `references/cheatsheet.md`

## 四、加载规则

- 先读本文件，再按路由表加载 **1** 张能力卡；任务明确跨层时最多 2 张。
- 概览类问题不加载能力卡，直接用「核心原则」回答。
- 路由表命不中的意图，直接说明超出范围，不要硬套。

## 五、边界与判停

- 没有使用场景与关键任务时，只做视觉层建议，并声明无法判断可用性。
- 数据纯为装饰的影视概念需求，交付时标注「非真实数据产品」。
- 车载 / 户外 / 政务等强环境光或法规场景，停止套用深底发光语言，改提可用性评估。
- 已有界面问「哪里有问题」→ 转 `hud-audit`；要从零做 → 转 `hud-design`。
