---
title: "重温Attention is all you need"
date: 2025-11-07T14:48:34+08:00
lastmod: 2024-11-20 18:00:00 +0800
showLastMod: true
draft: false
tags: ["Deep Learning", "Transformer", "NLP", "Attention"]
categories: ["技术笔记"]
series: []
author: "Suxilan"
ShowToc: true
TocWide: true
comments: true  # 默认启用评论
description: "深入理解Transformer架构：从RNN的局限到注意力机制的革命"
summary: "结合可视化工具和论文，系统学习Transformer的核心原理"
---

## 摘要

本笔记基于论文 ["Attention is All You Need"](https://arxiv.org/abs/1706.03762) (Vaswani et al., 2017)，结合 [Transformer Explainer](https://poloclub.github.io/transformer-explainer/) 可视化工具和相关博客资料，系统梳理 Transformer 架构的核心思想。

Transformer 是一个具有里程碑意义的神经网络架构，它从根本上改变了人工智能的发展方向。自 2017 年提出以来，Transformer 已成为深度学习的主流架构，支撑着 OpenAI 的 **GPT**、Meta 的 **Llama**、Google 的 **Gemini** 等文本生成模型。不仅如此，Transformer 还被应用于音频生成、图像识别、蛋白质结构预测，甚至游戏对弈等众多领域，展现了其跨域的强大能力。

---

## 1. 引言

### 1.1 Transformer 出现前的时代：RNN 和 LSTM

在 Transformer 出现之前，处理序列数据（如句子、语音或时间序列）的主流模型是**循环神经网络（Recurrent Neural Networks, RNN）**，特别是其高级变体：**LSTM**（Long Short-Term Memory，长短期记忆）和 **GRU**（Gated Recurrent Unit，门控循环单元）。

#### RNN 的核心思想

RNN 的设计理念非常直观：它像人类阅读一样，**逐个**处理序列中的元素（例如，一个一个地读取单词）。

假设我们要处理句子 "I am a student"：

1. **第 1 步**：RNN 读取第一个单词 "I"，生成一个"记忆"或"摘要"，称为**隐藏状态**（hidden state）记作 `h_I`
2. **第 2 步**：RNN 读取第二个单词 "am"，**结合**当前单词信息和**上一步的隐藏状态 `h_I`**，生成新的隐藏状态 `h_am`
3. **第 3 步**：读取 "a"，结合 `h_am`，生成 `h_a`
4. **第 4 步**：读取 "student"，结合 `h_a`，生成 `h_student`

最终的隐藏状态（或每一步状态的组合）就被认为是整个句子的编码表示。

这种**递归**结构在理论上非常适合处理序列，因为它自然地捕捉了单词的顺序和上下文关系。

### 1.2 RNN/LSTM 的两大瓶颈

然而，RNN 的这种"循环"或"串行"特性也正是其最大的问题所在。

#### **问题 1：信息传递的瓶颈——长程依赖难题**

在 RNN 中，信息必须**逐步传递**。如果一个句子有 50 个单词：

- 第 1 个单词的信息要传递到第 50 个单词，必须"走过" **49 步**
- 每一步传递都会有信息的损耗或变形
- 这导致了著名的**梯度消失/梯度爆炸**问题

用一个形象的比喻：RNN 就像**电话游戏（传话游戏）**。

- 第一个人说："今天天气真好"
- 传到第二个人："今天天气好"
- 传到第三个人："今天很好"
- ...
- 传到第 10 个人："好"

信息在逐步传递的过程中逐渐失真，远处的重要信息很难完整保留。

虽然 LSTM 通过引入"门控机制"（Gate Mechanism）缓解了这个问题，但并未从根本上解决。

#### **问题 2：计算效率的瓶颈——无法并行化**

RNN 的计算是**绝对串行**的：

```
h_I → h_am → h_a → h_student
```

- 你**必须**先计算完 `h_I`，才能计算 `h_am`
- 你**无法**在计算 `h_I` 的同时，去计算 `h_a`
- 每一步的计算都依赖于前一步的结果

这在现代硬件（如 GPU）上是个致命缺陷：

- **GPU** 的优势在于**大规模并行计算**（同时计算成千上万个矩阵元素）
- 但 RNN 的串行特性让 GPU 大部分算力都在"等待"
- 训练速度极慢，尤其在处理长序列或大规模数据集时

### 1.3 核心矛盾的总结

| 特性 | RNN/LSTM 的局限 |
|:---|:---|
| **信息路径** | 远距离单词间的信息需要逐步传递，容易失真（梯度消失） |
| **计算方式** | 串行计算，必须等待前一步完成 |
| **硬件利用** | 无法充分利用 GPU 的并行计算能力 |
| **训练效率** | 在大规模数据集上训练极慢 |

---

## 2. Transformer 的核心创新：自注意力机制

### 2.1 革命性的转变

Transformer 的核心突破在于：**完全抛弃了循环结构**，转而使用**自注意力机制（Self-Attention Mechanism）**。

#### **关键创新 1：并行化计算**

还是用句子 "I am a student" 为例。

在 Transformer 的 编码器（Encoder）中：

- 计算 "student" 的表示时，模型可以**一步到位**地、**直接**看到 "I", "am", "a" 三个词
- 计算 "am" 的表示时，也**同时**看到 "I", "a", "student"
- **所有单词的计算是同时进行的**

这不是通过 `h_am` 间接"传递"信息给 `h_a`，而是像一个**全连接图**，所有单词在**同一时间**互相"观察"（计算注意力分数）。

这个"观察"的过程，在数学上是**一个大规模的矩阵乘法**。而 GPU 极其擅长并行计算矩阵乘法！无论句子是 10 个词还是 50 个词，计算所有词的表示都只需要**一次矩阵运算的时间**。

#### **关键创新 2：直接的长程依赖**

在 Transformer 中：

- 第 1 个单词到第 50 个单词的信息传递：**一步直达**
- 没有逐步传递造成的信息损耗
- 模型可以直接捕捉任意距离的依赖关系

用比喻来说：Transformer 就像一个**圆桌会议**。

- 所有人（所有单词）同时在场
- 主持人（当前单词）可以直接询问（Query）在场的每一个人（Key）
- 所有人（Value）同时把信息汇总给主持人
- **没有中间的传话环节**

### 2.2 训练 vs 推理：并行与串行的平衡

这里需要澄清一个重要的概念混淆：

#### **在训练（Training）时：完全并行**

在训练 Transformer 时（以翻译任务为例："I am a student" → "我 是 一名 学生"）：

- 我们会把正确答案 "我 是 一名 学生" **整个**喂给解码器（Decoder）
- 所有位置（"我", "是", "一名", "学生"）的计算在**一个大矩阵中并行完成**
- 为了防止"作弊"（即防止 "一名" 偷看到未来的 "学生"），使用**带掩码的自注意力（Masked Self-Attention）**：
  - 计算 "我" 时，只能看到 "我"
  - 计算 "是" 时，能看到 "我" 和 "是"
  - 计算 "一名" 时，能看到 "我", "是", "一名"
  - 掩码通过将"未来"词的注意力分数设为负无穷实现

**关键**：虽然有掩码，但计算本身是并行的！

#### **在推理（Inference）时：自回归串行**

在生成文本时（如 GPT 生成回答）：

- 必须先生成第 1 个词，才能生成第 2 个词
- 这是**自回归（Auto-regressive）**的特性
- 这部分确实是串行的

但即使在推理时，Transformer 相比 RNN 仍有优势：

- 编码器部分（理解输入）仍然是并行的
- 每一步生成都能直接访问所有历史信息，无需逐步传递

### 2.3 小结

Transformer 通过**自注意力机制**实现了两个革命性突破：

1. **并行化**：充分利用现代硬件（GPU/TPU）的并行计算能力，训练速度大幅提升
2. **长程依赖**：任意距离的单词间可以直接交互，无需逐步传递信息

这使得 Transformer 能够在超大规模数据集（如整个互联网的文本）上训练，成为现代大语言模型（如 GPT、BERT、Llama）的**基础架构**。

正如论文标题所言："**Attention is All You Need**"（注意力就是你所需要的一切）。

---

## 3. 自注意力机制的数学原理

前面我们从宏观角度理解了自注意力的优势，现在让我们深入其内部，看看它到底是如何工作的。

### 3.1 核心思想：基于上下文的动态关联

自注意力机制的核心思想是：**一个词在句子中的含义，是由它与句子中所有其他词（及自身）的关系共同决定的。**

让我们看一个经典例子：

> "The animal didn't cross the street because **it** was too tired."

在这个句子中，**"it"** 指的是什么？

- 如果后面是 "it was too **tired**"，"it" 很可能指 **"animal"**（动物累了）
- 如果后面是 "it was too **wide**"，"it" 就很可能指 **"street"**（街道太宽了）

自注意力机制就是让模型学会这种**动态的、基于上下文的关联**。它通过计算 "it" 与句子中所有其他词的相关性分数，从而决定应该从哪些词中"吸收"信息。

### 3.2 核心组件：Query, Key, Value (Q, K, V)

为了实现上述目标，自注意力机制为**每个输入单词**（更准确地说是每个词的嵌入向量 Embedding）创建三个不同的向量：

#### **1. Query（查询向量，Q）**

- **"我要找什么？"** 它是当前单词的"代理人"，负责去"提问"
- 比如，当模型处理 "it" 时，"it" 的 Q 向量会问："嘿，句子里的大家，谁最符合'我'（it）所指代的对象？"

#### **2. Key（键向量，K）**

- **"我是什么标签？"** 它是每个单词的"标签"或"索引"，用来被 Query 查询
- "animal" 的 K 向量会说："我是一个名词，表示动物"
- "street" 的 K 向量会说："我是一个名词，表示街道"
- "tired" 的 K 向量会说："我是一个形容词，表示疲惫"

#### **3. Value（值向量，V）**

- **"我的实际内容是什么？"** 它代表该单词的**实际语义信息**
- 当 "it" 的 Q 向量通过匹配 K 向量，发现 "animal" 是最佳匹配时，它最终"取走"的是 "animal" 的 V 向量

#### 搜索引擎类比

这个过程可以类比为一次**网络搜索**：

| 注意力机制 | 搜索引擎 |
|:--:|:---|
| **Query (Q)** | 你在搜索框输入的**搜索词** |
| **Key (K)** | 搜索引擎索引中每个网页的**标题/关键词** |
| **Value (V)** | 搜索引擎返回的网页**实际内容** |

查询词（Q）与关键词（K）匹配计算相似度，然后相应的内容（V）被按权重返回。

### 3.3 计算SDPA(Scaled Dot-Product Attention)

现在我们详细看看 "it" 这个词是如何通过自注意力更新自己的表示的。

#### **步骤 1：生成 Q, K, V 向量**

假设：
- "it" 的原始嵌入向量是 \(x_{it}\)
- "animal" 的嵌入向量是 \(x_{animal}\)

模型有三组**可学习的权重矩阵**：\(W^Q\), \(W^K\), \(W^V\)（这三个矩阵在**整个句子**中是共享的）

通过矩阵乘法生成 Q, K, V：

$$
\begin{aligned}
q_{it} &= x_{it} \cdot W^Q \\
k_{it} &= x_{it} \cdot W^K \\
v_{it} &= x_{it} \cdot W^V
\end{aligned}
$$

句子中**每个其他词**（如 "animal"）也同样生成自己的 K 和 V：

$$
\begin{aligned}
k_{animal} &= x_{animal} \cdot W^K \\
v_{animal} &= x_{animal} \cdot W^V
\end{aligned}
$$

根据 [Transformer Explainer](https://poloclub.github.io/transformer-explainer/) 的说明，在 GPT-2 (small) 中：
- 输入嵌入维度：768
- Q, K, V 向量维度：64（单个注意力头）

#### **步骤 2：计算注意力分数（Score）**

"it"（Query）需要知道它应该给句子中其他每个词（Key）多少关注度。

这个"关注度"通过计算 **Q 向量**和**所有 K 向量**的**点积（Dot Product）**来得到：

$$
\begin{aligned}
\text{Score}(it, it) &= q_{it} \cdot k_{it} \\
\text{Score}(it, The) &= q_{it} \cdot k_{The} \\
\text{Score}(it, animal) &= q_{it} \cdot k_{animal} \\
\text{Score}(it, street) &= q_{it} \cdot k_{street}
\end{aligned}
$$

如果 $q_i$ 和 $k_j$ 向量方向相似，点积值大，说明关联性强

**为什么使用点积？**可以参考我的另一篇[笔记]({{< relref "scaled_dot_product_attention.md" >}})，详细说明了使用点积进行相似度衡量的原因。

#### **步骤 3：缩放（Scale）**

这是 "Scaled Dot-Product Attention" 中 "Scaled" 的来源。将所有分数除以 $\sqrt{d_k}$（$d_k$ 是 K 向量的维度，例如 64）。

$$
\text{Scaled Score} = \frac{\text{Score}}{\sqrt{d_k}}
$$

**💡 为什么要缩放？（重要的工程细节）**

* 防止 $d_k$ 维度过大时，点积结果过大，导致 Softmax 函数的梯度消失，使训练不稳定。

**数学直觉**：如果两个独立的标准正态分布随机变量相乘，其方差为 1；如果有 \(d_k\) 个这样的乘积求和，方差就变成了 \(d_k\)。因此除以 \(\sqrt{d_k}\) 可以将方差拉回 1。详细的数学推导可以参考[笔记]({{< relref "scaled_dot_product_attention.md" >}})

#### **步骤 4：Softmax 归一化**

将缩放后的分数传入 **Softmax** 函数，得到**注意力权重** ($\alpha$)。

$$
\alpha_{i,j} = \text{softmax}(\text{Scaled Score}_{i,j})
$$

- 这会将词 $i$ 对所有其他词（包括自身）的分数转换成一个总和为 1 的概率分布。
- 例如，$\alpha_{\text{it, animal}}$ 可能是 0.85，$\alpha_{\text{it, street}}$ 可能是 0.05。

#### **步骤 5：加权求和**

使用上一步得到的注意力权重 $\alpha_{i,j}$，对所有词的 **Value 向量** ($v_j$) 进行加权求和，得到词 $i$ 的最终输出向量 $z_i$。
$$
z_i = \sum_{j} \alpha_{i,j} \cdot v_j
$$
**这意味着什么？**

"it" 的新表示 $z_{it}$ 是一个**加权混合体**：例如，"it" 的新向量 $z_{it}$ 将约等于： $0.85 \times v_{\text{animal}} + 0.05 \times v_{\text{street}} + \ldots$
- 它 **85%** 的"内容"来自 "animal" 的语义
- 再加上少量其他词的信息（如 "tired" 贡献了 6%）

通过这个过程，"it" 的向量表示成功地**融合了它所指代的 "animal" 的信息**，模型"理解"了 "it" 的指代关系。

（**实际情况可能更为复杂，尤其是在多层的MHA中**，*我其实对Transformer这里的注意力可解释分析也挺困惑的*）

### 3.4 论文中的统一公式

上述所有步骤可以合并为一个高效的矩阵运算公式，这正是 Transformer 能够大规模并行计算的关键：
$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$
这里 $Q, K, V$ 是**矩阵**，它们的每一行代表一个词的 Q, K, V 向量。

1. **$QK^T$**：计算出 $(n \times n)$ 的**分数矩阵**（$n$ 是句子长度），一次性完成所有词对所有词的点积（步骤 2）。
2. **$/\sqrt{d_k}$**：对整个矩阵进行缩放（步骤 3）。
3. **$\text{softmax}(\ldots)$**：对矩阵的**每一行**分别应用 Softmax，得到 $(n \times n)$ 的**权重矩阵**（步骤 4）。
4. **$(\ldots)V$**：将权重矩阵与 $V$ 矩阵相乘，得到 $(n \times d_v)$ 的**输出矩阵 $Z$**。矩阵 $Z$ 的每一行就是该词融合了全局上下文的新表示（步骤 5）。

**核心优势**：

- **并行计算**：所有计算都是矩阵乘法，非常适合 GPU 加速。
- **一步直达**：任意两个词之间的关联（无论距离多远）都可以通过一次矩阵运算直接计算，解决了 RNN 的长距离依赖问题。

### 3.5 可视化理解

根据 [Transformer Explainer](https://poloclub.github.io/transformer-explainer/) 的展示，自注意力的计算流程可以可视化为：

![](https://cdn.jsdelivr.net/gh/Suxilan/Cloud-Image-alpha/imagebed/notes/compute_attn.png)

### 3.6 小结

**自注意力机制（Scaled Dot-Product Attention）** 是一个精妙的计算过程：

1. **Query**：当前词要"查询"什么信息
2. **Key**：其他词提供的"标签"
3. **Value**：其他词的实际语义内容
4. 通过 Q 和 K 的点积计算**相关性**
5. 通过 Softmax 得到**注意力权重**（概率分布）
6. 用权重对 V 进行**加权求和**，得到融合了上下文的新表示

> 关于SDPA的设计哲学，我总结了其三个比较重要的核心支柱，放在另一个[笔记]({{< relref "scaled_dot_product_attention.md" >}})里详细讨论了。

这个机制是 Transformer 的**心脏**，但论文还有一个关键创新来进一步增强其能力：**多头注意力（Multi-Head Attention）**。

---

## 4. 多头注意力（Multi-Head Attention，MHA）

自注意力（SDPA）存在一个潜在问题：虽然我们在进行softmax之前对点积结果进行缩放，但是softmax归一化依然可能导致只对少数几个词产生上下文关联，而其余的被压制。**（如果模型只有一个注意力“头”，它可能只会学到一种类型的上下文关联。）**

例如，在处理 "The animal...because **it** was too **tired**" 时，这一个头可能学会了 "it" -> "animal" 的指代关系，但可能忽略了 "tired" -> "animal" 的描述关系。

为了让模型能够**同时关注来自不同表示子空间的信息**，论文引入了多头注意力机制。

### 4.1 核心思想：并行与融合

**多头注意力的核心思想非常直观：**

> 与其进行一次昂贵（高维度）的单一注意力计算，不如将模型（$d_{\text{model}}$）的维度拆分成 ($h$) 个“头”（heads），让每个头（在较低维度上）独立地、并行地学习一种上下文关系，最后再将所有头的结果融合起来。

这就像一个专家委员会：

- **单一注意力**：一位全科专家试图独自分析所有问题。
- **多头注意力**：(h) 位不同领域的专家（例如，一位语法专家、一位语义专家、一位指代关系专家……）并行工作，然后汇总他们的见解，得出一个更全面、更鲁棒的结论。

### 4.2 MHA 架构：前向过程详解

假设我们的模型中：

- **输入嵌入矩阵**：(X) 形状: ($n \times d_{\text{model}}$)
- **头数 (h) (num_heads)**：例如 8
- **模型总维度 (d_{\text{model}})**：例如 512

**关键设定**：MHA 会将总维度 ($d_{\text{model}}$) 平均分配给 ($h$) 个头。因此，**每个头的 Q, K, V 向量维度**会变小：

- $d_k = d_{\text{model}} / h = 512 / 8 = 64$
- $d_v = d_{\text{model}} / h = 512 / 8 = 64$ *(注意：这里 (d_k) 和 (d_v) 必须相等)*

#### 步骤 1：独立线性投影 (Projection)

MHA 不会直接使用单一的 ($W^Q$, $W^K$, $W^V$) 矩阵。相反，它为 ($h$) 个头中的**每一个头**都创建了一组**独立的**权重矩阵。

对于第 ($i$) 个头($i \in [1, h]$）：

- **查询权重**：$W_i^Q \in \mathbb{R}^{d_{\text{model}} \times d_k}$
- **键权重**：$W_i^K \in \mathbb{R}^{d_{\text{model}} \times d_k}$
- **值权重**：$W_i^V \in \mathbb{R}^{d_{\text{model}} \times d_v}$

模型使用**相同的**输入矩阵 ($X$)，通过这些不同的权重矩阵，为**每个头**分别计算出 $Q, K, V$ 矩阵：
$$
\begin{aligned} Q_i &= X \cdot W_i^Q \\ K_i &= X \cdot W_i^K \\ V_i &= X \cdot W_i^V \end{aligned}
$$
**形状变化**

- $X$ (形状: $n, d_{\text{model}}$) 
- $W_i^Q$ (形状: $d_{\text{model}}, d\_k$) 
- $Q_i$ (形状: $n, d_k$)，同理 ($K_i$), ($V_i$) 

**直观理解**：$X W_i^Q$这一步，就是从原始的 512 维空间中，"投影" 出第 ($i$) 个头所关心的、维度为 64 的 "查询子空间"。

#### 步骤 2：并行计算注意力 (Parallel Attention) 

现在我们有了 ($h$) 组独立的 $(Q_i, K_i, V_i)$。MHA 会让这 ($h$) 个头**并行地**执行**缩放点积注意力（SDPA）**： 
$$
\text{head}_i = \text{Attention}(Q_i, K_i, V_i) = \text{softmax}\left(\frac{Q_i K_i^T}{\sqrt{d_k}}\right)V_i
$$
**并行性:**这 ($h$) 次 SDPA 计算是完全独立的，可以在 GPU 上高效并行。   

**输出:**我们得到 ($h$) 个输出矩阵 $(\text{head}_1, \text{head}_2, \ldots, \text{head}_h)$，每个矩阵的形状都是 $(n, d_v)$。 

**直观理解**：   

* $\text{head}_1$ (形状 $(n, 64)$) 可能学会了指代关系。 
* $\text{head}_2$ (形状 $(n, 64)$) 可能学会了时态关系。  
*  ...  
* $\text{head}\_8$ (形状 $(n, 64$)) 可能学会了主谓一致。

#### 步骤 3：拼接 (Concatenate) 

模型将这 ($h$) 个头并行计算的结果（它们都是 ($n, d_v$) 形状）在**最后一个维度**上进行**拼接**： 
$$
\text{Concat}(\text{head}_1, \text{head}_2, \ldots, \text{head}_h) 
$$
**形状变化**：

- 输入：$h$ 个 $(n, d_v)$ 矩阵
- 输出：一个 $(n, h \times d_v)$ 矩阵
- **维度恢复**：由于 $(d_v = d_{\text{model}} / h$，所以 $h \times d_v = d_{\text{model}}$。
- 拼接后的矩阵形状为 $(n, d_{\text{model}})$，**恢复到了模型的原始维度**。

**直观理解**：我们将 8 个专家的 64 维 "见解" 拼接在一起，形成一个丰富的、512 维的 "综合报告"。

#### 步骤 4：最终线性投影 (Final Projection)

最后，这个拼接后的 $(n, d_{\text{model}})$ 矩阵还不能直接作为输出。它会再通过一个**最终的线性层**（由权重矩阵 $W^O$ 定义），将这个"综合报告"进行一次**融合与转换**。

- **输出权重**：$W^O \in \mathbb{R}^{d_{\text{model}} \times d_{\text{model}}}$

- **最终输出 $Z$**：
  $$
  Z = \text{Concat}(\text{head}\_1, \ldots, \text{head}\_h) \cdot W^O
  $$

  * **形状**：Z 的形状为 $(n, d\_{\text{model}})$，与 MHA 模块的输入 $X$ 形状完全一致。这使得它可以被堆叠在 Transformer 的其他层中。

- **直观理解**：$W^O$ 矩阵是一个**可学习的**"融合线性层"。它学习如何最佳地组合 8 个头的输出。例如，它可能学到："在决定'it'的含义时，头 1 (指代) 的权重给 0.6，头 5 (语法) 的权重给 0.2，其他头的权重给 0.2..." 

### 4.3 统一的数学公式 

上述四个步骤可以被总结为 MHA 的统一公式：
$$
\text{MultiHead}(X) = \text{Concat}(\text{head}_1, \ldots, \text{head}_h) W^O
$$
其中，每个头 (\text{head}_i) 的计算如下：
$$
\text{head}_i = \text{Attention}(XW_i^Q, XW_i^K, XW_i^V) 
$$

* **Attention** 函数即为我们上一章定义的**缩放点积注意力 (SDPA)**。

- **$W_i^Q, W_i^K, W_i^V$ 和 $W^O$** 都是模型在训练中需要学习的参数。

### 4.4 可视化理解与小结

在 [Transformer Explainer](https://poloclub.github.io/transformer-explainer/) 网站上，当你在 "Multi-Head Self-Attention" 部分时，你会看到**多组（通常是 12 组）**注意力计算的权重矩阵。

**MHA 的核心优势**：

1. **多维视角**：允许模型在不同的表示子空间中捕捉不同类型的上下文关系。
2. **表达力更强**：一个头"算糊了"没关系，其他头可以补偿。
3. **并行高效**：($h$) 个头的计算完全可以并行化，计算效率高（尽管总计算量略大于单头，但效果提升显著）。



## 5. Transformer架构

![绘梨衣](https://69A69.github.io/picx-images-hosting/20250313/hly.7egxg4pqnu.webp "绘梨衣 || width=60%; style=border-radius:12px; caption=Sakura & 绘梨衣 の Rilakkuma; attr=照片：Suxilan; attrlink=https://suxilan.github.io")
