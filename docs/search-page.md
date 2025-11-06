# 搜索页面功能说明

> 本文档详细说明搜索页面的工作原理、tags 显示逻辑以及自定义方法。

---

## 📚 目录

- [搜索功能工作原理](#搜索功能工作原理)
- [Tags 显示逻辑](#tags-显示逻辑)
- [自定义搜索页面](#自定义搜索页面)
- [搜索配置优化](#搜索配置优化)

---

## 搜索功能工作原理

### 1. 技术栈

PaperMod 的搜索功能基于 **客户端搜索**，无需后端服务器：

```
用户访问 /search/
    ↓
加载 index.json（包含所有文章内容）
    ↓
Fuse.js 模糊搜索引擎
    ↓
实时显示搜索结果
```

**核心技术**：
- **Fuse.js**：轻量级模糊搜索库（~10KB）
- **index.json**：Hugo 生成的文章索引文件
- **fastsearch.js**：PaperMod 的搜索逻辑脚本

### 2. 搜索流程

```mermaid
graph LR
    A[用户输入] --> B[Fuse.js 分析]
    B --> C[匹配 index.json]
    C --> D[计算相似度]
    D --> E[返回结果列表]
```

### 3. index.json 内容

Hugo 会在构建时生成 `public/index.json`，包含所有文章的：

```json
[
  {
    "title": "文章标题",
    "content": "文章全文内容...",
    "permalink": "/notes/article-name/",
    "summary": "文章摘要"
  },
  ...
]
```

**配置位置**（`hugo.yaml`）：

```yaml
outputs:
  home:
    - HTML
    - RSS
    - JSON  # ← 生成 index.json
```

---

## Tags 显示逻辑

### 1. 实现方式

在 `layouts/_default/search.html` 中添加 Tags 云：

```html
{{- if site.Taxonomies.tags }}
<div class="tags-section">
    <h3 class="tags-title">标签云</h3>
    <div class="tags-cloud">
        {{- range $name, $taxonomy := site.Taxonomies.tags }}
        <a href="/tags/{{ $name }}/" class="tag-item">
            <span>{{ $name }}</span>
            <span>{{ $taxonomy.Count }}</span>
        </a>
        {{- end }}
    </div>
</div>
{{- end }}
```

### 2. Hugo 模板语法解释

| 代码 | 含义 |
|------|------|
| `site.Taxonomies.tags` | 获取所有 tags 分类 |
| `range $name, $taxonomy` | 遍历每个 tag |
| `$name` | Tag 名称（如 "Hugo"） |
| `$taxonomy.Count` | 该 tag 下的文章数量 |
| `site.GetPage` | 获取 tag 的页面对象 |
| `.Permalink` | Tag 页面的链接 |

### 3. Tags 数据来源

Tags 来自文章的 Front Matter：

```yaml
---
title: "我的文章"
tags: ["Hugo", "PaperMod", "教程"]  # ← 这里定义 tags
---
```

Hugo 会自动收集所有文章的 tags，并在 `site.Taxonomies.tags` 中统计。

---

## 自定义搜索页面

### 1. 文件结构

```
MyHomepage/
├── layouts/
│   └── _default/
│       └── search.html      ← 自定义搜索页面模板
├── content/
│   └── search.md            ← 搜索页面内容
└── hugo.yaml                ← 搜索配置
```

### 2. 当前搜索页面功能

✅ **已实现**：
- 实时搜索框
- 搜索结果列表
- Tags 云展示（带文章数量）
- Tags 点击跳转到分类页面
- 响应式设计（适配手机）

### 3. Tags 云样式特点

- **卡片式设计**：每个 tag 是一个独立的卡片
- **数量标签**：显示每个 tag 下有多少篇文章
- **悬停效果**：鼠标悬停时卡片上浮、变色
- **主题色**：使用橙色 `#E58F74` 作为主色调
- **自适应**：自动换行，适配不同屏幕尺寸

### 4. 修改 Tags 云样式

编辑 `layouts/_default/search.html`，找到 `<style>` 部分：

#### **4.1 修改 tag 卡片颜色**

```css
.tag-item {
    background: var(--entry);        /* 背景色（跟随主题） */
    border: 1px solid var(--border); /* 边框色 */
}

.tag-item:hover {
    background: var(--theme);        /* 悬停背景 */
    border-color: #E58F74;           /* 悬停边框（橙色） */
}
```

#### **4.2 修改数量标签样式**

```css
.tag-count {
    background: rgba(229, 143, 116, 0.15);  /* 浅橙色背景 */
    color: #E58F74;                          /* 橙色文字 */
}

.tag-item:hover .tag-count {
    background: #E58F74;  /* 悬停时变成纯橙色 */
    color: white;         /* 文字变白色 */
}
```

#### **4.3 修改 tag 大小（根据文章数量）**

如果想让文章多的 tag 显示得更大（类似"热力图"效果）：

```html
{{- range $name, $taxonomy := site.Taxonomies.tags }}
<a href="/tags/{{ $name }}/" class="tag-item" 
   style="font-size: {{ add 0.8 (mul 0.05 $taxonomy.Count) }}em;">
    <span>{{ $name }}</span>
    <span>{{ $taxonomy.Count }}</span>
</a>
{{- end }}
```

这样文章越多的 tag，字体会越大。

### 5. 添加 Tags 排序

#### **5.1 按字母排序**

```html
{{- range $name, $taxonomy := site.Taxonomies.tags }}
{{- $sortedTags := sort (slice $name) }}
<!-- 后续处理 -->
{{- end }}
```

#### **5.2 按文章数量排序（热门优先）**

```html
{{- $tags := slice }}
{{- range $name, $taxonomy := site.Taxonomies.tags }}
    {{- $tags = $tags | append (dict "name" $name "count" $taxonomy.Count) }}
{{- end }}

{{- range sort $tags "count" "desc" }}
<a href="/tags/{{ .name }}/" class="tag-item">
    <span>{{ .name }}</span>
    <span>{{ .count }}</span>
</a>
{{- end }}
```

---

## 搜索配置优化

### 1. 当前配置（hugo.yaml）

```yaml
params:
  fuseOpts:
    isCaseSensitive: false       # 不区分大小写
    shouldSort: true             # 按相关度排序
    location: 0                  # 匹配位置权重
    distance: 1000               # 搜索范围
    threshold: 0.4               # 相似度阈值（0-1，越小越严格）
    minMatchCharLength: 0        # 最小匹配字符长度
    keys: ["title", "permalink", "summary", "content"]  # 搜索字段
```

### 2. 配置参数详解

| 参数 | 含义 | 推荐值 | 说明 |
|------|------|--------|------|
| `isCaseSensitive` | 是否区分大小写 | `false` | 中文建议关闭 |
| `shouldSort` | 是否排序结果 | `true` | 按相关度排序 |
| `threshold` | 相似度阈值 | `0.3-0.5` | 越小越精确 |
| `distance` | 搜索距离 | `1000` | 匹配范围（字符） |
| `minMatchCharLength` | 最小匹配长度 | `2` | 避免单字符匹配 |
| `keys` | 搜索字段 | 见下方 | 决定搜索范围 |

### 3. 优化搜索字段（keys）

#### **当前配置**：

```yaml
keys: ["title", "permalink", "summary", "content"]
```

#### **推荐配置**（按权重）：

```yaml
keys: 
  - name: "title"      # 标题（权重最高）
    weight: 0.5
  - name: "tags"       # 标签
    weight: 0.3
  - name: "summary"    # 摘要
    weight: 0.2
  - name: "content"    # 正文（权重最低）
    weight: 0.1
```

这样搜索时会优先匹配标题，其次是 tags，最后才是正文。

### 4. 添加 Tags 到搜索索引

**编辑 `themes/PaperMod/layouts/_default/index.json`**（或在 `layouts/_default/` 创建覆盖）：

```json
{{- $.Scratch.Add "index" slice -}}
{{- range site.RegularPages -}}
    {{- if and (not .Params.searchHidden) (ne .Layout `archives`) (ne .Layout `search`) }}
    {{- $.Scratch.Add "index" (dict 
        "title" .Title 
        "content" .Plain 
        "permalink" .Permalink 
        "summary" .Summary
        "tags" .Params.tags
    ) -}}
    {{- end }}
{{- end -}}
{{- $.Scratch.Get "index" | jsonify -}}
```

然后更新 `hugo.yaml` 的 `fuseOpts.keys`：

```yaml
fuseOpts:
  keys: ["title", "tags", "summary", "content"]
```

这样就可以直接搜索 tags 了！

---

## 高级功能

### 1. 添加搜索历史

在 `layouts/_default/search.html` 中添加：

```javascript
<script>
// 保存搜索历史（使用 localStorage）
const searchInput = document.getElementById('searchInput');
const searchHistory = JSON.parse(localStorage.getItem('searchHistory') || '[]');

searchInput.addEventListener('input', function() {
  const query = this.value.trim();
  if (query && !searchHistory.includes(query)) {
    searchHistory.unshift(query);
    if (searchHistory.length > 10) searchHistory.pop();  // 最多保存 10 条
    localStorage.setItem('searchHistory', JSON.stringify(searchHistory));
  }
});

// 显示搜索历史
console.log('搜索历史：', searchHistory);
</script>
```

### 2. 添加搜索热词

在 Tags 云上方显示最热门的搜索词：

```html
<div class="hot-searches">
    <h4>热门标签</h4>
    {{- $topTags := first 5 (sort site.Taxonomies.tags "Count" "desc") }}
    {{- range $topTags }}
    <a href="{{ .Page.Permalink }}">{{ .Page.Title }}</a>
    {{- end }}
</div>
```

### 3. 添加搜索结果统计

修改 `fastsearch.js` 或在页面添加：

```javascript
<script>
// 监听搜索结果更新
const observer = new MutationObserver(() => {
  const results = document.querySelectorAll('#searchResults li');
  const count = results.length;
  console.log(`找到 ${count} 篇相关文章`);
});

observer.observe(document.getElementById('searchResults'), {
  childList: true
});
</script>
```

---

## 故障排查

### Q1: 搜索功能不工作？

**检查步骤**：

1. **确认 `index.json` 是否生成**

```bash
# 检查 public/index.json 是否存在
ls public/index.json
```

2. **确认 `outputs` 配置**

`hugo.yaml` 中必须包含：

```yaml
outputs:
  home:
    - HTML
    - RSS
    - JSON  # ← 必须有这个
```

3. **清理缓存重新构建**

```bash
hugo --gc --cleanDestinationDir
hugo server
```

### Q2: Tags 不显示？

**检查步骤**：

1. **确认文章有 tags**

```yaml
---
title: "测试"
tags: ["Hugo", "测试"]  # ← 必须有这个
---
```

2. **确认 taxonomies 配置**

`hugo.yaml` 中：

```yaml
taxonomies:
  tag: tags
  category: categories
```

3. **检查模板路径**

自定义模板必须放在 `layouts/_default/search.html`，而不是 `themes/` 下。

### Q3: 中文搜索不准确？

**解决方案**：

1. **降低 threshold**（提高精确度）

```yaml
fuseOpts:
  threshold: 0.3  # 从 0.4 降到 0.3
```

2. **调整搜索字段权重**

优先匹配标题和 tags，减少正文的权重。

3. **启用 CJK 支持**

```yaml
hasCJKLanguage: true
```

---

## 相关文档

- [Fuse.js 官方文档](https://fusejs.io/)
- [Hugo Taxonomies 文档](https://gohugo.io/content-management/taxonomies/)
- [PaperMod 搜索功能](https://github.com/adityatelange/hugo-PaperMod/wiki/Features#search-page)

---

## 效果预览

**搜索页面布局**：

```
┌─────────────────────────────────────────┐
│  🔍 Search                              │
│  ┌─────────────────────────────────┐   │
│  │ 搜索文章... ↵                    │   │
│  └─────────────────────────────────┘   │
│                                         │
│  📄 搜索结果列表                        │
│  • 文章标题 1                           │
│  • 文章标题 2                           │
│                                         │
│  ────────────────────────────────────  │
│                                         │
│  🏷️ 标签云                              │
│  ┌────────┐ ┌────────┐ ┌────────┐     │
│  │ Hugo 5 │ │ PaperMod│ │ 教程 3 │     │
│  └────────┘ └────────┘ └────────┘     │
│  ┌────────┐ ┌────────┐                │
│  │ CSS 2  │ │ 摄影 1 │                │
│  └────────┘ └────────┘                │
└─────────────────────────────────────────┘
```

---

## 总结

| 功能 | 实现方式 | 文件位置 |
|------|----------|----------|
| 搜索框 | Fuse.js | `themes/PaperMod/assets/js/fastsearch.js` |
| 搜索索引 | index.json | `layouts/_default/index.json` |
| Tags 显示 | Hugo 模板 | `layouts/_default/search.html` |
| 样式自定义 | CSS | `layouts/_default/search.html` (内联) |
| 搜索配置 | fuseOpts | `hugo.yaml` |

现在你的搜索页面既有实时搜索功能，又有完整的 Tags 云，方便读者快速找到相关内容！🎉

---

> 💡 **提示**：访问 `/search/` 查看效果，点击任意 tag 会跳转到该 tag 的所有文章列表！

