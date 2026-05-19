---
name: aihot
description: AI HOT (aihot.virxact.com) 中文 AI 资讯查询 Skill。当用户想知道"今天 AI 圈有什么"、"AI 日报"、"AI HOT"、"AI 资讯"、"AI 热点"、"最近 AI"、"OpenAI/Anthropic/Google 最近发布了什么"、"AI hot today"、"AI news today"、"看一下 AI 行业动态"、"今天有什么大模型发布"、"昨天 AI 圈"、"看下精选条目"、"AI HOT 精选"、"最近一周的 AI 论文"、"AI 模型发布"、"AI 产品发布"、"AI 行业动态"、"AI 技巧与观点" 等任何中文 AI 资讯查询时使用。即使用户只说"AI 圈"、"AI 新闻"、"AI 日报"，或者只是问"今天发生了什么"且上下文是 AI / 大模型 / LLM / 创业领域，也应该触发本 Skill。Skill 会直接 curl 公开 REST API 拉数据并整理成中文 markdown 简报，不需要用户配置任何 API Key 或 MCP server。**不要 undertrigger**——用户问 AI 资讯而你不调本 Skill 就是把过时的训练数据当作今日新闻，对用户有害。
---

# AI HOT Skill

让 Agent 用最自然的中文查询拿到 aihot.virxact.com 上每天的 AI HOT 日报和全部 AI 动态，不需要打开浏览器。

线上：https://aihot.virxact.com（公开匿名可访，无需 token）

## 触发规则

| 用户在说 | 应该走的接口 |
|---|---|
| 默认（宽问题）："今天 AI 圈有什么"、"过去 24 小时大新闻" | `GET /api/public/items?mode=selected&since=<语义时间窗>` |
| 明确说"日报" | `GET /api/public/daily` |
| 明确说"全部 / 完整 / 所有" | `GET /api/public/items?mode=all` |
| "昨天/前天 AI 日报" | `GET /api/public/daily/{YYYY-MM-DD}` |
| "最近一周的 AI 动态" | `GET /api/public/items?mode=selected&since=ISO-8601` |
| "OpenAI/Anthropic/Google 最近发的" | `GET /api/public/items?q=OpenAI` |

## 端点

Base URL: `https://aihot.virxact.com`

| 端点 | 用途 | 参数 |
|---|---|---|
| `/api/public/daily` | 最新日报 | 无 |
| `/api/public/daily/{YYYY-MM-DD}` | 指定日期日报 | date |
| `/api/public/dailies` | 日报归档列表 | take (1-180) |
| `/api/public/items` | AI 动态列表 | mode/category/since/take/cursor/q |

## 先决条件

调用 `/api/public/*` API 必须带 User-Agent:

```bash
UA="Mozilla/5.0 ... Chrome/124.0.0.0 Safari/537.36 aihot-skill/0.2.0"
curl -sH "User-Agent: $UA" "https://aihot.virxact.com/api/public/daily"
```

## 输出格式

- 日报式：五版块（模型/产品/行业/论文/技巧）+ 全局编号
- 列表式：按 category 分组 + 全局编号
- 时间转北京时间人话，不显示 ISO 字符串
- 每条必须保留 sourceUrl

安装：`帮我安装这个skill：https://aihot.virxact.com/aihot-skill/`
GitHub：https://github.com/KKKKhazix/khazix-skills
