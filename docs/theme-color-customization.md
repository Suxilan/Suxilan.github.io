# 主题色自定义系统

> 本文档详细说明主题色自定义功能的使用方法、工作原理和技术实现。

---

## 📚 目录

- [功能概述](#功能概述)
- [使用方法](#使用方法)
- [技术实现](#技术实现)
- [自定义扩展](#自定义扩展)
- [故障排查](#故障排查)

---

## 功能概述

### 1. 什么是主题色自定义？

主题色自定义系统允许你通过点击顶部的调色盘图标 🎨，实时更改整个网站的主题颜色，包括：

- ✅ 链接颜色
- ✅ 按钮颜色
- ✅ 标签云颜色
- ✅ 评论区按钮颜色（Giscus）
- ✅ 悬停效果颜色
- ✅ 其他所有使用主题色的地方

### 2. 主要特性

| 特性 | 说明 |
|------|------|
| **纯前端实现** | 无需后端服务器，完全由浏览器处理 |
| **实时预览** | 选择颜色后立即生效，无需刷新页面 |
| **持久化存储** | 使用 `localStorage` 保存，下次访问自动恢复 |
| **预设颜色** | 提供 9 种精选配色方案 |
| **自定义颜色** | 支持通过拾色器选择任意颜色 |
| **响应式设计** | 适配桌面端和移动端 |
| **Giscus 同步** | 自动同步评论区颜色 |

---

## 使用方法

### 1. 打开颜色选择器

在网站顶部找到 **调色盘图标** 🎨（位于日夜切换按钮旁边），点击打开颜色选择器。

**快捷键**：`Alt + C`

### 2. 选择颜色

#### **方式 1：使用预设颜色**

点击任意预设颜色块：

```
┌─────────────────────────────────────────┐
│  🎨 选择主题色                          │
├─────────────────────────────────────────┤
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐   │
│  │ 橙 │ │ 红 │ │ 青 │ │ 蓝 │ │ 绿 │   │
│  └────┘ └────┘ └────┘ └────┘ └────┘   │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐           │
│  │ 黄 │ │ 灰 │ │ 紫 │ │ 粉 │           │
│  └────┘ └────┘ └────┘ └────┘           │
└─────────────────────────────────────────┘
```

**预设颜色列表**：

| 颜色名 | 色值 | 适用场景 |
|--------|------|----------|
| 橙色（默认） | `#E58F74` | 温暖、友好、博客 |
| 红色 | `#FF6B6B` | 热情、活力、设计 |
| 青色 | `#4ECDC4` | 清新、现代、科技 |
| 蓝色 | `#45B7D1` | 专业、冷静、商务 |
| 绿色 | `#96CEB4` | 自然、健康、环保 |
| 黄色 | `#FFEAA7` | 明亮、活泼、创意 |
| 灰色 | `#DFE6E9` | 简约、优雅、极简 |
| 紫色 | `#A29BFE` | 神秘、优雅、艺术 |
| 粉色 | `#FD79A8` | 浪漫、可爱、个性 |

#### **方式 2：使用自定义颜色**

在 **自定义颜色** 区域：

1. 点击颜色选择器
2. 拖动滑块选择你喜欢的颜色
3. 或者输入 HEX 色值（如 `#FF5733`）

### 3. 预览效果

选择颜色后，弹窗内的 **预览区域** 会实时显示效果：

```
┌─────────────────────────────────────┐
│  预览效果：                         │
│  ┌────────┐ ┌────────┐ ┌────────┐ │
│  │ 按钮   │ │ 标签   │ │ 链接   │ │
│  └────────┘ └────────┘ └────────┘ │
└─────────────────────────────────────┘
```

### 4. 应用颜色

满意后点击 **"应用"** 按钮，颜色会：

1. ✅ 立即应用到整个网站
2. ✅ 保存到浏览器本地存储
3. ✅ 下次访问自动恢复

### 5. 恢复默认

如果想恢复到默认的橙色主题，点击 **"恢复默认"** 按钮。

### 6. 关闭弹窗

- 点击右上角的 **×** 按钮
- 点击弹窗外的背景区域
- 按 **ESC** 键

---

## 技术实现

### 1. 系统架构

```
┌─────────────────────────────────────────┐
│  用户选择颜色                           │
└───────────────┬─────────────────────────┘
                ↓
┌─────────────────────────────────────────┐
│  JavaScript 处理                        │
│  - hexToRgb() 转换颜色格式              │
│  - applyThemeColor() 应用颜色           │
└───────────────┬─────────────────────────┘
                ↓
┌─────────────────────────────────────────┐
│  更新 CSS 变量                          │
│  - --theme-color                        │
│  - --theme-color-rgb                    │
└───────────────┬─────────────────────────┘
                ↓
┌─────────────────────────────────────────┐
│  同步到所有组件                         │
│  - 标签云                               │
│  - 按钮                                 │
│  - 链接                                 │
│  - Giscus 评论区                        │
└───────────────┬─────────────────────────┘
                ↓
┌─────────────────────────────────────────┐
│  保存到 localStorage                    │
│  - 持久化存储                           │
│  - 下次访问自动恢复                     │
└─────────────────────────────────────────┘
```

### 2. 核心文件

| 文件 | 作用 |
|------|------|
| `layouts/partials/header.html` | 调色盘按钮 + 颜色选择器弹窗 HTML |
| `layouts/partials/color-customizer.html` | JavaScript 逻辑 |
| `assets/css/extended/custom.css` | CSS 变量定义 + 弹窗样式 |
| `layouts/partials/extend_footer.html` | 引入 JS 脚本 |
| `layouts/_default/search.html` | 标签云样式（使用 CSS 变量） |

### 3. CSS 变量系统

#### **定义（custom.css）**

```css
:root {
  /* 主题色变量 */
  --theme-color: #E58F74;              /* HEX 格式 */
  --theme-color-rgb: 229, 143, 116;    /* RGB 格式 */
  
  /* 衍生颜色 */
  --theme-color-light: rgba(var(--theme-color-rgb), 0.15);
  --theme-color-lighter: rgba(var(--theme-color-rgb), 0.05);
  --theme-color-hover: rgba(var(--theme-color-rgb), 0.85);
  --theme-color-dark: rgba(var(--theme-color-rgb), 0.95);
}
```

#### **使用方式**

在任何需要使用主题色的地方，使用 CSS 变量：

```css
/* ❌ 错误：硬编码颜色 */
.button {
  background: #E58F74;
}

/* ✅ 正确：使用 CSS 变量 */
.button {
  background: var(--theme-color);
}

/* ✅ 使用半透明效果 */
.tag {
  background: var(--theme-color-light);
  color: var(--theme-color);
}
```

### 4. JavaScript 核心函数

#### **4.1 颜色转换**

```javascript
// 十六进制转 RGB
function hexToRgb(hex) {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16)
  } : null;
}
```

#### **4.2 应用主题色**

```javascript
function applyThemeColor(color) {
  const rgb = hexToRgb(color);
  if (!rgb) return;

  const root = document.documentElement;
  root.style.setProperty('--theme-color', color);
  root.style.setProperty('--theme-color-rgb', `${rgb.r}, ${rgb.g}, ${rgb.b}`);

  updateGiscusColor(color, rgb);
}
```

#### **4.3 持久化存储**

```javascript
// 保存到 localStorage
function saveThemeColor(color) {
  localStorage.setItem('theme-color', color);
}

// 从 localStorage 加载
function loadThemeColor() {
  const savedColor = localStorage.getItem('theme-color');
  if (savedColor) {
    applyThemeColor(savedColor);
    return savedColor;
  }
  return '#E58F74'; // 默认颜色
}
```

### 5. Giscus 颜色同步

评论区（Giscus）的颜色同步通过动态注入 CSS 实现：

```javascript
function updateGiscusColor(color, rgb) {
  let giscusStyle = document.getElementById('giscus-color-override');
  if (!giscusStyle) {
    giscusStyle = document.createElement('style');
    giscusStyle.id = 'giscus-color-override';
    document.head.appendChild(giscusStyle);
  }

  giscusStyle.textContent = `
    .gsc-comment-box-tabs button:hover {
      border-bottom-color: ${color} !important;
    }
    /* 更多样式... */
  `;
}
```

---

## 自定义扩展

### 1. 添加更多预设颜色

编辑 `layouts/partials/header.html`，在 `.color-presets` 部分添加：

```html
<button class="color-preset" data-color="#你的颜色" 
        style="background: #你的颜色;" 
        title="你的颜色名称"></button>
```

### 2. 应用主题色到其他元素

#### **步骤 1：修改 CSS，使用变量**

```css
/* 你的自定义元素 */
.my-element {
  background: var(--theme-color);     /* 背景 */
  color: var(--theme-color);          /* 文字 */
  border-color: var(--theme-color);   /* 边框 */
  box-shadow: 0 4px 8px var(--theme-color-light);  /* 阴影 */
}

.my-element:hover {
  background: var(--theme-color-hover);
}
```

#### **步骤 2：重启 Hugo 服务器**

```bash
hugo server
```

### 3. 自定义默认颜色

编辑 `assets/css/extended/custom.css`：

```css
:root {
  --theme-color: #你的颜色;  /* 改成你想要的默认颜色 */
  --theme-color-rgb: R, G, B;  /* 对应的 RGB 值 */
}
```

也要修改 JavaScript 中的默认值（`layouts/partials/color-customizer.html`）：

```javascript
function loadThemeColor() {
  // ...
  return '#你的颜色'; // 改成你的默认颜色
}
```

### 4. 添加颜色分类

你可以扩展颜色选择器，添加颜色分类（如"暖色系"、"冷色系"）：

```html
<div class="color-category">
  <h4>暖色系</h4>
  <div class="color-presets">
    <button class="color-preset" data-color="#FF6B6B" ...></button>
    <button class="color-preset" data-color="#FFA07A" ...></button>
  </div>
</div>

<div class="color-category">
  <h4>冷色系</h4>
  <div class="color-presets">
    <button class="color-preset" data-color="#4ECDC4" ...></button>
    <button class="color-preset" data-color="#45B7D1" ...></button>
  </div>
</div>
```

---

## 故障排查

### Q1: 颜色没有生效？

**检查步骤**：

1. **清除浏览器缓存**

按 `Ctrl + Shift + Delete`（Windows）或 `Cmd + Shift + Delete`（Mac），清除缓存后刷新。

2. **强制刷新页面**

按 `Ctrl + F5`（Windows）或 `Cmd + Shift + R`（Mac）。

3. **检查 CSS 变量是否正确**

打开浏览器开发者工具（F12），在 **Console** 中输入：

```javascript
getComputedStyle(document.documentElement).getPropertyValue('--theme-color')
```

应该显示你选择的颜色值。

4. **检查元素是否使用了 CSS 变量**

在开发者工具的 **Elements** 面板中，检查目标元素的样式，确保使用的是 `var(--theme-color)` 而不是硬编码的颜色。

### Q2: 刷新页面后颜色丢失？

**原因**：`localStorage` 未保存成功。

**解决方案**：

1. 检查浏览器是否允许使用 `localStorage`（隐私模式下可能被禁用）
2. 在 Console 中手动测试：

```javascript
localStorage.setItem('theme-color', '#FF6B6B');
localStorage.getItem('theme-color');
```

3. 确保点击了 **"应用"** 按钮，而不是直接关闭弹窗

### Q3: Giscus 评论区颜色没有同步？

**可能原因**：

1. **评论区未加载**：颜色同步仅在评论区 iframe 加载后生效
2. **自定义 CSS 权重不够**：Giscus 的默认样式权重较高

**解决方案**：

编辑 `static/giscus-light.css` 和 `static/giscus-dark.css`，将硬编码的颜色改为你的主题色。

或者在 `layouts/partials/color-customizer.html` 中增强 CSS 注入：

```javascript
giscusStyle.textContent = `
  /* 使用 !important 提高优先级 */
  .gsc-comment-box-tabs button:hover {
    border-bottom-color: ${color} !important;
  }
`;
```

### Q4: 移动端弹窗显示异常？

**检查**：

1. 是否添加了响应式 CSS（已包含在 `custom.css` 中）
2. 弹窗是否被其他元素遮挡（检查 `z-index`）

**调整弹窗大小**：

编辑 `assets/css/extended/custom.css`：

```css
@media (max-width: 600px) {
  .color-modal-content {
    width: 98%;  /* 调整为更大 */
    max-height: 95vh;
  }
}
```

### Q5: 预设颜色选择后没有激活标记？

**原因**：JavaScript 未正确执行。

**检查**：

1. 打开浏览器 Console（F12），查看是否有错误信息
2. 确认 `layouts/partials/extend_footer.html` 已正确引入脚本
3. 检查 `color-customizer.html` 中的 JavaScript 是否有语法错误

---

## 使用技巧

### 1. 配色建议

| 网站类型 | 推荐配色 |
|----------|----------|
| 个人博客 | 橙色、粉色、紫色 |
| 技术博客 | 蓝色、青色、灰色 |
| 设计作品集 | 红色、黄色、绿色 |
| 摄影网站 | 灰色、黑色、极简 |

### 2. 对比度检查

选择颜色后，确保：

- **浅色背景** + **深色文字**：对比度 ≥ 4.5:1
- **深色背景** + **浅色文字**：对比度 ≥ 4.5:1

可以使用 [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) 测试。

### 3. 保持一致性

建议将你的品牌色、Logo 主色作为网站主题色，保持视觉一致性。

---

## 高级功能（未来计划）

- [ ] **渐变色支持**：支持线性渐变或径向渐变
- [ ] **多色主题**：同时定义主色和辅助色
- [ ] **暗色模式独立配色**：亮色/暗色模式使用不同主题色
- [ ] **颜色历史记录**：记录最近使用的 5 种颜色
- [ ] **分享配色方案**：生成 URL 参数，分享给他人
- [ ] **导入/导出配色**：JSON 格式导入导出配色方案

---

## 总结

| 功能 | 实现方式 | 文件位置 |
|------|----------|----------|
| 调色盘按钮 | HTML | `layouts/partials/header.html` |
| 颜色选择器弹窗 | HTML + CSS | `layouts/partials/header.html` + `custom.css` |
| 颜色应用逻辑 | JavaScript | `layouts/partials/color-customizer.html` |
| CSS 变量管理 | CSS Custom Properties | `assets/css/extended/custom.css` |
| 持久化存储 | localStorage | JavaScript |
| Giscus 同步 | 动态 CSS 注入 | JavaScript |

---

## 相关文档

- [Markdown 渲染与美化](markdown-rendering.md)
- [搜索页面功能说明](search-page.md)
- [自定义配置指南](customization-guide.md)

---

> 💡 **提示**：修改完成后记得重启 `hugo server`，然后访问网站，点击顶部的调色盘图标体验主题色自定义功能！🎨

