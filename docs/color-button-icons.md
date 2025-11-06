# 主题色按钮图标选项

> 提供多种图标选择，可以轻松切换主题色按钮的外观。

---

## 当前使用：🍀 四叶草图标

**特点**：可爱、有特色、悬停时有旋转效果

---

## 可选图标

### 1. ⭐ 五角星图标（简洁）

**替换方法**：

编辑 `layouts/partials/header.html`，找到第 77-87 行，将 SVG 代码替换为：

```html
{{- /* 主题色自定义按钮 - 五角星图标 */ -}}
<button id="color-toggle" accesskey="c" title="自定义主题色 (Alt + C)" aria-label="Choose theme color">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="18" viewBox="0 0 24 24"
        fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linecap="round"
        stroke-linejoin="round">
        <!-- 五角星图标 -->
        <polygon points="12,2 15,9 23,9 17,14 19,22 12,17 5,22 7,14 1,9 9,9" 
                 fill="currentColor" opacity="0.8"></polygon>
    </svg>
</button>
```

**效果**：简洁的实心五角星，悬停时放大

---

### 2. 🎨 调色板图标（经典）

**替换方法**：

```html
{{- /* 主题色自定义按钮 - 调色板图标 */ -}}
<button id="color-toggle" accesskey="c" title="自定义主题色 (Alt + C)" aria-label="Choose theme color">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="18" viewBox="0 0 24 24"
        fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
        stroke-linejoin="round">
        <!-- 调色板图标 -->
        <circle cx="12" cy="12" r="10"></circle>
        <circle cx="8" cy="10" r="1.5" fill="currentColor"></circle>
        <circle cx="12" cy="8" r="1.5" fill="currentColor"></circle>
        <circle cx="16" cy="10" r="1.5" fill="currentColor"></circle>
        <circle cx="10" cy="14" r="1.5" fill="currentColor"></circle>
        <circle cx="14" cy="14" r="1.5" fill="currentColor"></circle>
    </svg>
</button>
```

**效果**：经典的调色板造型，有多个小圆点

---

### 3. 💎 钻石图标（简约）

**替换方法**：

```html
{{- /* 主题色自定义按钮 - 钻石图标 */ -}}
<button id="color-toggle" accesskey="c" title="自定义主题色 (Alt + C)" aria-label="Choose theme color">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="18" viewBox="0 0 24 24"
        fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
        stroke-linejoin="round">
        <!-- 钻石图标 -->
        <polygon points="12,2 18,8 12,22 6,8" fill="none" stroke="currentColor"></polygon>
        <line x1="6" y1="8" x2="18" y2="8"></line>
        <line x1="12" y1="2" x2="12" y2="8"></line>
    </svg>
</button>
```

**效果**：简约的钻石形状

---

### 4. 🌈 彩虹图标（活泼）

**替换方法**：

```html
{{- /* 主题色自定义按钮 - 彩虹图标 */ -}}
<button id="color-toggle" accesskey="c" title="自定义主题色 (Alt + C)" aria-label="Choose theme color">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="18" viewBox="0 0 24 24"
        fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
        stroke-linejoin="round">
        <!-- 彩虹图标 -->
        <path d="M3 17 C 3 10, 21 10, 21 17" fill="none"></path>
        <path d="M5 17 C 5 12, 19 12, 19 17" fill="none"></path>
        <path d="M7 17 C 7 13.5, 17 13.5, 17 17" fill="none"></path>
    </svg>
</button>
```

**效果**：弧形的彩虹线条

---

### 5. 🌸 花朵图标（可爱）

**替换方法**：

```html
{{- /* 主题色自定义按钮 - 花朵图标 */ -}}
<button id="color-toggle" accesskey="c" title="自定义主题色 (Alt + C)" aria-label="Choose theme color">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="18" viewBox="0 0 24 24"
        fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
        stroke-linejoin="round">
        <!-- 花朵图标 -->
        <circle cx="12" cy="8" r="3" fill="none"></circle>
        <circle cx="8" cy="12" r="3" fill="none"></circle>
        <circle cx="16" cy="12" r="3" fill="none"></circle>
        <circle cx="10" cy="16" r="3" fill="none"></circle>
        <circle cx="14" cy="16" r="3" fill="none"></circle>
        <circle cx="12" cy="12" r="2" fill="currentColor"></circle>
    </svg>
</button>
```

**效果**：五瓣花朵造型

---

## 自定义悬停效果

### 旋转效果（当前）

```css
#color-toggle:hover svg {
  transform: rotate(15deg);
  transition: transform 0.3s ease;
}
```

### 弹跳效果

```css
#color-toggle:hover svg {
  animation: bounce 0.5s ease;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}
```

### 脉冲效果

```css
#color-toggle:hover svg {
  animation: pulse 0.6s ease;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.15); }
}
```

### 渐变色填充（五角星专用）

```css
#color-toggle:hover svg polygon {
  fill: url(#star-gradient);
}

/* 在 SVG 中添加渐变定义 */
<defs>
  <linearGradient id="star-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" style="stop-color:#FFD700;stop-opacity:1" />
    <stop offset="100%" style="stop-color:#FFA500;stop-opacity:1" />
  </linearGradient>
</defs>
```

---

## 修改步骤

1. **打开文件**

```bash
# 编辑器打开
code layouts/partials/header.html
```

2. **找到按钮代码**

搜索 `id="color-toggle"`（大约在第 77 行）

3. **替换 SVG**

复制上面你喜欢的图标代码，替换 `<svg>...</svg>` 部分

4. **保存并重启**

```bash
# 重启 Hugo 服务器
hugo server
```

5. **查看效果**

访问 http://localhost:1313/，查看新图标

---

## 推荐搭配

| 网站风格 | 推荐图标 |
|----------|----------|
| 可爱/个性博客 | 🍀 四叶草、🌸 花朵 |
| 简约/专业博客 | ⭐ 五角星、💎 钻石 |
| 设计/创意博客 | 🎨 调色板、🌈 彩虹 |
| 技术博客 | 💎 钻石、⭐ 五角星 |

---

## 注意事项

1. **viewBox 保持一致**：所有图标都使用 `viewBox="0 0 24 24"` 以确保大小一致
2. **width 和 height**：保持 `width="24" height="18"` 与日夜切换按钮一致
3. **stroke-width**：建议使用 `2` 以保持线条粗细统一
4. **fill 属性**：`fill="none"` 为线条图标，`fill="currentColor"` 为实心图标

---

## 效果对比

```
┌─────────────────────────────────────┐
│  Logo    [☾/☀] | [🍀] | [语言]  ← 当前（四叶草）
│  Logo    [☾/☀] | [⭐] | [语言]  ← 五角星
│  Logo    [☾/☀] | [🎨] | [语言]  ← 调色板
│  Logo    [☾/☀] | [💎] | [语言]  ← 钻石
│  Logo    [☾/☀] | [🌈] | [语言]  ← 彩虹
│  Logo    [☾/☀] | [🌸] | [语言]  ← 花朵
└─────────────────────────────────────┘
```

---

## 快速切换脚本

创建一个快速切换脚本（可选）：

**`scripts/change-icon.sh`**:

```bash
#!/bin/bash

echo "选择图标："
echo "1) 四叶草 (当前)"
echo "2) 五角星"
echo "3) 调色板"
echo "4) 钻石"
echo "5) 彩虹"
echo "6) 花朵"

read -p "输入选项 (1-6): " choice

case $choice in
  1) echo "已切换到四叶草" ;;
  2) echo "已切换到五角星" ;;
  # ... 添加替换逻辑
esac
```

---

> 💡 **推荐**：先用四叶草试试，如果觉得太可爱，可以换成五角星或钻石！

