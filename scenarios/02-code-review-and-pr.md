# Code Review 与 PR 异步博弈剧本 (Code Review & PR)

> 海外工程文化原则：**对代码严苛，对人温和。** 善用疑问句（Hedging），避免粗暴使用祈使句（Don't command, suggest）。

---

## 1. 提交 Review 意见的 4 级语气模板

### Level 1: 微小细节 (Nitpick - 可以不改，仅供参考)
* *“Nit: Could we rename this variable to `orderCount` for better readability?”*  
  （小细节：我们能不能把这个变量改成 `orderCount`，可读性更好些？）

### Level 2: 提出疑虑与隐患 (Concern / Suggestion)
* *“I'm a bit concerned about race conditions here under high concurrency. What if two requests arrive simultaneously?”*  
  （我有点担心高并发下的竞态问题。如果两个请求同时到达会怎么样？）
* *“Have we considered how this behaves when the downstream API times out?”*  
  （我们考虑过当下游 API 超时时这里会怎么表现吗？）

### Level 3: 必须阻断合并的问题 (Blocking Issue)
* *“I think this might break backward compatibility for existing mobile clients. We should probably version the endpoint first.”*  
  （我觉得这可能会破坏现有移动端客户端的向后兼容性。我们可能应该先给接口加版本号。）

### Level 4: 赞美与放行 (Appreciation & Approval)
* *“Clean solution! LGTM (Looks good to me).”*（代码写得真干净！没问题已过。）
* *“Good catch! Merging now.”*（抓虫抓得漂亮！这就合并。）

---

## 2. 回复他人的 Review 意见 (Responding to Reviews)

* **采纳并修改**：
  * *“Good point! Updated in the latest commit.”*（说得在理！最新提交已更新。）
  * *“Address in `b2f4c1`. Thanks for spotting that!”*（已在 commit 中修改，多谢指出！）
* **委婉解释并保留自己方案**：
  * *“I thought about that approach, but I went with this one because we need to keep latency under 50ms. Happy to discuss if you feel strongly about it.”*  
    （我也考虑过那个方案，但最终选这个是因为我们需要保证延迟在 50ms 以内。如果你觉得很有必要改，我们可以进一步讨论。）
