# -*- coding: utf-8 -*-
import re
from .tokens import Token, OZDIL_KEYWORDS

# Pre-compiled regex patterns at module level for maximum performance (native C) and zero redundant allocations
_SPACES_RE = re.compile(r'[ \t]+')
_NUM_FLOAT_RE = re.compile(r'\d+\.\d+|\d+\.')
_NUM_INT_RE = re.compile(r'\d+')
_STRING_DBL_RE = re.compile(r'"[^"\\]*(?:\\.[^"\\]*)*"')
_STRING_SGL_RE = re.compile(r"'[^'\\]*(?:\\.[^'\\]*)*'")
_ID_RE = re.compile(r'[a-zA-ZçğıöşüÇĞİÖŞÜ_][a-zA-Z0-9çğıöşüÇĞİÖŞÜ_]*')
_OP_MULTI_RE = re.compile(r'==|!=|<=|>=|\*\*')

# Fast constant-time lookup for single character operators
_SINGLE_CHAR_OPS = {
    '+': True, '-': True, '*': True, '/': True, '%': True, '=': True,
    '<': True, '>': True, '(': True, ')': True, '[': True, ']': True,
    '{': True, '}': True, ':': True, ',': True, '.': True
}

def tokenize_line(line_str, lineno):
    tokens = []
    i = 0
    n = len(line_str)
    
    while i < n:
        c = line_str[i]
        
        # 1. Skip spaces/tabs
        if c == ' ' or c == '\t':
            m = _SPACES_RE.match(line_str, i)
            i = m.end() if m else i + 1
            continue
            
        # 2. Skip comment till end of line
        if c == '#':
            break
            
        # 3. Identifiers & Keywords
        if c.isalpha() or c in 'çğıöşüÇĞİÖŞÜ_':
            m = _ID_RE.match(line_str, i)
            if m:
                val = m.group(0)
                if val in OZDIL_KEYWORDS:
                    tokens.append(Token('KEYWORD', val, lineno, i + 1))
                else:
                    tokens.append(Token('ID', val, lineno, i + 1))
                i = m.end()
                continue
                
        # 4. Multi-char operators
        m = _OP_MULTI_RE.match(line_str, i)
        if m:
            tokens.append(Token('OP', m.group(0), lineno, i + 1))
            i = m.end()
            continue
            
        # 5. Single-char operators
        if c in _SINGLE_CHAR_OPS:
            tokens.append(Token('OP', c, lineno, i + 1))
            i += 1
            continue
            
        # 6. Numbers (Float / Int)
        if c.isdigit():
            # Match the entire numeric-like run to prevent partial tokenization of malformed numbers
            m_run = re.match(r'[0-9][a-zA-Z0-9._]*', line_str[i:])
            if m_run:
                run_str = m_run.group(0)
                # Check if it is a valid integer
                if re.match(r'^[0-9]+$', run_str):
                    tokens.append(Token('NUM_INT', run_str, lineno, i + 1))
                    i += len(run_str)
                    continue
                # Check if it is a valid float
                elif re.match(r'^[0-9]+\.[0-9]+$|^[0-9]+\.$', run_str):
                    tokens.append(Token('NUM_FLOAT', run_str, lineno, i + 1))
                    i += len(run_str)
                    continue
                else:
                    raise SyntaxError(f"Geçersiz sayı literal'ı: '{run_str}'")
                
        # 7. Strings with escape support
        if c == '"':
            m = _STRING_DBL_RE.match(line_str, i)
            if m:
                tokens.append(Token('STRING', m.group(0), lineno, i + 1))
                i = m.end()
                continue
            else:
                unclosed = line_str[i:]
                raise SyntaxError(f"Kapatılmamış metin ifadesi: '{unclosed}'")
                
        if c == "'":
            m = _STRING_SGL_RE.match(line_str, i)
            if m:
                tokens.append(Token('STRING', m.group(0), lineno, i + 1))
                i = m.end()
                continue
            else:
                unclosed = line_str[i:]
                raise SyntaxError(f"Kapatılmamış metin ifadesi: '{unclosed}'")
                
        raise SyntaxError(f"Geçersiz karakter: '{c}'")
        
    return tokens

def lex_ozdil(code_str):
    lines = code_str.splitlines()
    all_tokens = []
    indent_stack = [0]
    
    for idx, line in enumerate(lines):
        lineno = idx + 1
        
        # Strip trailing spaces
        stripped = line.rstrip()
        
        # Ignore empty lines or pure comment lines
        if not stripped.strip() or stripped.strip().startswith('#'):
            continue
            
        # Efficiently calculate indentation
        physical_indent_chars = 0
        indent_level = 0
        for char in line:
            if char == ' ':
                physical_indent_chars += 1
                indent_level += 1
            elif char == '\t':
                physical_indent_chars += 1
                indent_level += 4
            else:
                break
                
        line_tokens = tokenize_line(stripped[physical_indent_chars:], lineno)
        if not line_tokens:
            continue
            
        # Handle indents and dedents
        current_indent = indent_stack[-1]
        if indent_level > current_indent:
            indent_stack.append(indent_level)
            all_tokens.append(Token('INDENT', '    ', lineno, 1))
        elif indent_level < current_indent:
            while indent_level < indent_stack[-1]:
                indent_stack.pop()
                all_tokens.append(Token('DEDENT', '', lineno, 1))
            if indent_level != indent_stack[-1]:
                raise IndentationError("Girinti düzeyleri eşleşmiyor.")
                
        all_tokens.extend(line_tokens)
        all_tokens.append(Token('NEWLINE', '\n', lineno, len(line) + 1))
        
    # Clean up trailing indents
    while len(indent_stack) > 1:
        indent_stack.pop()
        all_tokens.append(Token('DEDENT', '', len(lines), 1))
        
    return all_tokens

def decode_string_literal(literal_str):
    """
    Decodes escape sequences in string literals in a standardized, secure manner.
    """
    if len(literal_str) < 2:
        return ""
    # Strip enclosing quotes
    quote_char = literal_str[0]
    if literal_str.endswith(quote_char):
        content = literal_str[1:-1]
    else:
        content = literal_str[1:]
        
    # Standardize escape decode logic
    escape_re = re.compile(r'\\(x[0-9a-fA-F]{2}|u[0-9a-fA-F]{4}|U[0-9a-fA-F]{8}|.)')
    
    def replace_escape(match):
        esc = match.group(1)
        if esc.startswith('x'):
            try:
                return chr(int(esc[1:], 16))
            except ValueError:
                return match.group(0)
        elif esc.startswith('u') or esc.startswith('U'):
            try:
                return chr(int(esc[1:], 16))
            except ValueError:
                return match.group(0)
        mapping = {
            'n': '\n',
            'r': '\r',
            't': '\t',
            'b': '\b',
            'f': '\f',
            'v': '\v',
            '\\': '\\',
            '"': '"',
            "'": "'",
        }
        return mapping.get(esc, esc)
        
    return escape_re.sub(replace_escape, content)

