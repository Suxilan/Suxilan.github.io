---
title: "Vlad"
date: 2026-01-23T18:29:39+08:00
draft: false
tags: ["NetVLAD","VLAD","特征聚合","End2end Learning"]
categories: ["技术笔记"]
series: []
author: "Suxilan"
showlastmod: true
lastmod: 2026-01-23T18:29:39+08:00
ShowToc: true
TocWide: true
comments: true  # 默认启用评论
description: ""
summary: ""
weight: 1
---

# 前言

NetVLAD 确实是计算机视觉中一个里程碑式的工作，它不仅连接了传统特征工程（SIFT, VLAD）与深度学习，更是开启了端到端位置识别（Visual Place Recognition）的时代。



简单来说，NetVLAD 的核心贡献在于将传统的无监督聚类算法（如 K-Means）和特征聚合方法（VLAD）转化为了一个**可微的（Differentiable）、可训练的神经网络层**，从而允许网络直接针对“位置识别”这一任务进行端到端的优化，而不再依赖手工设计的特征。

> 为了彻底理解 NetVLAD 的设计动机，我们需要先建立一套统一的数学符号。
>
> **基础符号定义：**
>
> 假设我们需要描述一张图片：
>
> - **$X = \{x_1, x_2, ..., x_N\}$**：这是一张图像中提取出的 $N$ 个局部特征描述子（例如 SIFT 向量）。每个 $x_i$ 都是 $D$ 维的向量。
> - **$C = \{c_1, c_2, ..., c_K\}$**：这是我们通过 K-Means 算法预先训练好的 $K$ 个聚类中心（也叫“视觉词汇”，Visual Words）。每个 $c_k$ 也是 $D$ 维的

# 第一阶段：词袋模型 (Bag of Words, BoW) —— “硬分配”与“计数”

BoW的核心思想非常简单：我们只关心特征“掉”进了哪个聚类中心，然后数个数。简而言之可以总结为以下两个步骤：

**1. 硬分配 (Hard Assignment):**

对于每一个特征 $x_i$，我们通过寻找最近邻，将其分配给唯一的聚类中心 $c_k$。

我们定义一个分配函数 $a_k(x_i)$：
$$
a_k(x_i) = 
\begin{cases} 1, & \text{如果} k = \operatorname*{argmin}_{j} \|x_i-c_j\|^2 \\ 0, & \text{其他情况} \end{cases}
$$
**2. 聚合 (Aggregation):**

BoW 的最终向量只是一个直方图。对于第 $k$ 个聚类中心，它的值就是分配给它的特征数量：
$$
V_{\text{BoW}}[k] = \sum_{i=1}^{N} a_k(x_i)
$$
这个向量的长度是 $K$。

{{< notice info >}}

BoW 虽然简单，但它有一个致命的数学缺陷——“类内”无差。BoW 就像是在做“人口普查”，它只记录某个城市（聚类中心 $c_k$）里住了多少人，但不在乎这些人是住在“市中心”还是“郊区”，这也直接促成了 VLAD 的诞生！

{{< /notice >}}

# 第二阶段：VLAD —— 从“计数”到“向量和”

**VLAD (Vector of Locally Aggregated Descriptors)** 引入了**残差 (Residual)** 的概念。它记录的是每个居民相对于市中心的**相对位置**

“残差”：

对于赋给中心 $c_k$ 的特征 $x_i$，残差向量为：
$$
x_i - c_k
$$
在 BoW 中，我们要的是 **0阶统计量（计数）**：
$$
V_{\text{BoW}}[k] = \sum_{i=1}^{N} a_k(x_i) \cdot 1
$$
VLAD 想要的是 **1阶统计量（残差和）**。也就是把所有属于簇 $k$ 的特征的残差向量全部加起来。
$$
V_{\text{VLAD}}[k]= \sum_{i=1}^{N} a_k(x_i) \cdot (x_i - c_k)
$$
其中，残差向量为 $D$ 维，则最终的VLAD向量为 $K\cdot D$ 维

# 第三阶段：NetVLAD —— 软分配 (Soft Assignment)

现在我们已经有了 VLAD 的数学形式，但如果直接把它放进神经网络里训练，有一个巨大的障碍。请看公式里的 $a_k(x_i)$ 项。在传统 VLAD 中，这是一个**硬分配**（Hard Assignment）：
$$
a_k(x_i) = 1 \text{ (如果是最近邻) 否则 } 0
$$
这就意味着这是一个非黑即白的`argmax`操作。正是因为`argmax`是不可导的（或者说导数几乎处处为 0），会导致**梯度消失（Gradient Vanishing）**，无法反向传播来更新前面的特征提取网络。

### NetVLAD 的核心变革：软分配 (Soft Assignment)

为了解决这个问题，NetVLAD 借鉴了 T-SNE 等算法的思想，使用**Softmax**将“非 0 即 1”的硬分配变成了一个概率分布。

对于第 $k$ 个聚类中心 $c_k$ 和特征 $x_i$，软分配权重 $\bar{a}_k(x_i)$ 定义为：
$$
\bar{a}_k(x_i) = \frac{e^{-\alpha \|x_i - c_k\|^2}}{\sum_{j} e^{-\alpha \|x_i - c_j\|^2}}
$$
这里的 $\alpha$ 是一个控制参数：

- $\alpha \to \infty$ 时，这就逼近硬分配（One-hot）。
- $\alpha \to 0$ 时，分配趋于平均。

NetVLAD 的精妙之处在于它不仅提出了软分配，还发现可以用标准的 CNN 操作（卷积/全连接）来实现它，从而能无缝嵌入任何网络
$$
-\alpha \|x_i - c_k\|^2 = -\alpha (\|x_i\|^2 - 2c_k^T x_i + \|c_k\|^2)
$$
