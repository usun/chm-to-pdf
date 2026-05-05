# 贡献指南

感谢你对CHM-to-PDF项目的兴趣！我们欢迎各种形式的贡献。

## 贡献方式

### 1. 报告问题 (Issue)

如果你发现了Bug或有功能建议，欢迎提交Issue。

**提交Issue前，请检查：**
- 是否已存在相同或相似的Issue
- 问题描述是否清楚

**Issue模板：**

```markdown
## 问题描述
简洁描述你遇到的问题

## 复现步骤
1. 第一步
2. 第二步
3. ...

## 预期行为
应该发生什么

## 实际行为
实际发生了什么

## 环境信息
- Python版本：3.x.x
- 操作系统：Windows/Linux/macOS
- 其他相关信息

## 错误日志
（如果有）
```

### 2. 提交代码 (Pull Request)

**步骤：**

1. **Fork本仓库**
   ```bash
   # 在GitHub上点击Fork按钮
   ```

2. **克隆你的Fork**
   ```bash
   git clone https://github.com/your-username/chm-to-pdf.git
   cd chm-to-pdf
   ```

3. **创建特性分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或修复分支
   git checkout -b fix/your-bug-fix
   ```

4. **进行修改**
   - 修改代码
   - 添加/更新测试
   - 更新文档

5. **提交更改**
   ```bash
   git add .
   git commit -m "描述你的改动"
   ```

6. **推送到你的Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **在GitHub上创建Pull Request**
   - 标题：清楚描述改动内容
   - 描述：详细说明改动原因和实现方式
   - 链接相关Issue（如果有）

## 代码规范

### Python代码风格

- 遵循 **PEP 8** 风格指南
- 使用 4个空格缩进
- 行长不超过100个字符
- 使用有意义的变量名

**格式化工具：**
```bash
pip install black flake8
black chm_to_pdf.py
flake8 chm_to_pdf.py
```

### 提交信息格式

遵循 **Conventional Commits** 规范：

```
<type>: <subject>

<body>

<footer>
```

**Type类型：**
- `feat` - 新功能
- `fix` - Bug修复
- `docs` - 文档更新
- `style` - 代码风格改动（不影响功能）
- `refactor` - 代码重构
- `perf` - 性能优化
- `test` - 测试相关
- `chore` - 构建、依赖等杂项

**例子：**
```
feat: 添加并行处理支持

- 使用ThreadPoolExecutor并行处理HTML文件
- 新增--workers参数控制线程数
- 性能提升5倍

Closes #123
```

## PR审查过程

1. **代码审查** - 检查代码质量、风格、逻辑
2. **测试** - 验证改动是否有效
3. **文档** - 检查文档是否完整
4. **合并** - 审查通过后合并到main分支

## 开发指南

### 本地测试

```bash
# 安装依赖（开发版本）
pip install -r requirements.txt
pip install black flake8 pytest

# 运行测试
pytest tests/

# 格式化代码
black chm_to_pdf.py

# 检查代码风格
flake8 chm_to_pdf.py
```

### 添加新功能的检查清单

- [ ] 代码遵循PEP 8规范
- [ ] 添加了相关的函数文档字符串
- [ ] 新增的功能有对应的测试
- [ ] 更新了README.md（如果需要）
- [ ] 更新了QUICKSTART.md（如果涉及用法变化）
- [ ] 提交信息清晰描述改动

### 修复Bug的检查清单

- [ ] 问题描述清楚
- [ ] 修复方案合理
- [ ] 没有引入新Bug
- [ ] 添加了回归测试
- [ ] 代码风格一致

## 项目结构

```
chm-to-pdf/
├── chm_to_pdf.py      # 主程序
├── requirements.txt   # 依赖
├── README.md          # 项目说明
├── QUICKSTART.md      # 快速开始
├── CONTRIBUTING.md    # 贡献指南
├── LICENSE            # MIT许可证
├── tests/             # 测试文件
├── docs/              # 文档
└── examples/          # 使用示例
```

## 联系方式

- **GitHub Issues** - 问题和建议
- **GitHub Discussions** - 讨论和交流
- **邮件** - (可选)

## 致谢

感谢所有贡献者的支持！

---

**开始贡献：** 查看 [Good First Issues](https://github.com/your-username/chm-to-pdf/labels/good%20first%20issue) 找到合适的任务开始！
