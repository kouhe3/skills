# kouhe3/skills

三个 Agent Skill：**更好地帮助**（`helping`）、**面临屎山**（`face-spaghetti`）、**talk-audit**。

## 安装

推送到 GitHub 后：

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

## 结构

```
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
- Directory: https://skills.sh
- 校验：`python tools/validate_skills.py`
- 三个 skill 的 `name` 与目录名一致，`description` ≤ 1024 字符，正文 < 500 行；引用文件都在 `references/`、`scripts/` 或 `assets/` 下。

## 调用

三个 skill 都是 model-invoked：description 负责发现，名字也可以手动调用。`talk-audit` 如果要严格手动-only，在本地 frontmatter 加 `disable-model-invocation: true`（这是 Claude Code 引入、omp 也支持的扩展字段，不在 Agent Skills 规范里）。

## License

尚未选择 License；发布前加 `LICENSE`。