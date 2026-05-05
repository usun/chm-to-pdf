#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHM转PDF工具 - 将CHM帮助文档转换为按目录结构组织的PDF文件
使用reportlab作为PDF生成引擎，支持中文编码识别和完整的目录结构保留
"""

import os
import re
import glob
from pathlib import Path
import sys
import argparse
from html.parser import HTMLParser
import io

# 修复Windows编码问题
if sys.platform == 'win32':
    import codecs
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class TOCParser(HTMLParser):
    """解析CHM的目录结构"""
    def __init__(self):
        super().__init__()
        self.toc = []
        self.current_path = []
        self.depth = 0
        self.in_object = False
        self.current_object = {}

    def handle_starttag(self, tag, attrs):
        if tag == 'ul':
            self.depth += 1
        elif tag == 'object':
            attrs_dict = dict(attrs)
            if attrs_dict.get('type') == 'text/sitemap':
                self.in_object = True
                self.current_object = {}
        elif tag == 'param' and self.in_object:
            attrs_dict = dict(attrs)
            name = attrs_dict.get('name')
            value = attrs_dict.get('value')
            if name and value:
                self.current_object[name] = value

    def handle_endtag(self, tag):
        if tag == 'ul':
            self.depth = max(0, self.depth - 1)
        elif tag == 'object' and self.in_object:
            if self.current_object:
                entry = {
                    'depth': self.depth,
                    'name': self.current_object.get('Name', 'Untitled'),
                    'local': self.current_object.get('Local', ''),
                }
                self.toc.append(entry)
            self.in_object = False
            self.current_object = {}

def parse_hhc_file(hhc_path):
    """解析hhc文件获取目录结构"""
    try:
        # 优先使用GB2312（CHM最常用的编码），然后尝试其他编码
        encodings = ['gb2312', 'gbk', 'gb18030', 'utf-8']
        content = None
        for encoding in encodings:
            try:
                with open(hhc_path, 'r', encoding=encoding, errors='ignore') as f:
                    content = f.read()
                    if content:
                        break
            except:
                continue

        if not content:
            return []

        parser = TOCParser()
        parser.feed(content)
        return parser.toc
    except Exception as e:
        print(f"解析hhc文件失败: {e}")
        return []

def build_folder_structure(toc):
    """根据TOC构建文件路径映射 - 只为有local的条目生成完整的目录/文件路径"""
    structure = {}
    current_parents = {}  # 保存各深度的父级名称

    for entry in toc:
        depth = entry['depth']
        name = entry['name']
        local = entry['local']

        # 更新当前深度及以下的父级关系
        keys_to_remove = [d for d in current_parents.keys() if d > depth]
        for k in keys_to_remove:
            del current_parents[k]

        current_parents[depth] = name

        # 只为有local的条目构建完整路径
        if local:
            path_parts = []
            # 从depth=1开始遍历到当前depth，构建完整路径
            for d in sorted([x for x in current_parents.keys() if x <= depth]):
                if current_parents[d]:
                    clean_name = current_parents[d]
                    clean_name = clean_name.rstrip()
                    # 替换Windows不允许的字符
                    clean_name = re.sub(r'[<>:"|?*\\/\n\r\t]', '_', clean_name)
                    clean_name = re.sub(r'_+', '_', clean_name).strip('_')
                    if clean_name:
                        path_parts.append(clean_name)

            # 路径：目录/文件名（去掉.htm）.pdf
            if path_parts:
                # 倒数第一个是当前条目名（作为文件名）
                folder_path = '/'.join(path_parts[:-1]) if len(path_parts) > 1 else ''
                filename = path_parts[-1]
            else:
                folder_path = ''
                filename = local.replace('.htm', '').replace('.html', '')

            structure[local] = (folder_path, filename)

    return structure

def extract_text_from_html(html_file):
    """从HTML文件提取文本内容"""
    try:
        # 尝试GB2312编码，这是CHM文件常用的编码
        with open(html_file, 'r', encoding='gb2312', errors='ignore') as f:
            content = f.read()

        # 提取title
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
        title = title_match.group(1) if title_match else os.path.basename(html_file)

        # 移除script和style标签
        content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.IGNORECASE | re.DOTALL)
        content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.IGNORECASE | re.DOTALL)

        # 移除HTML标签
        content = re.sub(r'<[^>]+>', '\n', content)

        # 解码HTML实体
        content = re.sub(r'&nbsp;', ' ', content)
        content = re.sub(r'<br[^>]*>', '\n', content)
        content = re.sub(r'&lt;', '<', content)
        content = re.sub(r'&gt;', '>', content)
        content = re.sub(r'&amp;', '&', content)

        # 移除过多的空白
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        text = '\n'.join(lines)

        return title, text
    except Exception as e:
        print(f"提取文本失败 [{html_file}]: {e}")
        return os.path.basename(html_file), ""

def convert_html_to_pdf_with_reportlab(html_file, pdf_path):
    """使用reportlab将HTML转换为PDF"""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
        from reportlab.lib.enums import TA_LEFT, TA_CENTER
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.pdfbase import pdfmetrics

        # 注册中文字体（支持Windows系统）
        font_name = 'Helvetica'
        try:
            if sys.platform == 'win32':
                pdfmetrics.registerFont(TTFont('SimSun', 'C:\\Windows\\Fonts\\simsun.ttc'))
                font_name = 'SimSun'
            else:
                # Linux系统可能需要调整字体路径
                pdfmetrics.registerFont(TTFont('SimSun', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'))
                font_name = 'SimSun'
        except:
            pass

        title, text = extract_text_from_html(html_file)

        # 创建PDF文档
        doc = SimpleDocTemplate(pdf_path, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch,
                              leftMargin=0.5*inch, rightMargin=0.5*inch)
        story = []

        # 添加标题
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontName=font_name,
            fontSize=14,
            textColor='#000000',
            spaceAfter=12,
        )
        story.append(Paragraph(title[:100], title_style))
        story.append(Spacer(1, 0.2*inch))

        # 添加内容（按段落分割）
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontName=font_name,
            fontSize=10,
            leading=14,
        )

        paragraphs = text.split('\n')
        for para in paragraphs[:2000]:  # 限制段落数避免文件过大
            if para.strip():
                try:
                    story.append(Paragraph(para[:200], body_style))
                except:
                    pass

        # 构建PDF
        doc.build(story)
        return True

    except Exception as e:
        print(f"reportlab转换失败: {e}")
        return False

def convert_html_to_pdf_with_structure(html_dir, output_dir, folder_structure):
    """
    根据目录结构将HTML转换为PDF并放入对应文件夹
    """
    html_files = sorted(glob.glob(os.path.join(html_dir, '*.htm')))

    if not html_files:
        print(f"错误：在 {html_dir} 中未找到HTML文件")
        return False

    print(f"找到 {len(html_files)} 个HTML文件")
    print(f"使用reportlab进行转换...")
    print(f"开始按目录结构转换...\n")

    success_count = 0
    error_count = 0
    skipped_count = 0

    for i, html_file in enumerate(html_files, 1):
        filename = os.path.basename(html_file)

        # 查找该文件在目录中的位置
        if filename in folder_structure:
            folder_path, pdf_name = folder_structure[filename]
        else:
            # 找不到映射，放在Uncategorized目录
            folder_path = 'Uncategorized'
            pdf_name = os.path.splitext(filename)[0]

        # 创建输出路径
        if folder_path:
            pdf_folder = os.path.join(output_dir, folder_path)
        else:
            pdf_folder = output_dir

        os.makedirs(pdf_folder, exist_ok=True)

        # PDF文件名
        pdf_filename = pdf_name + '.pdf'
        pdf_path = os.path.join(pdf_folder, pdf_filename)

        if i % 50 == 0:
            print(f"  进度: {i}/{len(html_files)} (成功: {success_count}, 失败: {error_count}, 跳过: {skipped_count})")

        try:
            # 使用reportlab转换
            if convert_html_to_pdf_with_reportlab(html_file, pdf_path):
                success_count += 1
            else:
                error_count += 1

        except Exception as e:
            error_count += 1
            if error_count <= 5:
                print(f"  ✗ [{filename}]: {str(e)[:60]}")

    print(f"\n{'='*60}")
    print(f"转换完成！")
    print(f"{'='*60}")
    print(f"✓ 成功: {success_count}")
    print(f"✗ 失败: {error_count}")
    print(f"✓ 输出目录: {output_dir}")
    print(f"{'='*60}\n")

    return error_count < (len(html_files) * 0.1)  # 成功率>90%即认为成功


def main():
    parser = argparse.ArgumentParser(
        description='CHM转PDF工具 - 将CHM帮助文档转换为按目录结构组织的PDF文件',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例：
  python chm_to_pdf.py ./html ./output
  python chm_to_pdf.py /path/to/extracted/html /path/to/output --output-dir
        '''
    )

    parser.add_argument('html_dir', help='HTML文件所在目录（从CHM提取）')
    parser.add_argument('output_dir', nargs='?', help='PDF输出目录')
    parser.add_argument('--output-dir', '-o', dest='output_dir_opt', help='指定PDF输出目录')

    args = parser.parse_args()

    html_dir = args.html_dir
    output_dir = args.output_dir or args.output_dir_opt or os.path.join(os.path.dirname(html_dir), 'output_pdf')

    # 确定HHC文件路径
    hhc_file = os.path.join(html_dir, 'hhc.hhc')

    if not os.path.exists(html_dir):
        print(f"错误：目录不存在 {html_dir}")
        sys.exit(1)

    if not os.path.exists(hhc_file):
        print(f"错误：找不到目录文件 {hhc_file}")
        sys.exit(1)

    print(f"{'='*60}")
    print(f"CHM转PDF - 按目录结构生成")
    print(f"{'='*60}\n")

    print(f"1. 解析目录文件...")
    toc = parse_hhc_file(hhc_file)
    print(f"   ✓ 找到 {len(toc)} 个目录项\n")

    print(f"2. 构建文件夹结构...")
    folder_structure = build_folder_structure(toc)
    unique_folders = len(set([v[0] for v in folder_structure.values() if v[0]]))
    print(f"   ✓ 构建了 {unique_folders} 个文件夹\n")

    print(f"3. 转换HTML为PDF...")
    success = convert_html_to_pdf_with_structure(html_dir, output_dir, folder_structure)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
