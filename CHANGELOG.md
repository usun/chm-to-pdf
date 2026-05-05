# 更新日志

所有本项目的重要变更都会记录在此文件中。

## [1.0.0] - 2026-05-05

### 新增
- ✨ 首次发布CHM转PDF工具
- ✅ 支持GB2312/GBK/GB18030/UTF-8编码自动识别
- ✅ 完整保留原始CHM目录结构
- ✅ 中文字体支持（SimSun）
- ✅ 600+文件批量处理能力
- ✅ 命令行参数支持
- ✅ 进度显示和错误日志
- ✅ 跨平台支持（Windows/Linux/macOS）

### 特性
- **自动编码识别** - 优先级：GB2312 → GBK → GB18030 → UTF-8
- **HHC文件解析** - 完整提取目录结构和文件映射
- **智能路径构建** - 自动清理非法字符，保留中文
- **批量PDF生成** - 单次支持600+文件
- **完善的错误处理** - 详细的错误日志和提示

### 文档
- README.md - 完整的项目说明
- QUICKSTART.md - 快速开始指南
- CONTRIBUTING.md - 贡献指南

### 测试
- 实测IT.chm：602个HTML文件，100%成功率
- 支持超长文件名和特殊字符
- 中文目录和文件名正常显示

---

## 规划中的功能 (Roadmap)

### v1.1.0 (计划中)
- [ ] 并行处理支持（ThreadPoolExecutor）
- [ ] 配置文件支持（chm-to-pdf.conf）
- [ ] 增量更新功能
- [ ] 单元测试框架

### v1.2.0 (计划中)
- [ ] Web UI界面
- [ ] Docker镜像
- [ ] 输出格式扩展（DOCX、EPUB）

### v2.0.0 (计划中)
- [ ] 支持其他帮助格式（.hlp、HTML Help）
- [ ] 实时预览功能
- [ ] 批量操作队列

---

## 版本对应Python

- 1.0.0 - Python 3.7+

---

## 贡献者

感谢以下贡献者的支持：
- @YourName - 项目创建者

---

## 如何升级

```bash
# 从GitHub拉取最新版本
git pull origin main

# 或者重新安装
pip install -r requirements.txt
```

---

## 报告问题

如果你发现了Bug或有功能建议，请在 [GitHub Issues](https://github.com/your-username/chm-to-pdf/issues) 提交。
