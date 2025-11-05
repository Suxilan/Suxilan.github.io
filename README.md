# Suxilan's Wilderness

个人主页，基于 Hugo + PaperMod 主题。

## 快速开始

```bash
# 本地预览
hugo server -D

# 构建网站
hugo --gc --minify
```

## 创建内容

```bash
# 随笔
hugo new posts/article-name.md

# 笔记
hugo new notes/note-name.md

# 摄影
hugo new photography/album-name.md
```

## 项目结构

```
MyHomepage/
├── content/
│   ├── posts/       # 随笔
│   ├── notes/       # 笔记
│   ├── photography/ # 摄影
│   ├── about.md     # 关于
│   └── archives.md  # 归档
├── static/images/   # 图片资源
├── docs/            # 技术文档
└── hugo.yaml        # 配置文件
```

## 配置

### 修改个人信息

编辑 `hugo.yaml`：

```yaml
profileMode:
  title: "你的名字"
  subtitle: "你的简介"
  imageUrl: "/images/avatar.jpg"  # 放置头像

socialIcons:
  - name: github
    url: "你的 GitHub"
  - name: email
    url: "你的邮箱"
```

### 添加头像和图标

将头像图片（建议 300x300px 或更大）放到 `static/images/avatar.jpg`

**用途**：
- Profile 模式的头像显示
- 网站 Favicon（浏览器标签图标）
- 社交分享图片

## 文档

- [Hugo 操作指令](docs/hugo-commands.md)
- [PaperMod 功能详解](docs/papermod-features.md)
- [配置说明](docs/configuration.md)
- [自定义配置指南](docs/customization-guide.md)
- [内容发布工作流](docs/content-workflow.md)
- [评论系统配置](docs/comments-setup.md) - 评论配置详解
- [评论系统和访问统计](docs/comments-analytics.md) - 完整实现指南
- [Giscus 自定义配置](docs/giscus-customization.md) - 颜色、主题切换

## 参考

- [Hugo 官网](https://gohugo.io/)
- [PaperMod 主题](https://github.com/adityatelange/hugo-PaperMod)
- [PaperMod Demo](https://adityatelange.github.io/hugo-PaperMod/)

## 许可

内容：CC BY-NC-SA 4.0 | 代码：MIT
