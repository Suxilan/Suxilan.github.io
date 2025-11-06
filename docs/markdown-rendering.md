# Markdown 渲染与美化指南

> 本文档详细说明 Hugo + PaperMod 中 Markdown 渲染的工作原理、如何自定义和美化笔记的显示效果。

---

## 📚 目录

- [渲染系统概述](#渲染系统概述)
- [代码高亮配置](#代码高亮配置)
- [自定义样式](#自定义样式)
- [高级美化技巧](#高级美化技巧)

---

## 渲染系统概述

### 1. 渲染流程

```
Markdown 文件 (.md)
    ↓
Hugo Goldmark 引擎（Markdown → HTML）
    ↓
Hugo Chroma 引擎（代码高亮）
    ↓
PaperMod 主题样式（CSS）
    ↓
最终网页
```

### 2. 各部分职责

| 组件 | 职责 | 配置位置 |
|------|------|----------|
| **Goldmark** | Markdown 转 HTML | `hugo.yaml` → `markup.goldmark` |
| **Chroma** | 代码语法高亮 | `hugo.yaml` → `markup.highlight` |
| **PaperMod CSS** | 主题样式 | `themes/PaperMod/assets/css/` |
| **自定义 CSS** | 个性化样式 | `assets/css/extended/custom.css` |

---

## 代码高亮配置

### 1. 当前配置（hugo.yaml）

```yaml
# Markdown 渲染设置
markup:
  goldmark:
    renderer:
      unsafe: true  # 允许在 Markdown 中使用 HTML 标签
  highlight:
    anchorLineNos: false        # 行号不可点击（避免 URL 混乱）
    codeFences: true            # 启用围栏代码块（```）
    guessSyntax: false          # 不自动猜测语法（建议手动指定）
    lineNos: true               # 显示行号
    noClasses: false            # 使用 CSS 类而非内联样式
    style: monokai              # 代码高亮主题
```

### 2. 可用的代码高亮主题

Hugo Chroma 支持多种主题风格，你可以在 `style` 字段更改：

#### **深色系（推荐用于暗色模式）**
- `monokai` （当前使用，经典暗色）
- `dracula` （流行的紫色主题）
- `nord` （冷色调北欧风）
- `catppuccin` （柔和色彩）
- `gruvbox-dark` （复古风格）
- `one-dark` （Atom 编辑器风格）

#### **浅色系（推荐用于亮色模式）**
- `github` （GitHub 风格）
- `xcode` （苹果 Xcode 风格）
- `monokailight` （Monokai 浅色版）
- `gruvbox-light` （Gruvbox 浅色版）

#### **查看所有主题**

```bash
# 在终端运行
hugo gen chromastyles --style=help
```

### 3. 更换代码高亮主题

**步骤**：

1. **编辑 `hugo.yaml`**

```yaml
markup:
  highlight:
    style: dracula  # 改成你喜欢的主题名
```

2. **重启 Hugo 服务器**

```bash
hugo server
```

3. **查看效果**

访问包含代码块的文章，看看新主题是否符合你的审美。

---

## 自定义样式

### 1. 自定义 CSS 文件位置

PaperMod 支持通过 **`assets/css/extended/custom.css`** 覆盖默认样式。

**文件结构**：

```
MyHomepage/
├── assets/
│   └── css/
│       └── extended/
│           └── custom.css  ← 你的自定义样式文件
```

### 2. 常用样式自定义示例

#### **2.1 修改正文字体和大小**

```css
/* 正文内容区域 */
.post-content {
  font-size: 18px;           /* 字体大小 */
  line-height: 1.8;          /* 行高（影响可读性） */
  font-family: "Microsoft YaHei", "微软雅黑", sans-serif;  /* 中文字体 */
}
```

#### **2.2 修改标题样式**

```css
/* 文章内的标题 */
.post-content h1 {
  color: #E58F74;            /* 自定义标题颜色 */
  font-size: 2em;
  margin-top: 2em;
  border-bottom: 2px solid #E58F74;
  padding-bottom: 0.3em;
}

.post-content h2 {
  color: #E58F74;
  font-size: 1.5em;
  margin-top: 1.5em;
}

.post-content h3 {
  color: #666;
  font-size: 1.2em;
  margin-top: 1em;
}
```

#### **2.3 自定义代码块样式**

```css
/* 代码块容器 */
.highlight {
  border-radius: 8px;        /* 圆角 */
  overflow: hidden;
  margin: 1.5em 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);  /* 阴影 */
}

/* 代码块背景 */
.chroma {
  background-color: #282c34 !important;  /* 自定义背景色 */
  padding: 1em;
}

/* 代码字体 */
.chroma code {
  font-family: "Fira Code", "Consolas", "Monaco", monospace;
  font-size: 14px;
}

/* 行号样式 */
.chroma .lnt,
.chroma .ln {
  color: #5c6370;            /* 行号颜色 */
  font-size: 13px;
}
```

#### **2.4 美化引用块（Blockquote）**

```css
/* 引用块 */
.post-content blockquote {
  border-left: 4px solid #E58F74;  /* 左侧彩条 */
  background-color: rgba(229, 143, 116, 0.1);  /* 浅橙色背景 */
  padding: 1em 1.5em;
  margin: 1.5em 0;
  border-radius: 4px;
  font-style: italic;
  color: #666;
}

/* 引用块内的段落 */
.post-content blockquote p {
  margin: 0.5em 0;
}
```

#### **2.5 美化表格**

```css
/* 表格容器 */
.post-content table {
  width: 100%;
  border-collapse: collapse;
  margin: 2em 0;
  font-size: 16px;
}

/* 表头 */
.post-content table thead {
  background-color: #E58F74;
  color: white;
}

.post-content table th {
  padding: 12px 15px;
  text-align: left;
  font-weight: bold;
}

/* 表格行 */
.post-content table tbody tr {
  border-bottom: 1px solid #ddd;
}

.post-content table tbody tr:hover {
  background-color: rgba(229, 143, 116, 0.1);  /* 悬停高亮 */
}

/* 表格单元格 */
.post-content table td {
  padding: 12px 15px;
}

/* 斑马纹效果 */
.post-content table tbody tr:nth-child(even) {
  background-color: #f9f9f9;
}
```

#### **2.6 美化链接**

```css
/* 正文链接 */
.post-content a {
  color: #E58F74;
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: all 0.3s ease;
}

.post-content a:hover {
  color: #d67d5e;
  border-bottom-color: #E58F74;
}
```

#### **2.7 美化列表**

```css
/* 无序列表 */
.post-content ul {
  list-style-type: none;
  padding-left: 1.5em;
}

.post-content ul li::before {
  content: "▸";              /* 自定义列表符号 */
  color: #E58F74;
  font-weight: bold;
  display: inline-block;
  width: 1em;
  margin-left: -1em;
}

/* 有序列表 */
.post-content ol {
  padding-left: 1.5em;
}

.post-content ol li {
  margin: 0.5em 0;
}
```

### 3. 应用自定义样式

1. **编辑/创建文件**

```bash
# 如果文件不存在，创建目录和文件
mkdir -p assets/css/extended
touch assets/css/extended/custom.css
```

2. **添加你的 CSS 代码**

将上面的样式复制到 `custom.css` 中。

3. **重启 Hugo 服务器**

```bash
hugo server
```

4. **查看效果**

访问你的文章页面，样式会自动生效！

---

## 高级美化技巧

### 1. 代码块行号样式优化

```css
/* 让行号和代码对齐更美观 */
.highlight pre.chroma {
  padding: 1em;
}

.chroma .lntd:first-child {
  padding-right: 1em;
  border-right: 1px solid rgba(255, 255, 255, 0.1);
}

.chroma .lntd:last-child {
  padding-left: 1em;
}
```

### 2. 添加代码块标题

在 Markdown 中使用 Hugo Shortcode：

**创建 `layouts/shortcodes/code-with-title.html`**：

```html
<div class="code-block-with-title">
  <div class="code-title">{{ .Get "title" }}</div>
  {{ .Inner | markdownify }}
</div>
```

**CSS 样式**（`assets/css/extended/custom.css`）：

```css
.code-block-with-title {
  margin: 1.5em 0;
}

.code-title {
  background-color: #E58F74;
  color: white;
  padding: 0.5em 1em;
  border-radius: 8px 8px 0 0;
  font-weight: bold;
  font-size: 14px;
}

.code-block-with-title .highlight {
  margin-top: 0;
  border-radius: 0 0 8px 8px;
}
```

**使用方法**（在 Markdown 中）：

```markdown
{{</* code-with-title title="main.py" */>}}
```python
def hello_world():
    print("Hello, World!")
```
{{</* /code-with-title */>}}
```

### 3. 响应式字体大小

让字体在不同设备上自适应：

```css
/* 桌面端 */
@media (min-width: 1024px) {
  .post-content {
    font-size: 18px;
  }
}

/* 平板 */
@media (min-width: 768px) and (max-width: 1023px) {
  .post-content {
    font-size: 16px;
  }
}

/* 手机 */
@media (max-width: 767px) {
  .post-content {
    font-size: 15px;
  }
}
```

### 4. 添加文章阅读进度条

**CSS**（`assets/css/extended/custom.css`）：

```css
/* 阅读进度条 */
#progress-bar {
  position: fixed;
  top: 0;
  left: 0;
  width: 0%;
  height: 3px;
  background: linear-gradient(to right, #E58F74, #f5a97f);
  z-index: 9999;
  transition: width 0.1s ease;
}
```

**JavaScript**（`layouts/partials/extend_footer.html`）：

```html
{{- if .IsPage }}
<div id="progress-bar"></div>
<script>
  // 阅读进度条
  window.addEventListener('scroll', function() {
    const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (winScroll / height) * 100;
    document.getElementById('progress-bar').style.width = scrolled + '%';
  });
</script>
{{- end }}
```

### 5. 图片样式优化

```css
/* 图片居中并添加阴影 */
.post-content img {
  display: block;
  margin: 2em auto;
  max-width: 100%;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

/* 图片悬停放大效果 */
.post-content img:hover {
  transform: scale(1.02);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

/* 图片说明文字（alt） */
.post-content p > img + em {
  display: block;
  text-align: center;
  font-size: 14px;
  color: #999;
  margin-top: -1em;
}
```

---

## 完整示例：我的自定义主题

将以下代码复制到 `assets/css/extended/custom.css`，作为一个完整的美化方案：

```css
/* ========================================
   Suxilan's Blog - 自定义样式
   ======================================== */

/* 1. 正文字体和排版 */
.post-content {
  font-size: 17px;
  line-height: 1.8;
  color: #333;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif;
}

/* 2. 标题样式 */
.post-content h1,
.post-content h2,
.post-content h3 {
  color: #E58F74;
  font-weight: 600;
  margin-top: 2em;
  margin-bottom: 0.8em;
}

.post-content h1 {
  font-size: 2em;
  border-bottom: 2px solid #E58F74;
  padding-bottom: 0.3em;
}

.post-content h2 {
  font-size: 1.6em;
}

.post-content h3 {
  font-size: 1.3em;
  color: #666;
}

/* 3. 代码块 */
.highlight {
  border-radius: 8px;
  overflow: hidden;
  margin: 1.5em 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.chroma {
  background-color: #282c34 !important;
  padding: 1.2em;
}

.chroma code {
  font-family: "Fira Code", "Cascadia Code", "Consolas", monospace;
  font-size: 14px;
  line-height: 1.6;
}

/* 4. 行内代码 */
.post-content code:not(.chroma code) {
  background-color: rgba(229, 143, 116, 0.1);
  color: #E58F74;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 0.9em;
  font-family: "Fira Code", "Consolas", monospace;
}

/* 5. 引用块 */
.post-content blockquote {
  border-left: 4px solid #E58F74;
  background-color: rgba(229, 143, 116, 0.05);
  padding: 1em 1.5em;
  margin: 1.5em 0;
  border-radius: 4px;
  color: #555;
}

/* 6. 链接 */
.post-content a {
  color: #E58F74;
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: all 0.3s ease;
}

.post-content a:hover {
  color: #d67d5e;
  border-bottom-color: #E58F74;
}

/* 7. 图片 */
.post-content img {
  display: block;
  margin: 2em auto;
  max-width: 100%;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

/* 8. 表格 */
.post-content table {
  width: 100%;
  border-collapse: collapse;
  margin: 2em 0;
  font-size: 15px;
}

.post-content table thead {
  background-color: #E58F74;
  color: white;
}

.post-content table th,
.post-content table td {
  padding: 12px 15px;
  text-align: left;
}

.post-content table tbody tr {
  border-bottom: 1px solid #eee;
}

.post-content table tbody tr:hover {
  background-color: rgba(229, 143, 116, 0.05);
}

/* 9. 列表 */
.post-content ul li {
  margin: 0.5em 0;
}

.post-content ol li {
  margin: 0.5em 0;
}

/* 10. 分隔线 */
.post-content hr {
  border: none;
  border-top: 2px solid rgba(229, 143, 116, 0.3);
  margin: 3em 0;
}

/* 11. 响应式调整 */
@media (max-width: 768px) {
  .post-content {
    font-size: 16px;
  }
  
  .post-content h1 {
    font-size: 1.6em;
  }
  
  .post-content h2 {
    font-size: 1.4em;
  }
}
```

---

## 查看 Hugo Chroma 支持的语言

Hugo 支持超过 200 种编程语言的语法高亮。常用的有：

| 语言 | Markdown 标记 | 语言 | Markdown 标记 |
|------|---------------|------|---------------|
| Python | `python` | JavaScript | `javascript` / `js` |
| Go | `go` | TypeScript | `typescript` / `ts` |
| Java | `java` | HTML | `html` |
| C/C++ | `c` / `cpp` | CSS | `css` |
| Rust | `rust` | SQL | `sql` |
| Shell | `bash` / `sh` | YAML | `yaml` |
| JSON | `json` | Markdown | `markdown` / `md` |

**查看完整列表**：

```bash
hugo gen chromastyles --help
```

---

## 总结

| 需求 | 修改位置 | 难度 |
|------|----------|------|
| 更换代码高亮主题 | `hugo.yaml` → `markup.highlight.style` | ⭐ 简单 |
| 自定义字体/颜色 | `assets/css/extended/custom.css` | ⭐⭐ 简单 |
| 美化代码块/引用 | `assets/css/extended/custom.css` | ⭐⭐ 简单 |
| 添加自定义组件 | `layouts/shortcodes/` | ⭐⭐⭐ 中等 |
| 修改主题源码 | `themes/PaperMod/assets/css/` | ⭐⭐⭐⭐ 复杂（不推荐） |

**建议**：从修改 `custom.css` 开始，逐步调整成你喜欢的风格！

---

## 相关文档

- [Hugo Chroma 样式列表](https://xyproto.github.io/splash/docs/all.html)
- [PaperMod 自定义文档](https://github.com/adityatelange/hugo-PaperMod/wiki/FAQs#custom-css)
- [Goldmark 配置](https://gohugo.io/getting-started/configuration-markup/#goldmark)

---

> 💡 **提示**：修改 CSS 后记得刷新浏览器（Ctrl+F5 强制刷新），或者重启 `hugo server`！

