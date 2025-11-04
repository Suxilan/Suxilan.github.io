# 自定义配置指南

## 社交图标配置

### 位置
编辑 `hugo.yaml` 第 117-125 行

### 可用图标

PaperMod 支持的图标：
- **常用社交**: `github`, `gitlab`, `twitter`, `x`, `linkedin`, `facebook`, `instagram`
- **开发平台**: `stackoverflow`, `codepen`, `dribbble`, `behance`
- **摄影平台**: `500px`, `unsplash`, `flickr`
- **通讯**: `email`, `telegram`, `whatsapp`, `discord`, `qq`
- **其他**: `youtube`, `tiktok`, `reddit`, `rss`, `buymeacoffee`, `kofi`

### 添加图标

```yaml
socialIcons:
  - name: github              # 图标名称
    url: "你的链接"           # 链接地址
  - name: qq
    url: "QQ临时会话链接"
```

### QQ 临时会话链接格式
```
http://wpa.qq.com/msgrd?v=3&uin=你的QQ号&site=qq&menu=yes
```

### 删除图标
直接删除对应的几行即可

---

## 隐藏面包屑中的"主页"链接

### 位置
`assets/css/extended/custom.css` 第 134-153 行

### 原理
面包屑导航（breadcrumbs）会在文章页面显示"主页 » 分类 » 文章标题"这样的导航路径。通过 CSS 隐藏第一个"主页"链接。

### 实现方法
```css
/* 隐藏面包屑中的第一个链接（主页） */
.breadcrumbs a:first-child {
  display: none;
}

/* 隐藏第一个链接后的分隔符 */
.breadcrumbs a:first-child + span {
  display: none;
}
```

### 如果想恢复
删除或注释掉 `custom.css` 中相关的 CSS 规则即可。

---

## 背景图片和毛玻璃效果

### 1. 添加背景图片

**步骤**：
1. 准备一张背景图（建议 1920x1080px）
2. 放到 `static/images/background.jpg`
3. 刷新页面即可看到效果

**推荐图片**：
- 风景照（自然、天空、山川）
- 抽象纹理
- 低饱和度图片
- 避免太花哨的图片

### 2. 更换背景图

编辑 `assets/css/extended/custom.css` 第12行：

```css
background-image: url('/images/background.jpg'); 
/* 改成你的图片路径 */
```

### 3. 毛玻璃效果说明

**默认状态**：
- 背景图全屏清晰显示
- 内容区域完全透明，可以直接看到背景
- 按钮和社交图标有轻微毛玻璃效果

**鼠标悬停**：
- 悬停在头像、文字、按钮区域时：出现毛玻璃效果
- 移开鼠标时：恢复透明状态

### 4. 调整毛玻璃强度

编辑 `assets/css/extended/custom.css`：

```css
/* 第45-50行 - 悬停时的毛玻璃 */
.profile .profile_inner:hover {
  background: rgba(255, 255, 255, 0.3);  /* 透明度：0.2-0.5 */
  backdrop-filter: blur(25px);           /* 模糊度：15-35px */
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.3);
}
```

**参数说明**：
- `rgba` 最后一位：透明度（0完全透明，1完全不透明）
- `blur()` 数值：模糊程度（数字越大越模糊）
- 建议范围：透明度 0.2-0.5，模糊度 15-35px

### 5. 移除毛玻璃效果

如果不喜欢这个效果，删除 `assets/css/extended/custom.css` 即可。

### 6. 只要背景不要毛玻璃

在 `assets/css/extended/custom.css` 中删除第 45-58 行（`.profile .profile_inner:hover` 部分）。

### 7. 背景图片位置调整

如果背景图显示位置不理想，修改第 19 行：

```css
background-position: center;  /* 居中 */
/* 其他选项：top, bottom, left, right */
/* 或自定义：center 30%（水平居中，垂直30%位置）*/
```

---

## 关于页面

### 位置
`content/about.md`

### 当前内容
```markdown
Hi，我是 Suxilan。
```

### 扩展建议
可以添加：
- 个人简介
- 教育背景
- 兴趣爱好
- 联系方式
- 图片

---

## 常见自定义

### 修改首页标题和副标题

编辑 `hugo.yaml` 第 106-107 行：
```yaml
title: "My Wilderness"      # 主标题
subtitle: "记录、思考、探索"  # 副标题
```

### 修改网站名称

编辑 `hugo.yaml` 第 3 行：
```yaml
title: Suxilan's Blog
```

### 更换头像

将头像图片放到 `static/images/avatar.jpg`（建议 300x300px 以上）

### 修改主题颜色

目前使用 PaperMod 默认配色，如需自定义，在 `assets/css/extended/custom.css` 添加：

```css
:root {
    --theme: #fff;
    --entry: #fff;
    --primary: rgba(0, 0, 0, 0.88);
    --secondary: rgba(0, 0, 0, 0.56);
    --tertiary: rgba(0, 0, 0, 0.16);
    --content: rgba(0, 0, 0, 0.88);
}

.dark {
    --theme: #1d1e20;
    --entry: #2e2e33;
    --primary: rgba(255, 255, 255, 0.84);
    --secondary: rgba(255, 255, 255, 0.56);
    --tertiary: rgba(255, 255, 255, 0.16);
    --content: rgba(255, 255, 255, 0.74);
}
```

---

## Favicon（网站图标）配置

### 方法1：使用头像作为 Favicon（当前配置）

**配置文件**：
- `layouts/partials/extend_head.html` - 自定义头部
- `hugo.yaml` - 主配置文件

**效果**：
- 浏览器标签页显示头像
- 书签显示头像
- 苹果设备添加到主屏幕时显示头像

**使用的图片**：`static/images/avatar.jpg`

### 方法2：使用传统 Favicon.ico

如果想使用传统的 `.ico` 格式图标：

1. 制作 favicon.ico（16x16、32x32、48x48 多尺寸）
2. 放到 `static/favicon.ico`
3. 删除 `layouts/partials/extend_head.html`

**推荐工具**：
- [Favicon.io](https://favicon.io/) - 在线生成
- [RealFaviconGenerator](https://realfavicongenerator.net/) - 生成全套图标

---

## 故障排除

### 背景图不显示
1. 检查图片路径是否正确
2. 确认图片在 `static/images/` 目录
3. 刷新浏览器缓存（Ctrl+F5）

### 首页出现横向滚动条
已在 `custom.css` 中添加 `overflow-x: hidden` 解决。

### Favicon 不显示
1. 清空浏览器缓存（Ctrl+Shift+Delete）
2. 硬刷新（Ctrl+F5）
3. 检查 `static/images/avatar.jpg` 是否存在
4. 重启 Hugo 服务器

### 图标不显示
1. 检查图标名称是否正确（区分大小写）
2. 查看支持的图标列表
3. 确认 URL 格式正确

### "主页"/"Home"链接还在显示
1. 检查 `assets/css/extended/custom.css` 中第 134-153 行的CSS是否存在
2. 清空浏览器缓存（Ctrl+F5）
3. 重启 Hugo 服务器

### 毛玻璃效果不明显
1. 增大 `backdrop-filter` 的 `blur` 值
2. 调整 `background` 的透明度
3. 选择更清晰的背景图

