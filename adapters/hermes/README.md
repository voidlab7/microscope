# 安装到 Hermes

## 方法

Hermes Agent 框架使用分层架构，MicroScope 映射到其协调层和执行层：

```bash
# 1. 创建 Hermes Agent 目录
mkdir -p .hermes/agents/microscope

# 2. 复制核心定义
cp MicroScope/agent/AGENT.md .hermes/agents/microscope.md

# 3. 复制技能作为 Hermes 的 tools
cp MicroScope/skills/*.md .hermes/tools/

# 4. 复制提示词模板
cp MicroScope/prompts/*.md .hermes/prompts/
```

## Hermes 7 层映射

| Hermes 层 | MicroScope 对应 |
|-----------|----------------|
| 入口层 | 触发词："市场分析"、"帮我分析" |
| 治理层 | 三条铁律 + 数据标注规范 |
| 协调层 | 四步流水线（解析 → 联网 → 验证 → 输出） |
| 控制层 | 三档模式（Quick / Standard / Deep） |
| 执行层 | 8 个 Skills（PDF/Excel/图片/网络/企业/分析/验证/报告） |
| 状态层 | memory/ 跨会话记忆 |
| 学习层 | memory/lessons.md 经验积累 |

## 注意事项

- Hermes 的分层架构和 MicroScope 的设计高度吻合
- MicroScope 的 `skills/` 对应 Hermes 的 `tools/`
- MicroScope 的 `memory/` 对应 Hermes 的状态层 + 学习层
- 交叉验证逻辑在 Hermes 中可注册为执行层的 validator
