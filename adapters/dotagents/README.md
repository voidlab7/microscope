# 安装到 .agents Protocol

## 方法

```bash
# 1. 创建目录
mkdir -p .agents/agents/microscope .agents/skills

# 2. 复制 Agent 定义
cp MicroScope/agent/AGENT.md .agents/agents/microscope/agent.md

# 3. 复制技能
cp MicroScope/skills/*.md .agents/skills/

# 4. 复制记忆
cp MicroScope/memory/*.md .agents/memories/
```

## 注意事项

- .agents Protocol 要求 agent.md 使用 frontmatter 格式
- skills 目录下每个文件是一个独立技能
- memories 目录会跨会话保留
