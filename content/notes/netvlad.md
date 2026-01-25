---
title: "Netvlad"
date: 2026-01-26T01:19:40+08:00
draft: true

tags: []
categories: ["算法博客"]
series: []
author: "Suxilan"

comments: true
showlastmod: true
lastmod: 2026-01-26T01:19:40+08:00
# summary: "列表页卡片副标题（可选；没写就不显示）"
# description: "正文页标题下副标题（可选；没写就不显示）"

# Stack 主题内置字段（按需开启/关闭）
# toc: true
# math: true
image: ""   # Stack 原生封面字段（推荐）
---


## NetVLAD的梯度流

{{< notice note>}}

NetVLAD生来就是为了端到端训练的，此时梯度如何穿过 soft-assignment 与残差聚合，分别落到 descriptors 和 cluster centers？

{{< /notice >}}

首先，记梯度的主干为 $ g _ { k } = \frac { \partial L } { \partial v _ { k } } \in R ^ { D }$