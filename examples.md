# 示例

本目录包含使用CHM-to-PDF的完整示例。

## 示例1：基本转换

### 文件结构
```
example1/
├── input/
│   ├── hhc.hhc
│   ├── file1.htm
│   └── file2.htm
└── run.sh
```

### 运行命令
```bash
python chm_to_pdf.py ./input ./output
```

### 输出结构
```
output/
├── 分类A/
│   ├── 文档1.pdf
│   └── 子分类/
│       └── 文档2.pdf
└── 分类B/
    └── 文档3.pdf
```

## 示例2：IT.chm完整转换

### 准备工作
```bash
# 1. 提取CHM
hh -decompile it IT.chm

# 2. 查看目录结构
ls it/
# 输出：hhc.hhc  [602个.htm文件]
```

### 执行转换
```bash
python chm_to_pdf.py ./it ./it_pdfs
```

### 预期输出
```
============================================================
CHM转PDF - 按目录结构生成
============================================================

1. 解析目录文件...
   ✓ 找到 737 个目录项

2. 构建文件夹结构...
   ✓ 构建了 587 个文件夹

3. 转换HTML为PDF...
找到 602 个HTML文件
使用reportlab进行转换...
开始按目录结构转换...

  进度: 50/602 (成功: 49, 失败: 0, 跳过: 0)
  进度: 100/602 (成功: 99, 失败: 0, 跳过: 0)
  ...
  进度: 600/602 (成功: 599, 失败: 0, 跳过: 0)

============================================================
转换完成！
============================================================
✓ 成功: 602
✗ 失败: 0
✓ 输出目录: ./it_pdfs
============================================================
```

### 结果验证
```bash
# 检查输出
ls it_pdfs/
# Aspect  DB  DevOps  Others  Platform  Server  Tools  WEB  ...

# 检查具体文件
ls it_pdfs/Aspect/BI*/
# BI.pdf  BI工具.pdf  主流报表工具比较之心得 - - BI商业智能.pdf

# 统计总数
find it_pdfs -name "*.pdf" | wc -l
# 602
```

## 示例3：自定义输出目录

```bash
# 指定输出目录
python chm_to_pdf.py ./extracted_html -o ./my_pdfs

# 或
python chm_to_pdf.py ./extracted_html ./my_pdfs
```

## 示例4：Windows批处理

创建 `convert.bat`：

```batch
@echo off
setlocal enabledelayedexpansion

set CHM_FILE=IT.chm
set HTML_DIR=extracted_html
set OUTPUT_DIR=it_pdfs

echo 正在提取CHM文件...
hh -decompile %HTML_DIR% %CHM_FILE%

echo 正在转换PDF...
python chm_to_pdf.py %HTML_DIR% %OUTPUT_DIR%

echo 转换完成！
pause
```

运行：
```bash
convert.bat
```

## 示例5：错误处理

### 测试错误情况

**1. 找不到HTML目录**
```bash
python chm_to_pdf.py ./nonexistent ./output
# 输出：错误：目录不存在 ./nonexistent
```

**2. 找不到hhc.hhc文件**
```bash
mkdir test_html
echo "some html" > test_html/file.htm
python chm_to_pdf.py ./test_html ./output
# 输出：错误：找不到目录文件 ./test_html/hhc.hhc
```

**3. 空HTML目录**
```bash
mkdir empty_html
touch empty_html/hhc.hhc  # 创建空的hhc.hhc
python chm_to_pdf.py ./empty_html ./output
# 输出：错误：在 ./empty_html 中未找到HTML文件
```

## 常见用法

### 转换并保存到特定位置
```bash
python chm_to_pdf.py D:\extracted\IT D:\output\IT_PDFs
```

### 使用相对路径
```bash
cd /path/to/project
python chm_to_pdf.py ./html_files ./pdf_output
```

### 在脚本中调用
```python
import subprocess
import sys

result = subprocess.run([
    sys.executable, 'chm_to_pdf.py',
    './html_input',
    './pdf_output'
], capture_output=True, text=True)

if result.returncode == 0:
    print("转换成功！")
else:
    print("转换失败！")
    print(result.stdout)
```

## 性能参考

| 测试场景 | 文件数 | 转换时间 | 平均速度 |
|---------|--------|---------|---------|
| IT.chm | 602 | ~2分钟 | 5文件/秒 |
| 小型CHM | 50 | ~15秒 | 3.3文件/秒 |
| 大型CHM | 1000+ | ~3.5分钟 | 4.7文件/秒 |

*测试环境：Windows 10, SSD, i7处理器*

---

更多信息详见 [QUICKSTART.md](../QUICKSTART.md)
