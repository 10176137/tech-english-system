# 教程 01：英文技术需求与长难句“解剖法” (Sentence Anatomy for Tech Specs)

> **核心认知**：靠专业关键词（如 timeout、idempotent）去“猜”语义不叫阅读理解，那叫“关键词匹配”。一旦业务逻辑变复杂，猜就会彻底失效。必须掌握反编译式的“句子解剖法”。

---

## 一、 为什么工程师读英文需求容易晕？

英文 PRD 和 Jira 需求通常有大量**介词短语前置**、**多重后置定语**和**从句嵌套**。如果从第一个词硬读到最后一个词，大脑的“工作内存”很容易发生溢出（Memory Overflow）。

---

## 二、 句子解剖三步法 (The 3-Step Parsing Method)

我们拿真实的生产级需求长难句来做解剖：

> *"In the event of a downstream database timeout, the service SHOULD NOT fail the transaction immediately; instead, it MUST fall back to an out-of-band dead-letter queue with exponential backoff retry."*

### Step 1: 抽丝剥茧——砍掉所有修饰，只抓骨架 (SVO Core)
把所有条件、定语、修饰全部拿掉，只看主干：

```
[条件状语] In the event of timeout,
[前半句主干] the service SHOULD NOT fail the transaction;
[后半句主干] instead, it MUST fall back to a queue.
```
**一目了然的逻辑核心**：
* 条件：一旦超时
* 动作 1：服务不能让交易失败
* 动作 2：相反，必须降级到一个队列

---

### Step 2: 逐层挂载——看清修饰关系 (Modifiers & Prepositions)

1. **前置条件引导词**：
   * `In the event of [名词短语]`：等价于 `If [句子]`。技术文档中专用于引出故障分支或异常状态。
   * 挂载成分：`a downstream database timeout`（下游数据库超时）。
2. **后置修饰队列 (Post-modifiers)**：
   * 核心词：`a queue`（一个队列）。
   * 挂载修饰 1：`out-of-band`（带外的、异步的，不阻塞主流程）。
   * 挂载修饰 2：`dead-letter`（死信队列）。
   * 挂载修饰 3（介词 with 短语做后置定语）：`with exponential backoff retry`（带有指数退避重试机制）。

---

### Step 3: 技术词源与造词内幕 (Etymology & Lingo)

* **`back off`**：
  * 字面：往后退一步、让人喘口气。
  * 计算机含义：**退避机制**。下游快挂了，客户端不要死命重试，退后等等再来。
* **`exponential backoff`**：
  * 指数级后退：等待时间按 $1s \rightarrow 2s \rightarrow 4s \rightarrow 8s$ 翻倍递增。
* **`mutate state`**：
  * *mut-* 词根为改变/突变（如 mutation）。在工程中特指**改写既有内存或数据库状态**。
* **`idempotent / idempotency`**：
  * *idem-* (相同) + *potent* (力量/效果) = 无论发多少次，最终效果相同（幂等）。

---

## 三、 逆向拼装训练 (Reverse Scaffolding Exercise)

学完结构后，最好的检验方式是自己根据骨架拼装一句话：

* **中文意图**：
  > “在网络故障的情况下，系统不应立刻断开连接；相反，它必须尝试重连。”
* **骨架脚手架**：
  > `In the event of [网络故障], the system [不应立刻断开连接]; instead, it [必须尝试重连].`
* **标准答案**：
  > *"In the event of a network failure, the system SHOULD NOT disconnect immediately; instead, it MUST retry the connection."*
