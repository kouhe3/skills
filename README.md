# kouhe3/skills

仓库：https://github.com/kouhe3/skills

三个 Agent Skill：**更好地帮助**（`helping`）、**面临屎山**（`face-spaghetti`）、**talk-audit**。

## 安装

```bash
npx skills add kouhe3/skills
```

手动安装：把 `skills/<name>/` 复制到 agent 的 skills 目录，例如 `~/.claude/skills/`、`.agents/skills/` 或 `~/.omp/agent/skills/`。

## Skills

| Skill | 做什么 | 什么时候用 |
| --- | --- | --- |
| `helping` | Schein 式帮助：先问后答，一轮一个动作；`references/review.md` 是复盘 rubric。 | 用户求助、卡住、或你准备给未被请求的建议时。 |
| `face-spaghetti` | 屎山代码的开工闸门：先判能否开工，再按 claim → probe → 台账 建二值判据；`references/` 与 `scripts/` 是取证库。 | 遗留代码、反编译产物、无文档 SDK，或写不出验收标准时。 |
| `talk-audit` | 把想法拆成 claim，选操作、要证据、标 status；默认 talk 页，不判决；`references/class-trial.md` 是可选判决模式。 | 用户明确要压力测试一个想法/方案/判断、找隐藏假设、或反对奉承式“好主意”时。 |

## Before / After

一句话：**Before 是一次许愿，After 是一轮一个动作。** After 并不是更啰嗦——它把「谁承担判断」摆回原位。示例为示意，不是真实对话记录。

### `helping`

> 用户：「我不知道还该不该继续待在这个项目里。」

**Before**
```
AI：可以从三个角度看：1) 职业发展 2) 团队氛围 3) 你的兴趣和长期目标。
建议各打一分，再按权重排序。希望对你有帮助。
```

**After**（第 1 轮只做一件事）
```
AI：在我给建议之前想先确认：你现在最需要的是有人听你说、一起想，
还是一个具体方案？
```

> 用户：「想理清楚。」第 2 轮仍然是问讯，不给方案：
```
AI：能给我一个具体例子吗——最近哪件事让你开始这么想的？
```

差别不在语气，在**停点**。Before 一轮就结束了；After 每轮停在一个可观察的信号上——对方给出了具体例子、或者开始自己分析。

### `face-spaghetti`

> 用户：「这是从 exe 反编译出来的，帮我把这个函数补完。」

**Before**
```
AI：我先看看入口在哪……（打开 IDA，开始改代码）
三小时后：判据写不出来，改动的对错无法验证。
```

**After**
```
AI：形态判定：反编译产物 → 来源不可信，走闸门。
判定：改造后做（关键前提未证——这个函数是否真的被调用）。
第一个动作不是改代码，是台账落一行：
  待证 | 假设：该函数由 0x401000 的调用点进入
       | 互斥预测：若为死代码，则交叉引用数为 0
       | 判据：xref = 0 → 判死代码，进垃圾桶
先跑这个探针，再谈实现。
```

差别不在速度，在**第一条动作是记录而不是编辑**。Before 把「不知道」留在了脑子里，所以永远无法判断改对没改对。

### `talk-audit`

> 用户：「我想把整个站点换成静态生成器，你觉得呢？」

**Before**
```
AI：好主意！静态站更快、更省、更安全。建议先用 Astro 试一版，
我可以直接帮你搭起来。
```

**After**
```
AI：先拆 claim，标出承重的那条：
C1 静态生成更快      —— 事实，可测
C2 现有用户不需要发帖 —— 假设（承重）
C3 迁移成本低于维护成本 —— 事实，但要算
承重的是 C2，而它是假设。你要对这条做什么：赞同 / 质疑 / 重构 / 标未知？
```

> 用户：「质疑。」
```
AI：那先定一个廉价测试：统计近 90 天有发帖行为的用户占比。
低于 5%，才轮得到谈 C2 成立。
```

差别不在是否给建议，在**建议被挂在哪条 claim 上**。Before 的「好主意」没有可证伪的接口，所以对方只能选择信或不信。

三个 After 有同一个形状：**先把不知道的东西写出来，再往下走。**

## 结构

```
README.md
LICENSE
skills/
  helping/
    SKILL.md
    references/review.md
  face-spaghetti/
    SKILL.md
    agents/openai.yaml
    references/...
    scripts/...
  talk-audit/
    SKILL.md
    references/class-trial.md
    references/design-notes.md
tools/validate_skills.py
```

每个 skill 的 `SKILL.md` 是入口；`references/` 和 `scripts/` 按需加载。

## 规范

- Agent Skills specification: https://agentskills.io/specification
- 安装器/目录：https://skills.sh
- 校验：`python tools/validate_skills.py`
- 三个 skill 的 `name` 与目录名一致，`description` ≤ 1024 字符，正文 < 500 行；引用文件都在 `references/`、`scripts/` 或 `assets/` 下。

## 调用

三个 skill 都是 model-invoked：description 负责发现，名字也可以手动调用。`talk-audit` 如果要严格手动-only，在本地 frontmatter 加 `disable-model-invocation: true`（这是 Claude Code 引入、omp 也支持的扩展字段，不在 Agent Skills 规范里）。

## License

MIT. See [`LICENSE`](LICENSE).