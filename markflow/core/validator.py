"""
Document Validator Module
Validates Markdown documents for common issues
"""

import re
from pathlib import Path
from typing import Dict, Any, List, Tuple
from urllib.parse import urlparse


class DocumentValidator:
    """Validate Markdown documents"""
    
    def __init__(self):
        self.issues = []
        self.warnings = []
    
    def validate(self, content: str, file_path: Path = None) -> Dict[str, Any]:
        """Validate document content"""
        self.issues = []
        self.warnings = []
        
        # Run all validation checks
        self._check_links(content, file_path)
        self._check_images(content, file_path)
        self._check_headers(content)
        self._check_formatting(content)
        self._check_structure(content)
        self._check_accessibility(content)
        
        return {
            "valid": len(self.issues) == 0,
            "issues": self.issues,
            "warnings": self.warnings,
            "issue_count": len(self.issues),
            "warning_count": len(self.warnings),
        }
    
    def validate_file(self, file_path: Path) -> Dict[str, Any]:
        """Validate a Markdown file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            result = self.validate(content, file_path)
            result["file"] = str(file_path)
            return result
        except Exception as e:
            return {
                "valid": False,
                "issues": [{"type": "error", "message": str(e)}],
                "warnings": [],
                "issue_count": 1,
                "warning_count": 0,
                "file": str(file_path),
            }
    
    def _check_links(self, content: str, file_path: Path):
        """Check for link issues"""
        # Find all Markdown links
        links = re.findall(r'\[([^\]]*)\]\(([^)]+)\)', content)
        
        for text, url in links:
            # Empty link text
            if not text.strip():
                self.warnings.append({
                    "type": "warning",
                    "category": "link",
                    "message": f"Empty link text: [{text}]({url})",
                    "line": self._find_line(content, f"[{text}]({url})")
                })
            
            # Check for placeholder links
            if url in ["#", "", "http://", "https://"]:
                self.issues.append({
                    "type": "error",
                    "category": "link",
                    "message": f"Placeholder link: [{text}]({url})",
                    "line": self._find_line(content, f"[{text}]({url})")
                })
            
            # Check local file links
            if file_path and not url.startswith(('http://', 'https://', '#', 'mailto:')):
                resolved_path = file_path.parent / url
                if not resolved_path.exists() and not url.startswith('/'):
                    self.warnings.append({
                        "type": "warning",
                        "category": "link",
                        "message": f"Broken local link: [{text}]({url})",
                        "line": self._find_line(content, f"[{text}]({url})")
                    })
    
    def _check_images(self, content: str, file_path: Path):
        """Check for image issues"""
        # Find all images
        images = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', content)
        
        for alt, src in images:
            # Missing alt text
            if not alt.strip():
                self.warnings.append({
                    "type": "warning",
                    "category": "image",
                    "message": f"Missing alt text: ![]({src})",
                    "line": self._find_line(content, f"![]({src})")
                })
            
            # Check local image paths
            if file_path and not src.startswith(('http://', 'https://', '/')):
                resolved_path = file_path.parent / src
                if not resolved_path.exists():
                    self.issues.append({
                        "type": "error",
                        "category": "image",
                        "message": f"Missing image file: {src}",
                        "line": self._find_line(content, f"![{alt}]({src})")
                    })
    
    def _check_headers(self, content: str):
        """Check header structure"""
        lines = content.split('\n')
        prev_level = 0
        
        for i, line in enumerate(lines, 1):
            header_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if header_match:
                level = len(header_match.group(1))
                title = header_match.group(2).strip()
                
                # Check for skipped header levels
                if prev_level > 0 and level > prev_level + 1:
                    self.warnings.append({
                        "type": "warning",
                        "category": "header",
                        "message": f"Skipped header level: H{prev_level} to H{level}",
                        "line": i
                    })
                
                # Check for empty header
                if not title:
                    self.issues.append({
                        "type": "error",
                        "category": "header",
                        "message": "Empty header",
                        "line": i
                    })
                
                # Check for trailing punctuation in headers
                if title and title[-1] in '.,;:!?':
                    self.warnings.append({
                        "type": "warning",
                        "category": "header",
                        "message": f"Trailing punctuation in header: {title}",
                        "line": i
                    })
                
                prev_level = level
    
    def _check_formatting(self, content: str):
        """Check formatting issues"""
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Mixed list markers
            if re.match(r'^[\s]*[-*]\s', line) and re.match(r'^[\s]*\d+\.\s', line):
                self.warnings.append({
                    "type": "warning",
                    "category": "formatting",
                    "message": "Mixed list markers on same line",
                    "line": i
                })
            
            # Multiple consecutive blank lines
            if i > 1 and not line.strip() and not lines[i-2].strip():
                self.warnings.append({
                    "type": "warning",
                    "category": "formatting",
                    "message": "Multiple consecutive blank lines",
                    "line": i
                })
            
            # Trailing whitespace
            if line.rstrip() != line:
                self.warnings.append({
                    "type": "warning",
                    "category": "formatting",
                    "message": "Trailing whitespace",
                    "line": i
                })
            
            # Mixed emphasis markers
            if '*_' in line or '_*' in line:
                self.warnings.append({
                    "type": "warning",
                    "category": "formatting",
                    "message": "Mixed emphasis markers",
                    "line": i
                })
    
    def _check_structure(self, content: str):
        """Check document structure"""
        # Check for H1 (document should have one main title)
        h1_count = len(re.findall(r'^#\s+.+$', content, re.MULTILINE))
        
        if h1_count == 0:
            self.warnings.append({
                "type": "warning",
                "category": "structure",
                "message": "No H1 header found (document title)",
                "line": 0
            })
        elif h1_count > 1:
            self.warnings.append({
                "type": "warning",
                "category": "structure",
                "message": f"Multiple H1 headers found ({h1_count})",
                "line": 0
            })
        
        # Check for very long lines
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                self.warnings.append({
                    "type": "warning",
                    "category": "structure",
                    "message": f"Very long line ({len(line)} chars)",
                    "line": i
                })
    
    def _check_accessibility(self, content: str):
        """Check accessibility issues"""
        # Check for images without alt text (already checked in _check_images)
        # Check for tables without headers
        table_pattern = r'\|[^\n]+\|\n\|[-:\s|]+\|'
        tables = re.findall(table_pattern, content)
        
        # Check for bare URLs (should be linked text)
        bare_urls = re.findall(r'(?<![\[(])https?://[^\s<>"\')\]]+', content)
        for url in bare_urls:
            self.warnings.append({
                "type": "warning",
                "category": "accessibility",
                "message": f"Bare URL (should use linked text): {url[:50]}...",
                "line": self._find_line(content, url)
            })
    
    def _find_line(self, content: str, text: str) -> int:
        """Find line number of text in content"""
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if text in line:
                return i
        return 0
    
    def generate_report(self, result: Dict[str, Any]) -> str:
        """Generate validation report"""
        if "error" in result:
            return f"Validation Error: {result['error']}"
        
        file_info = result.get("file", "Unknown file")
        issues = result.get("issues", [])
        warnings = result.get("warnings", [])
        
        report = f"""# ✅ 文档验证报告

**文件**: {file_info}

## 📊 验证结果

| 类型 | 数量 |
|------|------|
| ❌ 错误 | {len(issues)} |
| ⚠️ 警告 | {len(warnings)} |
| **状态** | {'✅ 通过' if len(issues) == 0 else '❌ 未通过'} |

"""
        
        if issues:
            report += "## ❌ 错误\n\n"
            for issue in issues:
                line_info = f" (第 {issue.get('line', '?')} 行)" if issue.get('line') else ""
                report += f"- **{issue.get('category', 'general').upper()}**{line_info}: {issue.get('message', '')}\n"
            report += "\n"
        
        if warnings:
            report += "## ⚠️ 警告\n\n"
            for warning in warnings:
                line_info = f" (第 {warning.get('line', '?')} 行)" if warning.get('line') else ""
                report += f"- **{warning.get('category', 'general').upper()}**{line_info}: {warning.get('message', '')}\n"
            report += "\n"
        
        report += "---\n*报告由 MarkFlow 自动生成*\n"
        
        return report
