# 数学公式渲染支持

> 本文档说明如何在 Hugo PaperMod 中使用数学公式（LaTeX）

---

## ✅ 已配置完成

数学公式支持已全局启用，使用 **MathJax 3** 作为渲染引擎。

---

## 📝 使用方法

### 1. 行内公式（Inline Math）

在文本中插入数学符号，有两种写法：

**方法 1：使用 `$...$`**
```markdown
这是一个行内公式 $E = mc^2$，爱因斯坦质能方程。
```
**效果**：这是一个行内公式 $E = mc^2$，爱因斯坦质能方程。

**方法 2：使用 `\(...\)`**
```markdown
圆的面积公式是 \(A = \pi r^2\)。
```
**效果**：圆的面积公式是 \(A = \pi r^2\)。

---

### 2. 块级公式（Display Math）

独立成行的公式，居中显示：

**方法 1：使用 `$$...$$`**
```markdown
麦克斯韦方程组：

$$
\begin{cases}
\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t} \\
\nabla \times \mathbf{H} = \mathbf{J} + \frac{\partial \mathbf{D}}{\partial t} \\
\nabla \cdot \mathbf{D} = \rho \\
\nabla \cdot \mathbf{B} = 0
\end{cases}
$$
```

**方法 2：使用 `\[...\]`**
```markdown
贝叶斯定理：

\[
P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}
\]
```

---

### 3. 常用公式示例

#### 矩阵
```markdown
$$
\begin{bmatrix}
a_{11} & a_{12} & a_{13} \\
a_{21} & a_{22} & a_{23} \\
a_{31} & a_{32} & a_{33}
\end{bmatrix}
$$
```

#### 分数和根号
```markdown
$$
f(x) = \frac{1}{\sqrt{2\pi\sigma^2}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}
$$
```

#### 求和与积分
```markdown
$$
\sum_{i=1}^{n} i = \frac{n(n+1)}{2}
\quad
\int_{0}^{\infty} e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
$$
```

#### 上下标
```markdown
行内：$x^2 + y^2 = r^2$，$H_2O$，$x_i^2$

块级：
$$
E = \sum_{i=1}^{n} \frac{1}{2} m_i v_i^2
$$
```

#### 希腊字母
```markdown
$$
\alpha, \beta, \gamma, \delta, \epsilon, \zeta, \eta, \theta \\
\Alpha, \Beta, \Gamma, \Delta, \Epsilon, \Zeta, \Eta, \Theta
$$
```

#### 特殊符号
```markdown
$$
\infty, \partial, \nabla, \pm, \times, \div, \leq, \geq, \neq \\
\in, \notin, \subset, \subseteq, \cup, \cap, \emptyset
$$
```

---

## 🎨 预定义宏

为了方便书写，已预定义以下宏：

| 宏 | 效果 | 说明 |
|----|------|------|
| `\RR` | $\mathbb{R}$ | 实数集 |
| `\NN` | $\mathbb{N}$ | 自然数集 |
| `\ZZ` | $\mathbb{Z}$ | 整数集 |
| `\QQ` | $\mathbb{Q}$ | 有理数集 |
| `\CC` | $\mathbb{C}$ | 复数集 |
| `\bm{x}` | $\boldsymbol{x}$ | 粗体符号 |
| `\vec{v}` | $\mathbf{v}$ | 向量 |

**示例**：
```markdown
设 $f: \RR \to \RR$，向量 $\vec{v} \in \RR^n$。
```

---

## ⚙️ 控制公式渲染

### 全局控制

在 `hugo.yaml` 中：

```yaml
params:
  math: true  # 全局启用
```

### 单篇文章控制

在文章的 Front Matter 中：

```yaml
---
title: "我的文章"
date: 2024-01-20
math: true  # 启用数学公式
---
```

或者关闭：

```yaml
---
title: "我的文章"
math: false  # 禁用数学公式（减少页面加载）
---
```

---

## 🐛 常见问题

### 1. 公式不渲染？

**检查清单**：
- ✅ `hugo.yaml` 中 `params.math: true` 已设置
- ✅ 文章 Front Matter 中没有 `math: false`
- ✅ 公式语法正确（检查括号匹配）
- ✅ 特殊字符已转义（如 `\` 需要写成 `\\`）

### 2. 美元符号 `$` 被识别为公式？

如果需要显示普通的美元符号，使用转义：
```markdown
这个商品价格是 \$100。
```

### 3. 公式中有代码块或下划线？

在代码块中，数学公式不会被渲染。如果需要在代码块中显示 LaTeX 代码，直接写即可：

````markdown
```latex
E = mc^2
```
````

---

## 📖 LaTeX 参考资料

### 在线工具
- [LaTeX Live Editor](https://latexeditor.lagrida.com/) - 实时预览
- [Detexify](http://detexify.kirelabs.org/classify.html) - 手写识别符号
- [MathJax 官方文档](https://docs.mathjax.org/en/latest/)

### 教程
- [LaTeX 数学公式速查](https://www.cmor-faculty.rice.edu/~heinken/latex/symbols.pdf)
- [Overleaf 数学公式教程](https://www.overleaf.com/learn/latex/Mathematical_expressions)

---

## 🔧 技术细节

### 使用的库
- **MathJax 3**：最新版本，性能优异
- **CDN**：jsDelivr（国内可访问）

### 支持的扩展
- `ams`：AMS 数学符号和环境
- `mathtools`：增强的数学工具
- `physics`：物理学符号包

### 渲染性能
- 异步加载，不阻塞页面
- 字体缓存优化
- 自动跳过代码块和预格式化文本

---

## ✨ 示例文章

创建 `content/notes/math-demo.md` 测试：

```markdown
---
title: "数学公式测试"
date: 2024-01-20
math: true
---

## 行内公式

欧拉公式 $e^{i\pi} + 1 = 0$ 被誉为最美公式。

## 块级公式

薛定谔方程：

$$
i\hbar\frac{\partial}{\partial t}\Psi(\mathbf{r},t) = \hat{H}\Psi(\mathbf{r},t)
$$

## 矩阵

$$
\begin{pmatrix}
1 & 2 & 3 \\
4 & 5 & 6 \\
7 & 8 & 9
\end{pmatrix}
$$
```

---

**🎉 现在你可以在笔记中愉快地使用数学公式了！**

