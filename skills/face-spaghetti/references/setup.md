# 项目适配 setup

本 skill 的 setup，形态与 `setup-matt-pocock-skills` 相同：prompt 驱动，先读现状、再逐节确认、最后写文件；不装依赖、不改代码，不做第二套配置。区别只有一处——它只写 `docs/agents/face-spaghetti.md` 与指令文件里的指针，**不碰**同目录另外三个文件（issue tracker / triage labels / domain docs 归 `/setup-matt-pocock-skills`）。

入口是 `SKILL.md` §9：判定「直接做 / 改造后做」而仓库缺 `docs/agents/face-spaghetti.md` 时，先跑本流程。

## 何时跑

| 情况 | 动作 |
|---|---|
| 仓库首次进入 §2 循环，缺配置文件 | 跑 |
| 仓库只跑过 `/setup-matt-pocock-skills` | 跑；本 skill 的落点与指针还没建 |
| 只跑了本 setup，缺 `docs/agents/` 三个文件 | 不阻塞；backlog / glossary 用默认落点，提示用户跑 `/setup-matt-pocock-skills` |
| 台账 / 计划 / 仪器目录的实际位置变了 | 跑，覆盖更新 |
| 换 issue tracker 或 plan 目录约定 | 跑；同时让用户重跑 `/setup-matt-pocock-skills`（user-invoked，agent 不能替他触发） |
| 用户重跑过 `/setup-matt-pocock-skills` | 检查 `### Face Spaghetti` 指针还在；掉了就只补这一节 |
| 只是新增 task / fact / 探测 | 不跑 |
| 只想核验现状 | 跑，但用户说「只看不写，报漂移」时只报差异，不改文件 |

## 1. Explore（只读）

逐项读，别假设：

- `git remote -v` / `.git/config`；`docs/agents/` 现有文件：`issue-tracker.md` / `triage-labels.md` / `domain.md`（`/setup-matt-pocock-skills` 侧）与 `face-spaghetti.md`（本侧），别覆盖别人的；
- `CLAUDE.md` / `AGENTS.md`：哪个存在、有没有 `## Agent skills` 块、块里有没有 `### Face Spaghetti`；
- `GLOSSARY.md` / `GLOSSARY-MAP.md`、`docs/adr/`、`src/*/docs/adr/`；
- 台账候选（`docs/facts.md`、`FACTS_FILE`）、计划目录（`tasks/`、`docs/plans/`）、`work/`、`probe/`、`tools/`、`build/`；
- 门禁：`package.json` scripts、`Makefile`、`scripts/verify*`、`.github/workflows`；
- 共享资源信号：存档 / 配置目录、音频设备、单实例应用、注册表键。

先给一句「已有 / 缺什么」，再进确认。

## 2. 逐节确认

一次一节，推荐答案在前；探索已经定下来的节直接跳过。每节一句话解释，只有真分叉才展开。用户已经说「用默认」时把推荐答案当已答，不再逐节等回复，但草案仍要贴一遍。

**A. 台账与计划。** 推荐：台账 `docs/facts.md`；计划沿用仓库已有目录（`tasks/plan.md` + `tasks/todo.md`，或 `docs/plans/`）。列出的文件不存在只标「未建」，不替仓库创建；非默认路径才需要 `FACTS_FILE` / `PLAN_GLOBS`。

**B. 探测目录与仪器。** 推荐：一次性探测放仓库已有的 gitignored 目录（`work/`，没有则 `probe/`）；可复用仪器进 `tools/`；oracle 只读，运行副本放探测目录并记 md5。没有 oracle 就写「暂无」。

**C. 共享资源。** 只问探索发现的那几项（存档、音频端点、单实例进程、系统设置）：隔离方式 + 恢复命令。没有就不问，写出的文件里也删掉这一节，探索结论里报「无共享资源」。

**D. 门禁命令。** 推荐：仓库已有的 `verify` / `check` 脚本，加 `bash <skill 路径>/scripts/append-only-check.sh --worktree`。仓库没有任何 verify 类脚本时，门禁只写 append-only 检查。

一节一个回答，然后下一节；不要一次抛出四节。

## 3. 给出草案，允许编辑

把 `docs/agents/face-spaghetti.md` 的完整草案和指令文件里要加的那段贴出来，用户改完再写。

## 4. 写

1. 写 `docs/agents/face-spaghetti.md`（种子模板见下）。已存在 → 按新答案就地更新字段，保留用户手改的内容。
2. 选指令文件：`CLAUDE.md` 存在就编辑它；否则 `AGENTS.md`；两个都不存在 → 问用户建哪个，不替它选。
3. 放置指针：
   - 已有 `## Agent skills` 块 → 在块末尾追加或就地更新 `### Face Spaghetti`，绝不复制出第二个块，也不动同块里另外三节；
   - 没有该块 → 文末追加一行独立指针，**不**替 `/setup-matt-pocock-skills` 创建这个块。
4. 当前 harness 读的文件与 `CLAUDE.md` 不一致时（例如 Codex 只读 `AGENTS.md`），指针写 harness 实际读的那个文件；或让 `CLAUDE.md` 退化成一行指针。

指针长这样：

```markdown
### Face Spaghetti

台账 / 探测目录 / 仪器 / 门禁落点见 `docs/agents/face-spaghetti.md`；开工前先读它。
```

## 5. Done

报出：写了哪两个文件、哪些命令是门禁、哪些路径不是默认值、`docs/agents/` 三个文件哪些缺（缺文件不阻塞本 setup，标「未装」）。之后直接手改 `docs/agents/face-spaghetti.md`；重跑只在换 tracker、换目录约定或重建仓库时。

`docs/agents/issue-tracker.md` 缺失不影响本 setup；需要 backlog 进 tracker 时，提示用户跑 `/setup-matt-pocock-skills`。tracker 写的是 GitHub / GitLab 但 `git remote` 里没有对应主机时，只在本步报出来，不替它改。

## 种子模板：`docs/agents/face-spaghetti.md`

````markdown
# Face Spaghetti 落点

本仓库的 face-spaghetti 配置。`SKILL.md` §9 读它；手改优先于重跑 setup。

## 落点

「覆盖开关」列填对应的环境变量名（用默认路径也照填）；用不上的填 `—`。文件或目录不存在就标「未建」，不替仓库创建。

| 项 | 路径 / 命令 | 覆盖开关 |
|---|---|---|
| 台账 | `docs/facts.md` | `FACTS_FILE` |
| 计划 / todo | `tasks/plan.md`、`tasks/todo.md`（未建就标注） | `PLAN_GLOBS` |
| 判据定义域表 | `docs/coverage-domain.md`（未建就标注） | — |
| 进度 / surface 表 | `<项目约定目录>/surface.csv`、`surface-history.csv`（没有就写「未建」，目录未约定就只留文件名） | — |
| 领域语言 | `GLOSSARY.md`、`docs/adr/`（`/domain-modeling` 按需建；未建就标注） | — |
| 一次性探测目录 | `work/`（gitignored） | — |
| 仪器目录 | `tools/` | — |
| 只读 oracle | `<path>`（运行副本 + md5；没有写「暂无」） | — |
| backlog 发布 | `docs/agents/issue-tracker.md`（存在时） | — |
| 配套文件 | `docs/agents/issue-tracker.md` / `triage-labels.md` / `domain.md`（`/setup-matt-pocock-skills` 产物） | — |
| 门禁 | `bash <skill 路径>/scripts/append-only-check.sh --worktree`；`<verify 命令，没有就删>` | — |

配套分工（原型 / 研究 / 访谈、四本账）见 skill 的 `references/pairing.md`；本文件只记落点。

## 本机事实

解释器 / 工具绝对路径、SDK 安装位置、服务名、账号；skill 目录也算（门禁命令里的脚本路径）。单机不分节，换机器时按机器分节。

## 共享资源

没有共享资源就删掉本节。

| 资源 | 隔离方式 | 恢复命令 |
|---|---|---|
| （存档 / 音频端点 / 配置） | （独立 profile / 私有桌面 / 虚拟设备） | （每轮探测后执行） |

## 冻结树

（换目标时填：路径 / 冻结日期 / 基线提交 / 复跑门禁；没有就删掉本节。步骤见 face-spaghetti 的 `references/handoff.md`。）
````
