下面这份就是可以直接放进
Competitions/kelvin-2025-contest/README.md 的内容，你可以按需要再微调题目细节。

# Kelvin 2025 Contest – VIP Track 解题记录

本仓库用于整理我在 **Kelvin 2025 Programming Contest – VIP Track** 中的代码、资料和赛后复盘，方便后续回顾和作为简历作品展示。

> Commit 说明：`2025/12/7/6:00-9:00, Kelvin 2025 contest`  
> 比赛时间：2025-12-07，时长约 3 小时。

---

## 1. 仓库结构（Repository Structure）

```text
Competitions/
└─ kelvin-2025-contest/
   ├─ docs/
   │   └─ The VIP Track Handbook.pdf    # 官方比赛手册 / 题面资料
   ├─ results/
   │   └─ Rank.png                      # 比赛结果或排名截图
   ├─ src/                              # 参赛代码（C++ / Python 等）
   └─ README.md                         # 当前说明文档


docs/：主要是官方提供的 VIP Track Handbook，包括比赛规则、题目描述等。

src/：我在比赛中实际写的代码（含不同语言版本、不同尝试）。

results/：比赛最终成绩截图或排名证明。

2. 环境与依赖（Dependencies）

本项目刻意保持“竞赛环境风格”：只依赖标准工具和标准库，方便在任何普通评测环境（CodeGrade / 本地 / Linux 服务器）上复现。

2.1 通用环境（General）

操作系统：

本地开发：Windows 10/11

评测环境：基于 Linux 的在线评测系统（例如 CodeGrade）

基础工具：

Git（用于版本管理）

任意代码编辑器（VS Code / CLion / Vim / 等）

2.2 C++ 代码依赖

编译器：

g++ 或 clang++

支持 C++17 及以上标准

代码习惯：

常用头文件：#include <bits/stdc++.h>（GCC 环境常见写法）

只使用 C++ 标准库（vector, map, algorithm, cmath 等）

无第三方库依赖

只要评测机支持 C++17、GCC 常见头文件，本仓库中的 C++ 代码应该可以直接编译运行。

2.3 Python 代码依赖（如有）

如果 src/ 中包含 Python 版本解法，默认假设：

Python 版本：Python 3.9+

依赖库：仅使用 标准库（sys, math, itertools, collections 等）

无外部第三方库（如 numpy / pandas 等）

3. 代码运行说明（How to Run）

注意：具体文件名请以 src/ 目录下实际文件为准，下面以示例名代替。

3.1 运行 C++ 解法

以 solution.cpp 为例：

# 编译
g++ -std=c++17 -O2 -pipe -static -s -o solution solution.cpp

# 运行（从标准输入读取数据）
./solution < input.txt > output.txt


评测环境中通常是：

直接 g++ -std=c++17 -O2 solution.cpp -o solution

由评测系统自动喂输入、比对输出。

3.2 运行 Python 解法（如有）

以 solution.py 为例：

python3 solution.py < input.txt > output.txt


只依赖 Python 标准库，一般和本地环境/评测环境兼容性较好。

注意行末空格、换行符等细节以避免 WA（Wrong Answer）。

4. 解题思路概述（Solution Ideas Overview）

不展开完整题面，只记录主要思路和建模方式，方便自己以后回顾。
重点在：状态设计、转移方式、复杂度控制。

4.1 概览

本次 VIP Track 的核心题目之一，可以抽象为：

有若干 状态（例如系统的不同节点/局面），数量为 N。

有若干 动作 或 方案，数量为 M。

每个动作会在不同状态之间产生 概率转移，类似一个 马尔可夫链 / MDP（Markov Decision Process）。

目标是在有限步数 / 预算下，使某个代价或收益函数最优（例如最大化期望收益，或最小化期望成本）。

4.2 状态与转移设计

代码中使用了如下典型结构（以 C++ 为例）：

int T, N, M, L, Type;
double mu;
vector<int> R;
vector<vector<int>> C;
vector<vector<vector<double>>> P;   // P[a][i][j] 表示执行动作 a 时，状态 i -> j 的转移概率
vector<vector<double>> rs, rd, pp;  // 若干中间状态/期望缓存
vector<double> costab;
vector<vector<double>> V;           // DP/期望值表


核心思想：

使用长度为 N 的向量 d 表示当前状态分布（每个位置是处于该状态的概率）。

给定一个动作为 a 时，通过转移矩阵 P[a] 将 d 推进到下一步分布 nd：

inline void prop(const vector<double>& d, int a, vector<double>& nd) {
    fill(nd.begin(), nd.end(), 0.0);
    for (int i = 0; i < N; ++i) {
        double di = d[i];
        if (di <= 1e-15) continue;
        const auto &row = P[a][i];
        for (int j = 0; j < N; ++j) nd[j] += di * row[j];
    }
}


在多轮决策中，对不同动作序列进行递推（或使用 DP / 记忆化），计算最终期望收益或代价。

这种写法的优点：

逻辑清晰：代码结构与数学定义基本一一对应。

易于调试：可以单独打印中间的状态分布向量检查是否“守恒”（概率和是否接近 1）。

扩展性好：如果后续题目对奖励函数、约束条件有改变，只需要调整部分计算逻辑，不必推翻整体框架。

4.3 复杂度与优化

主要瓶颈在于：

对每个动作、每个状态做一次内层 O(N) 的转移 → 单步为 O(M * N^2)。

典型优化手段：

对于概率非常小的状态（例如 < 1e-15），直接跳过（如代码中所示）；

预先预处理固定不变的中间量（如 delta、costab 等），减少重复计算；

如果状态转移矩阵存在稀疏性，可进一步按“非零转移”进行压缩存储（此处根据题目需要可选）。

5. 比赛过程回顾（Contest Process）

这一部分更多是给“未来的自己”看的复盘记录，便于下次比赛、更好规划时间与策略。

5.1 赛前准备

提前确认：

本地编译环境：g++ / python3 可用

CodeGrade 提交流程熟悉（如何上传文件、查看评测结果）

准备好：

常用代码模板（快读、调试宏、基础 DP 框架等）

简单的 run.sh / test.sh（如需要）

5.2 比赛中策略

先扫题再决定顺序

先快速浏览题目，判断大致难度和可能的算法类别。

优先做“能 80% 确定能 AC 的题”，保证基础得分。

分阶段实现

第一阶段：先写出正确但可能较慢的解法，优先保证“能过样例、能过小数据”。

第二阶段：再根据时间考虑复杂度优化 / 常数优化。

调试与验证

为关键函数（例如概率转移、DP 更新）构造小样例，打印中间结果。

尤其是涉及浮点数、概率和时，重点检查：

概率和是否 ≈ 1

是否出现负概率 / 明显异常值

提交策略

每当完成一个稳定版本就上传一次（防止本地文件丢失）。

遇到不确定的优化，不在最后几分钟大改核心逻辑，以免“从 AC 改成 WA”。

5.3 赛后整理

把本地代码、手册、rank 截图统一整理进本仓库：

docs/：官方文档

src/：最终版本代码 + 可能的对比版本（如 Python 草稿 / C++ 最终版）

results/：成绩截图

适当补充注释、README，方便将来复用思路或改造成教学/展示用项目。
