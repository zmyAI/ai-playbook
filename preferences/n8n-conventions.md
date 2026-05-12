# n8n 约束规范

## 环境配置

| 配置项 | 值 |
|-------|-----|
| 启动方式 | WSL 运行 `wsl npx n8n` |
| 全局启动命令 | PowerShell 中定义 `n8n` 函数（见 `C:\Users\zmy\Documents\PowerShell\Microsoft.PowerShell_profile.ps1`） |
| 数据目录 | `$env:N8N_USER_FOLDER = "C:\Users\zmy\.n8n"`（映射到 Windows 路径） |
| 默认端口 | http://localhost:5678 |
| 版本 | n8n v1.119.1 |

---

## 修改工作流前必读

### ⚠️ 硬性规则：修改 n8n 工作流 JSON 前，必须先调用 `use_skill` 加载技能

**触发条件**：任何涉及修改 `D:\gitlab\xintg-test\n8n-test` 目录下工作流 JSON 的任务

**正确流程**：
1. 判断需要修改的节点类型
2. 调用 `use_skill("n8n-node-configuration")` 确认该节点类型的字段格式
3. 如有可工作的同类工作流，先读取对比差异
4. 针对性修改，避免盲改

### ⚠️ 优先参考现有工作流

- 若有可工作的同类工作流，**先读取对比差异后再修改**
- 避免"先改完再说"的低效模式
- 遇到不确定的配置，先问用户要参考示例

---

*记录于 2026-05-07，教训：修改 form-urlencoded 配置时未查文档导致多次返工*
