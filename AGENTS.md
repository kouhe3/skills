# AGENTS.md — 维护者须知

给在本仓库工作的 agent 和维护者。**使用者读 [`README.md`](README.md)**，那里只有：这是什么、怎么装、三个 skill 干什么、Before/After。

分界判据只有一条：**这段文字会不会改变「要不要装」**。会 → README；只影响「怎么改这个仓库」→ 这里。

## 结构

```
README.md          使用者：定位 / 安装 / skill 表 / Before-After
AGENTS.md          维护者：本文
LICENSE            MIT
skills/
  <name>/SKILL.md  入口。name 与目录名一致，kebab-case
  <name>/references/   按需加载的细则
  <name>/scripts/      可执行取证/校验脚本
  <name>/agents/       跨 agent 的元数据（如 openai.yaml）
tools/validate_skills.py
```

`SKILL.md` 是路由，`references/` 是手册。细则写进 SKILL.md 等于让它在最频繁的路径上反复收费。

## 校验

```bash
python tools/validate_skills.py
```

当前查：frontmatter 键是否在规范白名单内、`name` 与目录名一致、`description` 长度 1–1024、正文 < 500 行、被引用的 `references|scripts|assets` 路径存在。

### 已知缺口（都没做，按代价排序）

| 缺什么 | 后果 | 判据 |
| --- | --- | --- |
| 只查行数不查字符 | 中文 329 行 = 2 万字 ≈ 英文 2,500 词，成本差约 8 倍；审核「合规」而实际超标 | `len(SKILL.md) < 8000` |
| 不查 references 是否被引用 | 以后加文件必出孤儿，且没人会发现 | 每个 `references/*.md` 出现在 SKILL.md 或它链接的索引文件里 |
| 不查绝对路径 / 凭据样式 | 本机路径与 session 串混进公开仓库 | 禁 `C:\`、`~/.`、`(session\|cookie\|token\|key)\s*=` |
| 没有 CI | 有 validator 而没人跑 = 工具链没有测试 | `.github/workflows` 在 push/PR 时跑一次 |

**顺序不能反**：先修 `face-spaghetti/SKILL.md` 的字符预算，再加字数门。现在加，CI 一上线就是红的，而红的门会被关掉。

## 改一个 skill 的检查单

逐条 PASS/FAIL，全部通过才算改完：

1. **description 只回答「要不要加载我」。** 跨 skill 协作（「装了 X 时从这里入口」）、边界、流程都在正文。判据：description 里不出现策略句。
2. **SKILL.md 是路由不是手册。** 每个 `##` 要么是一个判定，要么是一行「读哪个 reference」。
3. **四节齐**：`限度` / `不该用我` / `归属` / `可观察的停点`。定义见下。
4. **停点列不混级。** 二值信号（「第一句是问句吗」「这一轮给结论了吗」）写成硬 gate；判断类（「对方开始自己分析」）降级成参考信号，不和 gate 并列在同一列。
5. **新引用的文件在正文或索引里出现**，否则是孤儿。
6. 跑 `python tools/validate_skills.py`。

### 四节的定义

- **限度**：写明这是概率性提示，改变行为分布，单次结果不代表稳定。挡住「装了就该每次都灵」的期待。
- **不该用我**：什么情况下调用它多余或有害。负例比正例更能定义边界，也直接降低误触发。
- **归属**：哪部分来自原书/原项目，哪部分是自己的操作化；引用以原文为准。摘要型 skill 不写这节，读者无法分辨哪句话有出处。
- **可观察的停点**：每轮/每步停在什么信号上，且这个信号能被第三方观察到。

### 现状（2026-11）

| Skill | 限度 | 不该用我 | 归属 | 可观察停点 |
| --- | --- | --- | --- | --- |
| `helping` | ✓ | ✗（有「边界」节，但那是例外条款，不是负例） | ✓ | 部分（「第一句是问句」可检，「开始自己分析」不可） |
| `face-spaghetti` | ✗ | ✗（§0 任务形态分流表可代） | ✗ | ✓ |
| `talk-audit` | ✓ | ✗ | ✗ | 部分 |

## references 组织

- 一个主题一个文件，文件名即主题（`claims.md`、`coverage-domain.md`）。
- 有多个子文件时写一个索引（`lessons.md`），SKILL.md 只链索引。
- 新增文件后回填索引，否则等于没写。

## 提交与发版

- 一个 PR 一件事。文档 PR 不夹带会立刻失败的检查（见上文「顺序不能反」）。
- PR 描述写「为什么加」＋「写法上守了什么」，不只写改了哪几行。
- **发布验证用安装，不用解析**：`npx -y skills use kouhe3/skills@<name>` 能打印全文，才算已发布且可解析。本地 validator 通过只证明符合规范，两件事分开报。
- 版本与变更记录：暂无 CHANGELOG（待办）。装了的人目前无法知道哪天变了什么。

## 不要做

- 不要把政策写进 `description`——它在每轮对话的技能索引里，等于让每个装了它的人持续付费。
- 不要在 SKILL.md 里堆细则——细则进 `references/`。
- 不要为通过检查而伪造判据。写不出二值判据的条目，标「无判据」，不写「已检查」。

## 语言与术语

正文中文，代码/路径/命令保持原文。固定术语：**台账**、**判据**、**二值**、**停点**、**承重 claim**、**status**、**UNMEASURED**。新造词先在这节登记。