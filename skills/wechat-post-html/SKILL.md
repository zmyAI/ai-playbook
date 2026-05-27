---
name: wechat-post-html
description: >
  将 Markdown 博客文章转换为微信公众号排版兼容的 HTML，采用「极简大留白」风格——纯间距和字号节奏，零装饰元素。
  触发词：公众号排版、公众号HTML、微信排版、公众号发布、wechat post format、wechat article HTML。
agent_created: true
---

# 微信公众号排版 HTML 生成

将 Markdown 博客文章转换为微信公众号后台编辑器兼容的 HTML，采用极简风格排版。输出文件可在浏览器中打开，全选（Ctrl+A）后直接粘贴进公众号后台编辑器——样式即刻生效。

## 何时使用

触发场景：

- 用户提供 `.md` 文件，要求转换为公众号 HTML
- 用户说「公众号排版」「微信排版」「生成公众号HTML」「公众号发布」
- 用户想把博客文章发布到公众号，需要 HTML 格式化
- 用户引用已有的 `.md` 草稿，要求输出 `.html` 文件

## 排版风格：极简大留白

零装饰元素。仅通过间距和字号节奏传达层级结构。

### CSS 常量

| 属性 | 值 |
|------|-----|
| 正文字体 | `'Microsoft YaHei', '微软雅黑', sans-serif` |
| 正文字号 | `15px` |
| 正文行高 | `1.75` |
| 正文颜色 | `#3a3a3a`（深灰） |
| 标题颜色 | `#1a1a1a`（近黑） |
| 页面宽度 | `max-width: 680px; margin: 0 auto` |
| 页面内边距 | `24px 16px 60px` |

### 元素样式

| 元素 | 样式 |
|------|------|
| H1（文章标题） | `text-align:center; font-size:22px; font-weight:bold; color:#1a1a1a; margin:40px 0` |
| H2（章节标题） | `font-size:18px; font-weight:bold; color:#1a1a1a; margin:36px 0 0` |
| H3（小节标题） | `font-size:16px; font-weight:bold; color:#1a1a1a; margin:28px 0 0` |
| 段落 | `margin:0 0 16px`（末段需根据后续元素调整 margin） |
| H2/H3 后首段 | `margin:16px 0 0`（避免与标题底部间距叠加） |
| 加粗 | 保留 `<strong>` 标签，不添加额外样式 |
| 引用块 | 不设特殊样式——当作普通段落处理。极简风格避免装饰元素 |
| 分割线 | 不渲染——仅用间距分隔章节 |

### 间距规则

1. **章节之间**：H2 的 `margin-top: 36px` 自然分隔
2. **章节内部**：段落使用 `margin-bottom: 16px`
3. **下一级标题前的末段**：使用 `margin:0 0 16px`，16px 底部间距 + 36px H2 顶部间距 ≈ 52px 视觉间隔
4. **H2/H3 后首段**：必须使用 `margin:16px 0 0`，防止与标题间距重叠
5. **H3 前的末段**：与 H2 前末段相同 —— `margin:0 0 16px`

## 工作流程

### 第一步：读取源 Markdown

读取用户指定的 `.md` 文件。记录其目录路径——封面图等资源可能在同一目录。

### 第二步：将 Markdown 解析为 HTML 元素

将 Markdown 元素转换为内联样式的 HTML。关键规则：

**所有样式必须内联。** 微信公众号会剥离 `<style>` 标签和外部 CSS。每个元素都需要自己的 `style` 属性。

**文章标题（H1）：**
```html
<h1 style="text-align:center;font-size:22px;font-weight:bold;color:#1a1a1a;margin:40px 0 40px;padding:0;">文章标题</h1>
```

**章节标题（H2）：**
```html
<h2 style="font-size:18px;font-weight:bold;color:#1a1a1a;margin:36px 0 0;padding:0;">章节标题</h2>
```

**小节标题（H3）：**
```html
<h3 style="font-size:16px;font-weight:bold;color:#1a1a1a;margin:28px 0 0;padding:0;">小节标题</h3>
```

**普通段落：**
```html
<p style="margin:0 0 16px;">段落文字。</p>
```

**H2 或 H3 后的首段：**
```html
<p style="margin:16px 0 0;">标题后的首段——注意间距不同。</p>
```

**加粗文字：**
```html
<strong>加粗文字</strong>
```

**引用块（MD 中的 `>`）：**
当作普通段落处理——不添加装饰元素。使用标准 `<p>` 标签。

**无序列表：**
```html
<ul style="margin:0 0 16px;padding-left:24px;">
<li style="margin:0 0 8px;">列表项</li>
</ul>
```

**有序列表：**
```html
<ol style="margin:0 0 16px;padding-left:24px;">
<li style="margin:0 0 8px;">列表项</li>
</ol>
```

### 第三步：处理图片

将所有 `![](url)` 和 `![alt](url)` Markdown 图片语法替换为占位文本：

```html
<p style="text-align:center;color:#999;font-size:14px;margin:0 0 36px;">[封面图：图片占位]</p>
```

对于正文插图（非封面），使用：
```html
<p style="text-align:center;color:#999;font-size:14px;margin:16px 0;">[图片：{替换文字或描述}]</p>
```

封面图占位紧跟在 H1 标题之后。

### 第四步：中英文间添加空格

在中文与英文/拉丁字符之间插入空格。遵循中文排版规范。

示例：`使用TRAE写代码` → `使用 TRAE 写代码`

### 第五步：组装完整 HTML

将所有元素包裹在 body 模板中：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{文章标题}</title>
</head>
<body style="max-width:680px;margin:0 auto;padding:24px 16px 60px;font-family:'Microsoft YaHei','微软雅黑',sans-serif;font-size:15px;line-height:1.75;color:#3a3a3a;background:#fff;">

<!-- 所有解析后的内容放这里 -->

</body>
</html>
```

### 第六步：写入文件

输出文件命名：`公众号版-{文章标题}.html`

默认输出目录：源 `.md` 文件所在目录的同级 `html/` 目录。
如用户指定了其他路径，使用用户指定的路径。

### 第七步：预览

写入文件后，使用 `preview_url` 在浏览器中打开，供用户在复制到公众号前验证效果。

## 重要约束

### 微信公众号 HTML 限制

- **禁止 `<style>` 标签** —— 公众号会完全剥离
- **禁止 `class` 属性** —— 只使用内联 `style`
- **禁止 `flex` 或 `grid` 布局** —— 公众号编辑器不支持
- **禁止 `@font-face` 自定义字体**
- **禁止外部 CSS 链接**
- **禁止 JavaScript** —— `<script>` 标签会被剥离
- **禁止复杂嵌套 div** —— 保持扁平结构，仅用 `<p>`、`<h1>`-`<h3>`、`<ul>`、`<ol>`

### 不应做的事

- 不要添加装饰元素（彩色边框、背景色、图标、emoji 项目符号）
- 不要给工具名配色（方案A 已被否决，选用方案C）
- 不要添加章节分割线或水平线
- 不要添加关于图片的脚注（方案C 假定用户知晓需手动上传图片）
- 不要修改文章内容——仅应用排版格式

## 参考

完整输出格式示例见 `assets/template.html`。
