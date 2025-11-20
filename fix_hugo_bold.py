#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hugo Goldmark 加粗渲染修复 - 终极鲁棒版本
修复 Goldmark 无法识别的加粗边界问题
"""

import re
from pathlib import Path
from typing import Tuple, List

class BoldFixer:
    def __init__(self):
        # 中文标点符号
        self.cjk_punctuation = r'[：？！。，、；）】」』]'
        # CJK 字符范围
        self.cjk_chars = r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]'
        # 引号（英文"和中文""）
        self.quotes = r'["\u201c\u201d]'
        
    def is_in_code_block(self, text: str, pos: int) -> bool:
        """检查位置是否在代码块内"""
        before = text[:pos]
        triple_backticks = before.count('```')
        return triple_backticks % 2 == 1
    
    def is_in_math_block(self, text: str, pos: int) -> bool:
        """检查位置是否在数学公式内"""
        before = text[:pos]
        double_dollars = before.count('$$')
        if double_dollars % 2 == 1:
            return True
        
        in_inline_math = False
        i = 0
        while i < len(before):
            if before[i] == '\\' and i + 1 < len(before) and before[i+1] == '$':
                i += 2
                continue
            if before[i] == '$':
                if i + 1 < len(before) and before[i+1] == '$':
                    i += 2
                    continue
                in_inline_math = not in_inline_math
            i += 1
        
        return in_inline_math
    
    def fix_quote_before_bold(self, text: str) -> Tuple[str, List[str]]:
        """修复：**"文字"** → ** "文字" ** (仅当引号紧贴**且内容不超过50字)"""
        changes = []
        # 只匹配紧贴的情况：**" (没有空格)，内容用.{1,50}限制长度
        pattern = r'\*\*(["\u201c\u201d])([^"\u201c\u201d\s][^"\u201c\u201d]{0,48}[^"\u201c\u201d\s])(["\u201c\u201d])\*\*'
        
        def add_space_around_quote(match):
            start_pos = match.start()
            
            if self.is_in_code_block(text, start_pos) or self.is_in_math_block(text, start_pos):
                return match.group(0)
            
            old_text = match.group(0)
            content = match.group(2)
            
            # 跳过超长内容(可能是误匹配)
            if len(content) > 50:
                return old_text
            
            quote_left = match.group(1)
            quote_right = match.group(3)
            new_text = f'** {quote_left}{content}{quote_right} **'
            changes.append(f'  {old_text} → {new_text}')
            return new_text
        
        result = re.sub(pattern, add_space_around_quote, text)
        return result, changes
    
    def fix_quote_partial_bold(self, text: str) -> Tuple[str, List[str]]:
        """修复：**"文字"**给 → ** "文字" **给 (仅当引号紧贴**且内容不超过50字)"""
        changes = []
        # 只匹配紧贴的情况：**"xxx"** (没有空格) 且后面紧跟非空格字符
        pattern = r'\*\*(["\u201c\u201d])([^"\u201c\u201d\s][^"\u201c\u201d]{0,48}[^"\u201c\u201d\s])(["\u201c\u201d])\*\*([^\s])'
        
        def add_space_after_quote(match):
            start_pos = match.start()
            
            if self.is_in_code_block(text, start_pos) or self.is_in_math_block(text, start_pos):
                return match.group(0)
            
            old_text = match.group(0)
            content = match.group(2)
            
            # 跳过超长内容(可能是误匹配)
            if len(content) > 50:
                return old_text
            
            quote_left = match.group(1)
            quote_right = match.group(3)
            next_char = match.group(4)
            new_text = f'** {quote_left}{content}{quote_right} **{next_char}'
            changes.append(f'  {old_text} → {new_text}')
            return new_text
        
        result = re.sub(pattern, add_space_after_quote, text)
        return result, changes
    
    def fix_punctuation_after_bold(self, text: str) -> Tuple[str, List[str]]:
        """修复：**文字：**紧跟非空格字符 → **文字：** 字符"""
        changes = []
        pattern = rf'(\*\*[^\*\n]+?{self.cjk_punctuation}\*\*)([^\s\n{self.cjk_punctuation}\*])'
        
        def add_space_if_needed(match):
            start_pos = match.start()
            
            if self.is_in_code_block(text, start_pos) or self.is_in_math_block(text, start_pos):
                return match.group(0)
            
            changes.append(f"  {match.group(1)}{match.group(2)} → {match.group(1)} {match.group(2)}")
            return f'{match.group(1)} {match.group(2)}'
        
        result = re.sub(pattern, add_space_if_needed, text)
        return result, changes
    
    def fix_colon_after_bold(self, text: str) -> Tuple[str, List[str]]:
        """修复：**并行性:** → **并行性：** (英文冒号改中文)"""
        changes = []
        # 匹配 **中文文字:** 格式（英文冒号在 ** 里面）
        pattern = r'\*\*([^*\n]*[\u4e00-\u9fff][^*\n]*):(\*\*)'
        
        def fix_colon(match):
            start_pos = match.start()
            
            if self.is_in_code_block(text, start_pos) or self.is_in_math_block(text, start_pos):
                return match.group(0)
            
            old_text = f"**{match.group(1)}:**"
            new_text = f"**{match.group(1)}：**"
            changes.append(f"  {old_text} → {new_text}")
            return new_text
        
        result = re.sub(pattern, fix_colon, text)
        return result, changes
    
    def process(self, text: str) -> Tuple[str, List[str]]:
        """处理所有修复"""
        all_changes = []
        
        # 1. 修复 **并行性:** → **并行性：**
        text, changes = self.fix_colon_after_bold(text)
        all_changes.extend(changes)
        
        # 2. 修复 **"引号"** → ** "引号" **
        text, changes = self.fix_quote_before_bold(text)
        all_changes.extend(changes)
        
        # 3. 修复 **"引号"**给** → ** "引号" **给**
        text, changes = self.fix_quote_partial_bold(text)
        all_changes.extend(changes)
        
        # 4. 修复 **文字：**紧跟字符
        text, changes = self.fix_punctuation_after_bold(text)
        all_changes.extend(changes)
        
        return text, all_changes


def process_file(file_path: Path, fixer: BoldFixer) -> Tuple[bool, List[str]]:
    """处理单个文件"""
    try:
        content = file_path.read_text(encoding='utf-8')
        fixed, changes = fixer.process(content)
        
        if fixed != content:
            file_path.write_text(fixed, encoding='utf-8')
            return True, changes
        return False, []
    
    except Exception as e:
        print(f"❌ 处理 {file_path.name} 时出错: {e}")
        return False, []


def main():
    notes_dir = Path('content/notes')
    
    if not notes_dir.exists():
        print(f"❌ 目录不存在: {notes_dir}")
        return 1
    
    md_files = sorted(notes_dir.glob('*.md'))
    
    if not md_files:
        print(f"⚠️  未找到 Markdown 文件")
        return 1
    
    print(f"🔍 扫描 {len(md_files)} 个文件...\n")
    
    fixer = BoldFixer()
    modified_count = 0
    total_changes = 0
    
    for md_file in md_files:
        changed, changes = process_file(md_file, fixer)
        if changed:
            print(f"✅ {md_file.name} ({len(changes)} 处修改)")
            for change in changes:
                print(change)
            print()
            modified_count += 1
            total_changes += len(changes)
        else:
            print(f"✓  {md_file.name} (无需修改)")
    
    print(f"\n{'='*70}")
    if modified_count > 0:
        print(f"✨ 修复了 {modified_count} 个文件，共 {total_changes} 处修改")
        print(f"\n💡 修复类型:")
        print(f"   1. **并行性:** → **并行性：** (英文冒号改中文)")
        print(f"   2. **\"引号\"** → ** \"引号\" ** (引号前后加空格)")
        print(f"   3. **\"引号\"**给** → ** \"引号\" **给** (引号后加空格)")
        print(f"   4. **文字：**字符 → **文字：** 字符 (标点后加空格)")
        print(f"\n💡 请运行 hugo server 验证效果")
    else:
        print(f"✓  所有文件都正确，无需修复")
    print(f"{'='*70}")
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
