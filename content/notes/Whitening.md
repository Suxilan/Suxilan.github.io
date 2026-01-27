---
title: "白化（Whitening）及其可微分做法"
date: 2025-11-25T20:52:47+08:00
draft: false
tags: ['Data science','Whitening','数据白化','Deep learning']
categories: ["算法博客"]
series: []
author: "Suxilan"
showlastmod: true
lastmod: 2025-11-25T20:52:47+08:00
ShowToc: true
TocWide: true
comments: true  # 默认启用评论
description: "特征白化的方法、效果，及其在检索任务的现代化设计"
summary: "数据白化Whitening及其在Deep learning的应用"
---

# 特征白化

**特征白化（Whitening）** 的核心目的是消除特征之间的相关性，并使特征具有单位方差。在深度学习和信息检索中，它主要解决了 **“特征各向异性”（Feature Anisotropy）** 的问题——即特征向量倾向于聚集在空间的一个狭窄锥体中，导致余弦相似度无法有效区分样本

## 一、特征白化的核心原理

白化本质上是对特征空间进行线性变换，使得变换后的数据满足两个条件：

1. **零均值（Zero-Mean）：** 数据中心移动到原点。
2. **单位协方差矩阵（Identity Covariance）：** \(Σ=I\)。这意味着特征之间 **去相关（decorrelation）且方差归一化** 。

#### 常见的两种白化方式

假设特征矩阵为\(X(N×D)\)，协方差矩阵为$Σ$。对Σ进行特征值分解：$Σ=UΛUT$。

1. **PCA 白化 (PCA Whitening)**：
   变换矩阵 $W_{PCA}=Λ^{−1/2}U^T$。
   - 先旋转到主成分方向，再缩放。
   - **缺点**：不仅去相关，还旋转了坐标轴，彻底改变了原始特征的物理/语义含义。
2. **ZCA 白化 (ZCA Whitening)**：
   变换矩阵 $W_{ZCA}=UΛ^{−1/2}U^T$。
   - 相当于 $W_{ZCA}=UW_{PCA}$`。在 PCA 白化后，又把坐标轴旋转回去了。
   - **优点**：**ZCA 白化后的数据与原始数据最接近（L2距离最小）** 。在计算机视觉中，ZCA 更常用，因为它保留了原始特征的拓扑结构。

#### 为什么对检索重要？

未经白化的深度特征往往存在高度冗余（Co-occurrence），导致某些维度（比如背景纹理）主导了距离计算。白化后，所有维度的权重变得均等，模型被迫关注那些方差较小但区分度高的细粒度特征。

## 二、如何在深度学习中实现端到端白化

在传统的检索流程中，白化通常是**后处理（Post-processing）**：提取所有库的特征 -> 计算 PCA -> 变换 -> 存库。

但在端到端训练中（如 LAttQE, NetVLAD, GeM），我们希望白化参数能随着网络一起更新，或者作为网络的一部分。

#### 实现策略：Learnable Linear Layer (Initialized by PCA)

目前工业界和学术界（如 Radenovic et al. ECCV 2018）最通用的做法是：**将白化层实现为一个全连接层（Linear Layer），并利用训练数据的统计信息对其进行初始化，随后允许其在训练中微调。**

其好处是：

1. **稳定性**：直接在 mini-batch 内计算协方差矩阵的逆平方根（矩阵求逆）非常不稳定且计算昂贵。
2. **适应性**：初始化提供了良好的白化起点，后续的反向传播（Backprop）允许网络根据 Loss（如 Contrastive Loss）调整变换矩阵，使其成为“判别式白化”（Discriminative Whitening）。

**代码实现：**

```python
import torch
import torch.nn as nn
import numpy as np

class WhiteningLayer(nn.Module):
    """
    端到端可训练的白化层。
    实质上是一个 Linear 层，但初始化非常关键。
    """
    def __init__(self, input_dim, output_dim=None, dropout=0.0):
        super(WhiteningLayer, self).__init__()
        self.input_dim = input_dim
        self.output_dim = output_dim if output_dim else input_dim
        
        # 定义核心组件：线性层
        # Bias 用于实现 Zero-centering (减去均值)
        # Weight 用于实现 Rotation & Scaling (去相关和归一化)
        self.linear = nn.Linear(self.input_dim, self.output_dim, bias=True)
        
        # 可选：白化后加 Dropout 有助于防止过拟合
        self.dropout = nn.Dropout(dropout) if dropout > 0 else nn.Identity()

    def init_params(self, X):
        """
        使用这一批数据(通常是整个训练集的子采样)来初始化白化参数。
        实现的是 PCA Whitening 的初始化逻辑。
        
        Args:
            X: (N, D) tensor, 用于计算统计信息的特征矩阵
        """
        print(f"Initializing whitening with {X.shape[0]} samples...")
        device = X.device
        
        # 1. 计算均值 (Mean)
        mean = torch.mean(X, dim=0)
        
        # 2. 计算中心化后的协方差矩阵 (Covariance)
        X_centered = X - mean
        # Cov = (X-u)^T * (X-u) / (N-1)
        cov = torch.matmul(X_centered.T, X_centered) / (X.shape[0] - 1)
        
        # 3. 特征值分解 (Eigendecomposition)
        # U: 特征向量矩阵, S: 特征值向量
        # torch.linalg.eigh 适用于对称矩阵(协方差矩阵是对称的)，比 svd 更快更稳
        S, U = torch.linalg.eigh(cov)
        
        # 确保特征值是正的并排序 (eigh 默认升序，我们需要降序对应的 PC)
        # 加上极小值 eps 防止除零
        eps = 1e-5
        S = torch.clamp(S, min=eps)
        
        # 降序排列
        # indices: [D-1, ..., 0]
        indices = torch.argsort(S, descending=True)
        S = S[indices]
        U = U[:, indices]
        
        # 如果需要降维 (output_dim < input_dim)，只取前 output_dim 个分量
        S = S[:self.output_dim]
        U = U[:, :self.output_dim]
        
        # 4. 构建白化矩阵 (Whitening Matrix)
        # PCA Whitening Matrix: W = \Lambda^(-1/2) * U^T
        # 但在 nn.Linear 中，计算方式是 y = xA^T + b
        # 所以我们需要构建的权重 A 应该是 W 的转置，即 A = U * \Lambda^(-1/2)
        
        inv_sqrt_S = torch.diag(1.0 / torch.sqrt(S))
        
        # Linear层的 weight 形状是 (out_features, in_features)
        # 公式推导:
        # y = (x - mean) @ U @ inv_sqrt_S
        # y = x @ (U @ inv_sqrt_S) - mean @ (U @ inv_sqrt_S)
        # 令 W_layer = (U @ inv_sqrt_S).T
        # 令 b_layer = - mean @ (U @ inv_sqrt_S)
        
        whitening_matrix = torch.matmul(U, inv_sqrt_S) # (Input, Output)
        
        weight = whitening_matrix.T # (Output, Input)适合 nn.Linear
        
        # 计算 Bias
        # bias = - mean * W
        bias = - torch.matmul(mean, whitening_matrix)
        
        # 5. 赋值给 Linear 层
        with torch.no_grad():
            self.linear.weight.copy_(weight)
            self.linear.bias.copy_(bias)
            
        print("Whitening layer initialized.")

    def forward(self, x):
        # x: (B, D)
        out = self.linear(x)
        out = self.dropout(out)
        return out
```

#### 如何在训练流程中使用

````python
class MyEncoder(pl.LightningModule):
    def __init__(self, ...):
        # ... Backbone ...
        self.whitening = WhiteningLayer(input_dim=2048, output_dim=2048) # 甚至可以降维到 512
        self.norm = nn.functional.normalize # L2 Norm 通常在白化之后
````

在开始 trainer.fit() 之前，或者在 on_train_start 钩子中，你需要跑一遍数据（或者采样几千个样本）来初始化这个层。如果不初始化，它就是一个随机的线性层，甚至会破坏预训练特征。

初始化后，开启训练。由于学习率通常较小，WhiteningLayer 的参数会微调，以适应当前的 Loss 目标（例如 Contrastive Loss 希望正样本距离近，白化层会尝试在这个约束下保持特征的散布）。

## 总结

- **一般做法**：使用 **PCA Whitening** 数学公式（去均值 -> 旋转 -> 缩放）。
- **端对端实现**：使用一个带 Bias 的 **nn.Linear** 层。
- **关键点**：**不要随机初始化！** 必须使用提取出的特征统计量进行 PCA 初始化，然后让网络在训练中微调它。这是目前图像检索领域的 SOTA（State-of-the-Art）实践。

> **Ps**：为什么在端到端训练中不使用ZCA？
>
> **答案是：**
>
> 本质上，神经网络学习的只是一个Linear函数，PCA只是用来进行初始化其权重达到数据白化的效果（初始化）
>
> **ZCA 仅仅是在 PCA 的结果上左乘了一个正交矩阵！！**
>
> * 正交旋转**不改变向量之间的欧氏距离和角度**。
>   因此，对于下游的 Loss（如 Contrastive Loss）或者检索匹配来说，**PCA 特征和 ZCA 特征的效果是完全数学等价的**。既然效果一样，为什么不选计算更简单、且能顺便做降维的 PCA 呢？
> * 在反向传播过程中，神经网络非常擅长学习旋转（Rotation）。如果 Loss 函数认为某种旋转能降低 Loss，它自己会去更新权重矩阵。因此，初始化的微小旋转差异（PCA vs ZCA）在经过几轮反向传播后，很快就会被网络的自我调整所淹没。

{{< notice info >}}

Whitening的经典操作出自**Radenovic et al.** 的论文 **"Fine-tuning CNN Image Retrieval with No Human Annotation" (ECCV 2018)**

{{< /notice >}}

