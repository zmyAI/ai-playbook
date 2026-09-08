---
name: wechat-post-html
description: >
  将 Markdown 博客文章转换为微信公众号排版兼容的 HTML。支持「极简留白」和「暖色羊皮纸」两种风格。
  触发词：公众号排版、公众号HTML、微信排版、公众号发布、wechat post format、wechat article HTML。
agent_created: true
---

# 微信公众号排版 HTML 生成

将 Markdown 博客文章转换为微信公众号后台编辑器兼容的 HTML。输出文件可在浏览器中打开，全选（Ctrl+A）后直接粘贴进公众号后台编辑器——样式即刻生效。

## 何时使用

触发场景：

- 用户提供 `.md` 文件，要求转换为公众号 HTML
- 用户说「公众号排版」「微信排版」「生成公众号HTML」「公众号发布」
- 用户想把博客文章发布到公众号，需要 HTML 格式化
- 用户引用已有的 `.md` 草稿，要求输出 `.html` 文件

## 可选风格

本技能提供两种排版风格。生成前先询问用户选择，用户未指定时默认使用**极简留白**。

### 风格一：极简留白

纯白底、零装饰。仅通过间距和字号节奏传达层级结构。适合技术文章、深度长文。

### 风格二：暖色羊皮纸

暖黄底色（#f5f4ed）、衬线字体、墨蓝标题色。阅读体验温暖沉静，适合随笔、散文、人文类内容。

灵感来源：html-anything 项目的 `doc-kami-parchment` 模板（致敬 tw93/kami）。

---

## 风格一：极简留白 — CSS 规格

### CSS 常量

| 属性 | 值 |
|------|-----|
| 页面背景 | `#fff` |
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
| 段落 | `margin:0 0 16px` |
| H2/H3 后首段 | `margin:16px 0 0` |
| 加粗 | 保留 `<strong>` 标签，不添加额外样式 |
| 引用块 | 当作普通段落处理 |
| 分割线 | 不渲染 |

### 间距规则

1. **章节之间**：H2 的 `margin-top: 36px` 自然分隔
2. **章节内部**：段落使用 `margin-bottom: 16px`
3. **下一级标题前的末段**：`margin:0 0 16px`（16px 底部 + 36px H2 顶部 ≈ 52px 视觉间隔）
4. **H2/H3 后首段**：`margin:16px 0 0`，防止与标题间距重叠
5. **H3 前的末段**：与 H2 前末段相同 —— `margin:0 0 16px`

---

## 风格二：暖色羊皮纸 — CSS 规格

### CSS 常量

| 属性 | 值 |
|------|-----|
| 页面背景 | `#f5f4ed`（暖黄羊皮纸） |
| 正文字体 | `'STSong', 'SimSun', '宋体', 'Noto Serif SC', serif` |
| 正文字号 | `16px` |
| 正文行高 | `1.85` |
| 正文颜色 | `#3d352a`（暖棕色，比纯黑柔和） |
| 标题颜色 | `#1a3a5c`（墨蓝） |
| 页面宽度 | `max-width: 680px; margin: 0 auto` |
| 页面内边距 | `32px 20px 60px` |

### 元素样式

| 元素 | 样式 |
|------|------|
| H1（文章标题） | `text-align:center; font-size:24px; font-weight:bold; color:#1a3a5c; margin:44px 0` |
| H2（章节标题） | `font-size:20px; font-weight:bold; color:#1a3a5c; margin:40px 0 0` |
| H3（小节标题） | `font-size:17px; font-weight:bold; color:#1a3a5c; margin:32px 0 0` |
| 段落 | `margin:0 0 18px` |
| H2/H3 后首段 | `margin:18px 0 0` |
| 加粗 | 保留 `<strong>` 标签，不添加额外样式 |
| 引用块 | 当作普通段落处理 |
| 分割线 | 不渲染 |

### 间距规则

1. **章节之间**：H2 的 `margin-top: 40px` 自然分隔
2. **章节内部**：段落使用 `margin-bottom: 18px`
3. **下一级标题前的末段**：`margin:0 0 18px`（18px 底部 + 40px H2 顶部 ≈ 58px 视觉间隔）
4. **H2/H3 后首段**：`margin:18px 0 0`
5. **H3 前的末段**：`margin:0 0 18px`

---

## 工作流程

### 第零步：确定排版风格

如果用户已指定风格，直接使用。否则询问用户选择「极简留白」还是「暖色羊皮纸」，用户未回复时默认使用极简留白。

### 第一步：读取源 Markdown

读取用户指定的 `.md` 文件。记录其目录路径——封面图等资源可能在同一目录。

### 第二步：将 Markdown 解析为 HTML 元素

根据选定的风格，使用对应 CSS 常量表中的样式值，将 Markdown 元素转换为内联样式的 HTML。关键规则：

**所有样式必须内联。** 微信公众号会剥离 `<style>` 标签和外部 CSS。每个元素都需要自己的 `style` 属性。

#### 极简留白 — HTML 模板

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

#### 暖色羊皮纸 — HTML 模板

**文章标题（H1）：**
```html
<h1 style="text-align:center;font-size:24px;font-weight:bold;color:#1a3a5c;margin:44px 0 44px;padding:0;">文章标题</h1>
```

**章节标题（H2）：**
```html
<h2 style="font-size:20px;font-weight:bold;color:#1a3a5c;margin:40px 0 0;padding:0;">章节标题</h2>
```

**小节标题（H3）：**
```html
<h3 style="font-size:17px;font-weight:bold;color:#1a3a5c;margin:32px 0 0;padding:0;">小节标题</h3>
```

**普通段落：**
```html
<p style="margin:0 0 18px;">段落文字。</p>
```

**H2 或 H3 后的首段：**
```html
<p style="margin:18px 0 0;">标题后的首段——注意间距不同。</p>
```

#### 两种风格通用的 HTML 元素

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

> 注意：暖色羊皮纸风格的列表 `margin-bottom` 应使用 `18px` 以匹配段落间距。

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

根据选定风格，将所有元素包裹在对应的 body 模板中：

**极简留白：**
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

**暖色羊皮纸：**
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{文章标题}</title>
</head>
<body style="max-width:680px;margin:0 auto;padding:32px 20px 60px;font-family:'STSong','SimSun','宋体','Noto Serif SC',serif;font-size:16px;line-height:1.85;color:#3d352a;background:#f5f4ed;">

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
- 不要给工具名配色（此前版本尝试过，已弃用）
- 不要添加章节分割线或水平线
- 不要添加关于图片的脚注（假定用户知晓需手动上传图片）
- 不要修改文章内容——仅应用排版格式

## 参考

- 极简留白示例：`assets/template.html`
- 暖色羊皮纸灵感：html-anything 的 `doc-kami-parchment` 模板（致敬 tw93/kami）
