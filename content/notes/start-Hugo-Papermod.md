---
title: "Hugo + PaperMod 从零搭建教程"
date: 2025-11-06T10:00:00+08:00
lastmod: 2024-11-20 18:00:00 +0800
showLastMod: true
draft: false
tags: ["Hugo", "PaperMod", "教程", "博客搭建"]
categories: ["教程笔记"]
series: ["Hugo 博客搭建"]
author: "Suxilan"
ShowToc: true
TocWide: true
comments: true
description: "从零开始搭建 Hugo + PaperMod 博客的完整教程，记录踩坑经历"
summary: "万恶之源 —— 记录我的博客搭建之路"
---

# 一切的开始

最近在用 Gemini 2.5 Pro“**学习辅导**”的时候，总是发现有些问过的问题会一而再、再而三地询问，究其原因可能还是缺少了总结的环节。因此结合我十年寒窗苦读的经验，“**总结本**”和“**错题本**”还是必不可少的。加之最近与师兄同门学习后发现写博客或者笔记记录是一个非常好的习惯，于是狠下心来踩一下这个坑！

选择 [Hugo-PaperMod](https://github.com/adityatelange/hugo-PaperMod) 的原因是因为我看上了它首页的 Profile Mode，刚好可以用来展示我的摄影作品🤭。加之 AI 大人极力推荐，遂下定决心开始操作！总体而言还是比较简单的，希望按照这个操作可以一遍过~

---

## 📋 准备工作

在开始之前，你需要准备：
- ☕ 一杯咖啡（或茶）
- 💻 一台电脑（废话）
- 🧠 一颗愿意折腾的心
- ⏰ 约 30 分钟时间

---

## 1. 安装必要工具

### 1.1 安装 Hugo

**Windows 用户**（就是我）：

```powershell
# 使用 Chocolatey 安装（推荐）
choco install hugo-extended

# 或者使用 Winget
winget install Hugo.Hugo.Extended

# 或者像我一样直接下载安装包
# 访问 https://github.com/gohugoio/hugo/releases
# 下载 hugo_extended_withdeploy_0.152.2_windows-amd64.zip 
# 解压后将 hugo.exe 添加到系统环境变量
```

**验证安装**：

```bash
hugo version
# 应该看到类似输出：hugo v0.152.2+extended...
```

⚠️ **注意**：一定要安装 **extended** 版本！普通版不支持 SCSS，主题会出问题。

---

### 1.2 安装 Git

**Windows**：

```powershell
# 使用 Chocolatey
choco install git

# 或者 Winget
winget install Git.Git

# 或者直接下载：https://git-scm.com/download/win
```

**验证安装**：

```bash
git --version
# 应该看到：git version 2.x.x
```

**配置 Git**（首次使用）：

```bash
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
```

---

## 2. 创建 Hugo 站点

### 2.1 新建项目

```bash
# 切换到你想要存放项目的目录
cd E:\Suxilan  # 改成你自己的路径

# 创建新站点
hugo new site MyHomepage

# 进入项目目录
cd MyHomepage
```

**项目结构预览**：

```bash
MyHomepage/
├── archetypes/       # 文章模板
├── assets/           # 静态资源（CSS、JS等）
├── content/          # 📝 你的文章放这里
├── data/             # 数据文件
├── layouts/          # 自定义布局
├── static/           # 🖼️ 静态文件（图片等）
├── themes/           # 主题目录
└── hugo.yaml         # ⚙️ 配置文件
```

---

## 3. 安装 PaperMod 主题

### 3.1 初始化 Git 仓库

```bash
git init
```

### 3.2 添加主题为 Git Submodule

**推荐方式**（使用 Submodule，方便更新）：

```bash
git submodule add --depth=1 https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
```

**或者直接克隆**（不推荐，无法方便更新）：

```bash
git clone https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod --depth=1
```

### 3.3 更新 Submodule（未来更新主题时用）

```bash
git submodule update --remote --merge
```

---

## 4. 配置站点

### 4.1 编辑 hugo.yaml

打开 `hugo.yaml`，替换为以下配置（根据自己需求修改）：

```yaml
baseURL: https://yourname.github.io/  # 改成你的域名
languageCode: zh-cn
title: 你的网站标题
theme: PaperMod

# 启用 emoji 支持
enableEmoji: true

# 启用 robots.txt
enableRobotsTXT: true

# 每页显示的文章数
pagination:
  pagerSize: 10

# 语言设置
languages:
  zh:
    languageName: "中文"
    weight: 1

# PaperMod 主题配置
params:
  # 基础信息
  author: "你的名字"
  description: "你的网站描述"
  
  # 显示设置
  ShowReadingTime: true      # 显示阅读时间
  ShowShareButtons: true     # 显示分享按钮
  ShowPostNavLinks: true     # 显示上一篇/下一篇
  ShowBreadCrumbs: true      # 显示面包屑导航
  ShowCodeCopyButtons: true  # 显示代码复制按钮
  ShowWordCount: true        # 显示字数统计
  ShowRssButtonInSectionTermList: true
  
  # 首页模式（三选一）
  # homeInfoParams:          # Home-Info 模式
  #   Title: "欢迎来到我的博客"
  #   Content: "这里是描述文字"
  
  profileMode:                # Profile 模式（我选的这个）
    enabled: true
    title: "My Wilderness"    # 主标题
    subtitle: "记录、思考、探索"
    imageUrl: "/images/avatar.jpg"  # 头像路径
    imageWidth: 120
    imageHeight: 120
    buttons:
      - name: 旷野
        url: /posts/
      - name: 关于
        url: /about/
  
  # 社交图标
  socialIcons:
    - name: github
      url: "https://github.com/yourname"
      title: "访问我的 GitHub"
    - name: email
      url: "mailto:your@email.com"
      title: "发送邮件给我"

# 菜单配置
menu:
  main:
    - identifier: posts
      name: 随笔
      url: /posts/
      weight: 10
    - identifier: notes
      name: 笔记
      url: /notes/
      weight: 20
    - identifier: photography
      name: 摄影
      url: /photography/
      weight: 30
    - identifier: about
      name: 关于
      url: /about/
      weight: 40
    - identifier: archives
      name: 归档
      url: /archives/
      weight: 50
    - identifier: search
      name: 搜索
      url: /search/
      weight: 60

# 输出格式（用于搜索功能）
outputs:
  home:
    - HTML
    - RSS
    - JSON
```

---

## 5. 创建内容目录和页面

### 5.1 创建必要的目录

```bash
# 创建内容目录
mkdir content\posts content\notes content\photography

# 创建首页索引文件（如果需要）
hugo new posts/_index.md
hugo new notes/_index.md
hugo new photography/_index.md
```

### 5.2 创建关于页面

```bash
hugo new about.md
```

编辑 `content/about.md`：

```yaml
---
title: "关于我"
date: 2025-11-06T10:00:00+08:00
draft: false
showToc: false
comments: true
---

Hi，我是 Suxilan。

这里可以写你的自我介绍...
```

### 5.3 创建归档页面

```bash
hugo new archives.md
```

编辑 `content/archives.md`：

```yaml
---
title: "归档"
layout: "archives"
url: "/archives/"
summary: archives
---
```

### 5.4 创建搜索页面

```bash
hugo new search.md
```

编辑 `content/search.md`：

```yaml
---
title: "搜索"
layout: "search"
url: "/search/"
summary: "search"
placeholder: "搜索文章..."
---
```

---

## 6. 创建第一篇文章

```bash
# 创建新文章
hugo new notes/my-first-note.md
```

编辑 `content/notes/my-first-note.md`：

```yaml
---
title: "我的第一篇笔记"
date: 2025-11-06T10:00:00+08:00
draft: false
tags: ["测试"]
categories: ["笔记"]
author: "xxx"
showToc: true
comments: true
description: "这是我的第一篇测试笔记"
---

## 开始写作

这是我的第一篇笔记内容！

### 测试功能

- **粗体文字**
- *斜体文字*
- `代码`

### 代码块测试

\```python
def hello_world():
    print("Hello, World!")
\```

### 图片测试

![测试图片](/images/test.jpg)
```

---

## 7. 本地运行

### 7.1 启动开发服务器

```bash
# 启动 Hugo 服务器（包含草稿）
hugo server -D

# 或者不显示草稿
hugo server
```

**看到输出**：

```
Web Server is available at http://localhost:1313/
```

### 7.2 访问网站

打开浏览器，访问：**http://localhost:1313/**

🎉 **恭喜！你的博客已经跑起来了！**

---

## 8. 常用操作

### 创建新文章

```bash
# 笔记
hugo new notes/article-name.md

# 随笔
hugo new posts/article-name.md

# 摄影作品
hugo new photography/photo-collection.md
```

### 停止服务器

在终端按 `Ctrl + C`

### 构建静态文件

```bash
# 生成 public/ 目录（部署用）
hugo

# 清理缓存后构建
hugo --gc --minify
```

---

## 9. 添加头像和图片

### 9.1 准备图片

```bash
# 创建图片目录
mkdir static\images
```

### 9.2 放置头像

将你的头像图片重命名为 `avatar.jpg`，放到 `static/images/` 目录。

**目录结构**：

```
static/
└── images/
    ├── avatar.jpg      # 你的头像
    └── ...             # 其他图片
```

### 9.3 在文章中引用图片

```markdown
![图片描述](/images/photo.jpg)
```

⚠️ **注意**：路径以 `/` 开头（根路径），不是相对路径！

---

## 🎯 下一步

现在你已经成功搭建了本地博客！接下来可以：

1. ✅ **自定义主题样式** → 修改 `assets/css/extended/custom.css`
2. ✅ **部署到 GitHub Pages** → 参考 [部署文档](/notes/deployment-guide/)
3. ✅ **添加评论系统** → 参考 [Giscus 配置](/notes/comments-setup/)
4. ✅ **配置 Google Analytics** → 参考 [访问统计](/notes/analytics-setup/)

---

## 💡 常见问题

### Q: 主题更新后怎么办？

```bash
git submodule update --remote --merge
```

### Q: 文章不显示？

检查：
1. `draft: false`（不是草稿）
2. `date` 不是未来时间（亲测踩坑）
3. 文件在正确的 `content/` 目录下

### Q: 图片不显示？

检查：
1. 图片在 `static/images/` 目录
2. 路径以 `/` 开头：`/images/photo.jpg`
3. 文件名大小写是否正确

---

## 📚 参考资料

- [Hugo 官方文档](https://gohugo.io/documentation/)
- [PaperMod 维基](https://github.com/adityatelange/hugo-PaperMod/wiki)
- [PaperMod Demo](https://adityatelange.github.io/hugo-PaperMod/)

---

## 🎉 结语

博主本人在AI大大的带领下成功实现，该教程大部摘自和其对话的输出，部分参考了官方实力文档。看到这里现在已经基本完成了PaperMod主题网页的搭建啦。

**记住**：最好的博客，是持续更新的博客。✍️
（这句是AI写的，感觉挺有意义，也算是对我的一种鼓励吧）

---

> 💬 有问题？欢迎在下方评论区留言！
