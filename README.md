# AI Playbook

AI Playbook 是一个用于管理和组织 AI 相关资源的项目，包括提示词、技能集和文档。

## 项目结构

```
ai-playbook/
├── prompts/        # 提示词集合
├── skills/         # 技能集（29 个目录 + 13 个独立参考文档）
└── claude/         # Claude Code 全局配置
```

## 目录说明

### prompts/
存放各种 AI 提示词，按功能或场景分类。

### skills/
存放技能文件，用于扩展 AI 的能力。详见 [skills/README.md](skills/README.md)。

### claude/
存放 Claude Code 全局配置（CLAUDE.md）。

## 使用方法

1. **提示词使用**：从 prompts 目录中选择适合的提示词，复制到 AI 对话中使用。

2. **技能安装**：将希望安装的技能路径告诉 AI Agent，它会自动识别运行环境并安装到正确位置。

3. **文档参考**：查阅 claude 目录中的全局配置。

## 贡献

欢迎贡献新的提示词、技能和文档。请按照项目结构组织内容，并确保内容质量和实用性。

## 许可证

本项目采用 MIT 许可证。
