---
name: 每日热点
description: 每日 9:00 从多平台获取热榜/热点内容。触发词：每日热点、热榜、今日热点、热搜。
---

# 每日热点

每日早 9:00 从多平台获取热榜，结构化输出 Top 榜。输出格式：AI 相关 > 财富/理财 > 分平台热榜。

输出到 `D:\github\zmyAI\每日热点\YYYY-MM-DD.md`。

## 覆盖平台

| 平台 | 命令 | 需登录 | 备注 |
|------|------|--------|------|
| 知乎 | `zhihu/hot` | ✅ | |
| B站 | `bilibili/popular` | ✅ | |
| 头条 | `toutiao/hot` | ❌ | |
| 36氪 | `36kr/newsflash` | ❌ | |
| 雪球 | `xueqiu/hot` | ❌ | 财富 |
| 东方财富 | `eastmoney/news` | ❌ | 财富 |
| ProductHunt | `producthunt/today` | ❌ | 技术 |
| Reddit | `reddit/hot` | ❌ | 综合 |
| 微博 | `weibo/hot` | — | 暂不获取 |
| 虎扑 | `hupu/hot` | — | 暂不获取 |
| V2EX | `v2ex/hot` | — | 暂不获取 |
| HackerNews | `hackernews/top` | — | 暂不获取 |

## 专题提取

- **AI 相关**：AI/大模型/LLM/GPT/智能体/Agent/MCP/机器人/Anthropic/OpenAI
- **财富/理财**：A股/港股/美股/基金/黄金/比特币/IPO/融资/央行/股票/行情

## 已排除（无热榜）

GitHub、StackOverflow、CSDN、博客园、Dev.to 仅有搜索功能，无热榜。
东方财富仅有 news/stock 单条，无聚合热榜。
Yahoo Finance 仅有单股 quote。

## 定时任务

Windows 任务计划程序，每日 9:00 触发。
