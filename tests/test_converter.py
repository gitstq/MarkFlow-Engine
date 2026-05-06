"""Tests for Markdown Converter"""

import unittest
from pathlib import Path
import tempfile
import shutil

from markflow.core.converter import MarkdownConverter


class TestMarkdownConverter(unittest.TestCase):
    """Test MarkdownConverter class"""
    
    def setUp(self):
        self.converter = MarkdownConverter()
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.test_dir)
    
    def test_md_to_html_headers(self):
        """Test header conversion"""
        md = "# Heading 1\n## Heading 2\n### Heading 3"
        html = self.converter.md_to_html(md, "Test")
        
        self.assertIn("<h1>Heading 1</h1>", html)
        self.assertIn("<h2>Heading 2</h2>", html)
        self.assertIn("<h3>Heading 3</h3>", html)
    
    def test_md_to_html_emphasis(self):
        """Test bold and italic conversion"""
        md = "**bold** and *italic* and __bold2__ and _italic2_"
        html = self.converter.md_to_html(md, "Test")
        
        self.assertIn("<strong>bold</strong>", html)
        self.assertIn("<em>italic</em>", html)
        self.assertIn("<strong>bold2</strong>", html)
        self.assertIn("<em>italic2</em>", html)
    
    def test_md_to_html_links(self):
        """Test link conversion"""
        md = "[link text](https://example.com)"
        html = self.converter.md_to_html(md, "Test")
        
        self.assertIn('<a href="https://example.com">link text</a>', html)
    
    def test_md_to_html_images(self):
        """Test image conversion"""
        md = "![alt text](image.png)"
        html = self.converter.md_to_html(md, "Test")
        
        self.assertIn('<img src="image.png" alt="alt text">', html)
    
    def test_md_to_html_code(self):
        """Test code block conversion"""
        md = "```python\nprint('hello')\n```"
        html = self.converter.md_to_html(md, "Test")
        
        self.assertIn('<pre><code class="language-python">', html)
        self.assertIn("print('hello')", html)
    
    def test_md_to_html_lists(self):
        """Test list conversion"""
        md = "- item 1\n- item 2\n- item 3"
        html = self.converter.md_to_html(md, "Test")
        
        self.assertIn("<ul>", html)
        self.assertIn("<li>item 1</li>", html)
        self.assertIn("</ul>", html)
    
    def test_convert_file(self):
        """Test file conversion"""
        input_path = Path(self.test_dir) / "test.md"
        output_path = Path(self.test_dir) / "test.html"
        
        input_path.write_text("# Test\n\nHello World", encoding='utf-8')
        
        result = self.converter.convert_file(input_path, output_path, "html")
        
        self.assertTrue(result)
        self.assertTrue(output_path.exists())
        
        content = output_path.read_text(encoding='utf-8')
        self.assertIn("<h1>Test</h1>", content)


if __name__ == "__main__":
    unittest.main()
