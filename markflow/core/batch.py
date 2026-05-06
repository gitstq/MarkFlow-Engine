"""
Batch Processor Module
Handles batch operations on multiple Markdown files
"""

import re
import shutil
from pathlib import Path
from typing import List, Dict, Any, Callable, Optional
from datetime import datetime


class BatchProcessor:
    """Process multiple Markdown files in batch"""
    
    def __init__(self):
        self.results = []
    
    def find_files(self, directory: Path, pattern: str = "*.md", recursive: bool = True) -> List[Path]:
        """Find all Markdown files in directory"""
        if recursive:
            return list(directory.rglob(pattern))
        else:
            return list(directory.glob(pattern))
    
    def batch_convert(self, files: List[Path], output_dir: Path, output_format: str = "html") -> Dict[str, Any]:
        """Batch convert files"""
        from .converter import MarkdownConverter
        
        converter = MarkdownConverter()
        results = {
            "total": len(files),
            "success": 0,
            "failed": 0,
            "errors": [],
            "converted": []
        }
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for file_path in files:
            try:
                output_path = output_dir / f"{file_path.stem}.{output_format}"
                if converter.convert_file(file_path, output_path, output_format):
                    results["success"] += 1
                    results["converted"].append(str(output_path))
                else:
                    results["failed"] += 1
                    results["errors"].append(f"Failed to convert: {file_path}")
            except Exception as e:
                results["failed"] += 1
                results["errors"].append(f"{file_path}: {str(e)}")
        
        return results
    
    def batch_rename(self, files: List[Path], pattern: str, replacement: str, dry_run: bool = False) -> Dict[str, Any]:
        """Batch rename files using regex pattern"""
        results = {
            "total": len(files),
            "renamed": 0,
            "skipped": 0,
            "errors": [],
            "operations": []
        }
        
        for file_path in files:
            try:
                new_name = re.sub(pattern, replacement, file_path.name)
                
                if new_name == file_path.name:
                    results["skipped"] += 1
                    continue
                
                new_path = file_path.parent / new_name
                
                operation = {
                    "from": str(file_path),
                    "to": str(new_path)
                }
                
                if not dry_run:
                    if new_path.exists():
                        results["errors"].append(f"Target exists: {new_path}")
                        continue
                    file_path.rename(new_path)
                
                results["renamed"] += 1
                results["operations"].append(operation)
                
            except Exception as e:
                results["errors"].append(f"{file_path}: {str(e)}")
        
        return results
    
    def batch_format(self, files: List[Path], dry_run: bool = False) -> Dict[str, Any]:
        """Batch format Markdown files"""
        results = {
            "total": len(files),
            "formatted": 0,
            "skipped": 0,
            "errors": []
        }
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                formatted = self._format_markdown(content)
                
                if formatted == content:
                    results["skipped"] += 1
                    continue
                
                if not dry_run:
                    # Backup original
                    backup_path = file_path.with_suffix('.md.backup')
                    shutil.copy2(file_path, backup_path)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(formatted)
                
                results["formatted"] += 1
                
            except Exception as e:
                results["errors"].append(f"{file_path}: {str(e)}")
        
        return results
    
    def batch_merge(self, files: List[Path], output_path: Path, add_toc: bool = True) -> Dict[str, Any]:
        """Merge multiple Markdown files"""
        results = {
            "total": len(files),
            "merged": 0,
            "errors": [],
            "output": str(output_path)
        }
        
        merged_content = []
        toc = []
        
        for i, file_path in enumerate(files):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Add file header
                header = f"## {file_path.stem}\n\n"
                toc.append(f"{i+1}. [{file_path.stem}](#{file_path.stem.lower().replace(' ', '-')})")
                
                merged_content.append(header + content)
                results["merged"] += 1
                
            except Exception as e:
                results["errors"].append(f"{file_path}: {str(e)}")
        
        if merged_content:
            final_content = ""
            
            if add_toc:
                final_content += "# 合并文档\n\n## 目录\n\n"
                final_content += "\n".join(toc)
                final_content += "\n\n---\n\n"
            
            final_content += "\n\n---\n\n".join(merged_content)
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(final_content)
        
        return results
    
    def batch_analyze(self, files: List[Path]) -> Dict[str, Any]:
        """Batch analyze files"""
        from .analyzer import DocumentAnalyzer
        
        analyzer = DocumentAnalyzer()
        results = {
            "total": len(files),
            "analyzed": 0,
            "errors": [],
            "summaries": []
        }
        
        total_stats = {
            "total_chars": 0,
            "total_words": 0,
            "total_lines": 0,
        }
        
        for file_path in files:
            try:
                stats = analyzer.analyze_file(file_path)
                
                if "error" in stats:
                    results["errors"].append(f"{file_path}: {stats['error']}")
                    continue
                
                basic = stats.get("basic", {})
                summary = {
                    "file": file_path.name,
                    "characters": basic.get("total_characters", 0),
                    "words": basic.get("word_count", 0),
                    "lines": basic.get("total_lines", 0),
                    "reading_time": basic.get("reading_time_minutes", 0),
                }
                
                results["summaries"].append(summary)
                
                total_stats["total_chars"] += summary["characters"]
                total_stats["total_words"] += summary["words"]
                total_stats["total_lines"] += summary["lines"]
                
                results["analyzed"] += 1
                
            except Exception as e:
                results["errors"].append(f"{file_path}: {str(e)}")
        
        results["totals"] = total_stats
        return results
    
    def _format_markdown(self, content: str) -> str:
        """Format Markdown content"""
        lines = content.split('\n')
        formatted = []
        
        prev_empty = False
        
        for line in lines:
            stripped = line.rstrip()
            
            # Remove trailing whitespace
            if stripped != line:
                line = stripped
            
            # Normalize multiple empty lines to single
            if not line:
                if prev_empty:
                    continue
                prev_empty = True
            else:
                prev_empty = False
            
            # Ensure space after header
            if re.match(r'^#{1,6}[^\s#]', line):
                line = re.sub(r'^(#{1,6})', r'\1 ', line)
            
            # Ensure space after list marker
            if re.match(r'^[\s]*[-*+][^\s]', line):
                line = re.sub(r'(^[\s]*[-*+])', r'\1 ', line)
            
            formatted.append(line)
        
        # Remove trailing empty lines
        while formatted and not formatted[-1]:
            formatted.pop()
        
        return '\n'.join(formatted)
    
    def generate_report(self, operation: str, results: Dict[str, Any]) -> str:
        """Generate batch operation report"""
        report = f"""# 📦 批量处理报告

**操作**: {operation}
**时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 📊 处理结果

| 指标 | 数值 |
|------|------|
| 总计 | {results.get('total', 0)} |
| 成功 | {results.get('success', results.get('renamed', results.get('formatted', results.get('merged', results.get('analyzed', 0)))))} |
| 跳过 | {results.get('skipped', 0)} |
| 失败 | {results.get('failed', 0)} |
| 错误数 | {len(results.get('errors', []))} |

"""
        
        if "totals" in results:
            totals = results["totals"]
            report += f"""## 📈 统计汇总

| 指标 | 数值 |
|------|------|
| 总字符数 | {totals.get('total_chars', 0):,} |
| 总单词数 | {totals.get('total_words', 0):,} |
| 总行数 | {totals.get('total_lines', 0):,} |

"""
        
        if results.get("errors"):
            report += "## ❌ 错误\n\n"
            for error in results["errors"][:10]:  # Show first 10 errors
                report += f"- {error}\n"
            if len(results["errors"]) > 10:
                report += f"- ... 还有 {len(results['errors']) - 10} 个错误\n"
            report += "\n"
        
        if results.get("operations"):
            report += "## 📝 操作记录\n\n"
            for op in results["operations"][:5]:  # Show first 5 operations
                report += f"- `{op['from']}` → `{op['to']}`\n"
            if len(results["operations"]) > 5:
                report += f"- ... 还有 {len(results['operations']) - 5} 个操作\n"
            report += "\n"
        
        if results.get("summaries"):
            report += "## 📄 文件详情\n\n"
            report += "| 文件 | 字符 | 单词 | 行数 | 阅读时间 |\n"
            report += "|------|------|------|------|----------|\n"
            for summary in results["summaries"][:10]:
                report += f"| {summary['file']} | {summary['characters']:,} | {summary['words']:,} | {summary['lines']:,} | {summary['reading_time']}m |\n"
            if len(results["summaries"]) > 10:
                report += f"| ... 还有 {len(results['summaries']) - 10} 个文件 | | | | |\n"
            report += "\n"
        
        report += "---\n*报告由 MarkFlow 自动生成*\n"
        
        return report
