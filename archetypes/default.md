---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
draft: true

tags: []
categories: []
series: []
author: "Suxilan"

comments: true
showlastmod: true
lastmod: {{ .Date }}

# summary: "列表页卡片副标题（可选；没写就不显示）"
# description: "正文页标题下副标题（可选；没写就不显示）"

# Stack 主题内置字段（按需开启/关闭）
# toc: true
# math: true

# 封面：推荐优先使用 Stack 原生字段 image
# image: ""

# 兼容旧文章/Photo 用法：cover.image（可选）
# cover:
#   image: ""
#   alt: ""
#   caption: ""
#   position: right
#   hiddenInSingle: false
#   relative: false
---
