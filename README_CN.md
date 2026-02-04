# Context Summarizer 技能

自动生成对话上下文摘要，实现无缝会话连续性。

## 功能特点

当你在使用AI助手进行编程时，这个技能可以：
- 📝 **生成摘要**：自动总结当前会话的上下文
- 💾 **保存上下文**：将摘要保存到本地文件
- 🔄 **会话恢复**：下次开始新会话时可以快速恢复
- ⚡ **自动检测**：当token使用率超过80%时提醒你

## 安装

```bash
npx skills add panglihaoshuai/context-summarizer-skill
```

## 使用方法

### 方式1：手动触发
直接对AI助手说：
- "总结一下"
- "生成摘要"
- "保存上下文"
- "会话总结"

### 方式2：自动检测
系统会自动监控token使用率：
- 当超过80%时，会提示你是否需要生成摘要
- 你可以选择继续工作或先生成摘要

## 输出内容

生成的摘要包含以下部分：

| 部分 | 内容 |
|------|------|
| **项目状态** | 当前阶段、完成进度、待办任务 |
| **技术决策** | 已确认的决策、备选方案、理由 |
| **代码上下文** | 当前文件、最近更改、架构模式 |
| **对话历史** | 关键讨论、已确认事项、待确认事项 |
| **恢复指南** | 下一步工作、关键上下文 |

## 输出格式

支持两种格式：
1. **人可读格式**（`.md`）- 方便阅读
2. **机器可读格式**（`.json`）- 方便程序处理

保存位置：
- `./session_summary.md` - 人类阅读
- `./session_summary.json` - 机器处理

## 开发者说明

如果你想自定义这个技能：

```bash
# 克隆仓库
git clone https://github.com/panglihaoshuai/context-summarizer-skill.git

# 编辑核心脚本
cd context-summarizer-skill
vim scripts/generate_summary.py
```

### 自定义选项

在 `scripts/generate_summary.py` 中可以修改：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `max_words` | 2000 | 摘要最大字数 |
| `token_threshold` | 0.8 | 自动触发阈值(80%) |
| `include_sections` | 全部 | 要包含的章节 |

## 适用场景

✅ **推荐使用**：
- 复杂项目的会话总结
- 长时间编码会话的上下文保存
- 切换任务前的工作记录
- 每日工作总结

❌ **不必要使用**：
- 简单的一次性问题
- 开头几句话的对话
- 纯阅读/查询类任务

## 文件结构

```
context-summarizer-skill/
├── SKILL.md              # OpenCode技能定义文件
├── README.md             # 英文版说明
├── README_CN.md          # 中文版说明（本文）
├── .gitignore            # Git忽略文件
└── scripts/
    └── generate_summary.py  # 核心生成脚本（~600行）
```

## 快速开始

```bash
# 1. 安装技能
npx skills add panglihaoshuai/context-summarizer-skill

# 2. 在对话中说"总结一下"

# 3. 查看生成的摘要
cat session_summary.md
```

## 注意事项

1. 这个技能生成的是**对话摘要**，不是项目文档
2. 建议在**重要节点**生成摘要（如完成一个功能、发现关键问题等）
3. 生成的摘要保存在**当前目录**，请及时备份
4. 建议每30-60分钟生成一次摘要，避免丢失重要上下文

## 许可证

MIT - 免费使用，欢迎贡献！
