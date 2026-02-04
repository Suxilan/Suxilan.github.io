---
title: "CricaVPR论文阅读"
date: 2026-02-03T16:27:38+08:00
draft: False

tags: ["CricaVPR","Visual Place Recognition","VPR","影响检索","Deep Learning"]
categories: ["论文阅读"]
series: ["VPR-Series"]
author: "Suxilan"

comments: true
showlastmod: true
lastmod: 2026-02-03T16:27:38+08:00
summary: "Lu Feng博士的另一神作，看看大佬是怎么写作的"
# description: "正文页标题下副标题（可选；没写就不显示）"

# Stack 主题内置字段（按需开启/关闭）
# toc: true
# math: true

image: "https://cdn.jsdelivr.net/gh/Suxilan/Cloud-Image-alpha/imagebed/20260203163858897.png"   # Stack 原生封面字段（推荐）
---

# 摘要(Abstract)

还是老样子，我们开篇先看摘要：

> Over the past decade, most methods in visual place recognition (VPR) have used  neural networks to produce feature representations. <mark>These networks typically produce
> a global representation of a place image using only this image itself and neglect the cross-image variations (e.g. viewpoint and illumination), which limits their  robustness in challenging scenes.</mark> In this paper, we propose a robust global representation method with cross-image correlation awareness for VPR, named CricaVPR. <mark style="background: palegreen">Our method uses the attention mechanism to correlate multiple images
> within a batch. These images can be taken in the same place with different conditions or viewpoints, or even captured from different places. </mark>Therefore, our method can utilize the cross-image variations as a cue to guide the representation learning, which ensures more robust features are produced. <mark style="background: lightpink">To further facilitate the robustness, we propose a multi-scale convolution-enhanced adaptation method to adapt pre-trained visual foundation models to the VPR task, which introduces the multi-scale local information to further enhance the cross-image correlation-aware representation.</mark> Experimental results show that our method outperforms state-of-the-art methods by a large margin with significantly less training time. The code is released at https://github.com/Lu-Feng/CricaVPR.

作者上来就放大招啊，非常的自信，直接点名现在的研究痛点

* 现有的网络通常只利用**单张图像本身**来生成全局特征，而忽略了**跨图像的变化**（cross-image variations），例如视角 (viewpoint) 和光照 (illumination) 的变化 。

  **后果：** 这限制了模型在复杂场景下的鲁棒性 。

因此这里作者也不卖关子了啊，直接点出两个贡献：

1. **跨图像相关性感知 (Cross-image Correlation Awareness):** 方法利用注意力机制 (attention mechanism) 将一个 batch 中的多张图像关联起来 。这些图像可能是同一地点不同条件下拍摄的，也可能是不同地点的 。通过这种关联，模型利用跨图像的变化作为线索来指导特征学习，从而生成更鲁棒的特征 
2. **多尺度卷积增强适配 (Multi-scale Convolution-enhanced Adaptation):** 作者并没有从头训练，而是利用了预训练的**视觉基础模型 (Visual Foundation Models)** 。为了让大模型适应 VPR 任务，他们设计了一种适配方法，引入多尺度局部信息来增强特征 。

{{< notice note>}}

从中这里可以看出，作者也是老CV人了啊，随便找一个CV人来看都不会怀疑这两个idea有任何的问题——因为实在是太稀疏平常了（对于CV中的trick而言）。重点还是看作者是怎么把这样的idea包装成一篇CVPR的论文的吧！

{{</ notice >}}

# 引言(Introduction)

引言的前两段我们直接来看重点内容：

> However, they lack robustness in challenging environments and are often susceptible to perceptual aliasing. <mark>A way to improve robustness is to perform re-ranking by matching local features [26, 59]</mark>, which incurs huge overhead in runtime and memory footprint, making it difficult to achieve large-scale VPR. One problem that has been neglected is that existing methods produce the feature of an image only using this image itself (without cross-image interaction), which does not explicitly consider cross-image variations. 
>

## 对于第一个动机

<a id="our-conclusion"></a>
这其实可以理解为一个很通俗的问题，光照、视点变换这些可以理解为一个噪声，对抗这些噪声，提升鲁棒性的最佳方法就是

1. 增大模型参数量 
2. 增加更多数据、计算量。

作者这里其实就是通过增大计算量，batch内相互检查的这样手段，有点类似于reranking（文中作者也提到了）当然作者这里特意只是提了一个基于local feature的ranking，因为这在当前并不是什么很新的东西。两阶段的检索都是带reranking的，只不过作者这里是online的端到端的这种reranking。这样写的好处是，**完全封死了审稿人对这种创新的质疑：*你的这种方法和R2Former、TransVPR这种有什么区别呀***

**答：**CricaVPR在**特征学习阶段**（Training）就做图像对比。模型在训练时“看”了很多图像对，学会了什么该忽略（噪声）、什么该保留（地标），最终把这种能力“压缩”进了单一的全局特征里。**推理时，我们依然是单次前向传播，速度完胜。**

## 第二个动机，硬凑？

> 在adaptor的提出中，作者动机是是什么。怎么与Cross-image Correlation这个动机耦合的？我感觉就是为了提点因凑的idea啊，随便环一个adapter的idea也许都可以（比如EMVP的dpn，selavpr等）

1. 这里作者的叙事逻辑是这样的：

   **大模型的“水土不服”：** 作者先捧了一下 DINOv2（基础模型强），然后马上说它直接用在 VPR 上有问题：

   > "directly using the pre-trained foundation model will encounter some problems... ignore some discriminative backgrounds, and are susceptible to interference from dynamic foregrounds"  （直接使用预训练模型会有问题……倾向于忽略一些有判别力的背景，且容易受动态前景干扰。）

* **潜台词：** DINOv2 这种通用大模型，可能更关注“这是一辆车”，而不是“这辆车后面那个特定的窗户形状”。

2. **现有 Adapter 的缺陷（Language-oriented vs. Vision-specific）：** 作者指出，现有的 PETL (Parameter-Efficient Transfer Learning) 方法大多源自 NLP，或者缺乏针对视觉任务的**多尺度局部先验 (Multi-scale local priors)**。

   > "lack the image-related (multi-scale) local priors for visual tasks (especially for VPR)."  （缺乏针对视觉任务——特别是 VPR——的图像相关（多尺度）局部先验。）

3. **VPR 的特殊性 —— 地标是“局部”且“多尺度”的：** 这是最关键的 justify：

   > "discriminative landmarks that need attention in VPR often occupy local regions of uncertain size"  （VPR 中需要关注的判别性地标通常占据大小不确定的局部区域。） 因此，作者提出了 **Multi-scale Convolution (MulConv)** Adapter，用卷积（Convolution）来强制模型关注局部几何结构，用多尺度（Multi-scale）来应对地标大小不一的问题。

我们再来看第二个贡献——“multi-scale convolution adapter”，就单独看它的动机，可以说完全没有问题！但是如果只是看了论文标题，可以说这个动机不完全耦合！我们可以强行解释一下，多尺度adapter提升了特征性能，这样在后面做cross image的时候这个全局特征会更好，更有利于相互之间捕捉到有用的信息。**文章后文中其实也有讲到**

不过，真的是这样吗？只能说，意味深长的笑一下（很像我们平时自己写论文时候的感觉）相比读了NetVLAD这样的神作，读了这种严丝合缝的逻辑链条，确实会让自己的审美更加挑剔一些，不过对当前的社区环境来讲，两个够硬的idea已经足够一篇顶会了。

# 方法(Methodology)

![](https://cdn.jsdelivr.net/gh/Suxilan/Cloud-Image-alpha/imagebed/20260204211105791.png "Pipeline of CricaVPR")

## 1. 跨图像相关性感知的位置表示 (Cross-image Correlation-aware Place Representation)

这是论文最核心的创新（对应原文 Section 3.2），旨在让模型在训练阶段就能“看到”Batch 内的其他图像，从而“取长补短”。

### **(1) 特征提取与空间金字塔划分**

- **输入：** 一个 Batch 的图像。
- **初步特征：** 图像经过 Backbone（ViT）输出 Patch Tokens，被重塑（Reshape）为特征图 。
- **空间金字塔 (Spatial Pyramid)：** 为了保留空间信息，作者没有直接把所有 Token 聚合，而是使用了空间金字塔池化 。
  - 将特征图划分为三个层级：$1\times1$（全图），$2\times2$（4个区域），$3\times3$（9个区域）。
  - 在这 $1+4+9=14$ 个区域内分别进行 **GeM (Generalized Mean) Pooling** 。
  - **细节：** 对于第1层（全局），作者直接使用了 ViT 的 **[class] token** 来代替 GeM 特征，因为 [class] token 表现更好 。
  - **结果：** 每张图片现在由 **14个区域特征向量** 表示。

### **(2) 核心机制：跨图像编码器 (Cross-image Encoder)**

这是最精彩的一步。传统的 Attention 是在“同一张图的不同 Patch 之间”做，而这里是在**“不同图的同一位置区域之间”**做。

- **序列构建：** 作者取出一个 Batch 中所有图像的**第 $i$ 个**区域特征，组成一个序列 $f_i$ 。
  - 例如：取 Batch 里所有图片的“左上角”特征，组成一个序列。
- **交互过程：** 将这个序列输入到 **Cross-image Encoder** 中 。
  - **结构：** 这个 Encoder 包含 2 层标准的 Transformer Encoder Layer（包含 MHA, MLP, LN 和残差连接）。
  - **作用：** 在这个过程中，图片 A 的“左上角”会和图片 B、C、D 的“左上角”进行 Attention 交互。
    - 如果是正样本（同地点的图），它们会相互增强，提取不变特征（如建筑轮廓）。
    - 如果是负样本（不同地点但相似的图），模型会学习区分细微差别 。
- **并行处理：** 对 14 个区域分别重复上述过程。

### **(3) 全特征生成**

- 经过 Cross-image Encoder 增强后的 14 个区域特征，被**拼接 (Flatten)** 起来，然后进行 **L2 归一化**，最终形成该图像的全局特征表示 。
- **注意：** 这里最终的特征维度其实是768×14，但是如果说这样就是（Ours）方法的最终维度那就大错特错啦！！！很容易被审稿人狙击，亲测踩坑！我们一般先用PCA之后的维度当作最终维度，一般PCA到合适的维度都不会降低效果，反而会增强性能，这里可以参考[另一篇白化的博客](/notes/whitening)！

## 2. 多尺度卷积增强适配 (Multi-scale Convolution-enhanced Adaptation)

这是为了解决直接使用 DINOv2 进行 VPR 效果不佳的问题（对应原文 Section 3.3）。作者认为 VPR 需要特定的局部几何信息，而这是纯 ViT 结构所欠缺的。

### **(1) 适配器 (Adapter) 的位置**

- 作者采用了参数高效微调 (PETL) 的思路，冻结预训练的 DINOv2 (ViT-B/14) 参数 。

  在 ViT 的每一个 Transformer Block 的 **MLP 层**旁边，**并联**插入了这个自定义的 Adapter 。

- 公式表示为：$Output = MLP(x) + s \cdot Adapter(x) + x$，其中 $s$ 是一个缩放因子（设为0.2）。

### **(2) MulConv Adapter 的内部结构**

这是对传统 Adapter（通常是 Down-project -> Activation -> Up-project）的改进，灵感来源于 GoogLeNet 的 Inception 模块 。

- **瓶颈结构 (Bottleneck)：** 首先通过一个下投影层减少维度，最后通过上投影层恢复维度，保持轻量化 。

- **核心模块：MulConv Module** 在激活函数（ReLU）之后，插入了一个多尺度卷积模块，包含三条并行的路径 ：

  1. **$1\times1$ 卷积：** 捕捉极小的局部细节。
  2. **$3\times3$ 卷积：** 捕捉中等尺度的局部几何结构。
  3. **$5\times5$ 卷积：** 捕捉较大范围的局部上下文。

- **降维细节：** 在 $3\times3$ 和 $5\times5$ 卷积之前，都先用一个 $1\times1$ 卷积来压缩通道数，以减少计算量 。

- **特征融合：** 三条路径的输出被**拼接 (Concatenated)**，再加上一个残差连接 (Skip Connection)，最后输出给上投影层 。

  <mark style="background:lightgreen">*这种先降维再升维度的做法又何尝不是一种低秩微调呢？*</mark>

### **(3) 设计动机**

- **为什么是卷积？** 为了引入图像相关的**局部归纳偏置 (Local Inductive Biases)**，这对于识别具体的物理地标至关重要 。
- **为什么是多尺度？** VPR 中的关键地标（如路牌、窗户、整个建筑）在图像中占据的大小是不确定的。多尺度卷积核能同时覆盖这些不同大小的特征，比单一尺度的卷积（如 Convpass 只用 3x3）更有效 。

{{< notice info>}}

看到这里，如果我是审稿人，突然就会觉得有一种峰回路转的感觉，作者这里的Cross-image Correlation-aware Place Representation巧妙在于，它使用了多尺度的GeM池化的输出，来进行进一步交互。这就和后面的MulConvAdaption耦合起来了，让人找不到攻击的点

{{</ notice >}}

# 实验 (Experiments) 

这里我们重点看消融实验，作者是如何通过实验设计来“圆”这个故事的。CricaVPR 的实验部分设计得非常严密，主要分为三个层次来回应他的核心动机：

##### 1. 证明“跨图像相关性” (Cross-image Correlation) 真的有用

**动机回顾：** 作者认为单张图容易受环境干扰，多张图交互可以增强鲁棒性（去噪）

**实验设计 (Table 4)：** 作者构建了三个基准特征，分别测试加上“Crica”模块后的效果：

- **基准 1 (GeM)：** 传统的全局池化。
- **基准 2 (SPMG)：** 基于 GeM 的空间金字塔（分块）。
- **基准 3 (SPM - 本文底座)：** 空间金字塔 + [class] token。

**结果与故事闭环：**

- **证据：** 加上 Crica 后，所有基准的性能都提升了。特别是在 **Tokyo24/7** 这个数据集上（包含极端的昼夜变化），`AdaptGeM + Crica` 比单纯的 `AdaptGeM` 提升了惊人的 **17.4%** (R@1) 。
- **结论：** 这强有力地证明了 Cross-image 机制确实赋予了模型对抗极端光照变化（Day/Night）的能力，不仅仅是分数提升，而是解决了他承诺的“环境不变性”问题。

#### 2. 证明“MulConv Adapter” 是最佳方案

**动机回顾：** 直接微调大模型会遗忘，且普通 Adapter 缺乏 VPR 所需的“多尺度局部几何信息”。

**实验设计 (Table 5)：** 作者对比了五种不同的微调策略：

1. **Frozen DINOv2:** 不动参数（基线）。
2. **FullTuned DINOv2:** 全量微调。
3. **VanillaAdapter:** 普通适配器（NLP 常用）。
4. **ConvAdapter:** 只有 3x3 卷积的适配器（类似 Convpass）。
5. **MulConvAdapter (Ours):** 多尺度卷积适配器。

**结果与故事闭环：**

- **击败全量微调（关于“遗忘”）：** 全量微调在 Pitts30k（简单）上很强，但在 Tokyo24/7（跨域）上反而比冻结模型还差！这证明了全量微调确实存在“灾难性遗忘” 。而作者的 Adapter 方法在 Tokyo24/7 上稳住了，证明了 PETL 方法的优越性。

{{< notice note>}}

不过这里有存疑的地方，作者只有两张3090，全量微调DINOv2是一件很困难的事情。而且GSVCitys大家能把它拿来当共认的训练benchmark，我感觉这种domain的泛化性应该还是很好的，不应该出现这种所谓的灾难性遗忘。

{{</ notice >}}

- **击败其他 Adapter（关于“多尺度”）：**
  - ConvAdapter (单尺度卷积) 比 VanillaAdapter (无卷积) 效果还差 。这看似打脸，实则被作者用来反证：**“不恰当的局部先验”是有害的**。
  - MulConvAdapter (多尺度) 取得了最好效果。
  - **结论：** 这完美支撑了 Intro 里的论点——VPR 的地标大小不一，必须用**多尺度**卷积来捕捉，单用 3x3 卷积是不够的。

####  3.效率反击战：打破“慢”的刻板印象

**动机回顾：** 大家通常认为加了 Cross-image 这种复杂的交互，训练肯定很慢。

**实验设计 (Table 7)：**

- 作者展示了训练时间：只需 **3.5小时** (10 epochs) 就能训练完，而竞品 MixVPR 需要 30 epochs，EigenPlaces 需要整整一天 。
- 甚至，只用 **10% 的数据训练 1 个 epoch**（仅耗时 2.3 分钟），效果就能超过很多旧的 SOTA 。

**结论：** 这是一个非常漂亮的“回马枪”。作者证明了：因为利用了强大的 DINOv2 底座 + 高效的 Cross-image 监督信号，模型收敛极快。这不仅消除了对计算量的担忧，还变成了一个额外的卖点（Data Efficiency）。

# **玄机揭晓** 

在之前的正文中，作者声称“检索过程和普通全局检索方法一样”（暗示单张图提取特征），但这其实是“避重就轻”。**实施细节以及补充材料 Section F (Effects of Batch Size)** 彻底揭开了这个盖子：

**原文实锤：**

> "Since our method learns cross-image correlation-aware representation during training, **setting the batch size to 1 during testing makes our cross-image encoder ineffective**... performance in this case will be reduced."  （由于我们的方法在训练时学习了跨图像相关性，测试时如果把 Batch Size 设为 1，会使 Cross-image encoder 失效……性能会下降。）

**具体配置：** 作者明确承认，他们在测试时并没有一张一张图推，而是强行凑了 Batch。

> "So we set it to 16 (except on Pitts30k/Pitts250k we set it to 8 for better results)."  （所以我们将推理 Batch Size 设为 16，Pitts 数据集设为 8。）

**这就带来了一个巨大的潜在问题：** 这意味着提取出的特征是不稳定的（Non-deterministic）。图片 A 的特征，取决于它是和图片 B 一起 Inference，还是和图片 C 一起 Inference。

- 如果 Batch 里的其他图是随机凑的，那么特征就会有波动。
- 作者实际上是利用了 Batch 内的统计信息（虽然是 Test time）来辅助特征生成。这在严格的 VPR 落地场景（比如这就来了一帧新图要定位）其实是有很大局限性的，因为你可能凑不齐 16 张图，或者凑出来的图对于当前图没有正向增益。

**[这里其实也印证了上面一开始我们的结论——提点无非就是“更大的模型参数、更多的计算量、信息量”](#our-conclusion)**

{{< notice danger>}}

这里其实还有一个非常值得探讨、存疑的地方，**一个可能产生OOD的地方**：

这种对比学习的训练、一个batch中必须包含正负样本，也对应作者这里的配置

- **配置：** Batch Size = 288 (72 个地点 $\times$ 4 张图/地点) 。
- **交互逻辑：** Cross-image Encoder 接收这 288 张图作为序列输入
- **正样本（Positives）：** 对于 Batch 中的任意一张图（Anchor），只有 **3张** 可能是它的“队友”（来自同一地点）。Cross-image Encoder 的 Attention 机制在此时的作用是 **“共识构建” (Consensus Building)** —— 即通过与这 3 张图交互，增强那些环境不变的特征（如建筑轮廓），抑制光照噪声。
- **负样本（Negatives）：** 剩下的 **284张** 都是“敌人”（来自其他 71 个地点）。Attention 机制在此时的作用是 **“判别增强” (Discriminative Learning)** —— 学习如何与这些长得很像但不是同一地点的图划清界限。

但是，推理时的输入完全不一样，在推理时，进来的 16 张 Query 图片通常是**随机**的或者**时序**的。如果是时序的，可能会有增强，但是也与训练时这种一个序列中大部分负样本的情况差异很大。如果是随机的，那就更可疑了，如果能够增强，只能说transfomer对特征区分度的增强，但是和文章故事——“视点变换”、“光照变化”等完全不耦合。

{{</ notice >}}

上述仅为个人浅薄的观点，如有逻辑漏洞，阅读漏洞还请指出。
