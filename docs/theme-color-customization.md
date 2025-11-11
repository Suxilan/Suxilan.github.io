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

## Spring.css 智能配色系统 🎨

> **新功能**：通过一个主题色自动生成完整的配色方案，并应用到 Spring.css 的所有绿色元素

### 1. 功能概述

当你选择一个主题色（例如橙色 `#E58F74`）后，系统会：

1. **自动分析**颜色的色相（H）、饱和度（S）、亮度（L）
2. **智能生成**10+ 种配色变体（深色、浅色、高饱和度、低饱和度等）
3. **一键应用**到 Spring.css 的 40+ 个颜色变量
4. **保持和谐**：所有生成的颜色保持相同色调，确保视觉统一

**效果**：你的整个博客（包括 Markdown 渲染样式）会立即改变为你选择的主题色系！

---

### 2. 可视化配色方案

#### 示例 1：橙色主题（默认 `#E58F74`）

```
主题色 #E58F74 (橙色)
  ↓ HSL 分析
色相: 14°  饱和度: 68%  亮度: 67%
  ↓ 智能生成变体
┌─────────────────────────────────────────────────────┐
│ 基础色 (base)                                        │
│ █ #E58F74  RGB(229,143,116)  原始主题色              │
├─────────────────────────────────────────────────────┤
│ 深色变体（用于文字、边框）                          │
│ █ #A05C41  darker (-45% 亮度)  粗体文字             │
│ █ #6E3B28  dark   (-30% 亮度)  列表标记、代码文字   │
├─────────────────────────────────────────────────────┤
│ 浅色变体（用于背景、高亮）                          │
│ █ #F5D9CE  light   (+35% 亮度)  高亮标记背景        │
│ █ #F9E8E1  lighter (+45% 亮度)  引用块背景、表头    │
├─────────────────────────────────────────────────────┤
│ 饱和度变体                                          │
│ █ #F4A489  vivid   (+20% 饱和度)  代码块圆点        │
│ █ #D4AD9C  muted   (-30% 饱和度)  表格边框          │
├─────────────────────────────────────────────────────┤
│ 特殊用途                                            │
│ █ #F3D4C7  selection  文本选择背景                  │
│ █ #C7886E  border     边框、引用块边框              │
│ ░ rgba(229,143,116,0.1)  hover  段落悬停背景        │
└─────────────────────────────────────────────────────┘
```

#### 示例 2：蓝色主题（`#45B7D1`）

```
主题色 #45B7D1 (蓝色)
  ↓ HSL 分析
色相: 194°  饱和度: 60%  亮度: 55%
  ↓ 智能生成变体
┌─────────────────────────────────────────────────────┐
│ 基础色 (base)                                        │
│ █ #45B7D1  RGB(69,183,209)   原始主题色             │
├─────────────────────────────────────────────────────┤
│ 深色变体                                            │
│ █ #1E5A6D  darker  深蓝色  粗体文字                 │
│ █ #2A7B92  dark    中蓝色  列表标记                 │
├─────────────────────────────────────────────────────┤
│ 浅色变体                                            │
│ █ #D4EEF5  light   淡蓝色  高亮标记背景             │
│ █ #E8F6FA  lighter 极淡蓝  引用块背景               │
├─────────────────────────────────────────────────────┤
│ 饱和度变体                                          │
│ █ #3DC9E8  vivid   鲜蓝色  代码块圆点               │
│ █ #7FB8CB  muted   柔和蓝  表格边框                 │
└─────────────────────────────────────────────────────┘
```

#### 示例 3：紫色主题（`#A29BFE`）

```
主题色 #A29BFE (紫色)
  ↓ HSL 分析
色相: 244°  饱和度: 97%  亮度: 79%
  ↓ 智能生成变体
┌─────────────────────────────────────────────────────┐
│ 基础色 (base)                                        │
│ █ #A29BFE  RGB(162,155,254)  原始主题色             │
├─────────────────────────────────────────────────────┤
│ 深色变体                                            │
│ █ #3B2AA0  darker  深紫色  粗体文字                 │
│ █ #5B4BC7  dark    中紫色  列表标记                 │
├─────────────────────────────────────────────────────┤
│ 浅色变体                                            │
│ █ #E0DEFF  light   淡紫色  高亮标记背景             │
│ █ #F0EEFF  lighter 极淡紫  引用块背景               │
├─────────────────────────────────────────────────────┤
│ 饱和度变体                                          │
│ █ #B5ADFF  vivid   鲜紫色  代码块圆点               │
│ █ #B5B3DB  muted   柔和紫  表格边框                 │
└─────────────────────────────────────────────────────┘
```

---

### 3. 应用映射表

以下是智能配色系统如何将生成的颜色应用到 Spring.css 元素：

| 配色变体 | 应用元素 | CSS 变量 | 示例 |
|---------|---------|---------|------|
| **base** | 引用块表头、H2 下划线 | `--blockquote-thead-bg-color`<br>`--write-h2-after-bg` | 橙色 `#E58F74` |
| **darker** | 粗体文字、代码块左圆点 | `--strong-color`<br>`--code-fences-before-bg` | 深棕 `#6E3B28` |
| **dark** | 列表标记、内联代码文字 | `--ul-marker-color`<br>`--code-color` | 棕色 `#A05C41` |
| **lighter** | 引用块背景、表头背景 | `--blockquote-bg-color`<br>`--table-thead-bg-color` | 浅橙 `#F9E8E1` |
| **light** | 高亮标记、分隔线两侧 | `--mark-bg-color`<br>`--hr-bg-image` (两侧) | 淡橙 `#F5D9CE` |
| **vivid** | 代码块右圆点、滚动条 | `--code-fences-before-box-shadow`<br>`--scrollbar-thumb-bg` | 鲜橙 `#F4A489` |
| **muted** | （保留用于扩展） | - | 柔和橙 `#D4AD9C` |
| **border** | 引用块边框、分隔线中心 | `--blockquote-border-color`<br>`--hr-bg-image` (中心) | 橙色边框 `#C7886E` |
| **selection** | 文本选择高亮 | `--selection-color` | 淡橙选择 `#F3D4C7` |
| **hover** | 段落悬停背景 | `--p-hover-bg-color` | 半透明橙 `rgba(229,143,116,0.1)` |

**完整应用列表**（40+ 个变量）：

```css
/* 标题样式 */
--write-h1-before-bg: 渐变(transparent → lighter → transparent)
--write-h2-after-bg: 渐变(transparent → base → transparent)

/* 列表 */
--ul-marker-color: dark
--ulul-marker-color: dark
--ululul-marker-color: dark

/* 引用块 */
--blockquote-border-color: border
--blockquote-bg-color: lighter
--blockquote-thead-bg-color: base
--blockquote-td-hover-bg: rgba(base, 0.15)

/* 表格 */
--table-thead-bg-color: lighter
--table-thead-text-color: darker
--table-tbody-border-color: lighter
--table-td-hover-bg: rgba(base, 0.15)

/* 文本样式 */
--strong-color: darker
--em-hover-color: darker
--u-border-color: dark
--code-bg-color: rgba(base, 0.15)
--code-color: dark
--code-hover-bg-color: rgba(base, 0.25)
--del-color: rgba(base, 0.5)
--mark-bg-color: light
--a-hover-color: darker

/* 代码块 */
--code-fences-before-bg: darker
--code-fences-before-box-shadow: 20px 0 dark, 40px 0 vivid
--cm-s-inner-linenumber-color: border

/* 分隔线 */
--hr-bg-image: 渐变(light → border → light)

/* 滚动条 */
--scrollbar-thumb-bg: 渐变(vivid → darker)

/* 其他 */
--selection-color: selection
--p-hover-bg-color: hover
```

---

### 4. 色彩生成算法

#### 工作流程

```
1. 用户选择主题色 (#E58F74)
   ↓
2. 十六进制 → RGB
   #E58F74 → RGB(229, 143, 116)
   ↓
3. RGB → HSL
   RGB(229, 143, 116) → HSL(14°, 68%, 67%)
   ↓
4. 调整 HSL 参数生成变体
   ┌─────────────────────────────────┐
   │ darker:  H=14°  S=68%  L=22%    │  (-45%)
   │ dark:    H=14°  S=68%  L=37%    │  (-30%)
   │ light:   H=14°  S=48% ▼ L=90%   │  (+35%, -20%)
   │ lighter: H=14°  S=38% ▼ L=95%   │  (+45%, -30%)
   │ vivid:   H=14°  S=88% ▲ L=67%   │  (+20%)
   │ muted:   H=14°  S=38% ▼ L=67%   │  (-30%)
   └─────────────────────────────────┘
   ↓
5. HSL → RGB → HEX
   各变体转回十六进制格式
   ↓
6. 应用到 CSS 变量
   root.style.setProperty('--ul-marker-color', '#A05C41')
```

#### 算法参数

| 变体 | 色相调整 | 饱和度调整 | 亮度调整 | 公式 |
|------|---------|-----------|---------|------|
| **darker** | 不变 | 不变 | `-45%`<br>最小 5% | `L = max(L - 45, 5)` |
| **dark** | 不变 | 不变 | `-30%`<br>最小 15% | `L = max(L - 30, 15)` |
| **light** | 不变 | `-20%`<br>最小 20% | `+35%`<br>最大 95% | `S = max(S - 20, 20)`<br>`L = min(L + 35, 95)` |
| **lighter** | 不变 | `-30%`<br>最小 15% | `+45%`<br>最大 98% | `S = max(S - 30, 15)`<br>`L = min(L + 45, 98)` |
| **vivid** | 不变 | `+20%`<br>最大 100% | 不变 | `S = min(S + 20, 100)` |
| **muted** | 不变 | `-30%`<br>最小 20% | 不变 | `S = max(S - 30, 20)` |
| **border** | 不变 | `-10%`<br>最小 30% | 限制到 65% | `S = max(S - 10, 30)`<br>`L = min(L, 65)` |
| **selection** | 不变 | `-25%`<br>最小 20% | `+40%`<br>最大 93% | `S = max(S - 25, 20)`<br>`L = min(L + 40, 93)` |

**为什么使用这些参数？**

- **亮度范围**：`5% - 98%`，避免纯黑/纯白
- **饱和度下限**：`15% - 30%`，确保背景色不会过于灰暗
- **亮色降饱和**：背景色降低饱和度，避免刺眼
- **深色保饱和**：文字颜色保持饱和度，确保对比度

---

### 5. 浏览器控制台调试

打开浏览器开发者工具（F12），选择一个颜色后查看生成的配色方案：

```javascript
// 控制台输出示例
✅ 主题色已更新: #E58F74
🎨 智能配色方案: {
  base: "#E58F74",
  baseRgb: "229, 143, 116",
  baseRgba: [Function],
  
  // 深色变体
  dark: "#A05C41",
  darker: "#6E3B28",
  
  // 浅色变体
  light: "#F5D9CE",
  lighter: "#F9E8E1",
  
  // 饱和度变体
  vivid: "#F4A489",
  muted: "#D4AD9C",
  
  // 特殊用途
  selection: "#F3D4C7",
  hover: "rgba(229, 143, 116, 0.1)",
  border: "#C7886E"
}
```

**测试不同颜色**：

在控制台中手动测试配色生成：

```javascript
// 测试紫色
const purple = generateColorPalette('#A29BFE');
console.table(purple);

// 测试蓝色
const blue = generateColorPalette('#45B7D1');
console.table(blue);
```

---

### 6. 不受影响的元素

以下元素的颜色**保持原样**，不随主题色变化：

| 元素类型 | 固定颜色 | 原因 |
|---------|---------|------|
| **警告提示框** | 红色 `#CF222E` | 警示语义，不宜更改 |
| **警示提示框** | 黄色 `#9A6700` | 注意语义，不宜更改 |
| **重要提示框** | 紫色 `#8250DF` | 重要语义，保持区分 |
| **笔记提示框** | 蓝色 `#0969DA` | 信息语义，保持区分 |
| **代码高亮** | Monokai 主题 | 语法高亮，独立系统 |
| **链接默认色** | 青色 `#0c8f94` | 保持可识别性 |
| **链接悬停色** | 使用 `darker` 变体 | 与主题色协调 |

---

### 7. 最佳实践

#### 选择合适的主题色

| 色系 | 推荐场景 | 注意事项 |
|------|---------|---------|
| **暖色系**（橙、红、黄） | 个人博客、创意网站 | 避免过于鲜艳（饱和度 < 80%） |
| **冷色系**（蓝、青、绿） | 技术博客、商务网站 | 选择中等亮度（40% < L < 70%） |
| **中性色**（灰、棕） | 极简风格、专业网站 | 可能对比度不足，需测试 |
| **高饱和色**（紫、粉） | 设计作品集、摄影网站 | 背景色会自动降饱和，无需担心 |

#### 避免的颜色

- ❌ 过亮的颜色（`L > 90%`）：生成的深色变体可能不够深
- ❌ 过暗的颜色（`L < 20%`）：生成的浅色变体可能不够浅
- ❌ 纯灰色（`S = 0%`）：失去色彩特征
- ❌ 荧光色（`S = 100%`, `L = 50%`）：过于刺眼

#### 对比度测试

应用新主题色后，检查以下元素的可读性：

1. **表格表头文字** vs **表头背景**
2. **粗体文字** vs **页面背景**
3. **内联代码文字** vs **代码背景**
4. **引用块边框** vs **引用块背景**

如果对比度不足（文字不清晰），尝试：
- 选择亮度更高或更低的颜色
- 调整饱和度（更饱和的颜色对比度更好）

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

