# 🚀 GitHub Pages 部署指南

## 📋 部署步骤

### 1. 创建 GitHub 仓库

1. 访问 https://github.com/new
2. 仓库名称：`Suxilan.github.io`（必须是这个格式）
3. 设置为 **Public**（公开）
4. **不要**勾选 "Add a README file"
5. 点击 "Create repository"

---

### 2. 本地提交代码

在项目根目录（`E:\Suxilan\MyHomepage`）打开终端：

```bash
# 初始化 Git（如果还没初始化）
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: Hugo PaperMod site"

# 设置主分支名称为 main
git branch -M main

# 关联远程仓库
git remote add origin https://github.com/Suxilan/Suxilan.github.io.git

# 推送代码
git push -u origin main
```

**注意**：如果遇到认证问题，需要使用 Personal Access Token (PAT) 代替密码。

---

### 3. 配置 GitHub Pages

1. 打开仓库页面：https://github.com/Suxilan/Suxilan.github.io
2. 点击 **Settings**（设置）
3. 左侧菜单找到 **Pages**
4. 在 "Build and deployment" 部分：
   - **Source**：选择 `GitHub Actions`
5. 保存

---

### 4. 触发部署

推送代码后会自动触发部署：

```bash
# 查看部署状态
# 访问：https://github.com/Suxilan/Suxilan.github.io/actions
```

等待 2-3 分钟，部署完成后访问：
**https://Suxilan.github.io**

---

## 🔄 日常更新流程

### 更新内容后重新部署

```bash
# 1. 添加更改
git add .

# 2. 提交更改
git commit -m "描述你的更改"

# 3. 推送到 GitHub
git push

# 4. 自动部署（无需手动操作）
```

### 手动触发部署

1. 访问：https://github.com/Suxilan/Suxilan.github.io/actions
2. 点击 "Deploy Hugo site to Pages"
3. 点击右侧 "Run workflow" → "Run workflow"

---

## 📝 Git 基础命令

### 查看状态
```bash
git status              # 查看当前状态
git log --oneline       # 查看提交历史
```

### 创建新文章
```bash
hugo new posts/my-article.md
# 编辑文章...
git add content/posts/my-article.md
git commit -m "Add new post: my article"
git push
```

### 更新配置
```bash
# 修改 hugo.yaml 或其他文件后
git add hugo.yaml
git commit -m "Update site configuration"
git push
```

### 添加图片
```bash
# 将图片放到 static/images/ 后
git add static/images/
git commit -m "Add new images"
git push
```

---

## ⚙️ GitHub Actions 工作流

### 工作流文件位置
`.github/workflows/deploy.yml`

### 工作流程
1. **触发**：推送到 main/master 分支
2. **构建**：
   - 安装 Hugo v0.128.0 Extended
   - 检出代码（包含子模块）
   - 运行 `hugo --gc --minify`
3. **部署**：
   - 上传到 GitHub Pages
   - 访问 https://Suxilan.github.io

### 查看构建日志
1. 访问：https://github.com/Suxilan/Suxilan.github.io/actions
2. 点击最新的工作流运行
3. 查看详细日志

---

## 🔧 常见问题

### Q1: 推送失败，提示认证错误？

**A**: 使用 Personal Access Token (PAT)

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token" → "Generate new token (classic)"
3. 勾选 `repo` 权限
4. 生成后复制 token
5. 推送时用 token 代替密码

或使用 SSH：
```bash
git remote set-url origin git@github.com:Suxilan/Suxilan.github.io.git
```

### Q2: 网站显示 404？

**A**: 检查：
1. GitHub Pages 是否启用（Settings → Pages）
2. Source 是否设置为 "GitHub Actions"
3. 工作流是否成功运行（Actions 页面）
4. 等待 5-10 分钟让 DNS 生效

### Q3: 主题样式没有显示？

**A**: 确保子模块正确：
```bash
git submodule update --init --recursive
git add .gitmodules themes/PaperMod
git commit -m "Update submodule"
git push
```

### Q4: 如何查看构建错误？

**A**: 
1. 访问 https://github.com/Suxilan/Suxilan.github.io/actions
2. 点击失败的工作流（红色 X）
3. 查看错误日志
4. 修复后重新推送

### Q5: 如何更新主题？

**A**:
```bash
cd themes/PaperMod
git pull origin master
cd ../..
git add themes/PaperMod
git commit -m "Update PaperMod theme"
git push
```

---

## 🌐 自定义域名（可选）

### 使用自己的域名

如果你有自己的域名（如 `suxilan.com`）：

1. 在 `static/` 目录创建 `CNAME` 文件：
   ```
   suxilan.com
   ```

2. 在域名提供商添加 DNS 记录：
   ```
   A    @    185.199.108.153
   A    @    185.199.109.153
   A    @    185.199.110.153
   A    @    185.199.111.153
   ```
   或者：
   ```
   CNAME    www    Suxilan.github.io
   ```

3. 推送 CNAME 文件：
   ```bash
   git add static/CNAME
   git commit -m "Add custom domain"
   git push
   ```

4. 在 GitHub 仓库 Settings → Pages 中设置自定义域名

---

## 📊 部署检查清单

部署前检查：

- [ ] `hugo.yaml` 中 baseURL 设置正确
- [ ] 所有文章的 `draft: false`
- [ ] 图片都已添加到 `static/images/`
- [ ] 主题子模块已正确添加
- [ ] `.github/workflows/deploy.yml` 文件存在
- [ ] `.gitignore` 包含 `public/` 和 `.hugo_build.lock`
- [ ] 本地测试通过：`hugo server`

---

## 🎯 快速命令参考

```bash
# 本地预览
hugo server -D

# 创建内容
hugo new posts/article.md

# Git 提交
git add .
git commit -m "Your message"
git push

# 更新主题
git submodule update --remote --merge

# 查看状态
git status
```

---

## 📚 相关资源

- [GitHub Pages 文档](https://docs.github.com/pages)
- [Hugo 部署文档](https://gohugo.io/hosting-and-deployment/hosting-on-github/)
- [Git 教程](https://git-scm.com/book/zh/v2)

---

**部署成功后访问**：https://Suxilan.github.io 🎉

