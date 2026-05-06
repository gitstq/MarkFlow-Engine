# 📝 MarkFlow

<p align="center">
  <strong>轻量级 Markdown 文档工作流引擎</strong><br>
  <strong>Lightweight Markdown Document Workflow Engine</strong><br>
  <strong>輕量級 Markdown 文件工作流程引擎</strong>
</p>

<p align="center">
  <a href="#简体中文">简体中文</a> •
  <a href="#繁体中文">繁體中文</a> •
  <a href="#english">English</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/platform-cross--platform-lightgrey.svg" alt="Cross Platform">
  <img src="https://img.shields.io/badge/dependencies-zero-brightgreen.svg" alt="Zero Dependencies">
</p>

---

<a name="简体中文"></a>
## 🎉 项目介绍

**MarkFlow** 是一个轻量级、零依赖的 Markdown 文档工作流引擎 CLI 工具，专为开发者和内容创作者设计，帮助您高效处理 Markdown 文档的各种需求。

### 灵感来源

在日常开发和技术写作中，我们经常需要：
- 将 Markdown 转换为 HTML 分享
- 批量处理大量文档
- 检查文档质量和链接有效性
- 从模板快速创建标准化文档

现有工具要么过于复杂，要么依赖众多。MarkFlow 应运而生，提供简洁、高效的解决方案。

### 自研差异化亮点

✨ **零依赖设计** - 纯 Python 标准库实现，无需安装任何第三方包
⚡ **极速处理** - 本地处理，无需网络，保护隐私
🎯 **功能全面** - 转换、分析、验证、批量处理一站式解决
🔧 **高度可扩展** - 模块化设计，易于扩展新功能
🌐 **多语言支持** - 原生支持中英双语界面

---

## ✨ 核心特性

### 📄 文档转换
- **Markdown → HTML** - 高质量转换，内置精美样式
- 支持代码高亮、表格、列表等完整 Markdown 语法
- 生成的 HTML 可直接在浏览器中打开

### 🎨 模板系统
- **7种内置模板** - 会议纪要、API文档、README、更新日志、PR模板、Bug报告、博客文章
- **变量替换** - 支持动态变量，一键生成标准化文档
- **自定义模板** - 轻松添加自己的文档模板

### 📊 文档分析
- **全面统计** - 字符数、单词数、行数、阅读时间
- **结构分析** - 标题层级、列表、表格、代码块统计
- **可读性评估** - 自动评估文档复杂度
- **链接分析** - 内部/外部链接统计

### ✅ 文档验证
- **链接检查** - 检测失效的本地链接和图片
- **格式检查** - 标题层级、空白字符、格式规范
- **可访问性** - 图片 alt 属性、裸链接检测
- **结构检查** - 文档完整性验证

### 📦 批量处理
- **批量转换** - 整个目录一键转换
- **批量重命名** - 正则表达式批量重命名
- **批量格式化** - 统一文档格式规范
- **批量合并** - 多个文档合并为单一文件

---

## 🚀 快速开始

### 环境要求

- **Python**: 3.8 或更高版本
- **操作系统**: Windows / macOS / Linux

### 安装

```bash
# 方式1: 直接安装
pip install markflow

# 方式2: 从源码安装
git clone https://github.com/gitstq/MarkFlow-Engine.git
cd MarkFlow-Engine
pip install -e .
```

### 基本使用

```bash
# 查看帮助
markflow --help

# 转换 Markdown 为 HTML
markflow convert input.md -o output.html

# 从模板创建文档
markflow template meeting -o meeting.md --var title="项目会议" --var host="张三"

# 分析文档
markflow analyze document.md

# 验证文档
markflow validate document.md

# 批量转换
markflow batch convert ./docs -o ./html
```

---

## 📖 详细使用指南

### 文档转换

```bash
# 基本转换
markflow convert README.md -o README.html

# 指定输出格式
markflow convert doc.md -o doc.html -f html
```

### 模板使用

```bash
# 列出所有模板
markflow template --list

# 使用会议模板
markflow template meeting -o meeting.md \
  --var title="周会" \
  --var host="李四" \
  --var attendees="张三, 王五"

# 使用 API 文档模板
markflow template api-doc -o api.md \
  --var api_name="用户接口" \
  --var endpoint="/api/v1/users"
```

### 文档分析

```bash
# 分析单个文件
markflow analyze article.md

# 批量分析目录
markflow analyze ./docs --batch

# 导出报告
markflow analyze doc.md -o report.md
```

### 批量处理

```bash
# 批量转换
markflow batch convert ./markdown -o ./html -f html

# 批量重命名
markflow batch rename ./docs -p "old_" -r "new_"

# 批量格式化
markflow batch format ./docs

# 批量合并
markflow batch merge ./chapters -o book.md
```

---

## 💡 设计思路与迭代规划

### 技术选型原因

- **纯 Python 标准库** - 零依赖意味着零安装烦恼，开箱即用
- **模块化架构** - 每个功能独立模块，便于维护和扩展
- **CLI 优先** - 命令行工具更适合自动化和脚本集成

### 后续功能迭代计划

- [ ] PDF 导出支持
- [ ] 更多文档模板
- [ ] 插件系统
- [ ] 配置文件支持
- [ ] 实时预览功能

### 社区贡献方向

欢迎提交 Issue 和 PR！重点关注：
- 新模板贡献
- Bug 修复
- 性能优化
- 文档改进

---

## 📦 打包与部署

### 从源码运行

```bash
git clone https://github.com/gitstq/MarkFlow-Engine.git
cd MarkFlow-Engine
python -m markflow --help
```

### 打包发布

```bash
# 构建分发包
python setup.py sdist bdist_wheel

# 上传到 PyPI
twine upload dist/*
```

---

## 🤝 贡献指南

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

---

## 📄 开源协议

本项目采用 [MIT](LICENSE) 协议开源。

---

<a name="繁体中文"></a>
## 🎉 專案介紹（繁體中文）

**MarkFlow** 是一個輕量級、零依賴的 Markdown 文件工作流程引擎 CLI 工具，專為開發者和內容創作者設計。

### 核心特性

- 📄 **文件轉換** - Markdown 轉 HTML，內建精美樣式
- 🎨 **模板系統** - 7種內建模板，支援變數替換
- 📊 **文件分析** - 完整統計、結構分析、可讀性評估
- ✅ **文件驗證** - 連結檢查、格式驗證、可訪問性檢查
- 📦 **批次處理** - 批次轉換、重新命名、格式化、合併

### 快速開始

```bash
# 安裝
pip install markflow

# 轉換文件
markflow convert input.md -o output.html

# 使用模板
markflow template meeting -o meeting.md --var title="專案會議"

# 分析文件
markflow analyze document.md
```

---

<a name="english"></a>
## 🎉 Introduction (English)

**MarkFlow** is a lightweight, zero-dependency Markdown document workflow engine CLI tool designed for developers and content creators.

### Core Features

- 📄 **Document Conversion** - Markdown to HTML with beautiful built-in styles
- 🎨 **Template System** - 7 built-in templates with variable substitution
- 📊 **Document Analysis** - Comprehensive statistics, structure analysis, readability assessment
- ✅ **Document Validation** - Link checking, format validation, accessibility checks
- 📦 **Batch Processing** - Batch conversion, renaming, formatting, and merging

### Quick Start

```bash
# Install
pip install markflow

# Convert document
markflow convert input.md -o output.html

# Use template
markflow template meeting -o meeting.md --var title="Project Meeting"

# Analyze document
markflow analyze document.md
```

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/gitstq">gitstq</a>
</p>
