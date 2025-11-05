# 评论系统配置说明

## 📋 配置层级理解

### 三个层级的区别

```
1. hugo.yaml (全局默认)
   ↓ 作用于所有页面
   ↓ 可被单篇文章覆盖
   
2. archetypes/xxx.md (新建文件模板)
   ↓ 只影响新创建的文件
   ↓ 不影响已存在的文件
   
3. 文章 Front Matter (单篇文章)
   ↓ 优先级最高
   ↓ 覆盖全局设置
```

---

## 🎯 当前配置（按需启用）

### hugo.yaml
```yaml
params:
  comments: false  # 全局默认关闭
```

**效果**：所有页面默认不显示评论

### archetypes/notes.md
```yaml
comments: true  # 新笔记默认启用
```

**效果**：运行 `hugo new notes/xxx.md` 时，自动包含 `comments: true`

### 单篇文章控制
```yaml
# content/about.md
---
comments: true  # 这篇显示评论
---

# content/posts/some-post.md
---
# 不写 comments，默认不显示
---
```

---

## 🛠️ 使用场景

### 场景1: 只在特定文章启用评论（推荐）✅

**配置**：
```yaml
# hugo.yaml
params:
  comments: false  # ← 当前配置
```

**使用**：
在需要评论的文章中添加：
```yaml
---
title: "文章标题"
comments: true  # ← 只这篇显示
---
```

**适合**：
- 重要文章才开评论
- 控制评论数量
- 避免垃圾评论

---

### 场景2: 全部启用，个别禁用

**配置**：
```yaml
# hugo.yaml
params:
  comments: true  # 全局启用
```

**使用**：
不想显示评论的文章：
```yaml
---
title: "某篇文章"
disableComments: true  # 这篇不显示
---
```

**适合**：
- 互动性强的博客
- 大部分文章都要评论

---

### 场景3: 按内容类型区分

**配置**：
```yaml
# hugo.yaml
params:
  comments: false

# archetypes/notes.md - 笔记默认有评论
comments: true

# archetypes/posts.md - 随笔默认没有评论
# 不写 comments
```

**效果**：
- 笔记自动带评论
- 随笔默认无评论
- 可在单篇文章中覆盖

---

## 📝 实际操作示例

### 示例1: 发布带评论的笔记

```bash
# 1. 创建笔记（自动包含 comments: true）
hugo new notes/python-tutorial.md

# 2. 编辑文件
# Front Matter 已自动包含：
# comments: true  ← 自动添加的

# 3. 写内容，改 draft: false

# 4. 推送
git add content/notes/python-tutorial.md
git commit -m "Add Python tutorial"
git push
```

### 示例2: 发布不带评论的随笔

```bash
# 1. 创建随笔
hugo new posts/daily-thoughts.md

# 2. 编辑文件
# Front Matter 中不写 comments
# 或写 comments: false

# 3. 推送发布
```

### 示例3: 为已有文章添加评论

编辑文章，在 Front Matter 添加一行：
```yaml
---
title: "已存在的文章"
date: 2024-11-01
comments: true  # ← 添加这行
---
```

---

## 🎨 评论区样式和主题

### 主题跟随已修复 ✅

**配置位置**：`layouts/partials/comments.html` 第 14 行

```html
data-theme="light dark"
```

**效果**：
- 浅色模式：Giscus 显示 light 主题
- 深色模式：Giscus 自动切换为 dark 主题
- 跟随 PaperMod 的主题切换按钮

### 评论区样式美化

**已添加 CSS**：`assets/css/extended/custom.css` 第 197-213 行

```css
/* 评论区宽度适配 */
.giscus, .giscus-frame {
  width: 100%;
  max-width: 100%;
}

/* 评论区容器样式 */
.comments-section {
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid var(--border);
}

/* 圆角 */
.giscus-frame {
  border-radius: 8px;
}
```

### 进一步美化（可选）

如果想要更多自定义，可以在 `custom.css` 中添加：

```css
/* 评论区背景 */
.comments-section {
  background: var(--entry);
  padding: 2rem;
  border-radius: 12px;
  margin-top: 3rem;
}

/* 评论区标题 */
.comments-section::before {
  content: "💬 评论";
  display: block;
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: var(--primary);
}
```

### Giscus 内部样式限制

**注意**：Giscus 评论框是通过 iframe 嵌入的，所以：
- ❌ 无法直接修改评论框内部的样式
- ✅ 可以调整评论框的容器、边距、圆角
- ✅ 可以选择 Giscus 提供的主题

**可用主题**：
- `light` - GitHub 浅色
- `dark` - GitHub 深色
- `dark_dimmed` - 稍暗的深色
- `dark_high_contrast` - 高对比度
- `transparent_dark` - 透明深色
- `light dark` - 自动切换 ✅（当前使用）

如果想换主题，修改 `comments.html` 第 14 行的 `data-theme` 值。

---

## 📊 配置总结

| 配置位置 | 作用 | 优先级 | 影响范围 |
|----------|------|--------|----------|
| `hugo.yaml` | 全局默认 | 低 | 所有页面 |
| `archetypes/notes.md` | 新文件模板 | - | 仅新建文件 |
| 文章 Front Matter | 单篇控制 | **高** | 该文章 |

---

## ✅ 当前状态

- ✅ 社交分享图标已关闭
- ✅ 评论默认不显示
- ✅ 评论主题自动跟随 PaperMod
- ✅ 需要评论的文章手动添加 `comments: true`
- ✅ 新建笔记自动带 `comments: true`（可删除）

---

## 🚀 现在推送测试

```bash
git add .
git commit -m "Configure Giscus comments and remove share buttons"
git push
```

等待部署后访问：
- https://Suxilan.github.io/about/ （有评论）
- https://Suxilan.github.io/notes/giscus-test/ （有评论）

文章底部应该**只有评论框**，没有社交分享按钮！🎉

