# 安装到 Claude Code

## 方法

Claude Code 使用项目根目录的 `CLAUDE.md` 作为系统指令：

```bash
# 方法 1：MicroScope 作为唯一 Agent
cp MicroScope/agent/AGENT.md CLAUDE.md

# 方法 2：追加到已有 CLAUDE.md（推荐）
echo "" >> CLAUDE.md
echo "---" >> CLAUDE.md
echo "" >> CLAUDE.md
cat MicroScope/agent/AGENT.md >> CLAUDE.md
```

技能和提示词作为项目文件，Claude Code 会自动读取：

```bash
# 可选：复制技能文件到项目根目录供 Claude Code 引用
cp -r MicroScope/skills/ .microscope-skills/
cp -r MicroScope/prompts/ .microscope-prompts/
cp -r MicroScope/templates/ .microscope-templates/
```

## 使用

在 Claude Code 中直接说：

```
帮我分析 AI 眼镜市场
```

Claude Code 会读取 CLAUDE.md 中的 MicroScope 人设和工作流，自动执行四步流水线。

## 注意事项

- Claude Code 的 `CLAUDE.md` 相当于 CodeBuddy 的 SKILL.md
- 技能文件放在项目内，Claude Code 可以通过 `read_file` 按需读取
- 记忆文件建议放在 `MicroScope/memory/` 下，Claude Code 支持跨会话读取
- Claude Code 原生支持 `web_search` 和 `web_fetch`，网络调研能力完整可用
