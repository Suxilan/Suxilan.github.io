# 配置说明

## hugo.yaml 结构

### 基本配置
```yaml
baseURL: https://example.org/
languageCode: zh-cn
title: 网站标题
theme: PaperMod

enableEmoji: true
enableRobotsTXT: true
buildDrafts: false
buildFuture: false
buildExpired: false
```

### 分页配置
```yaml
pagination:
  pagerSize: 10  # 每页文章数
```

### 输出格式
```yaml
outputs:
  home:
    - HTML
    - RSS
    - JSON  # 搜索功能需要
```

### 压缩优化
```yaml
minify:
  disableXML: true
  minifyOutput: true
```

## 主题参数

### 环境和元信息
```yaml
params:
  env: production
  description: "网站描述"
  keywords: [关键词1, 关键词2]
  author: "作者名"
  images: ["/images/default.png"]
  DateFormat: "2006-01-02"
```

### 主题外观
```yaml
params:
  defaultTheme: auto  # auto/light/dark
  disableThemeToggle: false
```

### 显示选项
```yaml
params:
  ShowReadingTime: true
  ShowShareButtons: true
  ShowPostNavLinks: true
  ShowBreadCrumbs: true
  ShowCodeCopyButtons: true
  ShowWordCount: true
  ShowToc: true
  TocOpen: false
```

### 首页模式选择

#### Home-Info 模式
```yaml
params:
  homeInfoParams:
    Title: "欢迎"
    Content: "内容"
  
  socialIcons:
    - name: github
      url: "https://github.com/username"
```

#### Profile 模式
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

### 封面图片
```yaml
params:
  cover:
    hidden: false
    hiddenInList: false
    hiddenInSingle: false
    linkFullImages: true
    responsiveImages: true
```

### 搜索配置
```yaml
params:
  fuseOpts:
    isCaseSensitive: false
    shouldSort: true
    location: 0
    distance: 1000
    threshold: 0.4
    minMatchCharLength: 0
    keys: ["title", "permalink", "summary", "content"]
```

### 编辑链接
```yaml
params:
  editPost:
    URL: "https://github.com/user/repo/tree/main/content"
    Text: "建议修改"
    appendFilePath: true
```

### Analytics
```yaml
googleAnalytics: UA-XXXXXXXXX-X

params:
  analytics:
    google:
      SiteVerificationTag: "XXXXXX"
```

## Markdown 配置

```yaml
markup:
  goldmark:
    renderer:
      unsafe: true  # 允许 HTML
  
  highlight:
    anchorLineNos: false
    codeFences: true
    guessSyntax: false
    lineNos: true
    noClasses: false
    style: monokai
```

## 菜单配置

### 基本菜单
```yaml
menu:
  main:
    - name: 首页
      url: /
      weight: 1
    - name: 博客
      url: /posts/
      weight: 2
    - name: 标签
      url: /tags/
      weight: 3
```

### 外部链接
```yaml
menu:
  main:
    - name: GitHub
      url: "https://github.com/username"
      weight: 99
```

### 多语言菜单
```yaml
languages:
  zh:
    menu:
      main:
        - name: 首页
          url: /
  en:
    menu:
      main:
        - name: Home
          url: /
```

## 隐私配置

```yaml
privacy:
  vimeo:
    disabled: false
    simple: true
  x:
    disabled: false
    enableDNT: true
    simple: true
  instagram:
    disabled: false
    simple: true
  youtube:
    disabled: false
    privacyEnhanced: true
```

## 服务配置

```yaml
services:
  instagram:
    disableInlineCSS: true
  x:
    disableInlineCSS: true
```

## 多语言配置

```yaml
languages:
  zh:
    languageName: "中文"
    weight: 1
    taxonomies:
      category: categories
      tag: tags
    params:
      homeInfoParams:
        Title: "你好"
  
  en:
    languageName: "English"
    weight: 2
    params:
      homeInfoParams:
        Title: "Hello"
```

## Taxonomies（分类系统）

```yaml
taxonomies:
  category: categories
  tag: tags
  series: series
```

## 自定义配置示例

### 博客网站
```yaml
params:
  homeInfoParams:
    Title: "技术博客"
    Content: "分享编程技术"
  ShowReadingTime: true
  ShowCodeCopyButtons: true
  ShowToc: true
```

### 作品集网站
```yaml
params:
  profileMode:
    enabled: true
    title: "设计师"
    imageUrl: "/images/avatar.jpg"
    buttons:
      - name: 作品
        url: /portfolio/
  ShowShareButtons: false
  ShowReadingTime: false
```

### 摄影网站
```yaml
params:
  cover:
    linkFullImages: true
    responsiveImages: true
  ShowToc: false
  ShowReadingTime: false
```

## 配置优先级

1. 命令行参数
2. Front Matter
3. hugo.yaml
4. 主题默认值

## 环境变量

```yaml
params:
  env: production  # production/development

# 根据环境自动调整
# production: 启用 minify，隐藏调试信息
# development: 显示调试信息
```

