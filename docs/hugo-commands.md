# Hugo 操作指令

## 服务器命令

```bash
# 启动本地服务器
hugo server

# 包含草稿
hugo server -D

# 指定端口
hugo server -p 8080

# 绑定所有网络接口
hugo server --bind 0.0.0.0

# 禁用快速渲染
hugo server --disableFastRender
```

## 内容管理

```bash
# 创建内容
hugo new posts/article-name.md
hugo new notes/note-name.md
hugo new portfolio/project-name.md
hugo new photography/album-name.md

# 列出所有内容
hugo list all

# 列出草稿
hugo list drafts

# 列出未来发布的文章
hugo list future
```

## 构建命令

```bash
# 基本构建
hugo

# 优化构建（压缩、清理）
hugo --gc --minify

# 构建草稿
hugo -D

# 构建未来文章
hugo -F

# 构建过期内容
hugo -E

# 指定目标目录
hugo -d /path/to/output
```

## 主题管理

```bash
# 初始化主题子模块
git submodule update --init --recursive

# 更新主题
git submodule update --remote --merge

# 查看主题信息
hugo list themes
```

## 配置相关

```bash
# 检查配置
hugo config

# 查看 Hugo 版本
hugo version

# 查看环境信息
hugo env
```

## 部署相关

```bash
# 生成部署文件
hugo --gc --minify

# 清理缓存
hugo --gc

# 查看构建统计
hugo --templateMetrics
```

## Git 操作（部署用）

```bash
# 添加所有更改
git add .

# 提交更改
git commit -m "Update content"

# 推送到远程
git push

# 更新主题子模块
git submodule update --remote --merge
git add themes/PaperMod
git commit -m "Update theme"
git push
```

## 常用组合

```bash
# 开发流程
hugo server -D                    # 预览
hugo new posts/new-article.md    # 创建文章
# 编辑并改 draft: false
git add . && git commit -m "Add new post" && git push

# 发布流程
hugo --gc --minify               # 构建
# 检查 public/ 目录
git add . && git commit -m "Publish" && git push
```

