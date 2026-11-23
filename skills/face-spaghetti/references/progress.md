# 进度账：主分母饱和之后

## 触发

- 主分母（函数 / 文件 / 模块数）已经 100%，但台账还有 open 项：图说完成，台账说没完。
- 用户问「什么加到分母、什么作为奖励任务」。
- 想拿「剩余任务清单」直接当完成度。

## 症状

- 继续数主分母 = 永远 100%，失去分辨率；再发现的差异无处记账。
- 拿剩余任务队列当分母：收口即删行，分母自己缩小，历史不可比；队列也不能证明完备性（只包含你想到的项）。
- 把函数数、行为 cell、测试行数混成一个百分比：单位不同；测试行数还会随工作增长，越干活进度越低。

## 规则

1. **两个分母，不混算**。主分母 = 清单单位（函数 / 文件 / 字节）；副分母 = 枚举的行为 lane cell。并排显示，不合成单一百分比。
2. **分母来自枚举，不来自队列**。队列只是工作集；完备性来自判据定义域表（`coverage-domain.md`）里的「决定行为的量」。队列收口只改 cell 状态，不删分母。
3. **cell = 可独立翻转的最小 lane**。每个开关的每个取值（含程序默认值）、每个分支 / 参数变体各一格。合并或拆分 cell 要留变更记录，否则分母可被随意缩水。
4. **证据门槛**：`status=measured` 必须有 `test` + `fact`；`unmeasured` / `unknown` 留在分母，必须写 `blocker` + `close`。行为状态仍以项目的行为状态表（test-matrix）为准——进度表是分母，不是第二个状态源；冲突时以状态表为准并修进度表。
5. **scope 二分**：`core` = 合同内且本机可裁决，blocker 只允许 `none|instrument|human`；`bonus` = 合同外、本机不可裁决（`machine|file|product`）、或严于合同。`bonus` 不进主百分比，单独计数。blocker 含义：
   - `instrument`：缺仪器或仪器未过自证；
   - `human`：需要真人判断 / 操作；
   - `machine`：需要另一台机器或另一个平台环境；
   - `file`：缺文件 / 资源 / 录制；
   - `product`：需要产品或上游先改。
6. **反例**：仪器难造不是 bonus（`blocker=instrument` 仍是 core）；新发现的行为差异必须进 core，不能塞 bonus 逃避分母；bonus 也不能反向拉低主进度。
7. **只增留痕**：收口改 `measured`，不删行；新增 cell 必须带 `source` + 理由，并 append 一行绝对计数历史。分母变大导致百分比下降是合法的——静默改分母才是错的。
8. **历史记绝对计数**（`measured/total`），不记百分比。分母变化可解释，历史不会因分母漂移而失真。
9. **每个 cell 带需求 tag（`needs`）**。`done / not-done` 不说明「为什么还不能测、需要谁到场」。`needs` 是逗号分隔的标签集合，空 = 全自动：
   - `click` = 必须真人点击 / 按键（合成输入不可替代，如只认真实修饰键 / 真实前台）；
   - `visual` = 判据只能靠人眼（主题外观、本地化排版、帮助内容）；
   - `desktop` = 私有桌面 / 离屏不足以裁决（像素、焦点、前台、真实合成控件）；
   - `platform` = 判据依赖特定平台实现（版本 / DPI / locale / 主题 / 字体），环境改变时**判据会变**，必须重测或降为 bonus。
   tag 与 `blocker` 正交：`blocker` 说现在卡在哪，`needs` 说裁决时谁 / 什么必须在场。tag 不是 `close` 的替代；`unmeasured` 仍要写 `close`。页面 / 台账必须能按 tag 筛选并汇总「带 tag 的未完成 core 数」，否则用户看不出自己何时被需要。`platform` 不得用来把 core 项推去 bonus 逃避分母——它只标记「换环境要重测」。

## 残余任务的外部依赖分类

agent 可做项耗尽时，剩余台账每行除「为什么暂缓 + 回流条件」外还要标外部依赖，否则「剩余 N 项」会把不可推进项混进可做项反复试跑。四类可叠加，并直接映射到 `needs` tag：

| 属性 | 判据 | 默认处置 | `needs` |
|---|---|---|---|
| `测平台` | 结论值必须实测具体平台组件（版本 / DPI / locale / 定时器 / 消息队列 / GDI / 系统控件），不能由 oracle 录制或反编译推出 | 换目标环境或另立 fact；不得用同机 oracle 冒充已测 | `platform` |
| `活动桌面` | 私有桌面 / 离屏窗口不足以裁决（前台 / 焦点、真实光标、真人点击） | 单独 lane，不进默认 gate；与其它 GUI 测试串行 | `desktop` |
| `实时输入` | 合同禁用合成输入（如 `SendInput`），唯一路径是真人实时键鼠 | 记 `blocked` + 回流条件；不得用近似事件冒充 | `click` |
| `目测` | 判据只能靠人眼（主题外观、本地化排版、帮助内容），没有可自动化的像素 / 结构基线 | 只作验收，不作开发判据；先找像素 / 结构基线，找不到才留人眼 | `visual` |

属性非空的行不计入「agent 可做剩余」；同一函数其它侧面 matched 也不能替它收口。

## 最小落地

```csv
# <项目约定目录>/surface.csv
id,area,item,lane,scope,status,blocker,needs,test,fact,source,close,notes
# needs = click|visual|desktop|platform 的逗号子集；空 = 全自动

# <项目约定目录>/surface-history.csv
date,core_measured,core_total,bonus_measured,bonus_total,note
```

路径是项目约定，写进 `docs/agents/face-spaghetti.md`（`SKILL.md` §9）。生成器 gate（缺一即 exit 2，不写输出）：

- `status=measured` 缺 `test` 或 `fact`；
- `status!=measured` 缺 `close`；
- `scope=core` 且 `blocker` 是 `machine|file|product`；
- `scope/status/blocker` 越界、`id` 重复、history 计数 `measured>total`；
- `needs` 含未知 tag、tag 重复、或表缺 `needs` 列（要求每行显式决定，空值也算决定）。

必做负例：改坏一条 measured 的 `test`/`fact`；把一条 core 的 blocker 改成 `machine`；把 history 的 `total` 改一格（应只警告 lag，不能 exit 0 静默通过）；把一条 `needs` 改成未知 tag（exit 2）。

页面验收：四类 tag 各有 chip；筛选「任一 tag」只显示带 tag 行；汇总卡给出「带 tag 的未完成 core 数 + 分项计数」；控制台 0 错误。

## 判定

主进度 = 主分母与副分母都满，且 gate 全绿。只有主分母 100% 时，最多写「函数维度完成」，不能写「项目完成」。
