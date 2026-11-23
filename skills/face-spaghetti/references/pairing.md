# 与 mattpocock/skills 配套

`mattpocock/skills` 是 `/ask-matt` 路由的那套 engineering / productivity skills。两边都不开箱即用，都要先跑 per-repo setup；配套的分工是：**本 skill 在前段**（把脏输入变成已证事实与术语）；那套 skill 提供后段（spec / tickets / implement）与可嵌入前段的取证工具（`/prototype`、`/research`、`/domain-modeling`）。

共用 `docs/agents/` 契约的价值：一次 setup 同时点亮两套 skill，且不会各写一份配置。本 skill 的 setup 只补 `face-spaghetti.md` 与指针；`issue-tracker.md` / `triage-labels.md` / `domain.md` 归 `/setup-matt-pocock-skills`。

不修改它的安装文件（插件缓存会被 marketplace 更新覆盖）；配套规则全部留在本 skill 与仓库 `docs/agents/` 里。`/ask-matt` 的路由表由上游维护，屎山语境下的入口修正写在这里。

## 依赖方向：本 skill 在前段

那套 skill 默认**用户与代码都是干净的**：用户能回答、代码可读、模块边界已知。屎山把三个前提同时打破，所以它不能当入口——不是因为它差，而是因为它的输入契约不成立。

| 下游 | 它假设 | 屎山打破时 |
|---|---|---|
| `/grilling` | 用户知道答案，且答案在脑子里 | 用户答不出 → 转 `待证` + 探针 |
| `/domain-modeling` | 术语已存在，或用户能定义 | 术语只能从 artifact 反推 → 先 `已证` 再进 glossary |
| `/to-spec` | 代码可读、模块边界已知 | 边界未知 → 先做定义域表 / 探针 |
| `/to-tickets` | 任务能按已知接口拆分 | 接口未证 → 先 `blocked` + 回流条件 |
| `/implement` | 实现路径与验收标准已知 | 判据写不出 → 可测性门挡住 |

本 skill 的产物就是下游的**输入契约**：`已证` fact + 判据 + 术语 + 覆盖表。下游只消费这个集合，不重新问用户，也不把 L1 当事实。

## 为什么入口是本 skill

那套 skill 的主流程，输入不止访谈：`/grilling` 从用户脑子里取**决定**；`/prototype` 是**先做后定**，用廉价可运行物把问题问出来；`/research` 从一手资料取**事实**。屎山缺的通常不是决定，是事实——格式、调用约定、状态迁移、分支覆盖，用户和文档都没有。

所以危险的不是那套 skill，而是**把 grilling 当默认取证方式**：它会把事实缺口排成一串「用户和文档都没记载」的追问，最后得到三种坏结果——用户被问住、agent 把猜测当答案、或为了结束访谈凭空补一个「合理」假设。本 skill 的预注册 + 探针 + 证据等级就是替代这条路径。

**入口规则**：命中本 skill 触发词时，从本 skill 开工；上游在三个位置接入：

| 位置 | 用什么 | 何时 |
|---|---|---|
| 取证 | `/prototype`、`/research` | 循环内（`SKILL.md` §2.2 Probe 的同族手段） |
| 账本 | `/domain-modeling`、`/to-tickets`、`/triage` | 术语 `已证` 后、backlog 发布时 |
| 交付 | `/to-spec`、`/implement`、`/tdd`、`/code-review` | 事实 `已证`、判据二值之后 |

`/grilling` 只作为取证行的例外：只取用户拥有的决定。

## 三种取证模式

| 模式 | 输入 | 擅长 | 在屎山里 |
|---|---|---|---|
| 探针 / 原型（先做后定） | 被测物 + 廉价可运行物 | 行为、格式、状态迁移、UI 形状 | **首选**；`/prototype` 与 `SKILL.md` §2.2 的一次性探针同族 |
| 研究 | 一手文档 / 源码 / 规范 | SDK / 平台 / 协议语义 | 可用；结论按 `SKILL.md` §4 定级 |
| 访谈 | 用户脑中的决定 | 范围、优先级、验收口径、取舍、命名 | **受限**：只问用户拥有的；机制问题不问 |

### 原型 = 探针

`/prototype` 的「先做后定」与本 skill 的「事实先于计划」同向：两者都用可运行物把答案逼出来，再决定。配套时按探针规则落：

1. 动生产代码 / 改共享状态前，先落 `待证` 行（假设 + 互斥预测 + 判据）；原型本身就是这一轮的 probe。
2. 原型放 gitignored 探测目录或 `probe/<name>` 分支；仓库已有 `/prototype` 约定的（`prototype/<name>` 分支），按仓库约定，路径写进 `docs/agents/face-spaghetti.md`。
3. 原型的结论进台账；`/prototype` 的「capture it when done」与 `SKILL.md` §2.4 Promote 是同一动作——原型留档，只把已证决定折进正式代码。
4. 原型若只回答「用户想要什么」，结论是**决定**，不是 fact；写进 plan / glossary，不占 `已证`。

`/prototype` 默认把原型放在被测模块旁边；屎山里按探针隔离优先（独立目录 / gitignored / `probe/<name>` 分支），仓库已有明确约定时从约定。两边冲突时，隔离规则赢——原型写脏生产树比丢上下文更贵。

### 研究不是 fact

`/research` 产出的是带引用的 Markdown，不是台账行。引用它时仍要落 fact：出处写「research 文件 + 一手来源」，等级按 `SKILL.md` §4 定级——有引用不等于 `已证`，二手转述不算一手来源。artifact 的行为问题（这个函数怎么走）不能用 research 收口，要用探针。

## 问题归属

决定一件事问谁，比怎么问更重要。未列出的问题按「被测物能答就问被测物」处理。

| 问题 | 谁答 | 动作 | 兜底 |
|---|---|---|---|
| 范围 / 优先级 / 验收口径 / 取舍 / 命名偏好 | 用户 | grill / ask；一轮问完 frontier | 用户不答 → 保守默认 + plan 记 `config=default` |
| 行为 / 格式 / 调用约定 / 状态迁移 / 分支覆盖 / 布局 / 常量 | 被测物 | claim → probe / prototype | 探针造不出 → `blocked` + 回流条件 |
| 第三方平台 / SDK / 协议的公开语义 | 一手文档 / 源码 | `/research` 或直接读 | 文档缺失 → L1 线索 + 探针 |
| 只有用户能看到的运行时现象（目测 / 人工操作） | 用户 | human lane（`needs` 标签） | 无法机器捕获 → 只作验收 |

三条硬规则：

1. **机制问题不问用户。** 用户答「不知道」是正常结果，不是阻塞；转 `待证` + 探针。
2. **grilling 的 frontier 里不得有被测物能答的问题。** 出现就移出本轮，进探针队列。
3. **用户的机制口述只算 L1 线索**（`SKILL.md` §4）；谈范围 / 取舍 / 验收口径时才是权威。

## 四本账

| 账 | 记什么 | 落点 | 谁写 |
|---|---|---|---|
| 事实账 | 二值 claim、等级、出处、状态 | `docs/facts.md` | `SKILL.md` §8 |
| 定义域 | `measured` / `unmeasured` 判据覆盖 | `docs/coverage-domain.md` | 本 skill `references/coverage-domain.md` |
| 领域语言 | glossary 术语、ADR 取舍 | `GLOSSARY.md`、`docs/adr/` | `/domain-modeling`，只收 `已证` |
| 工作队列 | backlog、tickets、triage 标签 | `docs/agents/issue-tracker.md` 指定处 | `/triage`、`/to-tickets` |

- **fact 是唯一事实源**：glossary 只收 `已证` 术语（或纯命名决定）；ticket / spec 只引用 fact id，不复述结论。
- **`待证` 不进 glossary / ADR**：猜测一旦写成领域文档，下一轮会被当前提引用。
- **同一结论只写一处**：台账写过的机制，spec / ticket 只写 id。

## 接入点：上游 skill × 角色

`invoke` 列按当前 marketplace 缓存里的 frontmatter 标注；升级后以各 SKILL.md 为准。`model` = 可在本 skill 流程内调用；`user` = `disable-model-invocation: true`，只能建议用户跑。

| 上游 skill | invoke | 在屎山里的角色 | 边界 / 禁止 |
|---|---|---|---|
| `/setup-matt-pocock-skills` | user | 写 `issue-tracker.md` / `triage-labels.md` / `domain.md` | 不写 `face-spaghetti.md`；本 skill 的 `references/setup.md` 只补指针 |
| `/domain-modeling` | model | 把 `已证` 术语固化进 glossary；记录取舍 ADR | 不收 `待证` 猜测；ADR 只记取舍，不记反编译推断 |
| `/prototype` | model | 先做后定：行为 / UI 形状 / 状态模型 | 按探针规则预注册与留档；隔离优先于它默认的「放被测模块旁」；结论进台账 |
| `/research` | model | 一手资料的后台调研 | 不替代 artifact 探针；不直接产生 `已证` |
| `/grilling` | model | 只取用户拥有的决定 | frontier 排除被测物能答的问题 |
| `/grill-with-docs` / `/grill-me` | user | 同上，带 glossary / 无状态两种包装 | 同上；glossary 侧只收 `已证` |
| `/triage` | user | 外部来的 bug / 需求分诊 | 只发布，不驱动探测；不 triage `/to-tickets` 产出 |
| `/to-tickets` | user | 已证事实拆成 tracer-bullet ticket | 每条 ticket 带 `依据：F##`；缺依据 → 拒绝开工 |
| `/to-spec` | user | 事实齐全后收敛 spec | 「Testing Decisions」引用 `docs/coverage-domain.md` 与 fact id；L1 不写成事实 |
| `/tdd` | model | RED→GREEN 执行形态 | 前置仍是本 skill 可测性门（正例 + 必失败负例） |
| `/diagnosing-bugs` | model | 有具体 bug 时，Phase 1 的 tight loop 就是 oracle / 判据来源 | 事实仍进 `docs/facts.md`；不另立台账 |
| `/implement` / `/implement-spec` | user | 事实齐全后的实现 | 前置：相关 fact `已证`、判据二值、lane 表就绪 |
| `/code-review` / `/pr` | model | Promote 之后的评审与交付 | 不改台账；review 发现的事实缺口回本 skill |
| `/wayfinder` | user | 大范围地图；destination / scope 仍是决定 | ticket 按问题归属选类型：事实 → prototype / probe；research 只接平台语义；grilling 只接决定 |
| `/ask-matt` | user | 用户问「用哪个 skill」时的路由器 | 屎山语境第一步是本 skill；主流程从事实 `已证` 之后接入 |

## 两个方向的交接

**本 skill → 上游**（事实已证，开始交付）：

1. plan 头部 gate 是 `passed`，相关任务行带 `依据：F##`；
2. 判据定义域表已交，未测项有 blocker；
3. 接 `/to-spec`（多会话）或 `/implement`（单会话）；每张 ticket 带 fact id 与判据命令；
4. 实现完 `/code-review`，按 `SKILL.md` §2.4 Promote 回写台账。

**上游 → 本 skill**（spec / ticket / 原型里出现事实缺口）：

1. 问「这是决定还是事实」：决定留在上游；事实开 `待证` 行；
2. 先探针或原型，后 spec；不得用 grilling 补事实；
3. 探针造不出 → `blocked` + 回流条件，ticket 标 `ready-for-human` 或留 backlog。

## 反模式

| 反模式 | 症状 | 处理 |
|---|---|---|
| 用 grilling 补事实 | 一轮问题里有「这个函数怎么处理 X」「格式是什么」 | 移出本轮，转 `待证` |
| 用户说「不知道」就停 | 任务标 blocked，但没有探针 | 先问「被测物能不能答」；能答就造探针 / 原型 |
| 原型做完就丢 | 结论没进台账，下一轮重新发明 | 原型 = 探针：先 `待证`，留档，结论进 fact |
| 把用户口述写进 glossary | 术语看起来精确，但没测过 | 只收 `已证`；命名偏好可以收，机制描述不行 |
| spec 里写「根据反编译，X 应该是 Y」 | L1 进了「事实」段 | 改成 `待证`，机制另起 claim 补到 L2+ |
| wayfinder 的 research ticket 直接收口 | 读了文档就关 ticket，没跑探针 | research 只解决平台语义；artifact 事实另开 ticket |
| 两套 setup 各写一份 `docs/agents` | 文件互相覆盖 | 各写各的：`docs/agents/` 三个文件归 `/setup-matt-pocock-skills`，`face-spaghetti.md` 归本 skill + 指针 |

## 完成判据

- 仓库有 `docs/agents/face-spaghetti.md`；`docs/agents/issue-tracker.md` 存在或明确不装；
- plan 任务行能指到 fact id，fact 出处能重放；
- glossary 里没有 `待证` 猜测；
- ticket / spec 不复制台账结论，只引用 id。
