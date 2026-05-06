"""Tests for Document Analyzer"""

import unittest
from pathlib import Path
import tempfile
import shutil

from markflow.core.analyzer import DocumentAnalyzer


class TestDocumentAnalyzer(unittest.TestCase):
    """Test DocumentAnalyzer class"""
    
    def setUp(self):
        self.analyzer = DocumentAnalyzer()
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.test_dir)
    
    def test_analyze_basic(self):
        """Test basic statistics"""
        content = "# Title\n\nThis is a test document with some words.\n\n- Item 1\n- Item 2"
        stats = self.analyzer.analyze(content)
        
        basic = stats["basic"]
        self.assertGreater(basic["total_characters"], 0)
        self.assertGreater(basic["word_count"], 0)
        self.assertGreater(basic["total_lines"], 0)
    
    def test_analyze_structure(self):
        """Test structure analysis"""
        content = "# H1\n## H2\n### H3\n\n- Item 1\n- Item 2"
        stats = self.analyzer.analyze(content)
        
        structure = stats["structure"]
        self.assertEqual(structure["total_headers"], 3)
        self.assertEqual(structure["unordered_lists"], 2)
    
    def test_analyze_links(self):
        """Test link analysis"""
        content = "[link](https://example.com) and ![image](img.png)"
        stats = self.analyzer.analyze(content)
        
        links = stats["links"]
        self.assertEqual(links["markdown_links"], 1)
        self.assertEqual(links["images"], 1)
    
    def test_analyze_code(self):
        """Test code analysis"""
        content = "```python\nprint('hello')\n```\n\n`inline code`"
        stats = self.analyzer.analyze(content)
        
        code = stats["code"]
        self.assertEqual(code["code_blocks"], 1)
        self.assertEqual(code["inline_code_snippets"], 1)
    
    def test_analyze_file(self):
        """Test file analysis"""
        file_path = Path(self.test_dir) / "test.md"
        file_path.write_text("# Test\n\nContent here.", encoding='utf-8')
        
        stats = self.analyzer.analyze_file(file_path)
        
        self.assertIn("file", stats)
        self.assertIn("basic", stats)
        self.assertEqual(stats["file"]["name"], "test.md")


if __name__ == "__main__":
    unittest.main()
