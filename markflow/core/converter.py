"""
Markdown Converter Module
Handles conversion between Markdown and other formats
"""

import re
import html
from pathlib import Path
from typing import Optional, Dict, Any
from urllib.parse import urlparse


class MarkdownConverter:
    """Convert Markdown to various formats and vice versa"""
    
    def __init__(self):
        self.html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
            background: #fff;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #2c3e50;
            margin-top: 24px;
            margin-bottom: 16px;
            font-weight: 600;
        }}
        h1 {{ border-bottom: 2px solid #eaecef; padding-bottom: 10px; }}
        h2 {{ border-bottom: 1px solid #eaecef; padding-bottom: 8px; }}
        code {{
            background: #f6f8fa;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 0.9em;
        }}
        pre {{
            background: #f6f8fa;
            padding: 16px;
            border-radius: 6px;
            overflow-x: auto;
        }}
        pre code {{
            background: none;
            padding: 0;
        }}
        blockquote {{
            border-left: 4px solid #dfe2e5;
            margin: 0;
            padding-left: 16px;
            color: #6a737d;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 16px 0;
        }}
        th, td {{
            border: 1px solid #dfe2e5;
            padding: 8px 12px;
            text-align: left;
        }}
        th {{
            background: #f6f8fa;
            font-weight: 600;
        }}
        img {{
            max-width: 100%;
            height: auto;
        }}
        a {{
            color: #0366d6;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        ul, ol {{
            padding-left: 24px;
        }}
        hr {{
            border: none;
            border-top: 1px solid #e1e4e8;
            margin: 24px 0;
        }}
    </style>
</head>
<body>
{content}
</body>
</html>"""
    
    def md_to_html(self, markdown_text: str, title: str = "Document") -> str:
        """Convert Markdown to HTML"""
        html_content = self._parse_markdown(markdown_text)
        return self.html_template.format(title=title, content=html_content)
    
    def _parse_markdown(self, text: str) -> str:
        """Parse Markdown text to HTML"""
        # Escape HTML entities
        text = html.escape(text)
        
        # Code blocks (must be before inline code)
        text = self._convert_code_blocks(text)
        
        # Headers
        text = self._convert_headers(text)
        
        # Bold and italic
        text = self._convert_emphasis(text)
        
        # Links
        text = self._convert_links(text)
        
        # Images
        text = self._convert_images(text)
        
        # Lists
        text = self._convert_lists(text)
        
        # Blockquotes
        text = self._convert_blockquotes(text)
        
        # Tables
        text = self._convert_tables(text)
        
        # Horizontal rules
        text = self._convert_hr(text)
        
        # Paragraphs
        text = self._convert_paragraphs(text)
        
        return text
    
    def _convert_code_blocks(self, text: str) -> str:
        """Convert fenced code blocks"""
        pattern = r'```(\w+)?\n(.*?)```'
        
        def replace_code_block(match):
            lang = match.group(1) or ""
            code = match.group(2)
            # Unescape code content
            code = html.unescape(code)
            return f'<pre><code class="language-{lang}">{code}</code></pre>'
        
        return re.sub(pattern, replace_code_block, text, flags=re.DOTALL)
    
    def _convert_headers(self, text: str) -> str:
        """Convert Markdown headers"""
        # H1
        text = re.sub(r'^# (.+)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
        # H2
        text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
        # H3
        text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
        # H4
        text = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', text, flags=re.MULTILINE)
        # H5
        text = re.sub(r'^##### (.+)$', r'<h5>\1</h5>', text, flags=re.MULTILINE)
        # H6
        text = re.sub(r'^###### (.+)$', r'<h6>\1</h6>', text, flags=re.MULTILINE)
        return text
    
    def _convert_emphasis(self, text: str) -> str:
        """Convert bold and italic"""
        # Bold (**text**)
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        # Bold (__text__)
        text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)
        # Italic (*text*)
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        # Italic (_text_)
        text = re.sub(r'_(.+?)_', r'<em>\1</em>', text)
        return text
    
    def _convert_links(self, text: str) -> str:
        """Convert Markdown links"""
        # [text](url)
        return re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
    
    def _convert_images(self, text: str) -> str:
        """Convert Markdown images"""
        # ![alt](url)
        return re.sub(r'!\[(.*?)\]\((.+?)\)', r'<img src="\2" alt="\1">', text)
    
    def _convert_lists(self, text: str) -> str:
        """Convert Markdown lists"""
        lines = text.split('\n')
        result = []
        in_ul = False
        in_ol = False
        
        for line in lines:
            # Unordered list
            ul_match = re.match(r'^[\s]*[-*+] (.+)$', line)
            # Ordered list
            ol_match = re.match(r'^[\s]*\d+\. (.+)$', line)
            
            if ul_match:
                if not in_ul:
                    if in_ol:
                        result.append('</ol>')
                        in_ol = False
                    result.append('<ul>')
                    in_ul = True
                content = html.unescape(ul_match.group(1))
                result.append(f'<li>{content}</li>')
            elif ol_match:
                if not in_ol:
                    if in_ul:
                        result.append('</ul>')
                        in_ul = False
                    result.append('<ol>')
                    in_ol = True
                content = html.unescape(ol_match.group(1))
                result.append(f'<li>{content}</li>')
            else:
                if in_ul:
                    result.append('</ul>')
                    in_ul = False
                if in_ol:
                    result.append('</ol>')
                    in_ol = False
                result.append(line)
        
        if in_ul:
            result.append('</ul>')
        if in_ol:
            result.append('</ol>')
            
        return '\n'.join(result)
    
    def _convert_blockquotes(self, text: str) -> str:
        """Convert Markdown blockquotes"""
        lines = text.split('\n')
        result = []
        in_quote = False
        
        for line in lines:
            if line.startswith('> '):
                if not in_quote:
                    result.append('<blockquote>')
                    in_quote = True
                content = html.unescape(line[2:])
                result.append(content)
            else:
                if in_quote:
                    result.append('</blockquote>')
                    in_quote = False
                result.append(line)
        
        if in_quote:
            result.append('</blockquote>')
            
        return '\n'.join(result)
    
    def _convert_tables(self, text: str) -> str:
        """Convert Markdown tables"""
        lines = text.split('\n')
        result = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            # Check if this is a table row
            if '|' in line:
                # Check if next line is separator
                if i + 1 < len(lines) and re.match(r'^[\s|:|-]+$', lines[i + 1]):
                    # This is a table header
                    headers = [cell.strip() for cell in line.split('|') if cell.strip()]
                    result.append('<table>')
                    result.append('<thead><tr>' + ''.join(f'<th>{html.unescape(h)}</th>' for h in headers) + '</tr></thead>')
                    result.append('<tbody>')
                    i += 2  # Skip separator line
                    # Process table body
                    while i < len(lines) and '|' in lines[i]:
                        cells = [cell.strip() for cell in lines[i].split('|') if cell.strip()]
                        result.append('<tr>' + ''.join(f'<td>{html.unescape(c)}</td>' for c in cells) + '</tr>')
                        i += 1
                    result.append('</tbody></table>')
                else:
                    result.append(line)
                    i += 1
            else:
                result.append(line)
                i += 1
        
        return '\n'.join(result)
    
    def _convert_hr(self, text: str) -> str:
        """Convert horizontal rules"""
        text = re.sub(r'^[\s]*[-*_]{3,}[\s]*$', '<hr>', text, flags=re.MULTILINE)
        return text
    
    def _convert_paragraphs(self, text: str) -> str:
        """Convert text to paragraphs"""
        lines = text.split('\n')
        result = []
        paragraph = []
        
        for line in lines:
            stripped = line.strip()
            # Skip empty lines and block-level elements
            if (not stripped or 
                stripped.startswith('<h') or 
                stripped.startswith('<pre') or
                stripped.startswith('<ul') or
                stripped.startswith('<ol') or
                stripped.startswith('<blockquote') or
                stripped.startswith('<table') or
                stripped.startswith('<hr') or
                stripped.endswith('</h1>') or
                stripped.endswith('</h2>') or
                stripped.endswith('</h3>') or
                stripped.endswith('</h4>') or
                stripped.endswith('</h5>') or
                stripped.endswith('</h6>') or
                stripped.endswith('</pre>') or
                stripped.endswith('</ul>') or
                stripped.endswith('</ol>') or
                stripped.endswith('</blockquote>') or
                stripped.endswith('</table>') or
                stripped.startswith('<li>') or
                stripped.startswith('<tr>')):
                
                if paragraph:
                    result.append('<p>' + ' '.join(paragraph) + '</p>')
                    paragraph = []
                result.append(line)
            else:
                paragraph.append(html.unescape(stripped))
        
        if paragraph:
            result.append('<p>' + ' '.join(paragraph) + '</p>')
        
        return '\n'.join(result)
    
    def convert_file(self, input_path: Path, output_path: Path, output_format: str = "html") -> bool:
        """Convert a Markdown file to specified format"""
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            title = input_path.stem
            
            if output_format.lower() == "html":
                result = self.md_to_html(content, title)
            else:
                raise ValueError(f"Unsupported output format: {output_format}")
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result)
            
            return True
        except Exception as e:
            print(f"Conversion error: {e}")
            return False
