#!/usr/bin/env python3
"""
MarkFlow CLI - Main entry point
"""

import sys
import argparse
from pathlib import Path
from typing import Optional

from .core.converter import MarkdownConverter
from .core.template import TemplateEngine
from .core.analyzer import DocumentAnalyzer
from .core.validator import DocumentValidator
from .core.batch import BatchProcessor


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser"""
    parser = argparse.ArgumentParser(
        prog="markflow",
        description="📝 MarkFlow - 轻量级 Markdown 文档工作流引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  markflow convert input.md -o output.html
  markflow template meeting -o meeting.md --var title="项目会议"
  markflow analyze document.md
  markflow validate document.md
  markflow batch convert ./docs -o ./html
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # Convert command
    convert_parser = subparsers.add_parser("convert", help="转换 Markdown 文件")
    convert_parser.add_argument("input", help="输入文件路径")
    convert_parser.add_argument("-o", "--output", required=True, help="输出文件路径")
    convert_parser.add_argument("-f", "--format", default="html", 
                               choices=["html"], help="输出格式")
    
    # Template command
    template_parser = subparsers.add_parser("template", help="从模板创建文档")
    template_parser.add_argument("template", help="模板名称")
    template_parser.add_argument("-o", "--output", required=True, help="输出文件路径")
    template_parser.add_argument("--var", action="append", default=[],
                                help="模板变量 (格式: key=value)")
    template_parser.add_argument("--list", action="store_true", 
                                help="列出可用模板")
    
    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="分析 Markdown 文档")
    analyze_parser.add_argument("input", help="输入文件或目录")
    analyze_parser.add_argument("-o", "--output", help="输出报告路径")
    analyze_parser.add_argument("--batch", action="store_true",
                               help="批量分析目录中的所有文件")
    
    # Validate command
    validate_parser = subparsers.add_parser("validate", help="验证 Markdown 文档")
    validate_parser.add_argument("input", help="输入文件或目录")
    validate_parser.add_argument("-o", "--output", help="输出报告路径")
    
    # Batch command
    batch_parser = subparsers.add_parser("batch", help="批量处理")
    batch_subparsers = batch_parser.add_subparsers(dest="batch_command", help="批量操作")
    
    # Batch convert
    batch_convert = batch_subparsers.add_parser("convert", help="批量转换")
    batch_convert.add_argument("input", help="输入目录")
    batch_convert.add_argument("-o", "--output", required=True, help="输出目录")
    batch_convert.add_argument("-f", "--format", default="html", help="输出格式")
    
    # Batch rename
    batch_rename = batch_subparsers.add_parser("rename", help="批量重命名")
    batch_rename.add_argument("input", help="输入目录")
    batch_rename.add_argument("-p", "--pattern", required=True, help="匹配模式")
    batch_rename.add_argument("-r", "--replacement", required=True, help="替换内容")
    batch_rename.add_argument("--dry-run", action="store_true", help="试运行")
    
    # Batch format
    batch_format = batch_subparsers.add_parser("format", help="批量格式化")
    batch_format.add_argument("input", help="输入目录")
    batch_format.add_argument("--dry-run", action="store_true", help="试运行")
    
    # Batch merge
    batch_merge = batch_subparsers.add_parser("merge", help="批量合并")
    batch_merge.add_argument("input", help="输入目录")
    batch_merge.add_argument("-o", "--output", required=True, help="输出文件")
    batch_merge.add_argument("--no-toc", action="store_true", help="不生成目录")
    
    # Version
    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")
    
    return parser


def parse_vars(var_list: list) -> dict:
    """Parse variable strings into dict"""
    result = {}
    for var in var_list:
        if "=" in var:
            key, value = var.split("=", 1)
            result[key] = value
    return result


def handle_convert(args) -> int:
    """Handle convert command"""
    converter = MarkdownConverter()
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    if not input_path.exists():
        print(f"❌ 错误: 输入文件不存在: {input_path}")
        return 1
    
    print(f"🔄 正在转换: {input_path} → {output_path}")
    
    if converter.convert_file(input_path, output_path, args.format):
        print(f"✅ 转换成功: {output_path}")
        return 0
    else:
        print(f"❌ 转换失败")
        return 1


def handle_template(args) -> int:
    """Handle template command"""
    engine = TemplateEngine()
    
    if args.list:
        print("📋 可用模板:")
        for name in engine.list_templates():
            print(f"  - {name}")
        return 0
    
    variables = parse_vars(args.var)
    output_path = Path(args.output)
    
    print(f"📝 正在创建文档: {args.template} → {output_path}")
    
    if engine.create_document(args.template, output_path, variables):
        print(f"✅ 文档创建成功: {output_path}")
        return 0
    else:
        print(f"❌ 文档创建失败")
        return 1


def handle_analyze(args) -> int:
    """Handle analyze command"""
    analyzer = DocumentAnalyzer()
    input_path = Path(args.input)
    
    if args.batch and input_path.is_dir():
        processor = BatchProcessor()
        files = processor.find_files(input_path)
        results = processor.batch_analyze(files)
        report = processor.generate_report("批量分析", results)
    elif input_path.is_file():
        stats = analyzer.analyze_file(input_path)
        report = analyzer.generate_report(stats)
    else:
        print(f"❌ 错误: 无效的输入路径: {input_path}")
        return 1
    
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(report, encoding='utf-8')
        print(f"✅ 分析报告已保存: {output_path}")
    else:
        print(report)
    
    return 0


def handle_validate(args) -> int:
    """Handle validate command"""
    validator = DocumentValidator()
    input_path = Path(args.input)
    
    if input_path.is_file():
        result = validator.validate_file(input_path)
        report = validator.generate_report(result)
        
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(report, encoding='utf-8')
            print(f"✅ 验证报告已保存: {output_path}")
        else:
            print(report)
        
        return 0 if result.get("valid") else 1
    else:
        print(f"❌ 错误: 无效的输入文件: {input_path}")
        return 1


def handle_batch(args) -> int:
    """Handle batch command"""
    processor = BatchProcessor()
    input_path = Path(args.input)
    
    if not input_path.exists():
        print(f"❌ 错误: 输入路径不存在: {input_path}")
        return 1
    
    if args.batch_command == "convert":
        files = processor.find_files(input_path) if input_path.is_dir() else [input_path]
        output_dir = Path(args.output)
        results = processor.batch_convert(files, output_dir, args.format)
        report = processor.generate_report("批量转换", results)
        
    elif args.batch_command == "rename":
        files = processor.find_files(input_path) if input_path.is_dir() else [input_path]
        results = processor.batch_rename(files, args.pattern, args.replacement, args.dry_run)
        report = processor.generate_report("批量重命名", results)
        
    elif args.batch_command == "format":
        files = processor.find_files(input_path) if input_path.is_dir() else [input_path]
        results = processor.batch_format(files, args.dry_run)
        report = processor.generate_report("批量格式化", results)
        
    elif args.batch_command == "merge":
        files = processor.find_files(input_path) if input_path.is_dir() else [input_path]
        output_path = Path(args.output)
        results = processor.batch_merge(files, output_path, not args.no_toc)
        report = processor.generate_report("批量合并", results)
    else:
        print("❌ 错误: 请指定批量操作类型")
        return 1
    
    print(report)
    return 0


def main(args: Optional[list] = None) -> int:
    """Main entry point"""
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    
    if not parsed_args.command:
        parser.print_help()
        return 0
    
    try:
        if parsed_args.command == "convert":
            return handle_convert(parsed_args)
        elif parsed_args.command == "template":
            return handle_template(parsed_args)
        elif parsed_args.command == "analyze":
            return handle_analyze(parsed_args)
        elif parsed_args.command == "validate":
            return handle_validate(parsed_args)
        elif parsed_args.command == "batch":
            return handle_batch(parsed_args)
        else:
            parser.print_help()
            return 0
    except KeyboardInterrupt:
        print("\n⚠️ 操作已取消")
        return 130
    except Exception as e:
        print(f"❌ 错误: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
