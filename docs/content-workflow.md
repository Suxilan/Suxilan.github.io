# 内容发布工作流

> 📘 **完整教程**：从创建到发布，掌握 Hugo 博客内容管理的所有技巧

---

## 📋 目录

1. [发布笔记的完整流程](#发布笔记的完整流程)
2. [Front Matter 字段完全解析](#front-matter-字段完全解析)
3. [网页显示内容解析](#网页显示内容解析)
4. [Markdown 语法参考](#markdown-语法参考)
5. [完整示例](#完整示例发布一篇-python-笔记)
6. [其他内容类型](#其他内容类型)
7. [内容管理最佳实践](#内容管理最佳实践)
8. [快捷工作流](#快捷工作流一键发布)
9. [故障排查和常见问题](#故障排查和常见问题)
10. [高级技巧](#高级技巧)

---

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

## 📋 Front Matter 字段完全解析

### 核心字段（必需）

| 字段 | 必需 | 说明 | 示例 | 显示位置 |
|------|------|------|------|----------|
| `title` | ✅ | 文章标题 | `"Python 基础笔记"` | 页面标题、列表页 |
| `date` | ✅ | 发布日期时间 | `2025-11-05T20:00:00+08:00` | 文章顶部元信息 |
| `draft` | ✅ | 是否为草稿 | `false`（发布）/ `true`（草稿） | 控制是否显示 |

**注意事项**：
- ⚠️ `date` 格式必须精确到秒：`YYYY-MM-DDTHH:MM:SS+08:00`
- ⚠️ `date` 不能是未来时间，否则文章不显示
- ⚠️ `draft: true` 的文章不会出现在生产环境
- ⚠️ `title` 会显示在浏览器标签页和搜索结果

---

### 元信息字段（推荐）

| 字段 | 类型 | 说明 | 示例 | 用途 |
|------|------|------|------|------|
| `author` | 字符串 | 作者名称 | `"Suxilan"` | 显示在文章顶部 |
| `description` | 字符串 | 简短描述（50-160字） | `"Python 编程基础"` | SEO、社交分享 |
| `summary` | 字符串 | 列表页摘要 | `"本文介绍..."` | 文章列表预览 |
| `tags` | 数组 | 文章标签 | `["Python", "编程"]` | 文章底部、标签页 |
| `categories` | 数组 | 文章分类 | `["技术笔记"]` | 分类页面 |

**最佳实践**：
- ✅ `author`: 统一使用你的名字或昵称
- ✅ `description`: 简洁描述文章内容，吸引读者点击
- ✅ `summary`: 可不填，Hugo 会自动提取前 70 个词
- ✅ `tags`: 3-5 个标签，便于读者查找
- ✅ `categories`: 1-2 个分类，组织文章结构

---

### 目录控制字段

| 字段 | 类型 | 说明 | 默认值 | 效果 |
|------|------|------|--------|------|
| `showToc` | 布尔 | 是否显示目录 | `false` | 右侧目录栏 |
| `TocOpen` | 布尔 | 目录默认展开 | `false` | 目录折叠状态 |
| `tocLevels` | 字符串 | 目录层级 | `"2..3"` | 显示 H2 和 H3 |

**使用建议**：
```yaml
# 长文章（>1000字）
showToc: true
TocOpen: true

# 短文章（<500字）
showToc: false
```

---

### 显示控制字段

| 字段 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `comments` | 布尔 | 启用评论 | `false` |
| `hideMeta` | 布尔 | 隐藏元信息（日期、作者等） | `false` |
| `hideFooter` | 布尔 | 隐藏页脚 | `false` |
| `searchHidden` | 布尔 | 从搜索中隐藏 | `false` |
| `robotsNoIndex` | 布尔 | 禁止搜索引擎索引 | `false` |

**常用组合**：
```yaml
# 需要讨论的技术文章
comments: true

# 临时页面/草稿
searchHidden: true
robotsNoIndex: true
```

---

### 高级字段

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `weight` | 整数 | 排序权重（越小越靠前） | `1` |
| `aliases` | 数组 | 旧 URL 重定向 | `["/old-url/"]` |
| `url` | 字符串 | 自定义 URL | `"/custom-path/"` |
| `slug` | 字符串 | URL 最后一部分 | `"my-post"` |
| `cover.image` | 字符串 | 封面图片 | `"/images/cover.jpg"` |
| `cover.alt` | 字符串 | 图片描述 | `"封面图"` |

**使用场景**：
```yaml
# 置顶文章
weight: 1

# URL 友好化
slug: "python-basics"  # → /notes/python-basics/

# 添加封面图
cover:
  image: "/images/notes/python-cover.jpg"
  alt: "Python 基础教程封面"
```

---

## 🔍 网页显示内容解析

### 实例分析：giscus-test.md

**你看到的显示**：
```
测试 Giscus 评论系统
2025-11-05 · 1 分钟 · 7 字 · Suxilan
```

**对应的 Front Matter**：
```yaml
---
title: "评论系统测试"              # ← 显示为"测试 Giscus 评论系统"
date: 2025-11-05T10:00:00+08:00    # ← 显示为"2025-11-05"
author: "Suxilan"                   # ← 显示为"Suxilan"
---

## 测试评论功能                    # ← 不显示在元信息中

这是一篇测试笔记...                # ← 用于计算字数和阅读时间
```

---

### 元信息字段详解

#### 1. **日期 (Date)**

```yaml
date: 2025-11-05T10:00:00+08:00
```

**显示格式**：`2025-11-05`

**格式说明**：
- `YYYY-MM-DD`：日期（2025-11-05）
- `T`：分隔符
- `HH:MM:SS`：时间（10:00:00）
- `+08:00`：时区偏移（北京时间）

**修改显示格式**：
- 在 `hugo.yaml` 中配置：
  ```yaml
  params:
    dateFormat: "2006-01-02"  # YYYY-MM-DD
    # dateFormat: "Jan 02, 2006"  # 英文格式
  ```

---

#### 2. **阅读时间 (Reading Time)**

```
1 分钟
```

**计算方式**：
- Hugo 自动计算
- 公式：`字数 ÷ 阅读速度`
- 默认阅读速度：**200 词/分钟**（英文）
- 中文约为：**500-700 字/分钟**

**计算基数**：
- ✅ 正文内容
- ❌ Front Matter
- ❌ Markdown 标题（`##`）
- ❌ 代码块（可选）

**自定义阅读速度**：
在 `hugo.yaml` 中配置：
```yaml
params:
  readingSpeed: 500  # 中文推荐 500-700
```

---

#### 3. **字数统计 (Word Count)**

```
7 字
```

**计算规则**：
- Hugo 默认按**英文单词**统计（空格分隔）
- 中文统计可能不准确

**你的文章统计分析**：
```markdown
## 测试评论功能              ← 不计入（标题）

这是一篇测试笔记，用于验证 Giscus 评论系统是否正常工作。
如果你能在下方看到评论框，说明配置成功！
欢迎留言测试 👇
```

**"7 字"可能的原因**：
1. Hugo 统计的是英文单词数（Giscus 算1个单词）
2. 中文被识别为连续字符，统计不准

**改善中文统计**：
Hugo 配置：
```yaml
hasCJKLanguage: true  # 启用中日韩语言支持
```

---

#### 4. **作者 (Author)**

```yaml
author: "Suxilan"
```

**显示位置**：
- 文章顶部元信息
- 列表页（可选）
- RSS 订阅源

**省略作者字段**：
- 如果不填，不显示作者信息
- 可在 `hugo.yaml` 设置全局作者：
  ```yaml
  params:
    author: "Suxilan"
  ```

---

### 元信息显示控制

**隐藏元信息**：
```yaml
---
title: "文章标题"
hideMeta: true  # 隐藏所有元信息（日期、作者、字数等）
---
```

**自定义显示内容**：
修改 PaperMod 主题的 `layouts/partials/post_meta.html` 可以自定义显示逻辑。

---

## 📝 Markdown 语法参考

### 基础语法

#### 标题
```markdown
# 一级标题
## 二级标题
### 三级标题
#### 四级标题
```

#### 文本格式
```markdown
**粗体文本**
*斜体文本*
***粗斜体***
~~删除线~~
`行内代码`
```

#### 列表
```markdown
# 无序列表
- 项目 1
- 项目 2
  - 子项目 2.1
  - 子项目 2.2

# 有序列表
1. 第一项
2. 第二项
3. 第三项
```

#### 链接和图片
```markdown
# 链接
[链接文本](https://example.com)
[链接文本](https://example.com "悬停提示")

# 图片
![图片描述](/images/photo.jpg)
![图片描述](/images/photo.jpg "图片标题")

# 图片链接
[![图片描述](/images/photo.jpg)](https://example.com)
```

#### 引用
```markdown
> 这是一段引用文本
> 可以有多行

> 嵌套引用：
>> 第二层引用
```

#### 分隔线
```markdown
---
***
___
```

---

### 高级语法

#### 表格
```markdown
| 列1 | 列2 | 列3 |
|-----|-----|-----|
| 内容1 | 内容2 | 内容3 |
| 左对齐 | 居中 | 右对齐 |

# 对齐方式
| 左对齐 | 居中 | 右对齐 |
|:-------|:----:|-------:|
| 文本 | 文本 | 文本 |
```

#### 任务列表
```markdown
- [x] 已完成任务
- [ ] 未完成任务
- [ ] 待办事项
```

#### 脚注
```markdown
这是一段文字[^1]，这里有另一个脚注[^2]。

[^1]: 这是脚注1的内容
[^2]: 这是脚注2的内容
```

---

### 代码块

#### 行内代码
```markdown
使用 `print()` 函数输出文本
```

#### 代码块（带语法高亮）
````markdown
```python
def hello_world():
    print("Hello, World!")
    
hello_world()
```

```javascript
function greet(name) {
  console.log(`Hello, ${name}!`);
}
```

```bash
git add .
git commit -m "Update"
git push
```
````

#### 支持的语言
```markdown
python, javascript, typescript, go, rust, java, c, cpp, 
csharp, php, ruby, swift, kotlin, scala, r, sql, bash, 
shell, powershell, yaml, json, toml, html, css, scss, 
markdown, dockerfile, nginx, apache, xml, ini
```

---

### Hugo Shortcodes（特殊功能）

#### Figure（图片）
```markdown
{{</* figure src="/images/photo.jpg" title="图片标题" caption="图片说明" alt="图片描述" */>}}
```

#### YouTube 视频
```markdown
{{</* youtube VIDEO_ID */>}}
```

#### Twitter
```markdown
{{</* tweet user="username" id="TWEET_ID" */>}}
```

#### Gist（GitHub 代码片段）
```markdown
{{</* gist username gist_id */>}}
```

---

### 数学公式（如果启用）

#### 行内公式
```markdown
这是行内公式：$E = mc^2$
```

#### 块级公式
```markdown
$$
\int_{a}^{b} f(x) dx = F(b) - F(a)
$$
```

---

### Emoji 表情

```markdown
:smile: :heart: :+1: :rocket: :fire:
😊 ❤️ 👍 🚀 🔥
```

**常用 Emoji**：
- ✅ `:white_check_mark:`
- ❌ `:x:`
- ⚠️ `:warning:`
- 💡 `:bulb:`
- 📝 `:memo:`
- 🎯 `:dart:`
- 🚀 `:rocket:`

---

### 最佳实践

#### 1. 标题层级
```markdown
# 一级标题（每篇文章一个）

## 主要章节

### 小节

#### 细节点

不要跳级使用（❌ # → ### → #####）
```

#### 2. 列表格式
```markdown
# 好的格式 ✅
- 项目 1
- 项目 2
  - 子项目

# 不好的格式 ❌
-项目1（缺少空格）
- 项目2（中英文混排不一致）
```

#### 3. 代码块
````markdown
# 始终指定语言 ✅
```python
print("Hello")
```

# 不指定语言 ❌（没有语法高亮）
```
print("Hello")
```
````

#### 4. 图片路径
```markdown
# 正确 ✅
![描述](/images/photo.jpg)  # 以 / 开头

# 错误 ❌
![描述](images/photo.jpg)   # 相对路径可能失效
![描述](E:/images/photo.jpg)  # 绝对路径不适用于网站
```

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

## 🔍 故障排查和常见问题

### 发布问题

#### Q: 推送后网站没更新？

**问题表现**：
- Git 推送成功
- 但网站内容没有变化

**排查步骤**：

1. **检查 GitHub Actions 构建状态**
   ```bash
   # 访问
   https://github.com/Suxilan/Suxilan.github.io/actions
   ```
   - ✅ 绿色勾勾：构建成功
   - ❌ 红色叉叉：构建失败（点击查看日志）

2. **等待 CDN 缓存刷新**
   - 新内容部署后，CDN 缓存需要时间更新
   - 通常需要 **1-5 分钟**
   - 强制刷新浏览器：`Ctrl+F5`（Windows）或 `Cmd+Shift+R`（Mac）

3. **清除浏览器缓存**
   ```
   Chrome: F12 → Network → Disable cache（勾选）
   Firefox: F12 → Network → Disable Cache（勾选）
   ```

4. **使用无痕模式访问**
   - 无痕模式不会使用缓存
   - 如果无痕模式能看到更新，说明是缓存问题

---

#### Q: 文章显示 404 Not Found？

**可能原因**：

**原因 1：`draft: true`（草稿状态）**
```yaml
---
draft: true  # ← 草稿不会发布到生产环境
---
```
**解决方法**：改为 `draft: false`

---

**原因 2：日期是未来时间**
```yaml
---
date: 2026-01-01T10:00:00+08:00  # ← 超过当前时间
---
```
**解决方法**：改为当前或过去的日期

---

**原因 3：文件路径或URL错误**
```
文件：content/notes/python.md
URL：https://Suxilan.github.io/notes/python/  ← 注意末尾有 /
```
**解决方法**：检查 URL 拼写，确保与文件名一致

---

**原因 4：文件名包含特殊字符**
```bash
# 错误 ❌
content/notes/Python 基础（入门）.md

# 正确 ✅
content/notes/python-basics.md
```
**解决方法**：使用英文和连字符命名

---

#### Q: 图片不显示？

**问题1：路径错误**
```markdown
# 错误 ❌
![图片](images/photo.jpg)          # 相对路径
![图片](../static/images/photo.jpg) # 错误的相对路径
![图片](E:/images/photo.jpg)       # 本地绝对路径

# 正确 ✅
![图片](/images/photo.jpg)         # 以 / 开头的网站根路径
```

**问题2：图片位置错误**
```
错误位置 ❌：content/images/photo.jpg
正确位置 ✅：static/images/photo.jpg

网站访问：https://Suxilan.github.io/images/photo.jpg
```

**问题3：文件名大小写**
```bash
# Windows 文件名
static/images/Photo.JPG

# Markdown 引用
![](/images/photo.jpg)  # ← 大小写不匹配，Linux 服务器会找不到
```
**解决方法**：保持大小写一致

**问题4：文件未提交**
```bash
# 检查图片是否已提交
git status

# 提交图片
git add static/images/photo.jpg
git commit -m "Add image"
git push
```

---

### 内容问题

#### Q: 字数统计不准确？

**原因**：Hugo 默认按英文单词统计（空格分隔）

**解决方法**：
在 `hugo.yaml` 添加：
```yaml
hasCJKLanguage: true  # 启用中日韩语言支持
```

---

#### Q: 目录（TOC）不显示？

**检查清单**：
1. Front Matter 中是否有 `showToc: true`
2. 文章是否有 `##` 二级标题（至少2个）
3. 标题格式是否正确（`##` 后要有空格）

```yaml
---
showToc: true  # ← 确保为 true
---

## 第一个标题  # ← 至少要有2个二级标题
## 第二个标题
```

---

#### Q: 评论框不显示？

**检查清单**：
1. Front Matter 中是否有 `comments: true`
2. `layouts/partials/comments.html` 文件是否存在
3. Giscus 配置是否正确
4. 本地预览时不显示是正常的（需要线上环境）

```yaml
---
comments: true  # ← 启用评论
---
```

**验证方法**：
- 本地：评论框不显示是正常的（Giscus 需要公网访问）
- 线上：访问 `https://Suxilan.github.io/notes/xxx/` 查看

---

### Git 操作问题

#### Q: 如何撤销错误的提交？

**场景1：还没 push（本地）**
```bash
# 撤销最后一次 commit（保留文件修改）
git reset --soft HEAD~1

# 撤销最后一次 commit（不保留文件修改）
git reset --hard HEAD~1
```

**场景2：已经 push（远程）**
```bash
# 不推荐：强制覆盖（谨慎使用）
git reset --hard HEAD~1
git push --force

# 推荐：创建反向提交
git revert HEAD
git push
```

---

#### Q: 如何删除文章？

**方法1：Git 命令**
```bash
git rm content/notes/文章名.md
git commit -m "Remove article: 文章名"
git push
```

**方法2：手动删除后提交**
```bash
# 1. 直接删除文件
rm content/notes/文章名.md

# 2. 提交删除
git add -A
git commit -m "Remove article: 文章名"
git push
```

---

#### Q: 如何重命名文章？

**方法1：Git mv（推荐）**
```bash
git mv content/notes/old-name.md content/notes/new-name.md
git commit -m "Rename article"
git push
```

**方法2：手动重命名**
```bash
# 1. 重命名文件
mv content/notes/old-name.md content/notes/new-name.md

# 2. 提交
git add -A
git commit -m "Rename article"
git push
```

**注意**：重命名会改变 URL，旧链接会失效！

**保持旧链接有效**：
在新文件的 Front Matter 添加：
```yaml
---
title: "新标题"
aliases:
  - /notes/old-name/  # ← 旧 URL 自动重定向到新 URL
---
```

---

### 构建错误

#### Q: Actions 构建失败（红叉❌）

**查看错误日志**：
1. 访问 https://github.com/Suxilan/Suxilan.github.io/actions
2. 点击失败的 workflow（红叉）
3. 点击 `build` → 查看详细错误信息

**常见错误**：

**错误1：YAML 语法错误**
```yaml
# 错误 ❌
title: Python基础  # 缺少引号，如果包含特殊字符会报错

# 正确 ✅
title: "Python基础"
```

**错误2：日期格式错误**
```yaml
# 错误 ❌
date: 2025/11/05

# 正确 ✅
date: 2025-11-05T10:00:00+08:00
```

**错误3：Markdown 语法错误**
```markdown
# 错误 ❌：代码块未闭合
```python
print("Hello")
# 缺少结束的 ```

# 正确 ✅
```python
print("Hello")
```
````

---

## 🚀 高级技巧

### 1. 批量创建文章

**创建多篇文章脚本**（PowerShell）：
```powershell
# create-notes.ps1
$titles = @(
    "python-basics",
    "javascript-intro",
    "hugo-tutorial"
)

foreach ($title in $titles) {
    hugo new "notes/$title.md"
    Write-Host "Created: $title" -ForegroundColor Green
}
```

使用：
```powershell
.\create-notes.ps1
```

---

### 2. 自定义文章模板

**编辑** `archetypes/notes.md`：
```yaml
---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
draft: false
tags: []
categories: ["技术笔记"]
author: "Suxilan"
showToc: true
TocOpen: false
comments: true  # 默认启用评论
description: ""
summary: ""
---

## 概述

在这里写概述...

## 正文

### 小节 1

内容...

## 总结

总结内容...

## 参考资料

- [链接](https://example.com)
```

创建新文章时会自动使用这个模板！

---

### 3. 系列文章管理

**方法：使用相同的标签和分类**
```yaml
---
title: "Python 教程（一）：基础"
tags: ["Python", "Python教程系列"]
series: ["Python完全教程"]
---
```

---

### 4. 定时发布

**设置未来时间**：
```yaml
---
date: 2025-11-10T08:00:00+08:00  # 未来时间
draft: false
publishDate: 2025-11-10T08:00:00+08:00  # 发布时间
---
```

文章会在指定时间自动发布（需要 `buildFuture: true`）。

**配置** `hugo.yaml`：
```yaml
buildFuture: true  # ✅ 已配置
```

---

### 5. 文章置顶

**使用 weight 字段**：
```yaml
---
title: "重要公告"
weight: 1  # 数字越小越靠前
---
```

其他文章不设置 `weight` 或使用更大的数字。

---

### 6. 添加阅读时间估算

**自定义阅读速度**（`hugo.yaml`）：
```yaml
params:
  ShowReadingTime: true  # 显示阅读时间
  readingSpeed: 500      # 中文阅读速度（字/分钟）
```

---

### 7. SEO 优化

**完整的 SEO Front Matter**：
```yaml
---
title: "Python 基础教程 | 零基础入门"
description: "Python 编程语言基础教程，适合零基础初学者，包含变量、数据类型、控制流等核心概念。"
keywords: ["Python", "编程", "教程", "初学者"]
tags: ["Python", "编程基础"]
categories: ["技术教程"]
author: "Suxilan"

# SEO 相关
canonicalURL: "https://Suxilan.github.io/notes/python-basics/"
images:
  - /images/notes/python-cover.jpg
---
```

---

### 8. 社交分享优化

**Open Graph 和 Twitter Card**：
```yaml
---
title: "文章标题"
images:
  - /images/share-image.jpg  # 社交媒体分享图片（1200x630 推荐）
```

PaperMod 会自动生成 Open Graph 标签。

---

### 9. 本地搜索功能

**生成搜索索引**（Hugo 自动生成）：
- 访问 `/index.json` 查看搜索索引
- PaperMod 提供内置搜索功能

**使用搜索**：
- 网站菜单 → 搜索
- 输入关键词即时搜索

---

### 10. RSS 订阅

**RSS 地址**：
```
所有文章：https://Suxilan.github.io/index.xml
笔记分类：https://Suxilan.github.io/notes/index.xml
标签：https://Suxilan.github.io/tags/python/index.xml
```

**自定义 RSS 配置**（`hugo.yaml`）：
```yaml
outputs:
  home:
    - HTML
    - RSS
    - JSON  # 用于搜索

params:
  rssFullContent: true  # RSS 包含全文
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

