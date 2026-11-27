# kouhe3/skills

我的skills，用来做冷门需求，特别是让LLM忍住不开工。

### face-spaghetti

当你遇到一个没有文档没有测试的代码库时使用。
会要求LLM先写台账（基本上是含假设的实验记录）和每条假设对应的机器判据。

### helping

当你不知道自己要什么时使用。
会让LLM思考你询问X但是实际可能需要的是Y。

### talk-audit

当你有一个不错的主意时用。
会要求LLM找出前提里的矛盾，交代证据，以减少出现[You're absolutely right!](https://absolutelyright.lol/)式奉承。

## 安装

```bash
npx skills add kouhe3/skills
```

## 依赖

本仓库自己写 skill 时依赖 [`mattpocock/skills@writing-for-agents`](https://skills.sh/mattpocock/skills/writing-for-agents)（MIT）：怎么给 agent 写文档——上下文指针的措辞、信息层级放多深、完成判据、leading words 与修剪。

它装在 `.agents/skills/writing-for-agents/`，与上游逐字节一致（不改，`npx skills update` 才不会撞哈希），版本锁在 `skills-lock.json`；不在 `skills/` 下，因为 `skills/` 只放本仓库产出的 skill。

## 规范检查

- Agent Skills specification: https://agentskills.io/specification
- 安装器/目录：https://skills.sh
- 校验：`python tools/validate_skills.py`
- 三个 skill 的 `name` 与目录名一致，`description` ≤ 1024 字符，正文 < 500 行；引用文件都在 `references/`、`scripts/` 或 `assets/` 下。

## License

MIT [`LICENSE`](LICENSE).
