# PaperMod 功能详解

## 1. 首页模式

### Regular Mode（常规模式）
显示文章列表，无需额外配置。

### Home-Info Mode（信息卡片模式）
```yaml
params:
  homeInfoParams:
    Title: "标题"
    Content: "内容"
```

### Profile Mode（个人资料模式）
```yaml
params:
  profileMode:
    enabled: true
    title: "名字"
    subtitle: "副标题"
    imageUrl: "/images/avatar.jpg"
    imageWidth: 120
    imageHeight: 120
    buttons:
      - name: 博客
        url: /posts/
```

## 2. Front Matter 配置

### 基础配置
```yaml
title: "文章标题"
date: 2024-01-20T10:00:00+08:00
draft: false
tags: ["标签"]
categories: ["分类"]
author: "作者"
```

### 显示控制
```yaml
showToc: true           # 显示目录
TocOpen: false          # 目录默认折叠
hidemeta: false         # 隐藏元信息
comments: true          # 启用评论
disableShare: false     # 禁用分享按钮
ShowReadingTime: true   # 显示阅读时间
ShowBreadCrumbs: true   # 显示面包屑
ShowPostNavLinks: true  # 显示上/下一篇
```

### SEO
```yaml
description: "文章描述"
summary: "文章摘要"
keywords: [关键词1, 关键词2]
canonicalURL: "https://example.com/page"
```

### 封面图片
```yaml
cover:
    image: "/images/cover.jpg"
    alt: "图片 alt 文本"
    caption: "图片说明"
    relative: false
    hidden: false
    hiddenInList: false
    linkFullImages: true
    responsiveImages: true
```

### 编辑链接
```yaml
editPost:
    URL: "https://github.com/user/repo/content"
    Text: "建议修改"
    appendFilePath: true
```

### 排序权重
```yaml
weight: 1  # 数字越小越靠前
```

### 系列文章
```yaml
series: ["系列名称"]
```

## 3. 搜索功能

### 启用搜索
```yaml
outputs:
  home:
    - HTML
    - RSS
    - JSON  # 必需
```

### 创建搜索页面
`content/search.md`:
```yaml
---
title: "搜索"
layout: "search"
---
```

### 搜索配置
```yaml
params:
  fuseOpts:
    isCaseSensitive: false
    shouldSort: true
    threshold: 0.4
    keys: ["title", "permalink", "summary", "content"]
```

## 4. 归档页面

`content/archives.md`:
```yaml
---
title: "归档"
layout: "archives"
---
```

## 5. 社交图标

### 配置
```yaml
params:
  socialIcons:
    - name: github
      url: "https://github.com/username"
    - name: email
      url: "mailto:email@example.com"
    - name: rss
      url: "/index.xml"
```

### 支持的图标
- **社交媒体**: github, gitlab, twitter, x, linkedin, facebook, instagram, youtube, tiktok, reddit, discord
- **开发平台**: stackoverflow, codepen, dribbble, behance
- **联系方式**: email, phone, telegram, whatsapp
- **其他**: rss, buymeacoffee, kofi, paypal

## 6. 代码高亮

### 配置
```yaml
markup:
  highlight:
    codeFences: true
    lineNos: true
    noClasses: false
    style: monokai  # 主题名称
```

### 可用主题
`monokai`, `dracula`, `github`, `vim`, `xcode`, `vs`, `solarized-dark`, `solarized-light`

### 高亮特定行
````markdown
```python {hl_lines=[2,3]}
line 1
line 2  # 高亮
line 3  # 高亮
```
````

## 7. 内容组织

### 标签和分类
```yaml
tags: ["Hugo", "Web"]
categories: ["技术"]
```

### 摘要
**方法1**：Front Matter
```yaml
summary: "自定义摘要"
```

**方法2**：分隔符
```markdown
摘要内容...

<!--more-->

正文内容...
```

## 8. 多语言支持

```yaml
languages:
  zh:
    languageName: "中文"
    weight: 1
  en:
    languageName: "English"
    weight: 2
```

文件命名：
- `content/posts/article.md` (中文)
- `content/posts/article.en.md` (英文)

## 9. 菜单配置

```yaml
menu:
  main:
    - name: 首页
      url: /
      weight: 1
    - name: 博客
      url: /posts/
      weight: 2
    - identifier: tags
      name: 标签
      url: /tags/
      weight: 3
```

## 10. 自定义

### 自定义 CSS
创建 `assets/css/extended/custom.css`:
```css
:root {
    --primary-color: #007bff;
}
```

### 自定义 JS
创建 `assets/js/extended/custom.js`:
```javascript
console.log('Custom script loaded');
```

### 自定义布局
在 `layouts/` 目录覆盖主题文件：
```
layouts/
├── _default/
│   ├── single.html
│   └── list.html
└── partials/
    ├── header.html
    └── footer.html
```

## 11. SEO 优化

### 自动生成
- Meta 标签
- Open Graph
- Twitter Cards
- Schema.org JSON-LD
- Sitemap
- Robots.txt

### Google Analytics
```yaml
googleAnalytics: UA-XXXXXXXXX-X

# 或 GA4
params:
  analytics:
    google:
      SiteVerificationTag: "XXXXXX"
```

## 12. 评论系统

### Disqus
```yaml
disqusShortname: your-shortname
```

### Utterances
创建 `layouts/partials/comments.html`:
```html
<script src="https://utteranc.es/client.js"
        repo="username/repo"
        issue-term="pathname"
        theme="github-light"
        crossorigin="anonymous"
        async>
</script>
```

## 13. 性能优化

### 配置
```yaml
minify:
  disableXML: true
  minifyOutput: true

params:
  cover:
    responsiveImages: true
```

### 图片优化
- 使用 WebP 格式
- 压缩图片大小
- 封面图建议 1200x630px

## 14. Shortcodes

### 内置
```markdown
{{</* figure src="/image.jpg" title="标题" */>}}
{{</* youtube video_id */>}}
{{</* tweet user="username" id="tweet_id" */>}}
```

### 自定义
创建 `layouts/shortcodes/note.html`:
```html
<div class="note">{{ .Inner }}</div>
```

使用：
```markdown
{{</* note */>}}
提示内容
{{</* /note */>}}
```

## 15. 隐私设置

```yaml
privacy:
  vimeo:
    disabled: false
    simple: true
  x:
    disabled: false
    enableDNT: true
  youtube:
    privacyEnhanced: true
```

## 16. RSS 配置

```yaml
copyright: "© 2024 Your Name"
rssLimit: 20  # RSS 文章数量

params:
  ShowFullTextinRSS: true
```

## 17. 构建控制

### 隐藏页面
```yaml
_build:
  list: never    # 不在列表显示
  render: true   # 但可直接访问
```

### 草稿和过期
```yaml
draft: true           # 草稿
publishDate: 2024-02-01  # 未来发布
expiryDate: 2024-12-31   # 过期时间
```

