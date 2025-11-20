import os
import re

def fix_markdown_bold(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 定义 CJK 字符和标点符号的范围
    # \u4e00-\u9fa5: 汉字
    # \u3000-\u303f: CJK 标点 (如 、 。)
    # \uff00-\uffef: 全角字符 (如 ！）)
    cjk_pattern = r'[\u4e00-\u9fa5\u3000-\u303f\uff00-\uffef]'

    # 策略 1: 在 CJK/标点 与 左侧 ** 之间添加空格
    # 匹配模式: (CJK字符)(**) -> \1 \2
    # 例如: "这是**粗体" -> "这是 **粗体"
    content = re.sub(f'({cjk_pattern})(\*\*)', r'\1 \2', content)

    # 策略 2: 在 右侧 ** 与 CJK/标点 之间添加空格
    # 匹配模式: (**)(CJK字符) -> \1 \2
    # 例如: "粗体**的" -> "粗体** 的"
    content = re.sub(f'(\*\*)({cjk_pattern})', r'\1 \2', content)

    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed: {file_path}")
        return True
    return False

def main():
    # 遍历 content 目录
    content_dir = os.path.join(os.getcwd(), 'content')
    count = 0
    
    print("开始扫描并修复 Markdown 粗体格式问题...")
    
    for root, dirs, files in os.walk(content_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                if fix_markdown_bold(file_path):
                    count += 1
    
    print(f"\n完成！共修复了 {count} 个文件。")
    print("现在 Hugo 应该能完美渲染所有粗体了。")

if __name__ == '__main__':
    main()
