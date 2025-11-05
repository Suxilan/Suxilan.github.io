# 内容发布工作流

## 📝 发布笔记的完整流程

### 方法1：使用 Hugo 命令（推荐）

```bash
# 1. 创建新笔记
hugo new notes/笔记标题.md

# 2. 编辑文件
# 使用任何文本编辑器打开 content/notes/笔记标题.md

# 3. 修改 Front Matter
# 将 draft: true 改为 draft: false

# 4. 本地预览
hugo server -D

# 5. 确认无误后提交
git add .
git commit -m "Add new note: 笔记标题"
git push

# 6. 等待自动部署（2-3分钟）
# 访问 https://Suxilan.github.io 查看
```

### 方法2：手动创建文件

1. 在 `content/notes/` 目录创建新文件 `笔记名.md`
2. 复制以下模板内容：

```yaml
---
title: "你的笔记标题"
date: 2024-11-05T20:00:00+08:00
draft: false
tags: ["标签1", "标签2"]
categories: ["技术笔记"]
author: "Suxilan"
showToc: true
TocOpen: true
description: "笔记简短描述"
---

## 概述

在这里写概述...

## 内容

### 知识点1

内容...

### 知识点2

内容...

## 总结

总结内容...
```

3. 保存文件
4. 本地预览：`hugo server -D`
5. 提交推送：`git add . && git commit -m "Add note" && git push`

---

## 📋 Front Matter 字段说明

| 字段 | 必需 | 说明 | 示例 |
|------|------|------|------|
| `title` | ✅ | 文章标题 | `"Python 基础笔记"` |
| `date` | ✅ | 发布日期时间 | `2024-11-05T20:00:00+08:00` |
| `draft` | ✅ | 是否为草稿 | `false`（发布）/ `true`（草稿） |
| `tags` | ⭕ | 标签 | `["Python", "编程"]` |
| `categories` | ⭕ | 分类 | `["技术笔记"]` |
| `author` | ⭕ | 作者 | `"Suxilan"` |
| `showToc` | ⭕ | 显示目录 | `true` / `false` |
| `TocOpen` | ⭕ | 目录默认展开 | `true` / `false` |
| `description` | ⭕ | SEO 描述 | `"这是笔记描述"` |
| `summary` | ⭕ | 列表页摘要 | `"笔记摘要"` |
| `weight` | ⭕ | 排序权重 | `1`（数字越小越靠前） |

---

## 🎯 完整示例：发布一篇 Python 笔记

### Step 1: 创建文件
```bash
hugo new notes/python-basics.md
```

### Step 2: 编辑内容

打开 `content/notes/python-basics.md`：

```yaml
---
title: "Python 基础笔记"
date: 2024-11-05T20:30:00+08:00
draft: false
tags: ["Python", "编程基础"]
categories: ["技术笔记"]
author: "Suxilan"
showToc: true
TocOpen: true
description: "Python 编程语言基础知识总结"
summary: "包含变量、数据类型、控制流等基础内容"
---

## 概述

Python 是一门简洁优雅的编程语言，适合初学者入门。

## 变量和数据类型

### 变量定义
```python
name = "Suxilan"
age = 20
is_student = True
```

### 数据类型
- **字符串**：`str`
- **整数**：`int`
- **浮点数**：`float`
- **布尔值**：`bool`

## 控制流

### if 语句
```python
if age >= 18:
    print("成年人")
else:
    print("未成年")
```

### for 循环
```python
for i in range(5):
    print(i)
```

## 总结

本笔记涵盖了 Python 的基础语法，是学习 Python 的第一步。

## 参考资料

- [Python 官方文档](https://docs.python.org/zh-cn/3/)
- [菜鸟教程](https://www.runoob.com/python3/)
```

### Step 3: 本地预览
```bash
hugo server -D
```

访问 http://localhost:1313/notes/python-basics/ 查看效果

### Step 4: 提交发布
```bash
git add content/notes/python-basics.md
git commit -m "Add Python basics note"
git push
```

### Step 5: 等待部署
- 访问 https://github.com/Suxilan/Suxilan.github.io/actions
- 等待绿色勾勾 ✅
- 访问 https://Suxilan.github.io/notes/

---

## 🔄 其他内容类型

### 发布随笔
```bash
hugo new posts/文章标题.md
# 编辑后
git add content/posts/文章标题.md
git commit -m "Add new post"
git push
```

### 发布摄影作品
```bash
hugo new photography/作品集名.md
# 添加图片到 static/images/photography/
# 在文章中引用：![描述](/images/photography/photo.jpg)
git add content/photography/ static/images/photography/
git commit -m "Add photography work"
git push
```

### 更新关于页面
```bash
# 直接编辑 content/about.md
git add content/about.md
git commit -m "Update about page"
git push
```

---

## 📅 内容管理最佳实践

### 1. 文件命名规范
- **使用英文或拼音**：`python-basics.md`
- **避免中文文件名**：可能导致 URL 问题
- **使用连字符**：`my-first-note.md`（不用下划线或空格）

### 2. 图片管理
```
static/images/
├── notes/          # 笔记配图
│   └── python/    # 可按主题分类
├── photography/   # 摄影作品
└── shared/        # 共用图片
```

### 3. 草稿管理
```bash
# 创建草稿
hugo new notes/draft-note.md
# draft: true 保持不变

# 本地预览草稿
hugo server -D

# 发布时改 draft: false
```

### 4. 定期备份
```bash
# 每次写完都推送到 GitHub
git push
```

---

## 🚀 快捷工作流（一键发布）

### Windows PowerShell 脚本

创建 `publish.ps1`：
```powershell
param(
    [string]$message = "Update content"
)

git add .
git commit -m $message
git push

Write-Host "已推送，等待自动部署..." -ForegroundColor Green
Write-Host "访问 https://github.com/Suxilan/Suxilan.github.io/actions 查看进度" -ForegroundColor Cyan
```

使用：
```powershell
.\publish.ps1 -message "Add new note"
```

### 或使用 Git Alias

```bash
# 配置快捷命令
git config --global alias.publish '!git add . && git commit -m "Update content" && git push'

# 使用
git publish
```

---

## 📊 内容检查清单

发布前检查：

- [ ] `draft: false`
- [ ] 日期正确（不是未来时间）
- [ ] 标题和描述已填写
- [ ] 标签和分类已设置
- [ ] 图片路径正确
- [ ] 本地预览无误
- [ ] 无拼写错误

---

## ⏱️ 发布时间线

```
提交代码
    ↓ (立即)
GitHub Actions 开始构建
    ↓ (1-2分钟)
构建完成，开始部署
    ↓ (30秒-1分钟)
部署完成
    ↓ (可能需要1-5分钟缓存刷新)
网站更新
```

**总计时间**：通常 3-5 分钟

---

## 🔍 常见问题

### Q: 推送后网站没更新？
A: 
1. 检查 Actions 是否成功（绿色勾勾）
2. 等待 5 分钟让 CDN 缓存刷新
3. 强制刷新浏览器（Ctrl+F5）

### Q: 文章显示 404？
A:
1. 检查 `draft: false`
2. 检查日期不是未来
3. 检查文件路径正确

### Q: 图片不显示？
A:
1. 图片在 `static/images/` 目录
2. 路径以 `/` 开头：`/images/photo.jpg`
3. 文件名大小写匹配

### Q: 如何删除文章？
A:
```bash
git rm content/notes/文章.md
git commit -m "Remove article"
git push
```

---

## 📈 内容规划建议

### 笔记频率
- **每周 2-3 篇**：保持更新
- **分类明确**：便于查找
- **加入系列**：相关笔记归为一个系列

### 标签策略
- **技术标签**：Python, JavaScript, Hugo
- **领域标签**：Web开发, 数据分析, 摄影
- **类型标签**：教程, 总结, 实践

### 分类建议
- **技术笔记**
- **读书笔记**
- **生活随笔**
- **摄影作品**

---

## 🎯 下一步行动

1. 使用上述流程发布你的第一篇笔记
2. 测试完整的发布流程
3. 根据需要调整配置

**提示**：先用简单内容测试流程，熟悉后再写正式笔记。

