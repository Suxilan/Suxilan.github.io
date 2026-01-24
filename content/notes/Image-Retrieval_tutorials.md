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
weight: 1
cover:
    image: "https://cdn.jsdelivr.net/gh/Suxilan/Cloud-Image-alpha/imagebed/notes/All%20You%20Need%20to%20Know%20About%20Training%20Image%20Retrieval%20Models.png"
    alt: "image retrieval"
    position: right
    hiddenInSingle: false
    caption: ""
    relative: false
---

## All You Need to Know About Training Image Retrieval Models

![](https://cdn.jsdelivr.net/gh/Suxilan/Cloud-Image-alpha/imagebed/notes/All%20You%20Need%20to%20Know%20About%20Training%20Image%20Retrieval%20Models.png "All You Need to Know About Training Image Retrieval Models || caption=Gabriele Berton大佬的技术手册; attr=gmberton; attrlink=https://gmberton.github.io/")

{{< notice note >}}

Gmberton 还是出手了，作者通过成千上万次实验以及根据他个人多年在图像检索领域的经验，总结了训练图像检索模型时的“黄金法则。算是一篇非常扎实的实战指南了，非常值得一看！

{{< /notice >}} 

首先一上来作者就提出了这样一些关键的问题：

* Which layers of the base model should be fine-tuned? 
* How should the learning rates be set? 
* How should the training dataset be sampled? 
* When creating a dataset, should the main focus be annotation quality, or dataset size? 
* What feature layer and feature dimensionality result in the best accuracy?

