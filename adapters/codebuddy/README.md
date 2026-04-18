# 安装到 CodeBuddy

## 方法

将 MicroScope 安装为 CodeBuddy Skill：

```bash
# 1. 创建 skill 目录
mkdir -p .codebuddy/skills/microscope/references .codebuddy/skills/microscope/assets

# 2. 复制核心文件
cp MicroScope/agent/AGENT.md .codebuddy/skills/microscope/SKILL.md

# 3. 复制提示词为参考文档
cp MicroScope/prompts/*.md .codebuddy/skills/microscope/references/

# 4. 复制模板为资源文件
cp MicroScope/templates/*.md .codebuddy/skills/microscope/assets/

# 5. 复制技能文件
cp MicroScope/skills/*.md .codebuddy/skills/microscope/references/
```

## 注意事项

- AGENT.md 的 frontmatter 中 `name` 字段会被 CodeBuddy 用作触发名
- CodeBuddy 会自动加载 `references/` 和 `assets/` 下的文件
- 技能文件在 CodeBuddy 中作为参考文档使用（CodeBuddy 没有独立的 skill 子调用机制）
