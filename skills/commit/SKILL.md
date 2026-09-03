---
name: commit
description: 按用户 Git 规范执行提交。触发词：提交、commit、暂存、提交修改、提交并推送、推送。无论用户说什么（"先给消息"、"提交并推送"、"commit"），都必须完整执行 skill 流程：status → add → diff --staged → 基于变更写消息 → 用户确认 → commit。禁止跳过 diff 直接编消息。支持 /commit <filepath> 快速提交
---

# commit

用户专用的 Git 提交流程技能。封装了 Windows 下的 Git 提交流程和约定的提交规范。

## ⚡ 快捷入口模式

`/commit` 省打字，**流程不变**。按参数情况自动判断：

- **`/commit <filepath>`**（如 `/commit README.md`）→ 文件路径已预填，提交指定文件
- **`/commit <repo-path>`**（如 `/commit zmyAI/ai-playbook`）→ 路径指向 Git 仓库根目录，提交该仓库
- **`/commit`（无参数）** → 根据当前对话上下文推断提交范围（如最近修改的文件、当前正在讨论的变更等）

区别仅在于：范围已预填或已推断，无需再问"提交哪个文件/仓库"。

## 核心流程

### 1. 接收指令（必须明确范围）

**只提交用户明确提到的文件或范围。** 不能把暂存区或其他未提及的修改一并提交。

- `/commit <filepath>` → 提交指定文件，直接进入预检
- `/commit <repo-path>` → 提交指定仓库，直接进入预检
- `/commit` → 根据上下文推断范围，推断后展示给用户确认
- 用户说"暂存这些文件"或"提交 xx 修改"→ 按文件操作
- 用户说"提交暂存区修改"或"提交 xx 仓库"→ 先判断是否可拆分为多个独立提交；如认为应该拆分，主动询问

### 2. 预检（不可跳过）

```bash
git status
```

- 检查工作区是否有未暂存修改（modified but not staged）
- 检查是否有未跟踪文件（untracked files）
- **如果有未暂存修改**：对每个文件执行 `git diff <file>` 对比暂存区与工作区版本
- 如发现有用户手动修改后未暂存的内容，提示用户确认是否纳入本次提交
- **避免 Agent 上次写入后又手动编辑的修改被遗漏**

### 3. 暂存

按用户明确提到的文件执行暂存：

```bash
git add <file1> <file2> ...
```

或用户说"全部提交"时：

```bash
git add -A
```

### 4. 确认变更

```bash
git diff --staged
```

查看实际要提交的变更内容，**基于实际变更编写提交信息**。

### 5. 编写提交信息

基于 `git diff --staged` 的实际变更内容编写。

**格式要求：**
- 纯中文（除非英文项目）
- 动词+内容格式，简洁明了
- 不包含引号

**Windows 提交命令（禁止用 `-m "..."`，也禁止用 `echo/printf | git commit -F -` 提交中文消息）：**

Windows shell 下 `-m "消息"` 会保留双引号到提交信息中；Git Bash/Windows 管道提交中文消息可能产生非 UTF-8 乱码。**必须先将提交信息写入 UTF-8 文件**，再执行：

```bash
git commit -F D:\github\tmp\commit_msg.txt
```

如需修复上一条提交信息，同样先写入 UTF-8 文件，再执行：

```bash
git commit --amend -F D:\github\tmp\commit_msg.txt
```

提交后、推送前必须检查提交标题：

```bash
git log -1 --pretty=%s
```

确认标题无乱码后，才允许 push。

**首次提交固定为：** `Initial commit`

### 6. 用户确认（必须）

向用户展示提交信息文本，**获得明确确认后再执行 `git commit`**。不能直接 commit。

### 7. 提交后

- **不要自动推送（push）**，除非用户明确说"提交并推送"或"push"
- 默认仅 commit，不 push

## 提交流程速查

```
user 说"提交 xx"或其他提交指令
  ↓
git status          ← 检查整体状态
  ↓
检查未暂存修改       ← 对每个 modified 文件 git diff <file>
  ↓
git add <files>     ← 严格按用户提到的文件
  ↓
git diff --staged   ← 确认实际变更
  ↓
编写提交信息         ← 基于实际变更，纯中文，动词+内容
  ↓
展示给用户确认       ← 必须等待用户批准
  ↓
git commit -F D:\github\tmp\commit_msg.txt   ← 使用 UTF-8 文件，禁止中文消息走 echo/printf 管道
  ↓
git log -1 --pretty=%s              ← 推送前检查标题无乱码
  ↓
完成（不自动 push）
```

## 分支命名

新建 Git 仓库时，主分支统一使用 `main`，不使用 `master`。

## 参考

本技能约束源自 `git-conventions.md` 和 `general-conventions.md` 中的提交规范。
