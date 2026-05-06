"""
MarkFlow - 轻量级 Markdown 文档工作流引擎
Lightweight Markdown Document Workflow Engine

A zero-dependency CLI tool for Markdown document processing,
conversion, templating, and workflow automation.
"""

__version__ = "1.0.0"
__author__ = "gitstq"
__license__ = "MIT"
__title__ = "MarkFlow"
__description__ = "轻量级 Markdown 文档工作流引擎"

from .core.converter import MarkdownConverter
from .core.template import TemplateEngine
from .core.analyzer import DocumentAnalyzer
from .core.validator import DocumentValidator

__all__ = [
    "MarkdownConverter",
    "TemplateEngine", 
    "DocumentAnalyzer",
    "DocumentValidator",
]
