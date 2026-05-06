"""
Template Engine Module
Handles document templates and generation
"""

import re
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime


class TemplateEngine:
    """Generate documents from templates"""
    
    def __init__(self):
        self.templates = self._load_builtin_templates()
    
    def _load_builtin_templates(self) -> Dict[str, str]:
        """Load built-in document templates"""
        return {
            "meeting": """# {title}

## 📋 会议信息

- **日期**: {date}
- **时间**: {time}
- **地点**: {location}
- **主持人**: {host}
- **记录人**: {recorder}
- **参会人员**: {attendees}

## 📝 会议议程

{agenda}

## 💬 讨论内容

{discussions}

## ✅ 决议事项

{decisions}

## 🎯 行动计划

| 任务 | 负责人 | 截止日期 | 状态 |
|------|--------|----------|------|
{action_items}

## 📎 附件

{attachments}

---
*会议纪要由 MarkFlow 自动生成*
""",
            
            "api-doc": """# {title}

## 📘 接口概述

- **接口名称**: {api_name}
- **接口路径**: `{endpoint}`
- **请求方法**: {method}
- **接口版本**: {version}
- **创建日期**: {date}

## 📝 接口说明

{description}

## 🔐 认证方式

{auth_method}

## 📤 请求参数

### 路径参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
{path_params}

### 查询参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
{query_params}

### 请求体

```json
{request_body}
```

## 📥 响应参数

### 成功响应

```json
{success_response}
```

### 错误响应

```json
{error_response}
```

## ⚠️ 错误码

| 错误码 | 说明 |
|--------|------|
{error_codes}

## 💡 示例

### 请求示例

```bash
curl -X {method} "{endpoint}" \\
  -H "Authorization: Bearer {token}" \\
  -H "Content-Type: application/json" \\
  -d '{request_example}'
```

### 响应示例

```json
{response_example}
```

---
*API 文档由 MarkFlow 自动生成*
""",
            
            "readme": """# {project_name}

{description}

## ✨ 特性

{features}

## 🚀 快速开始

### 环境要求

{requirements}

### 安装

```bash
{install_command}
```

### 使用

```bash
{usage_example}
```

## 📖 文档

{documentation}

## 🤝 贡献

{contributing}

## 📄 许可证

{license}

---
*README 由 MarkFlow 自动生成*
""",
            
            "changelog": """# 更新日志

所有项目的显著变更都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [{version}] - {date}

### ✨ 新增

{added}

### 🐛 修复

{fixed}

### 🔄 变更

{changed}

### ⚠️ 弃用

{deprecated}

### 🗑️ 移除

{removed}

### 🔒 安全

{security}

---
*更新日志由 MarkFlow 自动生成*
""",
            
            "pr-template": """## 📋 PR 描述

{description}

## 🔄 变更类型

- [ ] ✨ 新功能 (New feature)
- [ ] 🐛 错误修复 (Bug fix)
- [ ] 📝 文档更新 (Documentation)
- [ ] 🎨 代码重构 (Refactoring)
- [ ] ⚡ 性能优化 (Performance)
- [ ] 🔧 配置变更 (Configuration)
- [ ] 🧪 测试 (Tests)

## 🧪 测试

{tests}

## 📸 截图

{screenshots}

## 🔗 相关 Issue

{related_issues}

## ✅ 检查清单

- [ ] 代码遵循项目编码规范
- [ ] 所有测试通过
- [ ] 文档已更新
- [ ] 变更已在本地测试

---
*PR 模板由 MarkFlow 自动生成*
""",
            
            "bug-report": """# 🐛 错误报告

## 问题描述

{description}

## 复现步骤

{reproduction_steps}

## 期望行为

{expected_behavior}

## 实际行为

{actual_behavior}

## 环境信息

- **操作系统**: {os}
- **软件版本**: {version}
- **相关配置**: {config}

## 📸 截图或日志

{logs}

## 🔗 相关链接

{links}

---
*错误报告由 MarkFlow 自动生成*
""",
            
            "blog-post": """---
title: {title}
date: {date}
author: {author}
tags: {tags}
categories: {categories}
---

# {title}

## 引言

{introduction}

## 正文

{content}

## 总结

{conclusion}

## 参考资料

{references}

---
*本文由 MarkFlow 自动生成*
"""
        }
    
    def list_templates(self) -> List[str]:
        """List available templates"""
        return list(self.templates.keys())
    
    def get_template(self, template_name: str) -> Optional[str]:
        """Get template content by name"""
        return self.templates.get(template_name)
    
    def render(self, template_name: str, variables: Dict[str, Any]) -> str:
        """Render a template with variables"""
        template = self.get_template(template_name)
        if not template:
            raise ValueError(f"Template '{template_name}' not found")
        
        # Add default variables
        now = datetime.now()
        defaults = {
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M"),
            "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
            "year": now.year,
            "month": now.month,
            "day": now.day,
        }
        defaults.update(variables)
        
        # Simple template substitution
        result = template
        for key, value in defaults.items():
            placeholder = "{" + key + "}"
            result = result.replace(placeholder, str(value))
        
        return result
    
    def create_document(self, template_name: str, output_path: Path, variables: Dict[str, Any]) -> bool:
        """Create a document from template"""
        try:
            content = self.render(template_name, variables)
            
            # Create parent directory if needed
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
        except Exception as e:
            print(f"Template creation error: {e}")
            return False
    
    def add_custom_template(self, name: str, content: str) -> bool:
        """Add a custom template"""
        try:
            self.templates[name] = content
            return True
        except Exception as e:
            print(f"Add template error: {e}")
            return False
