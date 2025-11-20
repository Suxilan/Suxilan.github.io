# Hugo 项目维护工具集
# 在项目根目录运行: . .\hugo-tools.ps1

# 1. 修复 Markdown 加粗语法（增强版）
# 修复：内部空格、两个加粗之间缺少空格、代码块后紧跟加粗等问题
function Fix-Bold {
    Write-Host "🔧 修复 Markdown 加粗语法（增强版）..." -ForegroundColor Cyan
    python fix_bold_robust.py
    Write-Host ""
    Write-Host "💡 提示: 脚本已修复以下问题:" -ForegroundColor Yellow
    Write-Host "   - ** 文字 ** → **文字**" 
    Write-Host "   - **文字A**在**文字B** → **文字A** 在 **文字B**"
    Write-Host "   - 代码块后紧跟加粗 → 添加空行分隔"
    Write-Host ""
}

# 2. 启动 Hugo 开发服务器
function Start-Hugo {
    Write-Host "🚀 启动 Hugo 开发服务器..." -ForegroundColor Green
    hugo server -D
}

# 3. 构建生产版本
function Build-Hugo {
    Write-Host "📦 构建生产版本..." -ForegroundColor Yellow
    hugo --minify
}

# 4. 清理并重建
function Rebuild-Hugo {
    Write-Host "🧹 清理旧文件..." -ForegroundColor Magenta
    Remove-Item -Recurse -Force public, resources -ErrorAction SilentlyContinue
    Write-Host "📦 重新构建..." -ForegroundColor Yellow
    hugo --minify
}

# 5. 完整工作流：修复 + 启动服务器
function Start-Work {
    Fix-Bold
    Write-Host ""
    Start-Hugo
}

# 显示帮助信息
function Show-HugoHelp {
    Write-Host "==================================" -ForegroundColor Cyan
    Write-Host "   Hugo 项目维护工具" -ForegroundColor Cyan
    Write-Host "==================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "可用命令:" -ForegroundColor Yellow
    Write-Host "  Fix-Bold      - 修复 Markdown 加粗语法"
    Write-Host "  Start-Hugo    - 启动开发服务器"
    Write-Host "  Build-Hugo    - 构建生产版本"
    Write-Host "  Rebuild-Hugo  - 清理并重建"
    Write-Host "  Start-Work    - 修复语法 + 启动服务器"
    Write-Host ""
    Write-Host "快捷别名:" -ForegroundColor Yellow
    Write-Host "  fb   - Fix-Bold"
    Write-Host "  sh   - Start-Hugo"
    Write-Host "  bh   - Build-Hugo"
    Write-Host "  sw   - Start-Work"
    Write-Host ""
}

# 设置别名
Set-Alias -Name fb -Value Fix-Bold
Set-Alias -Name sh -Value Start-Hugo
Set-Alias -Name bh -Value Build-Hugo
Set-Alias -Name sw -Value Start-Work

# 加载时显示帮助
Show-HugoHelp
