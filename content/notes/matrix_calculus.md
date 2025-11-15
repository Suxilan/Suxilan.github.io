---
title: "深度学习中常见的矩阵微分（Matrix Calculus）"
date: 2025-11-07T16:00:00+08:00
draft: false
tags: ["Deep Learning", "矩阵微分", "Matrix Calculus", "反向传播"]
categories: ["技术笔记"]
series: []
author: "Suxilan"
ShowToc: true
TocWide: true
comments: true
description: "矩阵微积分在深度学习中的应用：从布局约定到微分-迹法，完整推导反向传播的数学基础"
summary: "常见的矩阵求导推导 + 速查表，掌握深度学习中梯度计算的数学原理"
---

## 引言

矩阵微积分（Matrix Calculus）是深度学习中反向传播（Backpropagation）的数学基础。这里我参考了各个优质博主的回答并经过AI大人的整合，严格推导标量对向量、标量对矩阵求导的核心公式，并整理成便于查阅的速查表。

**核心目标**：理解如何计算标量损失函数 $L$ 对向量参数（如偏置 $\mathbf{b}$）或矩阵参数（如权重 $\mathbf{W}$）的梯度，以用于梯度下降优化。

---

## 一、所属数学知识

这部分内容属于**多元微积分（Multivariable Calculus）** 在 **线性代数（Linear Algebra）** 中的应用，通常被称为：

- **矩阵微积分**（Matrix Calculus）
- **矩阵求导**（Matrix Differentiation）

它专门研究向量、矩阵的函数（通常输出为标量或向量）的微分问题。

在深度学习中，我们最关心的场景是：**一个标量损失函数（Scalar Loss, $L$）对向量参数（如偏置 $\mathbf{b}$）或矩阵参数（如权重 $\mathbf{W}$）求导（即计算梯度）**，以用于梯度下降。

---

## 二、核心概念：布局约定（Layout Conventions）

这是学习矩阵求导**最重要**且**最容易混淆**的地方。当对向量求导时，结果的维度布局有两种约定：

1. **分子布局 (Numerator Layout)**：导数的形状由**分子**决定。
2. **分母布局 (Denominator Layout)**：导数的形状由**分母**决定。

### 常规约定：分母布局

在深度学习和反向传播的推导中，**分母布局**是事实标准。

**原因**：它使得**梯度的形状与其所求导的变量的形状完全一致**。

- 例如：标量 $L$ 对列向量 $\mathbf{w}$ ($n \times 1$) 求导，$\frac{\partial L}{\partial \mathbf{w}}$ 也是一个 $n \times 1$ 的列向量。
- 这使得梯度下降更新 $\mathbf{w} \leftarrow \mathbf{w} - \alpha \nabla_{\mathbf{w}} L$ 在维度上天然匹配。

### 核心约定（基于分母布局）

1. **所有梯度（如 $\frac{\partial L}{\partial \mathbf{x}}$）默认是列向量**，与 $\mathbf{x}$ 形状一致。
2. **所有矩阵导数（如 $\frac{\partial L}{\partial \mathbf{W}}$）都满足 $df = \text{tr}((\frac{\partial f}{\partial \mathbf{X}})^\mathrm{T} d\mathbf{X})$ 这个"读数规则"**。
   
   - 标量函数对矩阵的全微分最朴素的写法是
     $$
     \mathrm{d}f = \sum_{i,j} \frac{\partial f}{\partial X_{ij}} \, \mathrm{d}X_{ij}
     $$
     又因为对任意同形矩阵有
     $$
     \mathrm{tr}(A^\mathrm{T} \mathrm{d}X) = \sum_{i,j} A_{ij} \, \mathrm{d}X_{ij},
     $$
     所以我们可以把全微分写成
     $$
     \mathrm{d}f = \mathrm{tr}\big( (\partial f / \partial X)^\mathrm{T} \mathrm{d}X \big)
     $$
   
   - 这个规则是"微分-迹"法的基石：我们求出 $f$ 的全微分 $df$，并将其"凑"成 $\text{tr}(\mathbf{A}^\mathrm{T} d\mathbf{X})$ 的形式，那么 $\mathbf{A}$ 就是我们想要的导数 $\frac{\partial f}{\partial \mathbf{X}}$。

---

## 三、知识点与详细推导（深度学习经典情况）

### 准备工作：定义（分母布局）

- $y$ 是标量，$\mathbf{x}$ 是 $n \times 1$ **列**向量，$\mathbf{W}$ 是 $m \times n$ 矩阵。
- **标量对向量求导**：$\frac{\partial y}{\partial \mathbf{x}}$ 是 $n \times 1$ 列向量。
- **标量对矩阵求导**：$\frac{\partial y}{\partial \mathbf{W}}$ 是 $m \times n$ 矩阵（与 $\mathbf{W}$ 同型）。

---

### 推导情况一：线性函数 ($y = \mathbf{a}^\mathrm{T} \mathbf{x}$)

**问题**：设 $y = \mathbf{a}^\mathrm{T} \mathbf{x}$，其中 $\mathbf{a}$ 和 $\mathbf{x}$ 都是 $n \times 1$ 的列向量。求 $\frac{\partial y}{\partial \mathbf{x}}$。

#### **推导（方法一：展开法）**

1. 展开 $y$：$y = \sum_{i=1}^n a_i x_i$
2. 逐元素求偏导：$\frac{\partial y}{\partial x_k} = a_k$
3. 按分母布局组合成列向量：$\frac{\partial y}{\partial \mathbf{x}} = [a_1, \dots, a_n]^\mathrm{T} = \mathbf{a}$

#### **推导（方法二：微分法）**

1. 求 $y$ 的全微分：$d y = d(\mathbf{a}^\mathrm{T} \mathbf{x}) = \mathbf{a}^\mathrm{T} d\mathbf{x}$
2. 根据向量微分的"**读数规则**" $dy = (\nabla_{\mathbf{x}} y)^\mathrm{T} d\mathbf{x}$，我们对比可得：
   $$(\nabla_{\mathbf{x}} y)^\mathrm{T} = \mathbf{a}^\mathrm{T} \implies \nabla_{\mathbf{x}} y = \mathbf{a}$$

**结论**：
$$
\frac{\partial (\mathbf{a}^\mathrm{T} \mathbf{x})}{\partial \mathbf{x}} = \frac{\partial (\mathbf{x}^\mathrm{T} \mathbf{a})}{\partial \mathbf{x}} = \mathbf{a}
$$

>  对于向量、梯度，通常以列向量的形式进行表达，比如上述的$\mathbf{a}$、$\mathbf{x}$。因此规定以下“读数规则”
>
>  **向量全微分读数规则：** 对**标量**函数 $f(\mathbf{x})$，若能把全微分写成
>
>  $$
>  \mathrm{d}f = \mathbf{v}^\mathrm{T} \mathrm{d}\mathbf{x},
>  $$
>
>  则有 $\nabla_{\mathbf{x}} f = \mathbf{v}$。若一开始得到的不是这个形状，比如 $(\mathrm{d}\mathbf{x})^\mathrm{T} \mathbf{u}$，由于这是标量，可转置为 $\mathbf{u}^\mathrm{T} \mathrm{d}\mathbf{x}$，再按上式读出梯度。
>
>  **矩阵全微分读数规则：** 对**标量**函数 $f(X)$，若能写成
>
>  $$
>  \mathrm{d}f = \mathrm{tr}(A^\mathrm{T} \mathrm{d}X),
>  $$
>
>  则 $\partial f / \partial X = A$。这里同样利用了“迹是标量，标量可以转置、可以循环”的性质来把 $\mathrm{d}X$ 调到最后。

---

### 推导情况二：二次型 ($y = \mathbf{x}^\mathrm{T} \mathbf{A} \mathbf{x}$)

**问题**：设 $y = \mathbf{x}^\mathrm{T} \mathbf{A} \mathbf{x}$，其中 $\mathbf{x}$ 是 $n \times 1$ **列**向量，$\mathbf{A}$ 是 $n \times n$ 矩阵。求 $\frac{\partial y}{\partial \mathbf{x}}$。

#### **推导（方法一：展开法/索引法）**

1. 先把标量 $y$ 全部展开到元素级：
   $$
   y = \sum_{i} \sum_{j} A_{ij} x_i x_j
   $$
   这一步只是把“行向量 × 矩阵 × 列向量”的乘法写成求和，方便对单个分量求偏导。

2. 我们要的是 $\frac{\partial y}{\partial x_k}$ （第$k$个分量的偏导）。对上式逐项求偏导：
   $$
   \frac{\partial y}{\partial x_k} = \frac{\partial}{\partial x_k} (\sum_{i} \sum_{j} A_{ij} x_i x_j)
   $$
   只有含有$x_k$的项才会产生非零导数。

3. 一个项长这样：$A_{ij} x_i x_j$。它对 $x_k$ 有两种“含法”：

   - **情况1：** 如果 $i = k$，这个项是 $A_{kj} x_k x_j$，对 $x_k$ 求导得到 $A_{kj} x_j$；
   - **情况2：** 如果 $j = k$，这个项是 $A_{ik} x_i x_k$，对 $x_k$ 求导得到 $A_{ik} x_i$。

   所以所有对 $x_k$ 有贡献的项加起来就是这两大堆：
   $$
   \frac{\partial y}{\partial x_k} = \sum_{j} A_{kj} x_j + \sum_{i} A_{ik} x_i
   $$
4. 这两个和其实都有熟悉的向量形式：

   - $\sum_{j} A_{kj} x_j$ 是矩阵 $\mathbf{A}$ 乘向量 $\mathbf{x}$ 的第 $k$ 个分量，也就是 $(\mathbf{A}\mathbf{x})_k$；
   - $\sum_{i} A_{ik} x_i$ 是 $\mathbf{A}^\mathrm{T}\mathbf{x}$ 的第 $k$ 个分量，也就是 $(\mathbf{A}^\mathrm{T} \mathbf{x})_k$。

   因此
   $$
   \frac{\partial y}{\partial x_k} = (\mathbf{A}\mathbf{x})_k + (\mathbf{A}^\mathrm{T} \mathbf{x})_k
   $$
5. 把所有分量 $k=1,\dots,n$ 拼成列向量，就是
   $$
   \frac{\partial y}{\partial \mathbf{x}}
   = \mathbf{A} \mathbf{x} + \mathbf{A}^\mathrm{T} \mathbf{x}
   = (\mathbf{A} + \mathbf{A}^\mathrm{T})\mathbf{x}
   $$

6. 组合成列向量：
   $$
   \frac{\partial y}{\partial \mathbf{x}} = \mathbf{A} \mathbf{x} + \mathbf{A}^\mathrm{T} \mathbf{x} = (\mathbf{A} + \mathbf{A}^\mathrm{T}) \mathbf{x}
   $$

#### **推导（方法二：微分法 - 更简洁）**

1. 求 $y$ 的全微分（使用 $d(\mathbf{u}^\mathrm{T} \mathbf{v}) = (d\mathbf{u})^\mathrm{T} \mathbf{v} + \mathbf{u}^\mathrm{T} d\mathbf{v}$）：
   $$
   \begin{aligned}
   dy &= d(\mathbf{x}^\mathrm{T} (\mathbf{A} \mathbf{x})) \\
   dy &= (d\mathbf{x})^\mathrm{T} (\mathbf{A} \mathbf{x}) + (\mathbf{x}^\mathrm{T}) d(\mathbf{A} \mathbf{x}) \\
   dy &= (d\mathbf{x})^\mathrm{T} \mathbf{A} \mathbf{x} + \mathbf{x}^\mathrm{T} \mathbf{A} d\mathbf{x}
   \end{aligned}
   $$
2. $dy$ 是标量，且观察可得这两项都是标量，标量等于其自身的转置，所以 $(d\mathbf{x})^\mathrm{T} \mathbf{A} \mathbf{x} = (\mathbf{x}^\mathrm{T} \mathbf{A}^\mathrm{T} d\mathbf{x})^\mathrm{T} = \mathbf{x}^\mathrm{T} \mathbf{A}^\mathrm{T} d\mathbf{x}$。
   $$dy = \mathbf{x}^\mathrm{T} \mathbf{A}^\mathrm{T} d\mathbf{x} + \mathbf{x}^\mathrm{T} \mathbf{A} d\mathbf{x}$$
3. $$dy = (\mathbf{x}^\mathrm{T} (\mathbf{A}^\mathrm{T} + \mathbf{A})) d\mathbf{x}$$
4. 对比 $dy = (\nabla_{\mathbf{x}} y)^\mathrm{T} d\mathbf{x}$，可得：
   $$(\nabla_{\mathbf{x}} y)^\mathrm{T} = \mathbf{x}^\mathrm{T} (\mathbf{A}^\mathrm{T} + \mathbf{A})$$
   $$\nabla_{\mathbf{x}} y = (\mathbf{A}^\mathrm{T} + \mathbf{A})^\mathrm{T} \mathbf{x} = (\mathbf{A} + \mathbf{A}^\mathrm{T}) \mathbf{x}$$

**结论**：

$$
\frac{\partial (\mathbf{x}^\mathrm{T} \mathbf{A} \mathbf{x})}{\partial \mathbf{x}} = (\mathbf{A} + \mathbf{A}^\mathrm{T}) \mathbf{x}
$$

**特例（重要）**：如果 $\mathbf{A}$ 是对称矩阵（$\mathbf{A} = \mathbf{A}^\mathrm{T}$），则：

$$
\frac{\partial (\mathbf{x}^\mathrm{T} \mathbf{A} \mathbf{x})}{\partial \mathbf{x}} = 2 \mathbf{A} \mathbf{x} \quad (\text{if } \mathbf{A} = \mathbf{A}^\mathrm{T})
$$

---

### 推导情况三：最小二乘法 (MSE Loss)

**问题**：损失函数 $L = \Vert\mathbf{y} - \mathbf{X} \mathbf{w}\Vert^2$，其中 $\mathbf{y}$ ($m \times 1$), $\mathbf{X}$ ($m \times n$), $\mathbf{w}$ ($n \times 1$)。求 $\frac{\partial L}{\partial \mathbf{w}}$。

> 这里$\mathbf{y}$可以理解为标签（$m$维），$\mathbf{X}$为输入的特征向量，$\mathbf{w}$为模型参数可以简单理解为一个线性层

#### **推导**

1. 改写 $L = (\mathbf{y} - \mathbf{X} \mathbf{w})^\mathrm{T} (\mathbf{y} - \mathbf{X} \mathbf{w})$
2. 展开 $L = \mathbf{y}^\mathrm{T} \mathbf{y} - \mathbf{y}^\mathrm{T} \mathbf{X} \mathbf{w} - \mathbf{w}^\mathrm{T} \mathbf{X}^\mathrm{T} \mathbf{y} + \mathbf{w}^\mathrm{T} \mathbf{X}^\mathrm{T} \mathbf{X} \mathbf{w}$
3. 合并中间两项（它们互为转置，都是标量）：
   $$L = \mathbf{y}^\mathrm{T} \mathbf{y} - 2 (\mathbf{X}^\mathrm{T} \mathbf{y})^\mathrm{T} \mathbf{w} + \mathbf{w}^\mathrm{T} (\mathbf{X}^\mathrm{T} \mathbf{X}) \mathbf{w}$$
4. 对 $\mathbf{w}$ 求导：
   - 第一项（常数）$\to \mathbf{0}$
   - 第二项（情况一 $y=\mathbf{a}^\mathrm{T} \mathbf{x}$，$\mathbf{a} = 2 (\mathbf{X}^\mathrm{T} \mathbf{y})$）$\to -2 \mathbf{X}^\mathrm{T} \mathbf{y}$
   - 第三项（情况二 $y=\mathbf{x}^\mathrm{T} \mathbf{A} \mathbf{x}$，$\mathbf{A} = \mathbf{X}^\mathrm{T} \mathbf{X}$ 是对称矩阵）$\to 2 (\mathbf{X}^\mathrm{T} \mathbf{X}) \mathbf{w}$
5. 合并：
   $$\frac{\partial L}{\partial \mathbf{w}} = -2 \mathbf{X}^\mathrm{T} \mathbf{y} + 2 \mathbf{X}^\mathrm{T} \mathbf{X} \mathbf{w} = 2 \mathbf{X}^\mathrm{T} (\mathbf{X} \mathbf{w} - \mathbf{y})$$

**结论**：

$$
\frac{\partial \Vert\mathbf{y} - \mathbf{X} \mathbf{w}\Vert^2}{\partial \mathbf{w}} = 2 \mathbf{X}^\mathrm{T} (\mathbf{X} \mathbf{w} - \mathbf{y})
$$

> **notion**：在深度学习中，更常用 $\displaystyle L = \frac{1}{2} \Vert\mathbf{y} - \mathbf{X} \mathbf{w}\Vert^2$ 作为损失，
> 此时梯度为： $\frac{\partial L}{\partial \mathbf{w}} = \mathbf{X}^\mathrm{T} (\mathbf{X} \mathbf{w} - \mathbf{y})$，形式更简洁。

---

### 推导情况四：全连接层（标量对矩阵）

**问题**：神经网络反向传播的核心。

- $L$ 是标量。
- $\mathbf{X} \in \mathbb{R}^{m \times n}$ (m条样本，n维特征)
- $\mathbf{W} \in \mathbb{R}^{n \times p}$ (权重)
- $\mathbf{Z} \in \mathbb{R}^{m \times p}$ (输出), 且 $\mathbf{Z} = \mathbf{X} \mathbf{W}$
- 已知上游梯度 $\frac{\partial L}{\partial \mathbf{Z}}$ (与 $\mathbf{Z}$ 同型， $m \times p$)。
- 求下游梯度 $\frac{\partial L}{\partial \mathbf{W}}$ (与 $\mathbf{W}$ 同型， $n \times p$)。

#### **推导（方法：微分-迹法）**

1. 根据链式法则和我们的"读数规则" (Section II)，$L$ 对 $\mathbf{Z}$ 的微分 $dL$ 可以写为：
   $$
   dL = \text{tr} \left( \left( \frac{\partial L}{\partial \mathbf{Z}} \right)^\mathrm{T} d\mathbf{Z} \right)
   $$

2. 我们知道 $\mathbf{Z} = \mathbf{X} \mathbf{W}$。求 $\mathbf{Z}$ 的微分（假设 $\mathbf{X}$ 是常量输入）：
   $$
   d\mathbf{Z} = d(\mathbf{X} \mathbf{W}) = \mathbf{X} d\mathbf{W}
   $$

3. 将 $d\mathbf{Z}$ 代入 $dL$：
   $$
   dL = \text{tr} \left( \left( \frac{\partial L}{\partial \mathbf{Z}} \right)^\mathrm{T} \mathbf{X} d\mathbf{W} \right)
   $$

5. 矩阵转置的规则 $\text{tr}(AB) = \text{tr}((B^T A^T)^T)$，整理成“**读数规则**”的形式可得：
   $$
   dL = \text{tr} \left( (\mathbf{X}^\mathrm{T} \frac{\partial L}{\partial \mathbf{Z}})^\mathrm{T} d\mathbf{W} \right)
   $$
   
5. 现在 $dL$ 完美匹配了我们的"读数规则" $dL = \text{tr}((\frac{\partial L}{\partial \mathbf{W}})^\mathrm{T} d\mathbf{W})$。

6. 我们可以"读"出梯度：
   $$
   \boxed{\frac{\partial L}{\partial W} = X^\top \frac{\partial L}{\partial Z}}
   $$

**结论**：

$$
\text{若 } \mathbf{Z} = \mathbf{X} \mathbf{W}, \quad \text{则 } \frac{\partial L}{\partial \mathbf{W}} = \mathbf{X}^\mathrm{T} \frac{\partial L}{\partial \mathbf{Z}}
$$

#### **补充：偏置项 $\mathbf{b}$ 的梯度**

假设全连接层为 $\mathbf{Z} = \mathbf{X} \mathbf{W} + \mathbf{1} \mathbf{b}^\mathrm{T}$，其中 $\mathbf{b} \in \mathbb{R}^p$ ( $p \times 1$ 列向量)，$\mathbf{1}$ 是 $m \times 1$ 的全1向量，$\mathbf{1} \mathbf{b}^\mathrm{T}$ 实现了广播（broadcast）。

$$
\begin{aligned}
d\mathbf{Z} &= d(\mathbf{X} \mathbf{W}) + d(\mathbf{1} \mathbf{b}^\mathrm{T}) = \mathbf{X} d\mathbf{W} + \mathbf{1} d\mathbf{b}^\mathrm{T} \\
dL &= \text{tr}((\frac{\partial L}{\partial \mathbf{Z}})^\mathrm{T} d\mathbf{Z}) \\
&= \text{tr}((\frac{\partial L}{\partial \mathbf{Z}})^\mathrm{T} \mathbf{X} d\mathbf{W}) + \text{tr}((\frac{\partial L}{\partial \mathbf{Z}})^\mathrm{T} \mathbf{1} d\mathbf{b}^\mathrm{T})
\end{aligned}
$$

我们只看 $\mathbf{b}$ 的部分，并注意这三个的形状：

- $(\partial L/\partial Z)^\top$: $p\times m$
- $\mathbf{1}$: $m\times 1$
- $\mathrm{d}b^\top$: $1\times p$

$$
\begin{aligned}
dL_b &= \text{tr}((\frac{\partial L}{\partial \mathbf{Z}})^\mathrm{T} \mathbf{1} d\mathbf{b}^\mathrm{T}) \\
&= \text{tr}(d\mathbf{b}^\mathrm{T} (\frac{\partial L}{\partial \mathbf{Z}})^\mathrm{T} \mathbf{1}) \\
&= \text{tr}( (\frac{\partial L}{\partial \mathbf{Z}})^\mathrm{T} \mathbf{1})^\mathrm{T} d\mathbf{b} )
\end{aligned}
$$

对比“读数规则” $dL_b = (\frac{\partial L}{\partial \mathbf{b}})^\mathrm{T} d\mathbf{b}$，可得：

$$\frac{\partial L}{\partial \mathbf{b}} = (\frac{\partial L}{\partial \mathbf{Z}})^\mathrm{T} \mathbf{1}$$

**结论（偏置）**：
$$
\frac{\partial L}{\partial \mathbf{b}} = (\frac{\partial L}{\partial \mathbf{Z}})^\mathrm{T} \mathbf{1} = \text{sum}(\frac{\partial L}{\partial \mathbf{Z}}, \text{axis}=0)^\mathrm{T}
$$

（即 $\frac{\partial L}{\partial \mathbf{Z}}$ 沿着**样本维度(axis=0)** 求和，再转置成 $p \times 1$ 的列向量）

---

### 推导情况五：逐元素激活函数（向量对向量求导）

**问题**：在反向传播中，我们经常遇到一个向量（如激活值 $\mathbf{a}$）依赖于另一个向量（如 $\mathbf{z}$）的情况。这就需要使用“向量对向量”的求导，其结果是一个**雅可比矩阵**。设 $\mathbf{z}$ 是 $n \times 1$ 向量，激活函数 $\sigma(\cdot)$ 逐元素（element-wise）作用于 $\mathbf{z}$ 得到 $\mathbf{a} = \sigma(\mathbf{z})$。
已知 $\frac{\partial L}{\partial \mathbf{a}}$，求 $\frac{\partial L}{\partial \mathbf{z}}$。

> #### 定义：雅可比矩阵 (Jacobian Matrix)
>
> 
>
> 向量 $\mathbf{y} \in \mathbb{R}^m$ 对向量 $\mathbf{x} \in \mathbb{R}^n$ 求导，在我们的**分母布局**下（导数形状由分母$\mathbf{x}$决定），结果是一个 $n \times m$ 的雅可比矩阵。
> $$
> \frac{\partial \mathbf{y}}{\partial \mathbf{x}} = \begin{bmatrix} \frac{\partial y_1}{\partial x_1} & \frac{\partial y_2}{\partial x_1} & \dots & \frac{\partial y_m}{\partial x_1} \\ \frac{\partial y_1}{\partial x_2} & \frac{\partial y_2}{\partial x_2} & \dots & \frac{\partial y_m}{\partial x_2} \\ \vdots & \vdots & \ddots & \vdots \\ \frac{\partial y_1}{\partial x_n} & \frac{\partial y_2}{\partial x_n} & \dots & \frac{\partial y_m}{\partial x_n} \end{bmatrix}_{n \times m}
> $$
>
> 链式法则应用：
>
> 假设有 $L \to \mathbf{y} \to \mathbf{x}$（$L$是标量），我们有：
>
> $$
> \frac{\partial L}{\partial \mathbf{x}} = \frac{\partial \mathbf{y}}{\partial \mathbf{x}} \frac{\partial L}{\partial \mathbf{y}}
> $$

**推导**：

1. 根据上面的链式法则：$\frac{\partial L}{\partial \mathbf{z}} = \frac{\partial \mathbf{a}}{\partial \mathbf{z}} \frac{\partial L}{\partial \mathbf{a}}$。

2. 我们来求解雅可比矩阵 $\frac{\partial \mathbf{a}}{\partial \mathbf{z}}$。

   $\mathbf{a} = [\sigma(z_1), \sigma(z_2), \dots, \sigma(z_n)]^\mathrm{T}$

3. 根据雅可比矩阵的定义（分母布局），$\frac{\partial \mathbf{a}}{\partial \mathbf{z}}$ 是一个 $n \times n$ 矩阵，其 $(i, j)$ 元素是 $\frac{\partial a_j}{\partial z_i}$。

   - **如果 $i \neq j$**：$\frac{\partial a_j}{\partial z_i} = \frac{\partial \sigma(z_j)}{\partial z_i} = 0$。（因为 $\sigma$ 是逐元素的，$a_j$ 只依赖于 $z_j$，与 $z_i$ 无关）。
   - **如果 $i = j$**：$\frac{\partial a_i}{\partial z_i} = \frac{\partial \sigma(z_i)}{\partial z_i} = \sigma'(z_i)$。

4. 因此，这个雅可比矩阵是一个对角矩阵：
$$
\frac{\partial \mathbf{a}}{\partial \mathbf{z}} = \begin{bmatrix} \sigma'(z_1) & 0 & \dots & 0 \\ 0 & \sigma'(z_2) & \dots & 0 \\ \vdots & \vdots & \ddots & \vdots \\ 0 & 0 & \dots & \sigma'(z_n) \end{bmatrix} = \text{diag}(\sigma'(\mathbf{z}))
$$

5. 将这个对角矩阵代入链式法则：
$$
\frac{\partial L}{\partial \mathbf{z}} = \text{diag}(\sigma'(\mathbf{z})) \frac{\partial L}{\partial \mathbf{a}} = \begin{bmatrix} \sigma'(z_1) & \dots & 0 \\ \vdots & \ddots & \vdots \\ 0 & \dots & \sigma'(z_n) \end{bmatrix} \begin{bmatrix} \frac{\partial L}{\partial a_1} \\ \vdots \\ \frac{\partial L}{\partial a_n} \end{bmatrix} = \begin{bmatrix} \sigma'(z_1) \frac{\partial L}{\partial a_1} \\ \vdots \\ \sigma'(z_n) \frac{\partial L}{\partial a_n} \end{bmatrix}
$$
6. 这个“对角矩阵乘以向量”的结果，等价于两个向量进行**逐元素相乘**。

**结论**：

$$
\text{若 } \mathbf{a} = \sigma(\mathbf{z}) \text{ (逐元素)}, \quad \text{则 } \frac{\partial L}{\partial \mathbf{z}} = \frac{\partial L}{\partial \mathbf{a}} \odot \sigma'(\mathbf{z})
$$

*其中 $\odot$ 表示逐元素乘法（Hadamard 积）。*

> 注：逐元素函数的雅可比是对角矩阵。但并非所有向量函数都如此。例如在推导 Softmax 梯度时，$\frac{\partial \mathbf{p}}{\partial \mathbf{z}}$ (Softmax 的雅可比) 是一个满矩阵（非对角），因为 $\mathbf{p}$ 的每个分量都依赖于 $\mathbf{z}$ 的所有分量。 此外有趣的是，当将其与Cross-Entropy 损失函数组合在一起时，其反向传播的梯度会惊人地简化。
>
> 目标：
>
> 给定 $L \to \mathbf{p} \to \mathbf{z}$，其中：
>
> 1. $\mathbf{p} = \text{Softmax}(\mathbf{z})$
>
> 2. $L = \text{CrossEntropy}(\mathbf{p}, \mathbf{y}) = -\sum_{i} y_i \log(p_i)$（$\mathbf{y}$ 是 one-hot 标签向量）
>
>    我们要求解 $\frac{\partial L}{\partial \mathbf{z}}$。
>
> 根据链式法则：$\frac{\partial L}{\partial \mathbf{z}} = \frac{\partial \mathbf{p}}{\partial \mathbf{z}} \frac{\partial L}{\partial \mathbf{p}}$
>
> ------
>
> **步骤 1：求 $\frac{\partial L}{\partial \mathbf{p}}$ (损失对 Softmax 输出的梯度)**
> $$
> L = -\sum_{k} y_k \log(p_k)\
> $$
> 我们求 $L$ 对 $p_j$ 的偏导：
> $$
> \frac{\partial L}{\partial p_j} = \frac{\partial}{\partial p_j} \left( -\sum_{k} y_k \log(p_k) \right)
> $$
> 将 $L$ 视为 $p_1, \dots, p_n$ 的多元函数，只有 $k=j$ 的那一项求导不为零：
> $$
> \frac{\partial L}{\partial p_j} = -y_j \frac{1}{p_j}
> $$
> 将所有 $j$ 组合成一个列向量（分母布局）：
> $$
> \frac{\partial L}{\partial \mathbf{p}} = \begin{bmatrix} -y_1/p_1 \\ -y_2/p_2 \\ \vdots \\ -y_n/p_n \end{bmatrix}
> $$
>
> ------
>
> **步骤 2：求 $\frac{\partial \mathbf{p}}{\partial \mathbf{z}}$ (Softmax 的雅可比矩阵)**
> $$
> p_j = \frac{e^{z_j}}{\sum_{k} e^{z_k}}
> $$
> 我们需要求解雅可比矩阵的 $(i, j)$ 项，即 $\frac{\partial p_j}{\partial z_i}$（注意分母布局，$i$ 是行索引，$j$ 是列索引）。
>
> 情况 1：$i = j$ (对角线元素)
> $$
> \frac{\partial p_i}{\partial z_i} = \frac{\partial}{\partial z_i} \left( \frac{e^{z_i}}{\sum_{k} e^{z_k}} \right)
> $$
> 使用商法则：
> $$
> \begin{aligned}
> &\frac{\partial p_i}{\partial z_i} = \frac{e^{z_i}(\sum_{k} e^{z_k}) - e^{z_i}(e^{z_i})}{(\sum_{k} e^{z_k})^2}  \\
> &\frac{\partial p_i}{\partial z_i} = \frac{e^{z_i}}{\sum_{k} e^{z_k}} \left( \frac{(\sum_{k} e^{z_k}) - e^{z_i}}{\sum_{k} e^{z_k}} \right)  \\
> &\frac{\partial p_i}{\partial z_i} = p_i (1 - p_i)
> \end{aligned}
> $$
> 情况 2：$i \neq j$ (非对角线元素)
> $$
> \frac{\partial p_j}{\partial z_i} = \frac{\partial}{\partial z_i} \left( \frac{e^{z_j}}{\sum_{k} e^{z_k}} \right)
> $$
> 使用商法则：
> $$
> \begin{aligned}
> &\frac{\partial p_j}{\partial z_i} = \frac{0 \cdot (\sum_{k} e^{z_k}) - e^{z_j}(e^{z_i})}{(\sum_{k} e^{z_k})^2}\\
> &\frac{\partial p_j}{\partial z_i} = - \left( \frac{e^{z_j}}{\sum_{k} e^{z_k}} \right) \left( \frac{e^{z_i}}{\sum_{k} e^{z_k}} \right)\\
> &\frac{\partial p_j}{\partial z_i} = -p_j p_i
> \end{aligned}
> $$
> 所以，Softmax 的雅可比矩阵 $\mathbf{J} = \frac{\partial \mathbf{p}}{\partial \mathbf{z}}$ 是一个满矩阵，其 $(i, j)$ 项为：
> $$
> \mathbf{J}_{ij} = \frac{\partial p_j}{\partial z_i} = \begin{cases} p_i(1 - p_i) & \text{if } i = j \\ -p_i p_j & \text{if } i \neq j \end{cases}
> $$
>
> ------
>
> **步骤 3：链式法则计算 $\frac{\partial L}{\partial \mathbf{z}} = \mathbf{J} \frac{\partial L}{\partial \mathbf{p}}$**
>
> 根据向量链式法则：
> $$
> \frac{\partial L}{\partial \mathbf{z}}
> = \frac{\partial \mathbf{p}}{\partial \mathbf{z}} \frac{\partial L}{\partial \mathbf{p}}
> $$
> 也就是对每个 $j$：
> $$
> \frac{\partial L}{\partial z_j}
> = \sum_{i=1}^K \frac{\partial p_i}{\partial z_j} \frac{\partial L}{\partial p_i}
> $$
> 将 $j=i$ 和 $j=i$ 的情况代入：
> $$
> \begin{aligned}
> \frac{\partial L}{\partial z_j}
> &= \frac{\partial p_j}{\partial z_j} \frac{\partial L}{\partial p_j} + \sum_{i \neq j} \frac{\partial p_i}{\partial z_j} \frac{\partial L}{\partial p_i} \\
> &= p_j(1-p_j)\left(-\frac{y_j}{p_j}\right) + \sum_{i\neq j} (-p_i p_j)\left(-\frac{y_i}{p_i}\right) \\
> &= -(1-p_j)y_j + \sum_{i\neq j} p_j y_i \\
> &= -y_j + p_j y_j + p_j \sum_{i\neq j} y_i
> \end{aligned}
> $$
> 因为 $\mathbf{y}$ 是一个 one-hot 标签向量，所以 $\sum_{j} y_j = 1$。
> $$
> \frac{\partial L}{\partial z_j}
> = -y_j + p_j y_j + p_j (1 - y_j)
> = -y_j + p_j
> $$
> 所以向量形式就是极其常用的那条（实在是太优美了！！！）：
> $$
> \boxed{
> \frac{\partial L}{\partial \mathbf{z}} = \mathbf{p} - \mathbf{y}
> }
> $$

---

### 推导情况六：高阶求导（向量对矩阵、矩阵对矩阵）

**背景**

在深度学习的反向传播中，我们主要处理的是"标量对向量/矩阵"的梯度（即梯度），但是在一些情况下，我们也需要计算更高阶的导数——**向量对矩阵的求导**和**矩阵对矩阵的求导**。这些高阶导数的结果通常是**张量**，但在实际计算中，我们往往使用**微分-迹法**来绕过这些复杂的张量计算，直接得到我们需要的梯度。

---

#### 1. 向量对矩阵求导（Vector w.r.t. Matrix）

**定义：**

设 $\mathbf{z} \in \mathbb{R}^m$ 是向量，$\mathbf{W} \in \mathbb{R}^{m \times n}$ 是矩阵，求 $\frac{\partial \mathbf{z}}{\partial \mathbf{W}}$。根据求导规则，结果是一个**三阶张量 (3rd-order Tensor)**，维度为 $m \times n \times m$，其 $(i, j, k)$ 元素定义为：

$$
\mathcal{T}_{ijk} = \frac{\partial z_k}{\partial W_{ij}}
$$

**深度学习中的应用：**

我们通常不显式计算这个三阶张量，因为它的维度过大且不必要。实际计算中，我们只需要**标量损失函数 $L$ 对矩阵 $\mathbf{W}$ 的梯度**，也就是 $\frac{\partial L}{\partial \mathbf{W}}$，而不是三阶张量。

**例子与绕过方法：**

考虑一个单样本的全连接层：$\mathbf{z} = \mathbf{W}\mathbf{x}$。

- $\mathbf{W} \in \mathbb{R}^{m \times n}$
- $\mathbf{x} \in \mathbb{R}^{n \times 1}$
- $\mathbf{z} \in \mathbb{R}^{m \times 1}$

根据链式法则 $L \to \mathbf{z} \to \mathbf{W}$，需要梯度 $\frac{\partial L}{\partial \mathbf{W}} =\frac{\partial \mathbf{z}}{\partial \mathbf{W}}\frac{\partial L}{\partial \mathbf{z}}$。

根据定义，$\frac{\partial \mathbf{z}}{\partial \mathbf{W}}$ 是一个三阶张量，维度为 $m \times n \times m$。然而，**我们并不显式计算这个三阶张量**，而是直接使用**微分-迹法**。

**推导步骤：**

1. **已知条件：**
   
   - 上游梯度：$\frac{\partial L}{\partial \mathbf{z}}$（形状为 $m \times 1$）
   - 函数关系：$\mathbf{z} = \mathbf{W}\mathbf{x}$（假设 $\mathbf{x}$ 是常量）
   
2. **计算 $\mathbf{z}$ 的微分：**
   $$
   d\mathbf{z} = d(\mathbf{W}\mathbf{x}) = (d\mathbf{W})\mathbf{x}
   $$

3. **根据链式法则，损失的微分为：**
   $$
   dL = \left(\frac{\partial L}{\partial \mathbf{z}}\right)^\mathbf{T} d\mathbf{z}
   $$

4. **代入 $d\mathbf{z}$：**
   $$
   dL = \left(\frac{\partial L}{\partial \mathbf{z}}\right)^\mathbf{T} (d\mathbf{W}) \mathbf{x}
   $$

5. **利用迹的性质（$dL$ 是标量）：**
   $$
   dL = \text{tr}\left( \left(\frac{\partial L}{\partial \mathbf{z}}\right)^\mathbf{T} (d\mathbf{W}) \mathbf{x} \right)
   $$

6. **使用迹的循环不变性 $\text{tr}(ABC) = \text{tr}(BCA)$，将 $d\mathbf{W}$ 移到最后：**
   $$
   dL = \text{tr}\left( \mathbf{x} \left(\frac{\partial L}{\partial \mathbf{z}}\right)^\mathbf{T} d\mathbf{W} \right)
   $$

7. **整理成标准的"迹-微分"形式：**
   $$
   dL = \text{tr}\left( \left(\frac{\partial L}{\partial \mathbf{z}} \mathbf{x}^\mathbf{T}\right)^\mathbf{T} d\mathbf{W} \right)
   $$

8. **对比"读数规则" $dL = \text{tr}\left( \left(\frac{\partial L}{\partial \mathbf{W}}\right)^\mathbf{T} d\mathbf{W} \right)$，读出梯度：**
   $$
   \frac{\partial L}{\partial \mathbf{W}} = \frac{\partial L}{\partial \mathbf{z}} \mathbf{x}^\mathbf{T}
   $$

**结论：**

$$
\frac{\partial L}{\partial \mathbf{W}} = \frac{\partial L}{\partial \mathbf{z}} \mathbf{x}^\mathbf{T}
$$

这是我们需要的梯度。整个过程完全绕过了三阶张量 $\frac{\partial \mathbf{z}}{\partial \mathbf{W}}$ 的计算。

---

#### 2. 矩阵对矩阵求导（高阶张量）

**定义：**

假设 $\mathbf{Z} \in \mathbb{R}^{m \times p}$ 是矩阵，$\mathbf{W} \in \mathbb{R}^{n \times p}$ 是矩阵，求 $\frac{\partial \mathbf{Z}}{\partial \mathbf{W}}$。根据求导规则，结果是一个**四阶张量 (4th-order Tensor)**，维度为 $n \times p \times m \times p$，其 $(i, j, k, l)$ 元素定义为：

$$
\mathcal{T}_{ijkl} = \frac{\partial Z_{kl}}{\partial W_{ij}}
$$

**同理：**

我们几乎从不显式计算这个四阶张量，实际计算中，我们只需要**标量损失函数 $L$ 对矩阵 $\mathbf{W}$ 的梯度**，也就是 $\frac{\partial L}{\partial \mathbf{W}}$，并通过代换的方式避免计算 $\frac{\partial \mathbf{z}}{\partial \mathbf{W}}$

---

#### 如何绕过四阶张量的显式计算？

使用**微分-迹法**，我们可以绕过计算四阶张量，直接得到梯度。

**推导步骤：**

考虑全连接层：$\mathbf{Z} = \mathbf{X} \mathbf{W}$，其中 $\mathbf{X} \in \mathbb{R}^{m \times n}$ 是输入矩阵，$\mathbf{W} \in \mathbb{R}^{n \times p}$ 是权重矩阵。

1. **从标量的微分写起：**
   $$
   \mathrm{d}L = \text{tr}\left( \left(\frac{\partial L}{\partial \mathbf{Z}}\right)^\mathbf{T} \mathrm{d}\mathbf{Z} \right)
   $$

2. **用 $\mathbf{Z}$ 对 $\mathbf{W}$ 的函数关系将 $\mathrm{d}\mathbf{Z}$ 替换成关于 $\mathrm{d}\mathbf{W}$ 的式子。**
   
   假设 $\mathbf{Z} = \mathbf{X} \mathbf{W}$（$\mathbf{X}$ 是常量），那么：
   $$
   \mathrm{d}\mathbf{Z} = \mathbf{X} \mathrm{d}\mathbf{W}
   $$

3. **代入微分表达式：**
   $$
   \mathrm{d}L = \text{tr}\left( \left(\frac{\partial L}{\partial \mathbf{Z}}\right)^\mathbf{T} \mathbf{X} \mathrm{d}\mathbf{W} \right)
   $$

4. **利用迹的循环不变性，变形为：**
   $$
   \mathrm{d}L = \text{tr}\left( \left( \mathbf{X}^\mathbf{T} \frac{\partial L}{\partial \mathbf{Z}} \right)^\mathbf{T} \mathrm{d}\mathbf{W} \right)
   $$

5. **对比"读数规则"，直接"读"出梯度：**
   $$
   \frac{\partial L}{\partial \mathbf{W}} = \mathbf{X}^\mathbf{T} \frac{\partial L}{\partial \mathbf{Z}}
   $$

### 总结

通过微分-迹法，我们在计算中避免了显式计算高阶张量。对于**向量对矩阵求导**和**矩阵对矩阵求导**的情况，我们依赖损失反向传播的**标量求导原则**，通过链式法则和迹的性质，最终都能直接得到我们需要的梯度，而无需处理复杂的高阶张量。

---

## 四、矩阵求导速查表（分母布局）

**核心约定**：

1. **布局**：统一使用**分母布局 (Denominator Layout)**。
2. **形状**：导数的形状与求导变量的形状**一致**。
   - $\frac{\partial L}{\partial \mathbf{w}}$ (梯度) 是一个列向量（同 $\mathbf{w}$）。
   - $\frac{\partial L}{\partial \mathbf{W}}$ (梯度) 是一个矩阵（同 $\mathbf{W}$）。
3. **变量**：$L, y$ 为标量。$\mathbf{a}, \mathbf{b}, \mathbf{w}, \mathbf{x}, \mathbf{y}, \mathbf{z}, \mathbf{p}$ 为**列向量**。$\mathbf{A}, \mathbf{B}, \mathbf{W}, \mathbf{X}, \mathbf{Y}, \mathbf{Z}$ 为矩阵。

### 1. 向量求导（标量对向量）

主要用于构建损失函数（如L2正则、MSE）及其梯度。

| 表达式 $y = f(\mathbf{x})$ | 导数 $\frac{\partial y}{\partial \mathbf{x}}$ (对向量x) | 备注 |
|:---|:---|:---|
| $y = \mathbf{a}^\mathrm{T} \mathbf{x}$ | $\mathbf{a}$ | **线性函数**。最基础的导数形式。$\mathbf{a}$ 是常数列向量。 |
| $y = \mathbf{x}^\mathrm{T} \mathbf{x}$ | $2\mathbf{x}$ | **L2范数的平方** |
| $y = \mathbf{x}^\mathrm{T} \mathbf{A} \mathbf{x}$ | $(\mathbf{A} + \mathbf{A}^\mathrm{T})\mathbf{x}$ | **二次型 (Quadratic Form)** |
| $y = \mathbf{x}^\mathrm{T} \mathbf{A} \mathbf{x}$ | $2\mathbf{A}\mathbf{x}$ | **对称二次型**。**前提：$\mathbf{A}$ 是对称矩阵** ($\mathbf{A} = \mathbf{A}^\mathrm{T}$)。在PCA、协方差矩阵等推导中很常见。 |
| $L = \Vert\mathbf{y} - \mathbf{X}\mathbf{w}\Vert^2$ | $2 \mathbf{X}^\mathrm{T} (\mathbf{X}\mathbf{w} - \mathbf{y})$ | **最小二乘** |
| $L = \text{CE}(\text{softmax}(\mathbf{z}), \mathbf{y})$ | $\mathbf{p} - \mathbf{y}$ | **Softmax+交叉熵 组合梯度**。$\mathbf{z}$ 是logits (网络原始输出)，$\mathbf{p}=\text{softmax}(\mathbf{z})$ 是预测概率，$\mathbf{y}$ 是 one-hot 真实标签。这个 $\mathbf{p} - \mathbf{y}$ 的简洁形式是**多分类问题反向传播的核心**。 |

### 2. 矩阵求导 (标量对矩阵)

主要使用“微分-迹”法推导，是推导全连接层（批量）梯度的基础。 **核心规则**：$dL = \text{tr}((\frac{\partial L}{\partial \mathbf{W}})^\mathrm{T} d\mathbf{W})$

| 表达式 $y = f(\mathbf{W})$ | 导数 $\frac{\partial y}{\partial \mathbf{W}}$ (对矩阵W) | 备注 |
|:---|:---|:---|
| $y = \text{tr}(\mathbf{A}^\mathrm{T} \mathbf{W})$ | $\mathbf{A}$ | **线性函数（矩阵版）** |
| $y = \text{tr}(\mathbf{A} \mathbf{W})$ | $\mathbf{A}^\mathrm{T}$ | |
| $y = \text{tr}(\mathbf{W}^\mathrm{T} \mathbf{A})$ | $\mathbf{A}$ | **通过迹变换为第一条** |
| $y = \text{tr}(\mathbf{W}^\mathrm{T} \mathbf{A} \mathbf{W})$ | $\mathbf{A} \mathbf{W} + \mathbf{A}^\mathrm{T} \mathbf{W}$ | **矩阵二次型** |
| $y = \det(\mathbf{W})$ | $\det(\mathbf{W}) (\mathbf{W}^{-1})^\mathrm{T}$ | **行列式的导数**。在涉及行列式优化（如变分推断）时使用。**前提：$\mathbf{W}$ 是方阵且可逆** |
| $f = \frac{1}{2} \Vert\mathbf{X}\mathbf{W} - \mathbf{Y}\Vert_F^2$ | $\mathbf{X}^\mathrm{T} (\mathbf{X}\mathbf{W} - \mathbf{Y})$ | **矩阵最小二乘** |

### 3. 深度学习链式法则（反向传播）

反向传播算法 (Backpropagation) 的核心。$L$ 是最终的标量损失，$\frac{\partial L}{\partial \mathbf{z}}$ 或 $\frac{\partial L}{\partial \mathbf{Z}}$ 是从“上游”（后续层）传来的梯度。

| 表达式 | 梯度 | 备注 |
|:---|:---|:---|
| $\mathbf{z} = \mathbf{W}\mathbf{x} + \mathbf{b}$ | $\frac{\partial L}{\partial \mathbf{W}} = \frac{\partial L}{\partial \mathbf{z}} \mathbf{x}^\mathrm{T}$ | 权重梯度 (单样本) |
| | $\frac{\partial L}{\partial \mathbf{x}} = \mathbf{W}^\mathrm{T} \frac{\partial L}{\partial \mathbf{z}}$ | |
| | $\frac{\partial L}{\partial \mathbf{b}} = \frac{\partial L}{\partial \mathbf{z}}$ | |
| $\mathbf{Z} = \mathbf{X}\mathbf{W} + \mathbf{1}\mathbf{b}^\mathrm{T}$ | $\frac{\partial L}{\partial \mathbf{W}} = \mathbf{X}^\mathrm{T} \frac{\partial L}{\partial \mathbf{Z}}$ | 对应推导情况4 |
| | $\frac{\partial L}{\partial \mathbf{X}} = \frac{\partial L}{\partial \mathbf{Z}} \mathbf{W}^\mathrm{T}$ | |
| | $\frac{\partial L}{\partial \mathbf{b}} = (\frac{\partial L}{\partial \mathbf{Z}})^\mathrm{T} \mathbf{1}$ | (对样本维axis=0相加) |
| $\mathbf{a} = \sigma(\mathbf{z})$ (逐元素) | $\frac{\partial L}{\partial \mathbf{z}} = \frac{\partial L}{\partial \mathbf{a}} \odot \sigma'(\mathbf{z})$ | **逐元素激活 (Activation)**。如 ReLU, Sigmoid, Tanh |

---

## 五、关键技巧总结

### 1. 微分-迹法（Differential-Trace Method）

**核心思想**：
1. 计算标量函数 $f(\mathbf{X})$ 的全微分 $df$
2. 将 $df$ 整理成 $\text{tr}(\mathbf{A}^\mathrm{T} d\mathbf{X})$ 的形式
3. 根据"读数规则"，$\frac{\partial f}{\partial \mathbf{X}} = \mathbf{A}$

**关键性质**：
- 迹的循环不变性：$\text{tr}(ABC) = \text{tr}(BCA) = \text{tr}(CAB)$
- 迹的转置不变性：$\text{tr}(A) = \text{tr}(A^\mathrm{T})$
- 标量的迹等于自身：$\text{tr}(a) = a$（$a$ 是标量）

### 2. 链式法则的矩阵形式

对于复合函数 $L(\mathbf{y}(\mathbf{x}))$：

$$
\frac{\partial L}{\partial \mathbf{x}} = \frac{\partial \mathbf{y}}{\partial \mathbf{x}} \frac{\partial L}{\partial \mathbf{y}}
$$

其中 $\frac{\partial \mathbf{y}}{\partial \mathbf{x}}$ 是雅可比矩阵。

---

## 参考与延伸阅读

1. **矩阵微积分基础**：Petersen & Pedersen, "The Matrix Cookbook"
2. **深度学习中的矩阵求导**：Goodfellow et al., "Deep Learning", Chapter 6
3. **反向传播的数学基础**：Bishop, "Pattern Recognition and Machine Learning", Chapter 5
4. **迹技巧的详细推导**：Magnus & Neudecker, "Matrix Differential Calculus"
5. **大神的博客**：
   * https://zhuanlan.zhihu.com/p/21816886321
   * https://zhuanlan.zhihu.com/p/263777564
   * https://zhuanlan.zhihu.com/p/262751195

> 上述所有公式和结论均是经过我推导加上查阅资料、AI老师验证后的，但不能保证绝对的正确性和严谨性，如有问题敬请指出！！
