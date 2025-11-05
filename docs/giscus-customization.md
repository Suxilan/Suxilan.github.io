# Giscus 自定义配置

## 🎨 自定义颜色方案

### 当前配置：#E58F74 主题色

**修改位置**：
- 浅色模式：`static/giscus-custom.css`
- 深色模式：`static/giscus-custom-dark.css`

**主要颜色**：
- 主色调：`#E58F74`（珊瑚橙色）
- 悬停色：`#d97d5f`（深一点的橙色）

### 自定义的元素

1. **评论按钮**：`#E58F74` 背景色
2. **链接**：作者名、时间链接、文章链接
3. **评论框焦点边框**：聚焦时显示橙色边框和阴影
4. **表情反应**：选中时的背景和边框
5. **回复按钮**：橙色文字

### 自定义 CSS 工作原理

```
Hugo 构建网站
    ↓
生成 static/giscus-custom.css → 部署到 https://suxilan.github.io/giscus-custom.css
    ↓
Giscus 从这个 URL 加载样式
    ↓
应用到评论框
```

**重要**：CSS 文件必须部署到线上才能生效，本地预览时可能看不到效果！

---

## 🔧 修改颜色

### 步骤1：修改浅色模式颜色

**编辑 `static/giscus-custom.css`**：

```bash
# 使用查找替换
Ctrl+H
查找：#E58F74
替换为：你的颜色（如 #007bff）
全部替换

# 同时替换悬停色
查找：#d97d5f
替换为：你的颜色的深色版本
```

### 步骤2：修改深色模式颜色

**编辑 `static/giscus-custom-dark.css`**

同样的操作，替换颜色。

### 步骤3：推送部署

```bash
git add static/
git commit -m "Update Giscus colors"
git push
```

---

## 🎨 颜色方案建议

**蓝色**：
```
主色：#007bff
悬停：#0056b3
```

**绿色**：
```
主色：#28a745
悬停：#218838
```

**紫色**：
```
主色：#6f42c1
悬停：#5a32a3
```

**粉色**：
```
主色：#e83e8c
悬停：#c92a72
```

**当前橙色**：
```
主色：#E58F74
悬停：#d97d5f
```

---

## 📊 可修改的样式元素

### 按钮
- `.gsc-comment-box-main-button` - 评论按钮
- `.gsc-comment-box-preview-button` - 预览按钮
- `.gsc-reply-button` - 回复按钮

### 链接
- `a.gsc-comment-author` - 作者名
- `a.gsc-comment-header-link` - 时间链接
- `.gsc-comment-content a` - 评论内容中的链接

### 输入框
- `.gsc-comment-box-textarea:focus` - 聚焦时的边框

### 表情反应
- `.gsc-emoji-button.selected` - 选中的表情
- `.gsc-emoji-count` - 表情数字

**位置**：
- 浅色模式：`static/giscus-custom.css` 第 5-73 行
- 深色模式：`static/giscus-custom-dark.css` 第 5-73 行

---

---

## 🔄 主题切换逻辑

### 当前实现方式

**使用 MutationObserver 监听 DOM 变化**：

```javascript
// 监听 <html> 标签的 class 属性变化
const observer = new MutationObserver(function(mutations) {
  if (mutation.attributeName === 'class') {
    setGiscusTheme();  // PaperMod 切换时自动触发
  }
});

observer.observe(document.documentElement, {
  attributes: true,
  attributeFilter: ['class']
});
```

**工作流程**：
1. PaperMod 切换主题时，会切换 `<html class="dark">` 或移除 dark
2. MutationObserver 检测到 class 变化
3. 立即调用 `setGiscusTheme()`
4. 通过 postMessage 通知 Giscus iframe 切换主题
5. 评论框从 `giscus-custom.css` 切换到 `giscus-custom-dark.css`

### 为什么需要两个 CSS 文件？

- `giscus-custom.css` - 基于 `noborder_light`，浅色模式
- `giscus-custom-dark.css` - 基于 `noborder_dark`，深色模式

两个文件都使用 `#E58F74` 主色调，但基础样式不同。

---

## 🧪 测试主题切换

### 本地测试

```bash
hugo server -D
```

**注意**：本地预览时 CSS 文件还没部署，所以：
- ❌ 自定义颜色不会显示（会显示默认颜色）
- ✅ 但主题切换逻辑可以测试（看控制台日志）

### 线上测试

```bash
git add .
git commit -m "Update Giscus theme"
git push
```

部署后：
1. 访问 https://Suxilan.github.io/about/
2. 查看评论按钮是否为 #E58F74 颜色
3. 点击主题切换按钮
4. 评论框应该立即切换主题

### 调试方法

按 F12 打开控制台，应该看到：
```
Giscus theme switched to: https://suxilan.github.io/giscus-custom-dark.css
```

---

## 🎯 主题切换问题

### 问题诊断

**症状**：点击主题切换按钮，评论框不变色

**原因分析**：
1. Giscus iframe 可能加载较慢
2. postMessage 时机不对
3. 浏览器安全策略限制

### 解决方案

**已改进的 JavaScript**（`layouts/partials/comments.html`）：

**改进点**：
1. 使用 `MutationObserver` 监听 `<html>` 的 class 变化
2. PaperMod 切换主题时会改变 `<html class="dark">` 或移除 dark
3. 一旦检测到变化，立即切换 Giscus 主题
4. 不依赖主题按钮，而是监听实际的 DOM 变化

**测试方法**：
```bash
hugo server -D
```

访问 http://localhost:56948/about/
- 打开 F12 → Console
- 点击主题切换
- 查看控制台输出

---

## 📊 Giscus 内置功能

### 评论排序

**位置**：评论区右上角

**功能**：
- ⬆️ 最早优先
- ⬇️ 最新优先
- 🔥 最热门

**Giscus 自带**，无需配置。

### 表情反应

**位置**：每条评论上方

**功能**：
- 👍 点赞
- 😄 笑脸
- 🎉 庆祝
- ❤️ 爱心
- 等等

**自定义颜色**：
在 `static/giscus-custom.css` 中已配置选中状态为 #E58F74

---

## 🔍 如果主题还是不切换

### 备用方案1: 使用浏览器主题

**编辑 `layouts/partials/comments.html` 第 14 行**：

```html
data-theme="preferred_color_scheme"
```

**删除**所有 JavaScript 代码（第 22-69 行）

**效果**：
- 跟随浏览器/系统的深色模式
- 不跟随 PaperMod 的主题按钮
- 更可靠，但需要系统级切换

---

### 备用方案2: 双 script 标签

有些情况下，需要根据初始主题加载不同的配置：

**编辑 `layouts/partials/comments.html`**：

```html
{{- if .Params.comments }}
<div class="comments-section">
  {{- if eq (.Site.Params.defaultTheme | default "auto") "dark" }}
  <script src="https://giscus.app/client.js"
          data-theme="noborder_dark"
          ...>
  </script>
  {{- else }}
  <script src="https://giscus.app/client.js"
          data-theme="noborder_light"
          ...>
  </script>
  {{- end }}
</div>
```

---

## 🎨 颜色修改位置总结

| 元素 | 文件 | 行号 | 当前颜色 |
|------|------|------|---------|
| 评论按钮 | `static/giscus-custom.css` | 4-5 | #E58F74 |
| 悬停色 | `static/giscus-custom.css` | 10 | #d97d5f |
| 链接 | `static/giscus-custom.css` | 25 | #E58F74 |
| 边框 | `static/giscus-custom.css` | 30 | #E58F74 |
| 表情反应 | `static/giscus-custom.css` | 36 | #E58F74 |

**快速修改**：
1. 打开 `static/giscus-custom.css`
2. Ctrl+H 查找 `#E58F74`，替换为新颜色
3. 查找 `#d97d5f`（悬停色），替换为新颜色的深色版本

---

## ⏰ 时间修正

已修正的文件：
- ✅ `content/about.md` → 2025-11-05
- ✅ `content/notes/giscus-test.md` → 2025-11-05
- ✅ `content/posts/_index.md` → 2025-11-05
- ✅ `content/archives.md` → 2025-11-05

---

## 🚀 推送测试

```bash
git add .
git commit -m "Fix Giscus theme switching and customize colors"
git push
```

部署后测试主题切换。

