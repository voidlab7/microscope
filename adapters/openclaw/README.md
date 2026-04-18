# 安装到 OpenClaw

## 方法

将 MicroScope 的人设和工作流写入 OpenClaw 工作区配置：

```bash
# 1. 将 AGENT.md 的人设部分写入 SOUL.md（合并到已有内容后面）
cat MicroScope/agent/AGENT.md >> SOUL.md

# 2. 将技能和流程写入 AGENTS.md
echo "## MicroScope 市场调研" >> AGENTS.md
cat MicroScope/skills/*.md >> AGENTS.md
```

## 注意事项

- OpenClaw 用 SOUL.md 管人设，AGENTS.md 管操作手册
- 技能在 OpenClaw 中会被自动学习，不需要独立文件
- MEMORY.md 对应 MicroScope 的 memory/lessons.md
