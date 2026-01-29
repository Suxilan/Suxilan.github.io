---
title: "NetVLAD论文阅读"
date: 2026-01-26T01:19:40+08:00
draft: false

tags: ["NetVLAD","Visual Place Recognition"]
categories: ["算法博客","论文阅读"]
series: ["VLAD族系","VPR必读经典"]
author: "Suxilan"

comments: true
showlastmod: true
lastmod: 2026-01-26T01:19:40+08:00
summary: "端到端VPR的万恶之源"
description: "学习如何将一个传统机器学习模块设计得可微分"
# Stack 主题内置字段（按需开启/关闭）
toc: true
math: true
image: "https://cdn.jsdelivr.net/gh/Suxilan/Cloud-Image-alpha/imagebed/covers/netvlad.png"   # Stack 原生封面字段（推荐）
---

---

# 摘要 (Abstract)

> &emsp;<u>We tackle the problem of large scale visual place recognition, where the task is to quickly and accurately recognize the location of a given query photograph</u>. We present the following three principal contributions. First, we develop a convolutional neural network (CNN) architecture that is trainable in an end-to-end manner directly for the place recognition task. The main component of this architecture, NetVLAD, is a new generalized VLAD layer, inspired by the “Vector of Locally Aggregated Descriptors” image representation commonly used in image retrieval.  The layer is readily pluggable into any CNN architecture and amenable to training via backpropagation. Second, we  develop a training procedure, based on a new weakly supervised ranking loss, to learn parameters of the architecture in an end-to-end manner from images depicting the same places over time downloaded from Google Street View Time Machine. Finally, we show that the proposed architecture significantly outperforms non-learnt image representations and off-the-shelf CNN descriptors on two challenging place recognition benchmarks, and improves over current state-of-the-art compact image representations on standard image retrieval benchmarks.

为什么说NetVLAD是VPR的万恶之源，其实从它的摘要中就不难看出了。虽然NetVLAD本质是在做特征聚合，也广泛应用到各种涉及到检索的任务上，但是文章开篇就说<mark style="background-color:yellow">"large scale visual place recognition"</mark>也是为今后VPR的快速发展埋下了种子了。

文章的三个contris，前两个是实质性的核心创新，后一个是实验性质的结论（这里暂且不表）。文章这里先提到两个issue（痛点）——大范围VPR的准确、快速的要求，传统CNN+手工描述符的割裂（不能端到端）；以及GSV-Time Machine数据集的Geo-Tag的标注噪声，因此引入以下两个创新：

1. **NetVLAD Layer**：即插即用、可微分端到端训练
2. **弱监督损失+端到端训练策略**：想要训练深度网络需要海量数据，但人工标注地点识别数据太贵太慢。谷歌街景虽然有 GPS，但 GPS 是有误差的（Noisy），而且两张照片即使 GPS 很近，拍的角度可能完全不同（这就叫 Weak Supervision）。作者必须设计一种机制来“容忍”这种噪声。

这里其实已经能看到作者的叙事思路了，The Gap+Contris都已经明确，现在去读intro应该会更清晰！

---

# 引言(Introduction)

intro一上来还是像大多数论文一样先讲，VPR在各个领域的巨大作用（视觉、机器人、自动驾驶导航定位等，<mark>不过怎么过了十年也是这个话术hhh</mark>）。然后比较好的一点是，作者没有继续平铺直叙，而是采用反问来激发思考：

> &emsp;The place recognition problem, however, still remains extremely challenging. How can we recognize the same street-corner in the entire city or on the scale of the entire country despite the fact <u>it can be captured in different illuminations or change its appearance over time</u>? The ***fundamental scientific question*** is what is **the appropriate representation of a place** that is <u>rich enough to distinguish similarly looking places yet compact to represent</u> entire cities or countries.

{{< notice note>}}

这里核心想要表述的就是——如何提升一个地点位置识别的特征表示的鲁棒性，并且作者把它上升到一个科学问题的角度。

{{< /notice >}}

这个问题其实相当常见，不光是VPR领域，其实做众源SfM的，地标检索的也同样面临着这个问题。作者通过实例列举加上，问题导向的方式进行写作，个人认为是一种非常高明的手段。

除此之外，我们从文章的引言中还能读到的是，虽然我们都知道NetVLAD这篇文章最大的创新就是这个模型本身，但是作者在叙事的时候**不是只在堆砌技术**，而是构建一个合乎逻辑的**叙事弧（Narrative Arc）**。作者通过指出“任务不匹配”（分类 vs. 检索）这个核心矛盾，让NetVLAD的出现显得不是为了创新而创新，而是解决问题的**必然选择**。

## 研究动机(Motivation)

作者使用了经典的 **"Success - But - Therefore"** 逻辑结构：

* **Success (承认现状):** 承认 CNN 在物体分类（Object Classification）任务上取得了巨大成功，且特征具有一定的迁移能力 。
* **But (提出冲突/Gap):** 这种“现成”（Off-the-shelf）的 CNN 特征直接拿来做地点识别（Instance-level recognition），效果提升有限 。
  - *深层原因:* 分类任务训练出的特征（黑盒），并没有被训练成适合用“欧氏距离”来直接比较相似度 。物体分类关注的是“这是什么类别”，而地点识别关注的是“这是哪个具体实例”。

* **Therefore (引出方案):** 因此，我们需要专门为“地点识别”任务训练一个新的 CNN 架构 。
  * *技术推导:* 要实现端到端训练 $\rightarrow$ 需要一个可微分的特征聚合层 $\rightarrow$ **NetVLAD Layer 诞生**。

{{< notice info>}}

NetVLAD诞生的时候才是2016年，这个时候CNN才刚起步，很多重量级的paper还没有诞生。作者这个时候还只是使用的AlexNet和VGG，所以这里认为CNN训练的黑盒也情有可原，毕竟很多后续对Deep Learning的可解释性研究、数学分析还没有出现。在这个时间点，作者已经意识到Domain Gap以及域迁移的问题，真的是非常厉害了。直至今日很多文章依然拿这个当作立足点讲故事~

{{< /notice >}}  

##   核心贡献(Contributions)

这时候作者已经铺垫完了背景（Context）和痛点（Gap），现在终于要亮出“杀手锏”了。

**🕵️‍♂️ 深度拆解：Challenge vs. Innovation：**

先来看作者这里的灵魂三问:

> * First, what is a good CNN architecture for place recognition?
>
> * Second, how to gather sufficient amount of annotated data for the training?
>
> * Third, how can we train the developed architecture in an end-to-end manner tailored for the place recognition task?

1. 这里作者其实是承接上文，我们现在已经有足够好的针对目标分类的CNN网络架构了。那么位置识别呢？对于位置识别任务，我们的网络更应该注意到哪些信息、特征？
2. 然后再说我们怎么获取足够的数据来训练这个模型？（属于是深度学习特有的搞数据环节）
3. 最后说，有了模型、有了数据，怎么样端到端训练这个任务？

整体看下来一气呵成，完全不拖泥带水，也顺势将后文的创新点突出出来，你能明显找到Innovation所解决的Challenge ，而不是现在很多论文流水账的记法。

|      NetVLAD Layer       |            Time Machine Datasets            |                       End2end Learning                       |
| :----------------------: | :-----------------------------------------: | :----------------------------------------------------------: |
| 可微分VLAD<br />即插即用 | GPS Tagged data<br />with weaky supervision | 网络学会聚焦于位置识别的内容<br />如建筑物、天际线<br />而忽略变化的元素“汽车”、“行人” |

---

# 方法(Methodology)

<a id="methodology"></a>

具体的NetVLAD网络架构、前向过程和工程细节这里就不探讨了，[详细见另一篇博客](/notes/vlad)。这里主要从写作和数学上分析一下作者是怎么叙事的。

作者把标准的检索流程分为两步：**(i) 提取局部特征** 和 **(ii) 池化 (Pooling)**

在论文这里局部特征提取器就是CNN，而时至今日这样的思路依然在使用在各种需要局部特征提取的任务里——[SuperPoint](https://github.com/magicleap/SuperPointPretrainedNetwork)、[DELG](https://arxiv.org/abs/1906.07155)。“池化”自然就是我们今天的主角——**NetVLAD**了

![NetVLAD](https://cdn.jsdelivr.net/gh/Suxilan/Cloud-Image-alpha/imagebed/notes/netvlad.png "CNN architecture with NetVLAD Layer|| width=100%; style=border-radius:12px; caption=NetVLAD标准架构，包含（卷积、softmax、L2-normalization）; attr=论文原图; attrlink=https://openaccess.thecvf.com/content_cvpr_2016/papers/Arandjelovic_NetVLAD_CNN_Architecture_CVPR_2016_paper.pdf")

## 参数解耦(Decoupling)

NetVLAD的标准架构、实现细节以及在[博文](/notes/vlad)里详细介绍了，我们这里来讨论一个平时容易忽略的细节——**参数解耦 (Decoupling)**。我们先来回顾VLAD的标准公式：
$$
V ( j , k ) = \sum _ { i = 1 } ^ { N } a _ { k } ( x _ { i } ) ( x _ { i } ( j ) - c _ { k } ( j ) )
$$
在标准的 VLAD 中，分配权重是由聚类中心 $c_k$ 决定的（距离越近，权重越大）。但在 NetVLAD 中，作者特意强调：

> "The NetVLAD layer has three **independent** sets of parameters $\{w_k\}$, $\{b_k\}$ and $\{c_k\}$"

这意味着控制“分配”（Assignment，由 $w, b$ 决定）的参数，和控制“残差计算”（Residual，由 $c$ 决定）的参数是**互不绑定**的。在标准的 VLAD 中，聚类中心（Cluster Centre）身兼两职：

1. **当“考官” (Assignment):** 决定谁属于这个类（根据距离）。
2. **当“原点” (Residual Anchor):** 作为计算残差向量的起点 ($x - c$)

而在 **NetVLAD** 中，作者把这两个职能分开了，从下面公式不难看出：
$$
V ( j , k ) = \sum _ { i = 1 } ^ { N } \frac { e ^ { w _ { k } ^ { T } x _ { i } + b _ { k } } } { \sum _ { k ^ { \prime } } e ^ { w _ { k } ^ { T } x _ { i } + b _ { k ^ { \prime } } } } \left( x _ { i } ( j ) - c _ { k } ( j ) \right)
$$

* **$\{w_k, b_k\}$ 负责当“考官”：** 它们画出了地盘的边界（决定谁归这一类）。

* **$\{c_k\}$ 负责当“原点”：** 它可以自由移动，决定残差向量的方向。

![Decoupling](https://cdn.jsdelivr.net/gh/Suxilan/Cloud-Image-alpha/imagebed/notes/netvlad_decoupling.png "Benefits of supervised VLAD|| width=20%; style=border-radius:12px;")

这里原论文中给了一个非常经典的解释（讲故事的艺术啊！）

> “where the two descriptors are known to belong to images which should not match”

在标准的VLAD中，中心点（$x_{VLAD}$）必须呆在特征空间的中央，这时的残差向量的方向与分配算法（分配的结果）严格相关，从中心 $x$ 指向绿点和红点的箭头方向高度一致，点积也比较大。

{{< notice note>}}

这就是所谓的“错误地增加两张不相干图片的相似度”——比如，图片 A 和图片 B 拍的是完全不同的地方（比如一个是巴黎，一个是东京）。但是，这两个局部特征长得很像，都被分配到了一个聚类中心，但其实我们的目标是让这两个计算出的相似度越低越好。

{{< /notice >}}   

而如果进行了解耦，我们就能很大程度规避这种情况，文中给出的示例是，<u>通过解耦学习的中心，其位置不一定是在这个特征空间的正中心位置。就使得分配到统一聚类的两个特征到中心的残差变小、且方向几乎相反（也就是降低了相似度）</u>。***当然也有可能是分配的时候不会将这两个局部向量分配到一个聚类中心***（who knows？反正别人已经把故事讲得很圆满了，皆大欢喜）

> 这里介绍一个小插曲：
>
> 在 NetVLAD 诞生之前（及当时），学术界主要有这么几类玩家。结合论文 **3.1 节结尾 "Relations to other methods"**  来看
>
> 1. “拼凑派” (Off-the-shelf CNN + Standard VLAD/FV):直接拿一个训练好的 CNN（比如做分类的 VGG）提取特征，然后强行接一个传统的 VLAD 或 Fisher Vector 算法 ;<mark>没有做到端到端</mark>
> 2. “半学习派” (Sydorov et al):试图联合训练 FV 参数和分类器 ;<mark>输入的特征依然是**手工设计**</mark>
> 3. “贪婪派” (Fisher Networks):把 Fisher Vector 层层堆叠 ,但只能一层一层贪婪地训练（Greedy bottom-up），<mark>不是真正的全局优化</mark>

因此，不难看出，NetVLAD能活到今天，全靠 **"Differentiable" (可微分)** 。它打通了任督二脉，让梯度可以从最后的损失函数一直流回最开始的卷积层。这意味着：**CNN 终于知道它提取什么样的特征，才能让后面的 VLAD 聚类得更好。**

## Datasets & Loss

>  数据集对于深度学习任务是至关重要的，有相当一大部分DL的论文都在搞数据。

* **数据集来源：** 谷歌街景时光机 (Time Machine， 全景影像)
* **数据标签：** GPS
* **潜在正样本 (Potential Positives, $\{p_i^q\}$):** 离查询图像 $q$ 很近的图，*可能*是匹配的，也可能不是
* **确定负样本 (Definite Negatives, $\{n_j^q\}$):** 离查询图像 $q$ 很远的图，*一定*是不匹配的 

{{< notice info>}}

这样设计的原因是因为，虽然 Time Machine 提供了海量数据，但它有一个巨大的缺陷——**GPS 噪声**：

1. **不完美的标签:** 每一张全景图（Panorama）只有一个 GPS 坐标。
2. **视角的歧义:** 当我们从全景图中采样出透视视角的图片（Perspective images）作为查询图像 $q$ 时，即使数据库里的图 $I_i$ 离它很近（GPS 距离近），它们也可能**并没有拍到同一个东西**（比如一个朝东拍，一个朝西拍；或者中间隔了一堵墙）

{{< /notice >}}    

> 来看看原文附录里的实现：
>
> &emsp;To create the training tuple for a query, we use all of its potential positives (images within 10 meters), and we perform randomized hard negative mining for the negatives (images further away than 25 meters). The mining is done by keeping the 10 hardest negatives from a pool of 1000 randomly sampled negatives and 10 hardest negatives from the previous epoch. We find that remembering previous hard
> negatives adds stability to the training process.

对于潜在正样本，作者这里只选和q最相似的算Loss，负样本也采用随机困难样本采样，如此构建以下损失公式：
$$
p_{i*}^q = \text{argmin}_{p^q} d_\theta(q, p_i^q)
$$

$$
L_\theta = \sum_j \text{max}(0, \underbrace{\min_i d^2(q, p_i)}_{\text{挑最像的正样本}} + \underbrace{m}_{\text{安全间隔}} - \underbrace{d^2(q, n_j)}_{\text{负样本距离}})
$$

这也就是$\text{TripletMarginLoss}$的形式，这个 $m$ 被称为 **Margin (间隔/边界)** ，我们不仅希望 $q$ 离 $p^*$ 近，离 $n$ 远。我们还希望这中间有一个**安全距离**，让正负样本的区别边界更为清晰。

## 现代视角

站在2026年的角度回顾十年前，NetVLAD是以**破局者**的姿态出现子大众视野的，它的这套训练策略绝对是**顶级（SOTA）水准，甚至是开创性**的。

1. **从“借用”到“原生”:** 当时大多数人还在用 ImageNet 分类任务预训练好的 CNN 提取特征（Off-the-shelf）。NetVLAD 证明了**专门为检索任务训练 (End-to-End training for retrieval)** 是必要的，这在当时是一个巨大的观念转变 。
2. **工程上的改进:** 当时，大规模数据的标注还停留在人工手动标注，自监督、无监督还没有兴起的时候，<u>作者提出的“在一堆潜在正样本里挑最好的 ($argmin$)”这一策略</u> ，巧妙地绕过了人工标注的成本，让大规模训练成为可能。同时提出负样本缓存机制（类似当今的Memory Bank），在那个显存极其昂贵的年代，极大程度利用了“穷人的智慧”。

从今天看，我们显然有了更好的框架——PML，更好的损失（InfoNCELoss、CircleLoss、MultisimilarityLoss等），以及更好的挖掘策略（Online Mining）。但是NetVLAD由于其架构的优势依然活跃在各大SOTA榜上，成为稳定必刷的baseline。

---

# 实验(Experiments)

**NetVLAD 实验设计与故事线梳理**

| **实验代号** | **实验目的 (The "Why")**                                     | **核心对比 (Comparison)**                                    | **关键结果 (The Result)**                                    | **故事结论 (The Story Beat)**                                |
| ------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **Exp 1**    | **核心立论：** 证明“直接用现成的 CNN 不行，必须针对任务训练”。 | **Off-the-shelf** (Blue lines)  vs. **Trained NetVLAD** (Red lines) | 在 Pitts250k 上，Recall@1 从 **55.0%** 提升到了 **81.0%** 。 | **结论：** 传统的 ImageNet 特征不适合地点识别。**端到端训练 (End-to-End Training) 是王道**，能带来质的飞跃。 |
| **Exp 2**    | **架构优越性：** 证明“复杂的 NetVLAD 层比简单的 Max Pooling 好”。 | **$f_{max}$** (Max Pooling)  vs. **$f_{VLAD}$** (NetVLAD)    | 实线 ($f_{VLAD}$) 始终高于虚线 ($f_{max}$)。即使都经过训练，NetVLAD 依然更强 。 | **结论：** 简单的池化丢失了太多信息。**统计特征聚合 (Aggregation)** 能捕捉更丰富的环境细节。 |
| **Exp 3**    | **数据必要性：** 回应“是不是只靠架构就赢了？弱监督数据真的重要吗？” | **Trained w/o Time Machine**  vs. **Trained w/ Time Machine** | 不用时光机数据训练，Recall@1 只有 **38.7%**；用了之后飙升到 **68.5%** 。 | **结论：** 架构虽好，但**数据 (Data) 是灵魂**。利用弱监督学习视角的变换（Time Machine），是网络具备泛化能力的关键。 |
| **Exp 4**    | **紧凑性 (Efficiency)：** 证明“不仅效果好，而且省空间（适合移动端/机器人）”。 | **High Dim** (4096-D)  vs. **Low Dim** (128-D/256-D)         | **128-D** 的 NetVLAD 竟然能打败 **512-D** 的 Max Pooling 。  | **结论：** NetVLAD 生成的描述符**极具辨识度 (Discriminative)**，可以用极小的代价实现高性能检索。 |
| **Exp 5**    | **泛化能力 (Generalization)：** 证明“不仅能认路，还能用来做通用的图像检索”。 | **State-of-the-Art** (SOTA)  vs. **NetVLAD**                 | 在 Oxford 5k / Paris 6k 等标准数据集上，全面超越当时的 SOTA  | **结论：** (这是一个 Bonus) 我们的方法是通用的，**它学到了图像匹配的本质**，而不只是记住了几条街道。 |

此时再回过头来看，这篇论文之所以能成为 VPR（Visual Place Recognition）领域的“万恶之源”或“开山之作”，是因为它**极其完整**。它没有留下明显的短板——从理论推导（VLAD微分化），到工程实现（弱监督挖掘），再到实验验证（全方位吊打 Baseline），形成了一个无懈可击的逻辑堡垒，基本上每一个issue、每一个Innovation都有回应，都给出了proof！

---

# 参考文献(八卦)

> 又到了喜闻乐见的环节，参考文献里的“彩蛋” (Easter Eggs in References)
>
> *注：该部分内容完全由Gemini生成，请自行甄别内容*

如果你仔细观察这篇论文的参考文献，你会发现几个非常有意思的“学术八卦”和“传承脉络”：

1. **“自己卷自己”的进化史 (The Evolution of Self):**
   -  "All about VLAD" (CVPR 2013): 这篇论文的第一作者（Arandjelović）和最后作者（Zisserman）在 2013 年其实已经把传统的 VLAD 算法做到了极致。
   - **彩蛋:** NetVLAD 其实是作者对自己过去工作的“自我革命”。他们意识到手工设计的 VLAD 已经到了天花板，于是通过引入可微分模块（NetVLAD Layer），亲手把自己的旧作“拍在沙滩上”。这是一种非常高级的学术自信。
2. **“数据大户”的加入 (The Data Provider):**
   -  Torii et al. (CVPR 2013/2015): 你会发现 Torii 的名字在参考文献里反复出现，同时他也是 NetVLAD 这篇论文的第三作者 。
   - **彩蛋:** 这解释了为什么 NetVLAD 能用上 Google Street View Time Machine 这么好的数据。Torii 团队之前一直在做基于街景的定位，他们手里有数据和 Baseline。这篇论文其实是 **Deep Learning 专家 (Oxford/INRIA)** 和 **Robotics/VPR 专家 (Tokyo Tech)** 的一次强强联手。
3. **计算机视觉与机器人的跨界 (Vision meets Robotics):**
   -  FAB-MAP (Cummins & Newman): 这是机器人领域做 SLAM 回环检测的神作。
   - **彩蛋:** 引用这些论文表明，NetVLAD 的野心不仅仅是做“图像检索”（像百度搜图那样），而是想解决“机器人定位”（Robotics Localization）的问题。这也是为什么它后来在自动驾驶领域（如 Apollo）如此火爆的原因。

---

# 插曲-NetVLAD的梯度流

{{< notice note>}}

NetVLAD生来就是为了端到端训练的，此时梯度如何穿过 soft-assignment 与残差聚合，分别落到 descriptors 和 cluster centers？

{{< /notice >}}    

首先，记回传梯度的主干为 $ g _ { k } = \frac { \partial L } { \partial v _ { k } } \in R ^ { D }$

1. 回传到聚类中心的梯度

   这是最简单也最优雅的一路。

   在 NetVLAD 的设计中，作者特意将**分配参数** ($w_k, b_k$) 与**残差中心** ($c_k$) 解耦了 。这意味着 $c_k$ **只出现在残差项** $(x_i - c_k)$ 中，而不参与计算分配权重 $\bar{a}_k$。

   因此，梯度流向 $c_k$ 的路径非常直接：
   $$
   \frac{\partial L}{\partial c_k} = \sum_{i=1}^{N} \frac{\partial L}{\partial V_k} \cdot \frac{\partial V_k}{\partial c_k} = \sum_{i=1}^{N} g_k \cdot (-\bar{a}_k(x_i))
   $$

   > **直观理解：**
   >
   > - **物理意义：** 聚类中心 $c_k$ 的更新，等于所有分配给它的特征点 $x_i$ 的梯度的**加权和**（方向取反）。
   > - **“引力”作用：** 如果 Loss 告诉我们某个 $V_k$ 太大了（需要减小），那么 $c_k$ 就会顺着梯度，向着那些“这一类里权重最大”的 $x_i$ 移动。这就像是 $c_k$ 被它管辖的 $x_i$ 们根据“投票权重”拉着跑，以此来减小残差。
   > - **"中心坍缩："** 这种依赖softmax的更新方式也导致一个新的问题，如果对于本身就没有得到分配的簇( $\bar{a}_k(x_i) \approx 0$ )，更新时梯度消失 $\frac{\partial L}{\partial c_k} \approx 0$。因为没有梯度，这个中心 $c_k$ 就不会移动；因为它不移动，它就永远离数据很远。它变成了一个“僵尸节点”，浪费了参数量，却对网络没有任何贡献。<mark>这再次说明NetVLAD对初始化和优化过程的要求很高。</mark>

2. 落到描述符的梯度

   这才是端到端训练的灵魂所在。前面的 CNN 到底该提取什么样的特征？这个信号就是通过 $x_i$ 的梯度传回去的。

   由于 $x_i$ 同时出现在公式的**两处**（既决定了它去哪个类，又决定了它的残差是多少），梯度会分化为两条路径回传：

   #### 路径 A：通过残差回传 (Via Residual)

   这是最直观的一路。假设分配权重 $\bar{a}$ 不变：

$$
( \frac { \partial L } { \partial x _ { i } } ) _ { r e s }= \sum_{k=1}^{K} \bar{a}_k(x_i)g_k
$$

- **物理意义：** 无论 $x_i$ 被分到哪个类 $k$，它都必须负责减小那个类的残差。这部分梯度告诉 CNN：**“微调一下特征值，让它离它所属的中心 $c_k$ 更近一点（或者更符合 Loss 的要求）。”**

  #### 路径 B：通过分配回传 (Via Assignment/Softmax)

   这是 NetVLAD 相比传统 VLAD 的必杀技。$x_i$ 的微小变化会改变它在各个聚类中心的 Softmax 权重 $\bar{a}_k$。根据[methodology章节](#methodology)的公式，Softmax 的输入分数（Logits）记为 $s_k$：
  $$
  s_k = w_k^T x_i + b_k
  $$
  
  $$
  ( \frac { \partial L } { \partial x _ { i } } ) _ {assign}=   \sum_{k=1}^{K} \left( \frac{\partial L}{\partial \bar{a}_k}   \right) \cdot \frac{\partial \bar{a}_k}{\partial x_i}
  $$
  
  这里 $\frac{\partial L}{\partial \bar{a}_k}$ 为从 Loss 传下来的、关于权重 $\bar{a}_k$ 的梯度标量($g_k^T (x_i - c_k)$)。
  $$
  \begin{aligned} \frac{\partial \bar{a}_k}{\partial x_i} 
  &=   \frac{\partial}{\partial x_i} \left( \frac{e^{s_k}}{\sum_j   e^{s_j}} \right) \\ &= \frac{ \left( \frac{\partial e^{s_k}}{\partial x_i} \right) (\sum_j e^{s_j}) - (e^{s_k}) \left( \frac{\partial \sum_j e^{s_j}}{\partial x_i} \right) }{(\sum_j e^{s_j})^2} \\
  &= \frac{ (e^{s_k} w_k) (\sum_j e^{s_j}) - (e^{s_k}) (\sum_j e^{s_j} w_j) }{(\sum_j e^{s_j})^2} \\
  &= \frac{e^{s_k}}{\sum_j e^{s_j}} \cdot w_k - \frac{e^{s_k}}{\sum_j e^{s_j}} \cdot \frac{\sum_j e^{s_j} w_j}{\sum_j e^{s_j}} \\
  &= \bar{a}_k w_k - \bar{a}_k \left( \sum_{j=1}^{K} \bar{a}_j w_j \right)
  \end{aligned}
  $$
   **整理得到最关键的“中心化”公式：**
  $$
  \frac{\partial \bar{a}_k}{\partial x_i} = \bar{a}_k \left( w_k - \underbrace{\sum_{j=1}^{K} \bar{a}_j w_j}_{\bar{w}_{\text{weighted}}} \right)
  $$
  
  $$
  ( \frac { \partial L } { \partial x _ { i } } ) _ {assign} = \sum_{k=1}^{K} \left[ g _ { k } ^ { T } ( x _ { i } - c _ { k } ) \right]  \bar{a}_k (w_k - \bar{w}_{\text{weighted}}) \\
  $$
  **物理意义（注意力机制）：** 这部分梯度告诉 CNN：**“如果当前的分类导致 Loss 很高，那就干脆改一下特征，把它扔到另一个更好、Loss 更低的聚类中心去！”**
  
  因此，总的梯度公式应该表示如下：
  $$
  \frac { \partial L } { \partial x _ { i } } = ( \frac { \partial L } { \partial x _ { i } } ) _ { r e s } + ( \frac { \partial L } { \partial x _ { i } } ) _ {assign} \cdot \\
  \frac { \partial L } { \partial x _ { i } } = \sum _ { k } \bar{a}_k(x_i) g _ { k } + \sum _ { k } \left[ g _ { k } ^ { T } ( x _ { i } - c _ { k } ) \right] \bar{a}_k(x_i) ( w _ { k } - \sum _ { j } \overline { a } _ { i j } w _ { j } ) .
  $$
  {{< notice note>}}
  
  此时我们再来回顾$\text{softmax}$的问题
  
  当分配饱和的时候，$\text{softmax}$成为$\text{one-hot}$向量，即存在某个$k$，使得$\bar{a}_k(x_i)\to1$，这就导致后一项$( w _ { k } - \sum _ { j } \overline { a } _ { i j } w _ { j } ) \to0$，因此整条 $assignment$ 路径几乎断掉，只剩下$res$流在回传梯度，最终导致幽灵簇的产生
  
  {{< /notice >}}    

> 因此 Input-Norm、合适的 $\alpha$/温度、以及良好 cluster init 的目的之一就是保持 early training 的 $\bar a$ 有足够熵，避免过早 one-hot，这也是[博客里](/notes/vlad)讨论的核心！