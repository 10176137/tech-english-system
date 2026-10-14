# Tech English System 🚀 (工程师英语无障碍实战库)

> **目标**：用 1 年时间，从基础表达打底，实现日常生活与研发工作双重无障碍交流，最终具备通过海外远程工作 / 欧盟蓝卡（EU Blue Card）技术面试的实力。

---

## 🎯 核心理念 (Core Philosophy)

1. **拒绝孤立死记硬背**：不背托福/雅思学术大词，专注积累 **1,500 个高频工程动词短语（Phrasal Verbs）与研发语块（Lexical Chunks）**。
2. **Standard Library 思维**：把地道语块当作开箱即用的“标准库函数”。想表达业务逻辑时，直接调用封装好的语块，不再用中英互译造轮子。
3. **闭环训练法 (The 4-Step Loop)**：
   * **输入 (Input)**：语块与场景输入（了解老外怎么说）。
   * **输出 (Attempt)**：模拟实战场景自述。
   * **重构 (Refactor)**：指出中式痛点，给出 Native / Senior 升级版。
   * **加固 (Lock-in)**：记入错题账本，换参数即刻复现。

---

## 📂 仓库目录导航

```
tech-english-system/
├── README.md                      # 体系介绍与核心指引
├── ZCODE_TUTOR_SKILL.md           # Zcode 专属英语私教 Skill 与全套指导规范
├── AI_COACH_PROMPT.md             # 专属 AI 私教系统提示词 (换电脑开箱即用)
├── ROADMAP.md                     # 1年 3 阶段 12 模块完整学习大纲
├── scripts/                       # 本地开源语音交互中继
│   └── voice_tutor.py             # 耳朵(Whisper) + 门禁(VAD) + 嘴巴(Kokoro) 全双工脚本
├── tutorials/                     # 深度教学实战课
│   └── 01-sentence-anatomy-tech-specs.md # 教程01: 需求长难句解剖法 (反编译读需求)
├── ledger/
│   ├── error-ledger.md            # 个人专属错题本 (Bug Tracker for English)
│   └── progress.md                # 学习打卡与进度表
├── library/                       # 核心语块标准库 (The Standard Library)
│   ├── 01-engineering-verbs.md    # 核心研发动词与动词短语
│   ├── 02-architecture-system.md  # 架构与系统设计高频词
│   ├── 03-daily-and-social.md     # 职场闲聊与日常交流语块
│   └── 04-reading-tech-specs.md   # 英文技术需求与 PRD 精读指南
└── scenarios/                     # 全真职场场景剧本库
    ├── 01-daily-standup.md        # 敏捷站会全真话术
    ├── 02-code-review-and-pr.md   # PR 评审与异步博弈
    └── 03-recruiter-screening.md  # 90 秒技术自述与 HR 筛选
```

---

## 🗓️ 一年三阶段路线图概览

* **Phase 1: 破冰打底与日常流利 (Month 1 ~ 3)**
  * 告别中式硬翻，掌握基础生活、职场打招呼、日常状态同步与基础发音弱读连读。
* **Phase 2: 研发全生命周期协作 (Month 4 ~ 8)**
  * 攻克敏捷站会、PR 评审、需求博弈（Push back）、RFC 架构评审与多口音磨耳朵。
* **Phase 3: 欧洲蓝卡与海外面试冲刺 (Month 9 ~ 12)**
  * 算法 Live Coding 边写边讲（Thinking Aloud）、系统设计全英对线、BQ 行为面试（STAR 法则）。

---

## 💡 每日 15 分钟极简工作流

1. **Morning / Commute (5 mins)**：打开 `library/` 扫一眼今天掌握的 2~3 个语块。
2. **Evening Drill (10 mins)**：打开 AI 对话或录音，根据 `scenarios/` 进行微场景造句或角色扮演。
3. **Commit (Weekly)**：把新纠正的表达同步到 `ledger/error-ledger.md`。
