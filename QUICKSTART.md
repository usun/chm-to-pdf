# 快速开始指南

## 三步快速上手

### 步骤1：提取CHM文件

使用Windows自带的 `hh.exe` 或第三方工具（如CHM Explorer）将CHM文件解包：

**方法A：使用hh.exe（推荐）**

```bash
# Windows命令行执行
hh -decompile extracted_html your_file.chm
```

**方法B：使用其他工具**
- CHM Explorer
- Universal Extractor
- 7-Zip（部分版本支持）

提取完成后你会得到一个包含：
- 大量HTML文件（GUID命名，如 `b7bffe56-f5e1-4212-92d1-67a824306ba7.htm`）
- `hhc.hhc` 文件（目录结构定义文件）

### 步骤2：安装依赖

```bash
pip install -r requirements.txt
```

### 步骤3：执行转换

```bash
python chm_to_pdf.py /path/to/extracted_html /path/to/output_pdf
```

**示例：**
```bash
python chm_to_pdf.py D:\chm2pdf\it D:\chm2pdf\IT_PDFs
```

## 实际案例

以IT.chm为例，转换结果统计：

```
输入：
  - HTML文件：602个
  - 目录结构条目：737个

输出：
  - PDF文件：602个
  - 目录层级：25个顶级分类
  - 成功转换率：100%
```

最终目录结构示例：
```
IT_PDFs/
├── Aspect/（方面类）
│   ├── BI&DM&AI/
│   │   ├── BI/
│   │   │   ├── BI.pdf
│   │   │   ├── BI工具.pdf
│   │   │   └── 主流报表工具比较之心得 - - BI商业智能.pdf
│   │   └── 从BI到AI.pdf
│   ├── DFA敏感词查询的算法.pdf
│   └── OLAP/
│       ├── Druid...
│       ├── mondrian.pdf
│       └── Pentaho.pdf
├── DB/（数据库）
├── 技术与思考/（思考笔记）
├── 职场/（职场发展）
└── ...（其他分类）
```

## 命令行参数

```bash
python chm_to_pdf.py <html_dir> [output_dir]

参数：
  html_dir     - CHM提取后的HTML文件目录（必需）
  output_dir   - PDF输出目录（可选，默认为html_dir同级的output_pdf）

选项：
  -o, --output-dir  - 指定输出目录
```

## 常见问题

### Q1: 提取CHM时报错

**问题**：`Error: xxx.chm not found` 或提取失败

**解决**：
1. 确认CHM文件路径正确
2. 使用完整路径，避免中文路径
3. 尝试用其他工具（CHM Explorer）
4. 检查CHM文件是否损坏

### Q2: 转换时出现中文乱码

**问题**：PDF中文显示为乱码

**解决**：
1. 确保系统已安装SimSun字体（Windows通常预装）
2. Linux系统需要安装中文字体包：`sudo apt-get install fonts-noto-cjk`
3. 检查HTML文件编码是否正确（应为GB2312）
4. 尝试修改脚本中的编码优先级

### Q3: 找不到HTML文件

**问题**：转换时报 `错误：在 xxx 中未找到HTML文件`

**解决**：
1. 检查HTML目录是否存在
2. 确保目录中有 `.htm` 文件
3. 确认 `hhc.hhc` 文件在HTML目录中

### Q4: 目录结构不对

**问题**：PDF文件没有按预期的目录结构组织

**解决**：
1. 检查hhc.hhc文件是否存在（位置应在HTML目录根目录）
2. 用文本编辑器打开hhc.hhc，验证是否包含中文内容
3. 重新提取CHM文件

### Q5: 转换速度很慢

**问题**：处理600+文件花费较长时间

**说明**：这是正常的。性能取决于：
- 文件数量和大小
- 系统磁盘速度
- 需要生成的PDF数量

**优化建议**：
- 使用SSD存储
- 关闭杀毒软件（可能拖累磁盘I/O）

## 输出文件说明

每个PDF文件包含：
- **标题**：从HTML的 `<title>` 标签提取
- **正文**：HTML页面内容（限制2000段落）
- **编码**：使用UTF-8编码的PDF
- **字体**：SimSun中文字体（自动注册）

## 更多信息

详见 [README.md](../README.md)，包含：
- 完整的特性说明
- 详细的工作流程
- API调用流程
- 性能参数
- 故障排查指南
