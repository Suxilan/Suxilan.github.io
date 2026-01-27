---
title: "Image Retrieval Tutorials"
date: 2025-11-30T15:47:27+08:00
draft: False
tags: ['Image retrieval','影像检索','contrastive learning','对比学习','Deep learning','Gabriele Berton']
categories: ["论文阅读"]
series: []
author: "Suxilan"
showlastmod: true
lastmod: 2025-11-30T15:47:27+08:00
ShowToc: true
TocWide: true
comments: true  # 默认启用评论
description: ""
summary: ""
cover:
    image: "https://cdn.jsdelivr.net/gh/Suxilan/Cloud-Image-alpha/imagebed/notes/All%20You%20Need%20to%20Know%20About%20Training%20Image%20Retrieval%20Models.png"
    alt: "image retrieval"
    position: right
    hiddenInSingle: false
    caption: ""
    relative: false
---

# All You Need to Know About Training Image Retrieval Models

![](https://cdn.jsdelivr.net/gh/Suxilan/Cloud-Image-alpha/imagebed/notes/All%20You%20Need%20to%20Know%20About%20Training%20Image%20Retrieval%20Models.png "All You Need to Know About Training Image Retrieval Models || caption=Gabriele Berton大佬的技术手册; attr=gmberton; attrlink=https://gmberton.github.io/")

{{< notice info >}}

Gmberton 还是出手了，作者通过成千上万次实验以及根据他个人多年在图像检索领域的经验，总结了训练图像检索模型时的“黄金法则。算是一篇非常扎实的实战指南了，非常值得一看！

{{< /notice >}} 

首先一上来作者就提出了这样一些关键的问题：

> * Which layers of the base model should be fine-tuned? 
> * How should the learning rates be set? 
> * How should the training dataset be sampled? 
> * When creating a dataset, should the main focus be annotation quality, or dataset size? 
> * What feature layer and feature dimensionality result in the best accuracy?

---

# Q&A.

我们直接先来点对点回答这些问题：

> **Q1.选择什么样的模型并微调什么层？**
>
> **A.** 优先微调整个DINOv2-Base模型，相比微调最后几层效果更好
>
> “<mark>*个人感觉相当的废话啊，能调肯定都调呀*</mark>”

>  **Q2: 学习率怎么设置？**
>
> **A.** 对于上述模型（全微调）学习率保持在 **$1e-6$**，Classifier Layer (仅限 Classification Losses)推荐 LR 为 **$1$ 或更高**
>
> “<mark>*这个还是很中肯的，个人实践下来，微调一层，学习率开**$1e-4$**就行了，微调层数越多，学习率越低*</mark>”

> **Q3: 训练集怎么采样？**
>
> **A.** **取决于你选用的 Loss 类型。**
>
> - **对于 Classification Losses:**
>   - **最佳设定:** **$M=1$** (每类采 1 张) 。
>   - **现象:** 它们不需要在 Batch 内构建正样本对，采样更多同类样本反而减少了 Batch 内类别的多样性，导致性能轻微下降 。
> - **对于 Contrastive Losses:**
>   - **最佳设定:** **$M=2$ 到 $4$** (每类采 2-4 张) 。
>   - **现象:** 必须至少采 2 张构成正样本对。实验显示 4 张通常是最佳平衡点 
>
> “<mark>*中肯的，虽然对对比学习来说，大家都在强调负样本，其实正样本的作用也是毋庸置疑的，尤其是在现代的PML框架里，不构成显式的anchor-pair配对，正样本的数量和质量还是需要保证的。越多越难的正样本往往有利于收敛*</mark>”

> **Q4.在制作数据集的时候应该把重心放在标注质量？还是数量上？**
>
> **A.** **数量 > 质量**。与其纠结标注是否完美，不如去搞更多的数据。
>
> - **抗噪性:** 所有 Metric Learning Losses 对错误标注（Noisy Labels）都有很强的鲁棒性。即使有 32% 的标签是错的，性能下降也不明显 。
> - **类别数量:** 减少训练集的**类别数**（即数据量）会直接导致性能线性下降 。
> - **建议:** 既然模型对噪声不敏感，在构建数据集时，应优先扩大规模，而不必过度清洗数据 。
>
> “<mark>*对表征学习而言，模型学习的本身也是一个去噪、对抗的过程，自监督任务里完全有可能掺入错误的样本（点名MoCo），但模型依然能够抵抗这种噪声，学习到数据本质的表征*</mark>”
>
> “<mark>*此外，感觉作者实验的这几个数据集都不算大，类别也不算多，不过也要带一点怀疑：作者的噪声注入方式是“随机改标签”，而不是更贴近现实的“相近类混淆/长尾类系统性错标”。但就检索这个任务而言，本质还是学习表征，肯定是数据越多越好*</mark>”

> **Q5.特征维度怎么选？怎么样带来最优的精度**
>
> **A.** 直接使用 Backbone 的输出（如 DINOv2 Base 的 CLS token，**768维**）效果最好 。
>
> - 如果加一个 Linear Layer 降维，通常会降低精度，除非是为了极端的存储压缩 。
>
> “<mark>*那可不一定呀，作者这里只讨论了对原始特征进行线性表达的情况。当然一般降维都会影响精度，但**往往接一个白化的linear改善表征能大幅提升检索精度***</mark>”

---

# Loss

理解这篇论文结论的前提，是理解作者对损失函数的分类。作者将 Loss 分为两类 ：

| **特性**      | **Stateless (Contrastive)**                                  | **Stateful (Classification)**       |
| ------------- | ------------------------------------------------------------ | ----------------------------------- |
| **代表 Loss** | Contrastive Loss, Multi-Similarity, NT-Xent (SimCLR), Triplet | ArcFace, CosFace, Softmax           |
| **参数**      | 无额外可训练参数                                             | 有额外的分类器层 (Weights $W$)      |
| **训练要求**  | 需要 Miner (挖掘困难样本)，Batch 内需有正样本对              | 不需要 Miner，不需要 Batch 内正样本 |
| **显存依赖**  | **依赖大 Batch Size** (为了挖掘到足够好的负样本)             | **小 Batch Size 也能工作良好**      |
| **适用场景**  | 资源充足 (High-Resource)                                     | 资源受限 (Resource-Constrained)     |

> 这里就需要增加一个Q&A： 显存资源（Batch Size）如何决定 Loss 的选择？
>
> **A：这取决于你的 Batch Size 是否能超过 256。**
>
> - **资源受限场景 (Batch Size < 256):**
>   - **推荐:** 使用 **Classification Losses** (如 CosFace, ArcFace) 。
>   - **原因:** 在小 Batch 下，Contrastive Losses 很难挖掘到有效的负样本，性能极差；而 Classification Losses 依然稳健 。
> - **资源充足场景 (Batch Size $\ge$ 256):**
>   - **推荐:** 使用 **Contrastive Losses** (如 Threshold-Consistent Margin, Multi-Similarity) 。
>   - **原因:** 随着 Batch Size 增大，Contrastive Losses 的性能显著提升并反超 Classification Losses 。

---

# 总结

| **配置项**        | **方案 A: 显存土豪版 (High VRAM)** | **方案 B: 显存吃紧版 (Low VRAM)**          |
| ----------------- | ---------------------------------- | ------------------------------------------ |
| **判定标准**      | Batch Size 能开到 $\ge 256$        | Batch Size 只能开到 $< 256$                |
| **推荐 Loss**     | **Multi-Similarity** 或 **TCM**    | **CosFace** 或 **ArcFace**                 |
| **采样策略**      | **$M=4$** (每类 4 张)              | **$M=1$** (每类 1 张)                      |
| **Miner**         | Online Miner (必须)                | 不需要                                     |
| **Backbone**      | DINOv2-base (全参数微调)           | DINOv2-base (全参数微调)                   |
| **Optimizer**     | Adam                               | Adam                                       |
| **Learning Rate** | Model: $1e-6$                      | Model: $1e-6$   **Classifier Head: $1.0$** |
| **数据建议**      | 尽可能多收集类别，容忍少量标注错误 | 同左                                       |
