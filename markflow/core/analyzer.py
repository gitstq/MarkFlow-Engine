"""
Document Analyzer Module
Analyzes Markdown documents and generates statistics
"""

import re
from pathlib import Path
from typing import Dict, Any, List, Tuple
from collections import Counter


class DocumentAnalyzer:
    """Analyze Markdown documents"""
    
    def __init__(self):
        self.word_reading_speed = 200  # words per minute
        self.chinese_char_speed = 400  # chinese chars per minute
    
    def analyze(self, content: str) -> Dict[str, Any]:
        """Analyze document content and return statistics"""
        stats = {
            "basic": self._analyze_basic(content),
            "structure": self._analyze_structure(content),
            "links": self._analyze_links(content),
            "code": self._analyze_code(content),
            "readability": self._analyze_readability(content),
        }
        return stats
    
    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a Markdown file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            stats = self.analyze(content)
            stats["file"] = {
                "name": file_path.name,
                "path": str(file_path),
                "size": file_path.stat().st_size,
            }
            return stats
        except Exception as e:
            return {"error": str(e)}
    
    def _analyze_basic(self, content: str) -> Dict[str, Any]:
        """Analyze basic statistics"""
        lines = content.split('\n')
        
        # Character counts
        total_chars = len(content)
        total_chars_no_spaces = len(content.replace(' ', '').replace('\n', ''))
        
        # Word counts
        words = re.findall(r'\b\w+\b', content)
        word_count = len(words)
        
        # Chinese character count
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', content))
        
        # Line counts
        total_lines = len(lines)
        non_empty_lines = len([l for l in lines if l.strip()])
        
        # Reading time estimation
        reading_time = self._estimate_reading_time(word_count, chinese_chars)
        
        return {
            "total_characters": total_chars,
            "characters_no_spaces": total_chars_no_spaces,
            "word_count": word_count,
            "chinese_characters": chinese_chars,
            "total_lines": total_lines,
            "non_empty_lines": non_empty_lines,
            "reading_time_minutes": reading_time,
        }
    
    def _analyze_structure(self, content: str) -> Dict[str, Any]:
        """Analyze document structure"""
        headers = re.findall(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE)
        
        header_counts = {}
        header_tree = []
        
        for level, title in headers:
            level_num = len(level)
            header_counts[f"h{level_num}"] = header_counts.get(f"h{level_num}", 0) + 1
            header_tree.append({
                "level": level_num,
                "title": title.strip()
            })
        
        # Count other elements
        lists = len(re.findall(r'^[\s]*[-*+]\s', content, re.MULTILINE))
        ordered_lists = len(re.findall(r'^[\s]*\d+\.\s', content, re.MULTILINE))
        blockquotes = len(re.findall(r'^>\s', content, re.MULTILINE))
        tables = len(re.findall(r'\|.*\|.*\|', content))
        horizontal_rules = len(re.findall(r'^[\s]*[-*_]{3,}[\s]*$', content, re.MULTILINE))
        
        return {
            "headers": header_counts,
            "header_tree": header_tree,
            "total_headers": len(headers),
            "unordered_lists": lists,
            "ordered_lists": ordered_lists,
            "blockquotes": blockquotes,
            "tables": tables,
            "horizontal_rules": horizontal_rules,
        }
    
    def _analyze_links(self, content: str) -> Dict[str, Any]:
        """Analyze links in document"""
        # Markdown links [text](url)
        md_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        
        # Bare URLs
        bare_urls = re.findall(r'https?://[^\s<>"\')\]]+', content)
        
        # Images
        images = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', content)
        
        # Categorize links
        internal_links = []
        external_links = []
        
        for text, url in md_links:
            if url.startswith('http'):
                external_links.append({"text": text, "url": url})
            else:
                internal_links.append({"text": text, "url": url})
        
        return {
            "markdown_links": len(md_links),
            "bare_urls": len(bare_urls),
            "images": len(images),
            "internal_links": internal_links,
            "external_links": external_links,
            "total_references": len(md_links) + len(bare_urls),
        }
    
    def _analyze_code(self, content: str) -> Dict[str, Any]:
        """Analyze code blocks"""
        # Fenced code blocks
        code_blocks = re.findall(r'```(\w+)?\n(.*?)```', content, re.DOTALL)
        
        # Inline code
        inline_code = re.findall(r'`([^`]+)`', content)
        
        # Count languages
        languages = Counter([block[0] or "text" for block in code_blocks])
        
        # Code lines
        total_code_lines = 0
        for _, code in code_blocks:
            total_code_lines += len(code.split('\n'))
        
        return {
            "code_blocks": len(code_blocks),
            "inline_code_snippets": len(inline_code),
            "languages_used": dict(languages),
            "total_code_lines": total_code_lines,
        }
    
    def _analyze_readability(self, content: str) -> Dict[str, Any]:
        """Analyze document readability"""
        # Remove code blocks for text analysis
        text_only = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
        text_only = re.sub(r'`[^`]+`', '', text_only)
        
        # Sentence count (approximate)
        sentences = re.split(r'[.!?。！？]+', text_only)
        sentence_count = len([s for s in sentences if s.strip()])
        
        # Word count
        words = re.findall(r'\b\w+\b', text_only)
        word_count = len(words)
        
        # Average sentence length
        avg_sentence_length = word_count / max(sentence_count, 1)
        
        # Paragraph count
        paragraphs = [p.strip() for p in text_only.split('\n\n') if p.strip()]
        paragraph_count = len(paragraphs)
        
        # Complexity score (simple heuristic)
        complexity = "simple"
        if avg_sentence_length > 20:
            complexity = "complex"
        elif avg_sentence_length > 15:
            complexity = "moderate"
        
        return {
            "sentence_count": sentence_count,
            "average_sentence_length": round(avg_sentence_length, 2),
            "paragraph_count": paragraph_count,
            "average_paragraph_length": round(word_count / max(paragraph_count, 1), 2),
            "complexity": complexity,
        }
    
    def _estimate_reading_time(self, word_count: int, chinese_chars: int) -> float:
        """Estimate reading time in minutes"""
        english_time = word_count / self.word_reading_speed
        chinese_time = chinese_chars / self.chinese_char_speed
        return round(english_time + chinese_time, 1)
    
    def generate_report(self, stats: Dict[str, Any]) -> str:
        """Generate a formatted analysis report"""
        if "error" in stats:
            return f"Error: {stats['error']}"
        
        basic = stats.get("basic", {})
        structure = stats.get("structure", {})
        links = stats.get("links", {})
        code = stats.get("code", {})
        readability = stats.get("readability", {})
        
        report = f"""# 📊 文档分析报告

## 📄 基本信息

| 指标 | 数值 |
|------|------|
| 总字符数 | {basic.get('total_characters', 0):,} |
| 字符数（不含空格） | {basic.get('characters_no_spaces', 0):,} |
| 单词数 | {basic.get('word_count', 0):,} |
| 中文字符 | {basic.get('chinese_characters', 0):,} |
| 总行数 | {basic.get('total_lines', 0):,} |
| 非空行数 | {basic.get('non_empty_lines', 0):,} |
| 预计阅读时间 | {basic.get('reading_time_minutes', 0)} 分钟 |

## 🏗️ 文档结构

| 元素类型 | 数量 |
|----------|------|
| 标题总数 | {structure.get('total_headers', 0)} |
| 无序列表 | {structure.get('unordered_lists', 0)} |
| 有序列表 | {structure.get('ordered_lists', 0)} |
| 引用块 | {structure.get('blockquotes', 0)} |
| 表格 | {structure.get('tables', 0)} |
| 分隔线 | {structure.get('horizontal_rules', 0)} |

### 标题层级分布

"""
        
        headers = structure.get("headers", {})
        for i in range(1, 7):
            count = headers.get(f"h{i}", 0)
            if count > 0:
                report += f"- H{i}: {count} 个\n"
        
        report += f"""
## 🔗 链接分析

| 指标 | 数值 |
|------|------|
| Markdown 链接 | {links.get('markdown_links', 0)} |
| 裸链接 | {links.get('bare_urls', 0)} |
| 图片 | {links.get('images', 0)} |
| 内部链接 | {len(links.get('internal_links', []))} |
| 外部链接 | {len(links.get('external_links', []))} |

## 💻 代码统计

| 指标 | 数值 |
|------|------|
| 代码块 | {code.get('code_blocks', 0)} |
| 行内代码 | {code.get('inline_code_snippets', 0)} |
| 代码总行数 | {code.get('total_code_lines', 0)} |

### 使用语言

"""
        
        languages = code.get("languages_used", {})
        for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True):
            report += f"- {lang}: {count} 个代码块\n"
        
        report += f"""
## 📖 可读性分析

| 指标 | 数值 |
|------|------|
| 句子数 | {readability.get('sentence_count', 0)} |
| 平均句长 | {readability.get('average_sentence_length', 0)} 词 |
| 段落数 | {readability.get('paragraph_count', 0)} |
| 平均段长 | {readability.get('average_paragraph_length', 0)} 词 |
| 复杂度 | {readability.get('complexity', 'unknown')} |

---
*报告由 MarkFlow 自动生成*
"""
        
        return report
