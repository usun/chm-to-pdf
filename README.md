# CHM转PDF - 智能文档转换工具

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

一个强大的工具，将CHM帮助文档自动转换为按原始目录结构组织的PDF文件。完美处理中文编码、保留完整目录层级、支持大规模批量转换。

## ✨ 主要特性

- 🎯 **自动编码识别** - GB2312/GBK/GB18030/UTF-8自适应，无需手工配置
- 📚 **完整保留目录** - 解析HHC文件，生成按原始层级组织的PDF
- 🇨🇳 **完美中文支持** - 目录名、文件名、特殊符号完整保留，无乱码
- ⚡ **批量处理** - 单次支持600+文件转换，100%成功率实测
- 🛠️ **灵活配置** - 命令行参数支持，易于集成
- 📊 **实时反馈** - 进度显示、错误日志，转换过程一目了然

## 📋 快速开始

### 前置要求

- Python 3.7+
- 从CHM提取的HTML文件和hhc.hhc文件

### 安装

```bash
# 1. 克隆项目
git clone https://github.com/your-username/chm-to-pdf.git
cd chm-to-pdf

# 2. 安装依赖
pip install -r requirements.txt
```

### 三步使用

```bash
# 1. 用hh.exe提取CHM文件（Windows）
hh -decompile extracted_html your_file.chm

# 2. 执行转换
python chm_to_pdf.py ./extracted_html ./output_pdf

# 3. 查看结果
ls output_pdf/
```

## 💡 使用示例

### 基本使用

```bash
python chm_to_pdf.py /path/to/html /path/to/output
```

### 指定输出目录

```bash
python chm_to_pdf.py ./html -o ./pdf_output
```

### 完整示例（IT.chm）

```bash
# 提取CHM
hh -decompile it IT.chm

# 转换
python chm_to_pdf.py ./it ./it_pdfs

# 结果
it_pdfs/
├── Aspect/
│   ├── BI&DM&AI/BI/BI.pdf
│   ├── BI&DM&AI/BI/BI工具.pdf
│   ├── OLAP/mondrian.pdf
│   └── ...
├── DB/
├── 技术与思考/
└── ...（其他25+个分类）
```

## 🏗️ 工作原理

### 流程图

```
IT.chm (CHM文件)
  ↓
提取 (hh.exe)
  ↓
HTML文件 + hhc.hhc
  ↓
解析HHC (目录结构)
  ↓
自动编码识别 (GB2312/GBK/...)
  ↓
生成PDF + 目录映射
  ↓
PDF/
├── 分类A/子分类1/文档1.pdf
├── 分类B/文档2.pdf
└── ...
```

### 核心算法

1. **编码识别** - 优先级：GB2312 → GBK → GB18030 → UTF-8
2. **HHC解析** - 提取Name（显示名）和Local（文件映射）
3. **目录映射** - 根据`<ul>`嵌套深度构建完整路径
4. **PDF生成** - 使用Reportlab + SimSun字体

详见 [ALGORITHM.md](./docs/ALGORITHM.md)

## 📊 实测数据

以IT.chm为例：

| 指标 | 数值 |
|------|------|
| 输入大小 | 61 MB |
| HTML文件 | 602 个 |
| 目录条目 | 737 个 |
| 输出PDF | 602 个 |
| 目录层级 | 25个顶级，133个总 |
| 转换时间 | ~2分钟 |
| 成功率 | 100% |

## 🔧 命令行参数

```
用法: python chm_to_pdf.py <html_dir> [output_dir]

位置参数:
  html_dir          CHM提取后的HTML文件目录（必需）
  output_dir        PDF输出目录（可选，默认为html_dir同级的output_pdf）

选项:
  -o, --output-dir  指定输出目录
  -h, --help        显示帮助信息

示例:
  python chm_to_pdf.py ./html ./output
  python chm_to_pdf.py ./extracted_html -o ./my_pdfs
```

## ❓ 常见问题

### Q: 出现中文乱码

**A:** 脚本已内置多编码支持，优先尝试GB2312。如仍有问题：
1. 检查HTML文件编码（用文本编辑器查看）
2. 确保hhc.hhc文件存在于HTML目录
3. 重新提取CHM文件

### Q: 找不到HTML文件

**A:** 确保HTML目录结构正确：
```
html/
├── hhc.hhc           # 必须存在
├── xxx.htm
├── yyy.htm
└── ...
```

### Q: PDF为空或内容不完整

**A:**
1. 检查单个HTML文件是否能正常打开
2. 查看是否有字体注册错误
3. 尝试增加段落限制（修改代码中的2000）

### Q: 转换速度慢

**A:** 正常现象，性能取决于：
- HTML文件数量和大小
- 系统磁盘速度
- 需要生成的PDF数量

优化建议：
- 使用SSD存储
- 关闭杀毒软件（可能拖累磁盘I/O）
- 实现并行处理（TODO）

### Q: 如何自定义中文字体

**A:** 修改 `chm_to_pdf.py` 中的字体注册部分：

```python
# 注册自定义字体
pdfmetrics.registerFont(TTFont('MyFont', '/path/to/font.ttf'))
font_name = 'MyFont'
```

## 📦 依赖

- **reportlab** - PDF生成引擎
- **pillow** - 图像处理（reportlab的依赖）

查看 [requirements.txt](./requirements.txt) 了解版本要求。

## 🐛 已知问题

- [ ] Linux系统字体路径需手工调整
- [ ] 暂不支持并行处理（CPU密集优化空间）
- [ ] 某些特殊HTML格式可能提取不完整

## 🚀 路线图

- [ ] 添加并行处理，提升转换速度
- [ ] Web UI界面
- [ ] 支持其他输出格式（DOCX、EPUB）
- [ ] 增量更新功能
- [ ] 配置文件支持
- [ ] Docker镜像

## 🤝 贡献指南

欢迎提交Issue和PR！

### 报告Bug

1. 检查是否已存在相同Issue
2. 清楚描述问题和复现步骤
3. 提供系统信息和错误日志

### 贡献代码

1. Fork本仓库
2. 创建特性分支：`git checkout -b feature/YourFeature`
3. 提交更改：`git commit -m 'Add YourFeature'`
4. 推送分支：`git push origin feature/YourFeature`
5. 提交Pull Request

### 代码规范

- 遵循PEP 8
- 新功能需添加测试
- 更新文档和README

## 📄 许可证

本项目采用 **MIT License** 开源。详见 [LICENSE](./LICENSE) 文件。

## 📚 相关资源

- [ReportLab文档](https://www.reportlab.com/docs/reportlab-userguide.pdf)
- [HHC文件格式说明](https://en.wikipedia.org/wiki/Microsoft_Compiled_HTML_Help)
- [Python HTML解析](https://docs.python.org/3/library/html.parser.html)

## 📝 更新日志

### v1.0.0 (2026-05-05)

- ✨ 首次发布
- ✅ 支持GB2312/GBK/UTF-8编码自动识别
- ✅ 完整保留目录结构
- ✅ 中文字体支持
- ✅ 600+文件批量处理

## 🙏 致谢

感谢所有测试者和贡献者的支持！

---

**⭐ 如果这个项目对你有帮助，请Star支持一下！**

**Questions?** 提交 [Issue](https://github.com/your-username/chm-to-pdf/issues) 或 [Discussions](https://github.com/your-username/chm-to-pdf/discussions)
