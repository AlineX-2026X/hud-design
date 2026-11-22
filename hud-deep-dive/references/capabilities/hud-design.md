# HUD 设计全流程（摘要卡）

> 完整版见独立技能 `hud-design` 的 `SKILL.md`。本卡保留骨架与阈值，供只安装本技能时使用。

## 七层

1. **决策清单**：3 秒内必须回答的 3 个问题——状态 / 动作 / 风险。答不出不开工。
2. **分区**：顶栏 / 左轨 / 右轨 / 中央舞台 / 底栏；中央留净空 ≥35%。
3. **数据清单**：层级（环境 / 上下文 / 关键）、编码、单位、量程、刷新、阈值；关键项 ≤5。
4. **token**：单主色相 + 单告警色 + 深底；三级亮度 100 / 55 / 22；角标代替完整边框；介质痕迹 ≤3。
5. **组件库**：8–12 个参数化 widget，改参数不重画。
6. **动效**：进入 0–400ms、状态 120–240ms、常态 2–4s、强调一次性；并发 ≤3。
7. **集成与验收**：screen / world / diegetic 三选一；3 秒、灰阶、25% 缩略、色觉、状态完备、叠层 ≤4。

原则：**先可读，再可信，最后好看**。

## 输入与输出

输入：项目类型、主体、≤3 条用户任务、交付形态、运行环境、约束，另加界面显示语言（不填则自动探测）。

输出八件：`HUD Brief`、`Zone Map`、`Data Inventory`、`Design Tokens`、`Component List`、`Motion Timeline`、`Integration Spec`、`Acceptance Record`。

## 与相邻能力

- 已有界面要挑毛病 → `hud-audit`。
- 只改一层 → `layout-grammar` / `information-hierarchy` / `visual-language` / `motion-choreography` / `diegetic-integration`。
- 普通 App、官网、营销页、Logo、海报 → 不适用。

## 边界

- 假数据只能用于影视概念，不能标称「数据产品设计」。
- 户外强光、车载、政务公开屏需另加可用性评估。
- 无 3D / 实时主体时，改用常规仪表盘规范。

## 依据

> `3D ADJUSTABLE WIDGETS, REAL GEOMETRY` · `ADJUST TIME AND KEYFRAMES` —— 制作花絮里的画面字幕
> `ENGINE DIAGNOSTIC TOOL /READY` · `FUEL SYSTEM` · `HEADER 273` —— 工程屏上的模块标题

画面中未展示需求与验收阶段，本卡把这两步作为工程约定补齐。
