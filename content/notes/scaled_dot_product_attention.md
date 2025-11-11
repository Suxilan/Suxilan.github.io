---
title: "Scaled Dot-Product Attention 的数学剖析"
date: 2025-11-07T15:30:00+08:00
draft: false
tags: ["Deep Learning", "Transformer", "Attention", "数学推导"]
categories: ["技术笔记"]
series: []
author: "Suxilan"
showToc: true
TocOpen: false
comments: true
description: "深入推导 Scaled Dot-Product Attention 的数学原理：从方差分析到对称性破缺"
summary: "严格的数学推导 + 教学性解释，揭示 SDPA 的设计精髓"
---

## 引言

Scaled Dot-Product Attention (SDPA) 是 Transformer 架构的核心计算单元。这里我**摘录了和AI对话的结果**，结合个人查阅到的资料，从数学第一性原理出发，严格推导其设计背后的统计学依据、几何直觉和训练动力学。

我们将回答以下关键问题：
1. **为什么要除以 $\sqrt{d_k}$？** —— 方差稳定性的严格证明
2. **Q 和 K 为什么看起来对称却不能交换？** —— 对称性破缺的机制
3. **训练过程中权重矩阵如何演进？** —— 从随机初始化到语义角色分化
4. **为什么选择点积而非其他相似度？** —— 计算复杂度与几何意义

---

## 1. 核心公式的分解

Scaled Dot-Product Attention 的完整数学表达式：

$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$

### 符号定义

| 符号 | 形状 | 含义 |
|:--:|:--:|:---|
| $Q$ | $(n, d_k)$ | **Query 矩阵**：$n$ 个查询向量，每个维度 $d_k$ |
| $K$ | $(n, d_k)$ | **Key 矩阵**：$n$ 个键向量，每个维度 $d_k$ |
| $V$ | $(n, d_v)$ | **Value 矩阵**：$n$ 个值向量，每个维度 $d_v$ |
| $n$ | 标量 | 序列长度（如句子中的词数） |
| $d_k$ | 标量 | Query 和 Key 的向量维度 |
| $d_v$ | 标量 | Value 的向量维度（可以与 $d_k$ 不同） |

### 计算流程

**步骤 1：线性投影生成 Q, K, V**

$$
\begin{aligned}
Q &= XW^Q \quad \text{其中 } W^Q \in \mathbb{R}^{d_{\text{model}} \times d_k} \\
K &= XW^K \quad \text{其中 } W^K \in \mathbb{R}^{d_{\text{model}} \times d_k} \\
V &= XW^V \quad \text{其中 } W^V \in \mathbb{R}^{d_{\text{model}} \times d_v}
\end{aligned}
$$

其中 $X \in \mathbb{R}^{n \times d_{\text{model}}}$ 是输入嵌入矩阵。下图为Transformer Explainer的可视化效果：

<img src="https://cdn.jsdelivr.net/gh/Suxilan/Cloud-Image-alpha/imagebed/notes/projection_qkv.png" alt="projection_qkv" style="zoom:67%;" />

<img src="https://cdn.jsdelivr.net/gh/Suxilan/Cloud-Image-alpha/imagebed/notes/compute_attn.png" style="zoom: 50%;" />

**步骤 2：计算注意力分数**

$$
S = QK^T \in \mathbb{R}^{n \times n}
$$

矩阵 $S$ 的第 $(i, j)$ 元素：

$$
S_{ij} = q_i \cdot k_j = \sum_{\ell=1}^{d_k} q_{i\ell} k_{j\ell}
$$

这个点积衡量了第 $i$ 个查询与第 $j$ 个键的相似度。

**步骤 3：缩放**

$$
S' = \frac{S}{\sqrt{d_k}} = \frac{QK^T}{\sqrt{d_k}}
$$

**步骤 4：Softmax 归一化**

对 $S'$ 的每一行应用 Softmax：

$$
A_{ij} = \frac{\exp(S'_{ij})}{\sum_{k=1}^n \exp(S'_{ik})}
$$

结果 $A \in \mathbb{R}^{n \times n}$ 称为**注意力权重矩阵**，满足：
- $A_{ij} \geq 0$ （非负性）
- $\sum_{j=1}^n A_{ij} = 1$ （每行和为 1，概率分布）

**步骤 5：加权求和**

$$
Z = AV \in \mathbb{R}^{n \times d_v}
$$

输出矩阵 $Z$ 的第 $i$ 行：

$$
z_i = \sum_{j=1}^n A_{ij} v_j
$$

即第 $i$ 个输出是所有值向量的加权平均，权重由注意力决定。

---

## 2. 为什么是 $\sqrt{d_k}$？—— 方差稳定性的严格推导

这绝对是论文中最精妙的数学细节之一。缩放因子 $\sqrt{d_k}$ 不是随便选的"魔法数字"，而是有严格的统计学理由。

### 2.1 目标

**保持点积 $q \cdot k$ 的方差为 1**，以防止 Softmax 函数饱和。

### 2.2 问题

当 $q$ 和 $k$ 的维度 $d_k$ 变大时，它们的点积 $q \cdot k$ 的方差会发生什么？

### 2.3 推导

我们来分析点积。首先明确符号和维度：

- **$S \in \mathbb{R}^{n \times n}$**：注意力分数矩阵
- **$S_{ij}$**：第 $i$ 个查询向量 $q_i \in \mathbb{R}^{d_k}$ 与第 $j$ 个键向量 $k_j \in \mathbb{R}^{d_k}$ 的点积
- **$q_i, k_j$**：分别是 $Q$ 和 $K$ 矩阵的第 $i$ 行和第 $j$ 行

对于固定的 $(i, j)$，点积计算为：

$$
S_{ij} = q_i \cdot k_j = \sum_{\ell=1}^{d_k} q_{i\ell} k_{j\ell}
$$

其中 $\ell$ 是向量维度索引（$\ell = 1, 2, \ldots, d_k$），$q_{i\ell}$ 表示 $q_i$ 的第 $\ell$ 个分量。

**维度变化说明**：
- $q_i \in \mathbb{R}^{d_k}$（行向量）
- $k_j \in \mathbb{R}^{d_k}$（行向量）
- $S_{ij} \in \mathbb{R}$（标量）
- 点积操作：$\mathbb{R}^{d_k} \times \mathbb{R}^{d_k} \to \mathbb{R}$

为了简化推导，我们固定 $(i, j)$，记 $s = S_{ij}$，$q = q_i$，$k = k_j$，则：

$$
s = q \cdot k = \sum_{\ell=1}^{d_k} q_\ell k_\ell
$$

#### **前提假设 (Assumption)**

为了进行分析，我们做出两个合理的统计假设（这也是论文作者的隐含假设，与 Xavier/Glorot 初始化一致）：

1. $q$ 和 $k$ 的每个分量 $q_\ell$ 和 $k_\ell$（$\ell = 1, 2, \ldots, d_k$）都是**独立同分布 (i.i.d.)** 的。
2. 它们是从一个**均值 $\mathbb{E} = 0$，方差 $\text{Var} = 1$** 的分布中抽取的。

形式化：

$$
\begin{aligned}
\mathbb{E}[q_\ell] &= 0, \quad \mathbb{E}[k_\ell] = 0 \\
\text{Var}(q_\ell) &= 1, \quad \text{Var}(k_\ell) = 1
\end{aligned}
$$

其中 $\ell = 1, 2, \ldots, d_k$。

#### **第 1 步：计算 $s$ 的均值 $\mathbb{E}[s]$**

$$
\mathbb{E}[s] = \mathbb{E}\left[ \sum_{\ell=1}^{d_k} q_\ell k_\ell \right]
$$

根据期望的**线性性质**：

$$
\mathbb{E}[s] = \sum_{\ell=1}^{d_k} \mathbb{E}[q_\ell k_\ell]
$$

因为 $q_\ell$ 和 $k_\ell$ 相互**独立**，所以：

$$
\mathbb{E}[q_\ell k_\ell] = \mathbb{E}[q_\ell] \cdot \mathbb{E}[k_\ell]
$$

代入假设：

$$
\mathbb{E}[s] = \sum_{\ell=1}^{d_k} (\mathbb{E}[q_\ell] \cdot \mathbb{E}[k_\ell]) = \sum_{\ell=1}^{d_k} (0 \cdot 0) = 0
$$

**结论 1**：点积 $s$ 的均值（期望）为 0。✓

#### **第 2 步：计算 $s$ 的方差 $\text{Var}(s)$**

$$
\text{Var}(s) = \text{Var}\left( \sum_{\ell=1}^{d_k} q_\ell k_\ell \right)
$$

因为 $q_\ell k_\ell$ 与 $q_m k_m$ ($\ell \neq m$) 之间是相互**独立**的（$q_\ell$ 和 $q_m$ 独立，$k_\ell$ 和 $k_m$ 独立），所以**"和的方差等于方差的和"**：

$$
\text{Var}(s) = \sum_{\ell=1}^{d_k} \text{Var}(q_\ell k_\ell)
$$

> **说明**：这是概率论中的关键性质。对于独立随机变量 $X_1, X_2, \ldots, X_n$：
> $$\text{Var}(X_1 + X_2 + \cdots + X_n) = \text{Var}(X_1) + \text{Var}(X_2) + \cdots + \text{Var}(X_n)$$

现在，我们只需要计算 $\text{Var}(q_\ell k_\ell)$。

#### **第 3 步：计算 $\text{Var}(q_\ell k_\ell)$**

根据方差的定义：

$$
\text{Var}(X) = \mathbb{E}[X^2] - (\mathbb{E}[X])^2
$$

应用到 $q_\ell k_\ell$：

$$
\text{Var}(q_\ell k_\ell) = \mathbb{E}[(q_\ell k_\ell)^2] - (\mathbb{E}[q_\ell k_\ell])^2
$$

从**第 1 步**我们知道 $\mathbb{E}[q_\ell k_\ell] = 0$，所以：

$$
\text{Var}(q_\ell k_\ell) = \mathbb{E}[(q_\ell k_\ell)^2] = \mathbb{E}[q_\ell^2 k_\ell^2]
$$

因为 $q_\ell$ 和 $k_\ell$ **独立**，所以 $q_\ell^2$ 和 $k_\ell^2$ 也独立：

$$
\mathbb{E}[q_\ell^2 k_\ell^2] = \mathbb{E}[q_\ell^2] \cdot \mathbb{E}[k_\ell^2]
$$

#### **第 4 步：计算 $\mathbb{E}[q_\ell^2]$**

我们需要知道 $\mathbb{E}[q_\ell^2]$ 是什么。再次使用方差公式：

$$
\text{Var}(q_\ell) = \mathbb{E}[q_\ell^2] - (\mathbb{E}[q_\ell])^2
$$

根据我们的假设：$\text{Var}(q_\ell) = 1$ 且 $\mathbb{E}[q_\ell] = 0$：

$$
1 = \mathbb{E}[q_\ell^2] - (0)^2 \quad \Rightarrow \quad \mathbb{E}[q_\ell^2] = 1
$$

同理，$\mathbb{E}[k_\ell^2] = 1$。

#### **第 5 步：回代**

将结果代入：

$$
\text{Var}(q_\ell k_\ell) = \mathbb{E}[q_\ell^2] \cdot \mathbb{E}[k_\ell^2] = 1 \cdot 1 = 1
$$

最后，将它代入 $s$ 的方差总和中：

$$
\text{Var}(s) = \sum_{\ell=1}^{d_k} \text{Var}(q_\ell k_\ell) = \sum_{\ell=1}^{d_k} 1 = d_k
$$

### 2.4 关键结论

$$
\boxed{\text{Var}(q \cdot k) = d_k}
$$

**点积的方差等于它的维度 $d_k$。**

### 2.5 后果分析

这个结论意味着：

- **如果 $d_k = 64$**：$\text{Var}(s) = 64$，标准差 $\sigma = \sqrt{64} = 8$
- **如果 $d_k = 512$**：$\text{Var}(s) = 512$，标准差 $\sigma = \sqrt{512} \approx 22.6$

维度 $d_k$ 越大，点积 $s$ 的值就会（在 0 附近）**波动得越剧烈**。

根据"3-sigma 规则"，大约 99.7% 的值会落在 $[\mu - 3\sigma, \mu + 3\sigma]$ 内。由于 $\mu = 0$：

- $d_k = 512$ 时：点积值约在 $[-68, 68]$ 范围内

### 2.6 对 Softmax 的影响

#### **2.6.1 Softmax 函数的定义与性质**

对于输入向量 $\mathbf{z} = [z_1, z_2, \ldots, z_n] \in \mathbb{R}^n$，Softmax 函数定义为：

$$
\text{softmax}(\mathbf{z})_j = \frac{e^{z_j}}{\sum_{i=1}^n e^{z_i}} = \frac{e^{z_j}}{Z}
$$

其中 $Z = \sum_{i=1}^n e^{z_i}$ 是归一化常数（配分函数）。

**关键性质**：
1. **非负性**：$\text{softmax}(\mathbf{z})_j \geq 0$（因为指数函数 $e^{z_j} > 0$）
2. **归一性**：$\sum_{j=1}^n \text{softmax}(\mathbf{z})_j = 1$（概率分布）
3. **单调性**：如果 $z_i > z_j$，则 $\text{softmax}(\mathbf{z})_i > \text{softmax}(\mathbf{z})_j$

#### **2.6.2 数值稳定性技巧**

实际计算中，为了避免数值溢出，通常使用"减去最大值"的技巧：

$$
\text{softmax}(\mathbf{z})_j = \frac{e^{z_j - \max(\mathbf{z})}}{\sum_{i=1}^n e^{z_i - \max(\mathbf{z})}}
$$

其中 $\max(\mathbf{z}) = \max\{z_1, z_2, \ldots, z_n\}$。

**为什么这样做？**

- 指数函数增长极快：$e^{50} \approx 5.18 \times 10^{21}$，可能超出浮点数表示范围
- 减去最大值后，最大的指数项变为 $e^0 = 1$，其他项为负指数，数值稳定
- 数学上等价（分子分母同除以 $e^{\max(\mathbf{z})}$）

#### **2.6.3 问题：Softmax 对极端输入敏感**

**问题**：Softmax 对非常大或非常小的输入值**非常敏感**。

如果输入（即我们的点积 $s$）的方差很大（比如 512），就意味着很多 $s_j$ 的值会是 $+20, -15, +30$ 这样的极端值。

**数值示例**：

- $e^{20} \approx 4.85 \times 10^8$ 已经是一个天文数字
- $e^{-15} \approx 3.06 \times 10^{-7}$ 几乎为 0

**具体例子**：

考虑输入向量 $\mathbf{z} = [50, 1, 1, 1]$（$n=4$）：

$$
\begin{aligned}
\text{softmax}([50, 1, 1, 1])_1 &= \frac{e^{50}}{e^{50} + e + e + e} = \frac{e^{50}}{e^{50} + 3e} \\
&\approx \frac{5.18 \times 10^{21}}{5.18 \times 10^{21} + 8.15} \\
&\approx \frac{5.18 \times 10^{21}}{5.18 \times 10^{21}} = 1.0
\end{aligned}
$$

对于 $j = 2, 3, 4$：

$$
\text{softmax}([50, 1, 1, 1])_j = \frac{e}{e^{50} + 3e} \approx \frac{2.72}{5.18 \times 10^{21}} \approx 0.0
$$

因此：

$$
\text{softmax}([50, 1, 1, 1]) \approx [1.0, 0.0, 0.0, 0.0]
$$

这会导致 Softmax 的输出**饱和 (saturate)**，变成一个接近"one-hot"的向量（例如 $[1, 0, 0, 0]$）。

### 2.7 梯度消失问题：Softmax 梯度的详细推导

当 Softmax 输出饱和时，**梯度会消失 (Vanishing Gradients)**，因为 Softmax 的梯度在这些饱和区域几乎为 0。

#### **2.7.1 Softmax 梯度的推导**

设 $\mathbf{z} = [z_1, z_2, \ldots, z_n]$，$p_j = \text{softmax}(\mathbf{z})_j = \frac{e^{z_j}}{\sum_{i=1}^n e^{z_i}}$。（这里涉及向量求导的雅可比矩阵计算，详情可以到[矩阵微分笔记]({{< relref "matrix_calculus.md" >}})查看）

我们需要计算：

$$
\frac{\partial p_j}{\partial z_k} = \frac{\partial}{\partial z_k} \left( \frac{e^{z_j}}{\sum_{i=1}^n e^{z_i}} \right)
$$

**情况 1：$j = k$（对角元素）**

使用商的求导法则：

$$
\frac{\partial p_j}{\partial z_j} = \frac{e^{z_j} \cdot \sum_{i=1}^n e^{z_i} - e^{z_j} \cdot e^{z_j}}{(\sum_{i=1}^n e^{z_i})^2}
$$

化简：

$$
\begin{aligned}
\frac{\partial p_j}{\partial z_j} &= \frac{e^{z_j}(\sum_{i=1}^n e^{z_i} - e^{z_j})}{(\sum_{i=1}^n e^{z_i})^2} \\
&= \frac{e^{z_j}}{\sum_{i=1}^n e^{z_i}} \cdot \frac{\sum_{i=1}^n e^{z_i} - e^{z_j}}{\sum_{i=1}^n e^{z_i}} \\
&= p_j \cdot (1 - p_j)
\end{aligned}
$$

**情况 2：$j \neq k$（非对角元素）**

$$
\frac{\partial p_j}{\partial z_k} = \frac{0 \cdot \sum_{i=1}^n e^{z_i} - e^{z_j} \cdot e^{z_k}}{(\sum_{i=1}^n e^{z_i})^2} = -\frac{e^{z_j} e^{z_k}}{(\sum_{i=1}^n e^{z_i})^2}
$$

化简：

$$
\begin{aligned}
\frac{\partial p_j}{\partial z_k} &= -\frac{e^{z_j}}{\sum_{i=1}^n e^{z_i}} \cdot \frac{e^{z_k}}{\sum_{i=1}^n e^{z_i}} \\
&= -p_j \cdot p_k
\end{aligned}
$$

#### **2.7.2 统一公式**

使用 Kronecker delta $\delta_{jk}$（$j=k$ 时为 1，否则为 0），可以统一两种情况：

$$
\frac{\partial p_j}{\partial z_k} = p_j (\delta_{jk} - p_k)
$$

**验证**：
- 当 $j = k$：$\frac{\partial p_j}{\partial z_j} = p_j (1 - p_j)$ ✓
- 当 $j \neq k$：$\frac{\partial p_j}{\partial z_k} = p_j (0 - p_k) = -p_j p_k$ ✓

#### **2.7.3 梯度消失的数值分析**

使用之前的例子：$\mathbf{z} = [50, 1, 1, 1]$，则 $\mathbf{p} = \text{softmax}(\mathbf{z}) \approx [1.0, 0.0, 0.0, 0.0]$。

**计算梯度矩阵** $\frac{\partial p_j}{\partial z_k}$：

对于 $j = 1$（第一个元素）：

$$
\begin{aligned}
\frac{\partial p_1}{\partial z_1} &= p_1 (1 - p_1) = 1.0 \cdot (1 - 1.0) = 0 \\
\frac{\partial p_1}{\partial z_2} &= p_1 (0 - p_2) = 1.0 \cdot (0 - 0) = 0 \\
\frac{\partial p_1}{\partial z_3} &= p_1 (0 - p_3) = 1.0 \cdot (0 - 0) = 0 \\
\frac{\partial p_1}{\partial z_4} &= p_1 (0 - p_4) = 1.0 \cdot (0 - 0) = 0
\end{aligned}
$$

对于 $j = 2, 3, 4$：

$$
\frac{\partial p_j}{\partial z_k} = p_j (\delta_{jk} - p_k) \approx 0 \cdot (\delta_{jk} - \cdot) = 0
$$

**结论**：梯度矩阵几乎全为 0！

#### **2.7.4 梯度消失的后果**

当 $\text{softmax}(z_i) \approx 0$ 或 $\approx 1$ 时：

- **如果 $p_i \approx 0$**：梯度 $\frac{\partial p_i}{\partial z_k} = p_i (\delta_{ik} - p_k) \approx 0 \cdot (\cdot) \approx 0$
- **如果 $p_i \approx 1$**：
  - 对于 $k = i$：$\frac{\partial p_i}{\partial z_i} = p_i (1 - p_i) \approx 1 \cdot (1 - 1) = 0$
  - 对于 $k \neq i$：$\frac{\partial p_i}{\partial z_k} = p_i (0 - p_k) \approx 1 \cdot (0 - 0) = 0$

**结果**：**模型将停止学习**，因为梯度无法反向传播，参数无法更新。

### 2.8 解决方案：缩放

我们希望将 $s$ 的方差"拉回"到 1。

#### **关键性质**：方差的缩放性质

对于随机变量 $X$ 和常数 $c$：

$$
\text{Var}(c \cdot X) = c^2 \cdot \text{Var}(X)
$$

> **证明**：
> $$\text{Var}(cX) = \mathbb{E}[(cX - \mathbb{E}[cX])^2] = \mathbb{E}[(cX - c\mathbb{E}[X])^2] = c^2 \mathbb{E}[(X - \mathbb{E}[X])^2] = c^2 \text{Var}(X)$$

#### **求解常数 $c$**

我们希望找到一个常数 $c$，使得：

$$
\text{Var}(c \cdot s) = 1
$$

应用性质：

$$
c^2 \cdot \text{Var}(s) = 1
$$

代入 $\text{Var}(s) = d_k$：

$$
c^2 \cdot d_k = 1
$$

解得：

$$
c^2 = \frac{1}{d_k} \quad \Rightarrow \quad c = \frac{1}{\sqrt{d_k}}
$$

### 2.9 最终推论

我们不应该使用原始点积 $s$，而应该使用**缩放后的点积**：

$$
s' = c \cdot s = \frac{s}{\sqrt{d_k}} = \frac{q \cdot k}{\sqrt{d_k}}
$$

这个新的缩放后的分数 $s'$ 的方差是：

$$
\text{Var}(s') = \text{Var}\left(\frac{s}{\sqrt{d_k}}\right) = \left(\frac{1}{\sqrt{d_k}}\right)^2 \cdot \text{Var}(s) = \frac{1}{d_k} \cdot d_k = 1
$$

$$
\boxed{\text{Var}\left(\frac{q \cdot k}{\sqrt{d_k}}\right) = 1}
$$

### 2.10 总结

通过**除以 $\sqrt{d_k}$**，我们将点积得分的方差从 $d_k$ 重新标准化回 1，使其**独立于维度 $d_k$ 的大小**。

这保证了：
1. **Softmax 的输入始终处于一个"合理"的、非饱和的范围**（通常在 $[-3, 3]$ 内）
2. **梯度能够稳定流动**
3. **模型得以成功训练**

这就是 **"Scaled"** Dot-Product Attention 中 "Scaled" 的精确数学含义。

---

## 3. Q 与 K 的表观对称性：可交换性分析

### 3.1 核心问题

$W^Q$ 和 $W^K$ 在初始化时完全对称（同分布），且维度相同（都是 $\mathbb{R}^{d_{\text{model}} \times d_k}$）。那么：

1. **为什么约定计算 $QK^T$ 而不是 $KQ^T$？**
2. **Q 和 K 能否互换？**
3. **训练后它们为什么会分化？**

### 3.2 数学形式化

定义标准自注意力：

$$
A_{\text{std}} = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)
$$

如果交换 Q 和 K：

$$
A_{\text{swap}} = \text{softmax}\left(\frac{KQ^T}{\sqrt{d_k}}\right)
$$

### 3.3 初始化阶段：统计等价性

假设采用 Xavier/Glorot 初始化：

$$
W^Q \sim \mathcal{N}\left(0, \frac{2}{d_{\text{model}} + d_k}\right), \quad W^K \sim \mathcal{N}\left(0, \frac{2}{d_{\text{model}} + d_k}\right)
$$

两者从**相同分布独立采样**，统计特性完全相同：

$$
\mathbb{E}[W^Q] = \mathbb{E}[W^K] = 0, \quad \text{Var}(W^Q) = \text{Var}(W^K)
$$

生成的 Q 和 K：

$$
Q = XW^Q, \quad K = XW^K
$$

考虑注意力分数矩阵：

$$
QK^T = XW^Q(W^K)^TX^T
$$

$$
KQ^T = XW^K(W^Q)^TX^T
$$

### 3.4 关键观察：实例不等价

虽然 $W^Q(W^K)^T$ 和 $W^K(W^Q)^T$ **统计等价**（同分布），但它们是**不同的随机矩阵实例**。

**期望层面**：

$$
\mathbb{E}[W^Q(W^K)^T] = \mathbb{E}[W^Q]\mathbb{E}[(W^K)^T] = 0 \cdot 0 = 0
$$

（零均值矩阵）

**但实际实例不同**：
$$
W^Q(W^K)^T \neq W^K(W^Q)^T
$$

**原因**：矩阵乘法**不满足交换律**（$AB \neq BA$ 一般情况下）。

### 3.5 训练阶段：对称性破缺

#### **梯度的不对称性**

反向传播时，损失函数 $\mathcal{L}$ 对 $W^Q$ 和 $W^K$ 的梯度不同：

$$
\frac{\partial \mathcal{L}}{\partial W^Q} = \frac{\partial \mathcal{L}}{\partial Q} \frac{\partial Q}{\partial W^Q} = \frac{\partial \mathcal{L}}{\partial Q} \cdot X^T
$$

$$
\frac{\partial \mathcal{L}}{\partial W^K} = \frac{\partial \mathcal{L}}{\partial K} \frac{\partial K}{\partial W^K} = \frac{\partial \mathcal{L}}{\partial K} \cdot X^T
$$

**关键问题**：$\frac{\partial \mathcal{L}}{\partial Q}$ 和 $\frac{\partial \mathcal{L}}{\partial K}$ 相等吗？

#### **答案：不相等**

考虑注意力机制的前向传播：

$$
S = QK^T, \quad A = \text{softmax}(S), \quad \text{Out} = AV
$$

对于 $S = QK^T$ 的梯度（链式法则）：

$$
\frac{\partial S}{\partial Q} = K, \quad \frac{\partial S}{\partial K} = Q
$$

更详细地，假设上游梯度为 $\frac{\partial \mathcal{L}}{\partial S} \in \mathbb{R}^{n \times n}$：

$$
\frac{\partial \mathcal{L}}{\partial Q} = \frac{\partial \mathcal{L}}{\partial S} \cdot \frac{\partial S}{\partial Q} = \frac{\partial \mathcal{L}}{\partial S} \cdot K
$$

$$
\frac{\partial \mathcal{L}}{\partial K} = \frac{\partial \mathcal{L}}{\partial S} \cdot \frac{\partial S}{\partial K}^T = \left(\frac{\partial \mathcal{L}}{\partial S}\right)^T \cdot Q
$$

> **推导细节**：对于 $S_{ij} = \sum_\ell Q_{i\ell} K_{j\ell}$：
> $$\frac{\partial S_{ij}}{\partial Q_{i\ell}} = K_{j\ell}, \quad \frac{\partial S_{ij}}{\partial K_{j\ell}} = Q_{i\ell}$$

**结论**：

$$
\frac{\partial \mathcal{L}}{\partial Q} = \frac{\partial \mathcal{L}}{\partial S} \cdot K
$$

$$
\frac{\partial \mathcal{L}}{\partial K} = \left(\frac{\partial \mathcal{L}}{\partial S}\right)^T \cdot Q
$$

**两者结构完全不同！**

- $\frac{\partial \mathcal{L}}{\partial Q}$ 是 $\frac{\partial \mathcal{L}}{\partial S}$ 右乘 $K$
- $\frac{\partial \mathcal{L}}{\partial K}$ 是 $\frac{\partial \mathcal{L}}{\partial S}$ 的**转置**右乘 $Q$

#### **梯度下降的分化效应**

参数更新（简化的 SGD）：

$$
W^Q \leftarrow W^Q - \eta \frac{\partial \mathcal{L}}{\partial W^Q}
$$

$$
W^K \leftarrow W^K - \eta \frac{\partial \mathcal{L}}{\partial W^K}
$$

由于 $\frac{\partial \mathcal{L}}{\partial W^Q} \neq \frac{\partial \mathcal{L}}{\partial W^K}$（即使初始时接近），经过若干轮迭代后：

$$
W^Q \neq W^K \quad \text{（对称性破缺）}
$$

### 3.6 语义角色的涌现

经过训练，即使初始对称，$W^Q$ 和 $W^K$ 会沿不同方向演化：

- **$W^Q$ 学习编码"查询意图"**：
  - 例如：代词（"it"）的 $W^Q$ 学习提取"需要找指代对象"的特征
  
- **$W^K$ 学习编码"被查询特征"**：
  - 例如：名词（"animal"）的 $W^K$ 学习提供"我是潜在指代目标"的特征

这是**数据驱动的分工**，不是人为设计。

### 3.7 命名约定的任意性

理论上，可以定义：

$$
\text{Attention}(K, Q, V) = \text{softmax}\left(\frac{KQ^T}{\sqrt{d_k}}\right)V
$$

只要：
1. **前向传播一致**
2. **反向传播正确实现**
3. **全局约定统一**

数学上完全等价。

选择 $QK^T$ 是因为：
- **"Query-Key"** 语义更直观（搜索引擎类比）
- 工程惯例（论文发表后成为标准）

### 3.8 不可互换性的数学证明

**定理**：假设已训练的 Transformer 中 $W^Q \neq W^K$。如果交换 Q 和 K，注意力矩阵一般会改变。

**证明**：

设 $A = \text{softmax}(\frac{QK^T}{\sqrt{d_k}})$，$A' = \text{softmax}(\frac{KQ^T}{\sqrt{d_k}})$。

则：

$$
A_{ij} = \frac{\exp(q_i \cdot k_j / \sqrt{d_k})}{\sum_\ell \exp(q_i \cdot k_\ell / \sqrt{d_k})}
$$

$$
A'_{ij} = \frac{\exp(k_i \cdot q_j / \sqrt{d_k})}{\sum_\ell \exp(k_i \cdot q_\ell / \sqrt{d_k})}
$$

注意到：
- $A_{ij}$ 的分子：$\exp(q_i \cdot k_j)$
- $A'_{ij}$ 的分子：$\exp(k_i \cdot q_j)$

由于点积交换律：$q_i \cdot k_j = k_j \cdot q_i$

但是：**分母不同！**

- $A_{ij}$ 的分母：对 $k$ 的所有索引求和
- $A'_{ij}$ 的分母：对 $q$ 的所有索引求和

**关键**：$q_i$ 和 $k_i$ 来自不同的投影矩阵，值不同。

因此：**$A \neq A'$**（一般情况下）

$$
\boxed{\text{交换 Q 和 K 会改变注意力权重分布}}
$$

---

## 4. 权重矩阵的训练演进

### 4.1 阶段 1：随机初始化（Epoch 0）

采用 Xavier 初始化：

$$
W^Q, W^K, W^V \sim \mathcal{N}\left(0, \frac{2}{d_{\text{model}} + d_k}\right)
$$

**特点**：
- $W^Q \approx W^K$（统计意义上）
- 注意力权重接近均匀分布：

$$
A_{ij} \approx \frac{1}{n} + \epsilon, \quad \epsilon \sim \mathcal{N}(0, \sigma^2)
$$

其中 $\sigma$ 很小。

**直觉**：每个词对所有其他词的关注度几乎相等，模型还没有学到任何结构。

### 4.2 阶段 2：早期训练（Epoch 1-10）

**观察**：
- 损失快速下降
- $W^Q, W^K, W^V$ 开始分化
- $\|W^Q - W^K\|_F$ 增大（Frobenius 范数）

**注意力模式**：
- 开始出现局部偏好（相邻词权重略高）
- 但仍然较为分散

**数学刻画**：

定义"角色分化度"：

$$
D(t) = \|W^Q(t) - W^K(t)\|_F = \sqrt{\sum_{i,j} (W^Q_{ij}(t) - W^K_{ij}(t))^2}
$$

此阶段：$D(t)$ 快速增长。

### 4.3 阶段 3：中期训练（Epoch 10-50）

**注意力模式稳定化**：
- 不同层学习不同抽象层次：
  - **浅层**（Layer 1-3）：短程依赖（词性、相邻关系、语块）
  - **中层**（Layer 4-8）：中程依赖（句法结构、从句关系）
  - **深层**（Layer 9-12）：长程依赖（主谓一致、指代消解、主题跟踪）

**实证研究**（Visualizing Attention in Transformer Models）表明：
- 第 1 层的注意力高度局部（邻近词）
- 第 12 层的注意力呈现长程跳跃模式

### 4.4 阶段 4：收敛（Epoch 50+）

**特点**：
- $W^Q, W^K, W^V$ 趋于稳定
- $D(t)$ 达到平台期
- 注意力模式清晰、可解释

**可视化示例**（以 "it" 为例）：

收敛后的注意力权重：

$$
A_{\text{it}, :} = [0.02, 0.85, 0.01, \ldots, 0.03, 0.06]
$$

其中：
- "animal" 获得 0.85 的权重（主要关注）
- "tired" 获得 0.06 的权重（次要关注）
- 其他词权重很小

这表明模型学会了**指代消解**。

### 4.5 训练动力学的理论视角

从优化理论角度，可以将 $W^Q, W^K$ 的演化视为在损失地形 (loss landscape) 上的运动：

$$
\mathcal{L}(W^Q, W^K, W^V, \ldots)
$$

- **初始点**：$W^Q \approx W^K$（接近高对称性的鞍点）
- **对称性破缺**：由于梯度噪声（SGD 的随机性），系统脱离鞍点
- **吸引子**：训练收敛到低损失的**非对称配置**

类比物理学中的**自发对称性破缺**（Spontaneous Symmetry Breaking）。

---

## 5. 点积相似度的几何解释与复杂度分析

### 5.1 几何解释

点积可以表示为：

$$
q \cdot k = \|q\| \|k\| \cos\theta
$$

其中 $\theta$ 是向量 $q$ 和 $k$ 在 $d_k$ 维空间中的夹角。

**几何意义**：
- $\theta = 0°$（方向一致）：$\cos\theta = 1$，点积最大
- $\theta = 90°$（正交）：$\cos\theta = 0$，点积为 0
- $\theta = 180°$（方向相反）：$\cos\theta = -1$，点积最小

### 5.2 缩放后的几何解释

缩放后的点积：

$$
\frac{q \cdot k}{\sqrt{d_k}} = \frac{\|q\| \|k\|}{\sqrt{d_k}} \cos\theta
$$

**典型情况**：如果 $\|q\| \approx \|k\| \approx \sqrt{d_k}$（这在标准初始化下常见），则：

$$
\frac{q \cdot k}{\sqrt{d_k}} \approx \frac{d_k}{\sqrt{d_k}} \cos\theta = \sqrt{d_k} \cos\theta
$$

相似度主要由**角度 $\theta$** 决定，而幅度的影响被归一化。

### 5.3 计算复杂度分析

#### **点积注意力（Scaled Dot-Product Attention）**

**步骤 1**：计算 $QK^T$

- 矩阵乘法：$(n \times d_k) \times (d_k \times n) = (n \times n)$
- 复杂度：$O(n^2 d_k)$

**步骤 2**：Softmax

- 对 $n \times n$ 矩阵的每一行归一化
- 复杂度：$O(n^2)$

**步骤 3**：计算 $AV$

- 矩阵乘法：$(n \times n) \times (n \times d_v) = (n \times d_v)$
- 复杂度：$O(n^2 d_v)$

**总复杂度**：

$$
O(n^2 d_k) + O(n^2) + O(n^2 d_v) = O(n^2 d)
$$

其中 $d = \max(d_k, d_v)$（通常 $d_k = d_v = d_{\text{model}}/h$，$h$ 是头数）。

#### **加法注意力（Bahdanau Attention）**

公式：

$$
\text{score}(q, k) = v^T \tanh(W_1 q + W_2 k)
$$

其中 $W_1, W_2 \in \mathbb{R}^{d_{\text{hidden}} \times d}$，$v \in \mathbb{R}^{d_{\text{hidden}}}$。

**计算每个词对 $(i, j)$ 的分数**：

1. 计算 $W_1 q_i$：$O(d^2)$
2. 计算 $W_2 k_j$：$O(d^2)$
3. 加法和 $\tanh$：$O(d)$
4. 计算 $v^T \cdot$：$O(d)$

**每个词对**：$O(d^2)$

**总共 $n^2$ 个词对**：

$$
O(n^2 d^2)
$$

#### **对比**

| 方法 | 时间复杂度 | 空间复杂度 |
|:--:|:--:|:--:|
| **点积注意力** | $O(n^2 d)$ | $O(n^2 + nd)$ |
| **加法注意力** | $O(n^2 d^2)$ | $O(n^2 + nd)$ |

**结论**：点积注意力少一个 $d$ 因子，**更快**。

### 5.4 硬件友好性

**点积注意力的优势**：

1. **矩阵乘法高度优化**：
   - BLAS 库（cuBLAS、MKL）对 GEMM（通用矩阵乘法）极度优化
   - GPU/TPU 的 Tensor Core 专为矩阵乘法设计

2. **内存访问模式**：
   - 连续内存访问，缓存友好
   - 加法注意力需要逐元素计算，内存跳跃

3. **并行性**：
   - 矩阵乘法天然并行
   - 加法注意力的 $\tanh$ 是逐元素操作，并行度受限

### 5.5 为什么不用余弦相似度？

余弦相似度：

$$
\text{cosine}(q, k) = \frac{q \cdot k}{\|q\| \|k\|}
$$

**问题**：

1. **额外计算开销**：
   - 需要计算每个向量的范数 $\|q\|, \|k\|$
   - 复杂度增加 $O(nd)$

2. **梯度复杂性**：
   - 余弦相似度的梯度涉及除法，数值不稳定
   - 点积的梯度简单：$\frac{\partial (q \cdot k)}{\partial q} = k$

3. **经验表现**：
   - 实验表明点积 + 缩放与余弦相似度性能相当
   - 点积更简单，工程上更优

---

## 6. 小结：SDPA 的三个支柱

Scaled Dot-Product Attention 的设计建立在三个核心支柱上：

### 6.1 支柱表格

| 设计选择 | 数学依据 | 效果 |
|:--:|:---|:---|
| **点积相似度** | 复杂度 $O(n^2 d)$ vs $O(n^2 d^2)$<br>矩阵乘法硬件优化 | 计算高效、硬件友好 |
| **缩放因子 $\sqrt{d_k}$** | $\text{Var}(\frac{s}{\sqrt{d_k}}) = 1$<br>防止 Softmax 饱和 | 方差稳定、梯度健康、训练收敛 |
| **Q-K-V 分离** | 梯度不对称：$\frac{\partial \mathcal{L}}{\partial Q} \neq \frac{\partial \mathcal{L}}{\partial K}$<br>对称性破缺 | 有向关系建模、表达力强、语义角色分化 |

### 6.2 核心洞察

1. **$\sqrt{d_k}$ 不是经验调参，而是严格的统计学结论**
   - 方差随维度线性增长的必然后果
   - 保证模型在任意维度下稳定训练

2. **Q 和 K 初始对称，但训练后必然分化**
   - 梯度结构的不对称性驱动演化
   - 数据驱动的语义角色涌现

3. **点积不仅简单，而且数学上优雅**
   - 几何直观（角度相似度）
   - 计算高效（矩阵乘法）
   - 硬件友好（GPU/TPU 优化）

### 6.3 工程与理论的统一

SDPA 的设计体现了深度学习的一个核心哲学：

> **优雅的数学往往带来高效的工程实现。**

- **理论保证**（方差稳定性）→ **训练稳定**
- **简单形式**（点积）→ **计算高效**
- **对称破缺**（Q-K 分化）→ **表达能力**

这三个支柱共同支撑起 Transformer 的强大性能，使其成为现代 AI 的基石。

---

## 参考与延伸阅读

1. **原始论文**：Vaswani et al., "Attention is All You Need", NeurIPS 2017
2. **初始化理论**：Glorot & Bengio, "Understanding the difficulty of training deep feedforward neural networks", AISTATS 2010
3. **注意力可视化**：Vig, J., "A Multiscale Visualization of Attention in the Transformer Model", ACL 2019
4. **复杂度分析**：Tay et al., "Efficient Transformers: A Survey", ACM Computing Surveys 2022

---

**最后更新**：2025-11-07

