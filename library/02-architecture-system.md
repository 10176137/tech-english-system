# 架构与系统设计高频语块库 (Architecture & System Design Chunks)

> 系统设计面试与 RFC 讨论中，如何表达权衡（Trade-offs）与高并发痛点。

---

## 1. 核心架构术语与高频搭配

* **ingestion** [ɪnˈdʒestʃən]
  * `order ingestion pipeline`（订单接入流水线）
  * `handle high-throughput data ingestion`（处理高吞吐量数据接入）
* **orchestrate** [ˈɔːkɪstreɪt]
  * `orchestrate the distributed workflow`（编排分布式工作流）
  * `workflow orchestration engine`（工作流编排引擎）
* **state transition**
  * `manage state transitions across the order lifecycle`（管理整个订单生命周期的状态扭转）
  * `idempotent state transition`（幂等状态流转）
* **decouple** [diːˈkʌpl]
  * `decouple the producer from the consumer via Kafka`（通过 Kafka 解耦生产者与消费者）
* **idempotency** [ˌaɪdəmˈpoʊtənsi]
  * `ensure idempotency using distributed locks / unique keys`（使用分布式锁/唯一键保证幂等性）
* **bottleneck** [ˈbɒtlnek]
  * `the primary bottleneck is the database I/O`（主要瓶颈在数据库 I/O）
* **single point of failure (SPOF)**
  * `eliminate single points of failure with multi-region replicas`（通过多地域副本消除单点故障）

---

## 2. 阐述权衡 (Weighing Trade-offs) 的黄金句架

1. **两者权衡对比**：
   * *“We need to weigh the trade-offs between consistency and latency.”*  
     （我们需要在一致性和低延迟之间权衡利弊。）
2. **两害相权取其轻**：
   * *“Option A gives us higher throughput, but at the cost of higher operational overhead.”*  
     （方案 A 能带来更高的吞吐量，但代价是运维开销增加。）
3. **经验法则引出决策**：
   * *“As a rule of thumb, for read-heavy workloads, adding a Redis cache is the safest bet.”*  
     （作为经验法则，对于读多写少的场景，增加 Redis 缓存是最稳妥的选择。）
