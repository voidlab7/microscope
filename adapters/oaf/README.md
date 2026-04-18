# 安装为 OAF (Open Agent Format)

## 方法

OAF 只需要一个 AGENTS.md 文件：

```bash
# 将 AGENT.md 复制为 OAF 格式的 AGENTS.md
cp MicroScope/agent/AGENT.md my-vendor/microscope/AGENTS.md
```

## 注意事项

- OAF 的 AGENTS.md 是唯一必需文件
- frontmatter 需要包含 vendorKey/agentKey/version 等 OAF 特有字段
- skills/ 目录可选，OAF 支持直接引用
