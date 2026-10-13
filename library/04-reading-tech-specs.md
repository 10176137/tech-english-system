# 英文技术需求与 PRD 精读指南 (Reading Tech Specs & Jira Tickets)

> 为什么工程师读英文文档会累？不是单词难，而是**长难句嵌套、商业逻辑边界（Edge Cases）和 RFC 2119 约束词**。

---

## 1. 敏捷开发核心需求语法：Gherkin 规范 (Given-When-Then)

海外团队的 Jira Ticket / User Story 90% 都遵循这个结构：

* **User Story 格式**：
  * *“As a [role], I want to [action], so that [business value].”*  
    （作为[角色]，我想要[做某事]，以便于[实现商业价值]。）
* **Acceptance Criteria (验收标准 - AC)**：
  * **Given** [前置条件 / 初始状态]
  * **When** [触发动作 / API 请求]
  * **Then** [预期结果 / 状态变更]
  * **And / But** [额外约束 / 异常分支]

---

## 2. 必须分清的“法律级约束动词” (RFC 2119 规范)

在海外 PRD 和技术规范中，动词的轻重缓急有严格界限：

| 词汇 | 实际技术含义 | 工程师应对策略 |
| :--- | :--- | :--- |
| **MUST / REQUIRED / SHALL** | **绝对强制**（必须实现） | 不做就属于严重 Bug，无法上线 |
| **MUST NOT / SHALL NOT** | **绝对禁止**（严禁发生） | 必须有防御性代码或报错拦截 |
| **SHOULD / RECOMMENDED** | **强烈推荐**（应做尽做） | 除非有极充分理由，否则必须实现 |
| **SHOULD NOT / NOT RECOMMENDED** | **不建议** | 尽量避免，存在已知隐患 |
| **MAY / OPTIONAL** | **可选** | 根据排期和复杂度自主决定是否交付 |

---

## 3. 需求文档中的“边界高频黑话” (Edge Case Vocabulary)

* `subject to [condition]`：受制于…… / 取决于……条件
* `fall back to [default]`：回退到默认值 / 降级处理
* `out-of-band`：带外异步处理（非主流程阻塞）
* `rate-limiting kicks in`：限流生效 / 被触发
* `graceful degradation`：优雅降级
* `edge case mitigation`：极端边界情况缓解
* `retroactive update`：追溯更新（历史数据刷洗）
