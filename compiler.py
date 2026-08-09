# -*- coding: utf-8 -*-
import sys
import json
import ast
import tokenize
from io import BytesIO, StringIO

MAPPING = {
    'yazdir': 'print',
    'yazdır': 'print',
    'eger': 'if',
    'eğer': 'if',
    'degilse_eger': 'elif',
    'değilse_eğer': 'elif',
    'degilse_eğer': 'elif',
    'değilse_eger': 'elif',
    'degilse': 'else',
    'değilse': 'else',
    'dongu': 'for',
    'döngü': 'for',
    'her': 'for',
    'iken': 'while',
    'fonksiyon': 'def',
    'islem': 'def',
    'işlem': 'def',
    'dondur': 'return',
    'dogru': 'True',
    'doğru': 'True',
    'yanlis': 'False',
    'yanlış': 'False',
    've': 'and',
    'veya': 'or',
    'degil': 'not',
    'değil': 'not',
    'icinde': 'in',
    'içinde': 'in',
    'sinif': 'class',
    'sınıf': 'class',
    'dene': 'try',
    'hata_yakala': 'except',
    # Extra helper keywords
    'aralik': 'range',
    'aralık': 'range',
    'uzunluk': 'len',
    'ekle': 'append',
    'tam_sayi': 'int',
    'tam_sayı': 'int',
    'metin': 'str',
    'ondalik': 'float',
    'ondalık': 'float',
    'liste': 'list',
    'sozluk': 'dict',
    'sözlük': 'dict',
    'olarak': 'as',
    'getir': 'import',
    'dur': 'break',
    'devam_et': 'continue',
    'yok': 'None',
    'bos': 'None',
    'boş': 'None',
}

def translate(code_str):
    # Ensure code starts with a clean string and handle empty/whitespace code
    if not code_str.strip():
        return ""
        
    try:
        # tokenize expects code to start with a newline or be fully valid, let's wrap and clean
        # We need to encode to bytes for tokenize
        bytes_io = BytesIO(code_str.encode('utf-8'))
        tokens = list(tokenize.tokenize(bytes_io.readline))
        new_tokens = []
        
        for tok in tokens:
            if tok.type == tokenize.NAME and tok.string in MAPPING:
                # Replace with the mapped Python keyword
                new_tokens.append((tok.type, MAPPING[tok.string], tok.start, tok.end, tok.line))
            else:
                new_tokens.append(tok)
                
        translated = tokenize.untokenize(new_tokens).decode('utf-8')
        return translated
    except Exception as tok_err:
        # Fallback to safe regex-based replacement on word boundaries
        import re
        # Sort keys descending by length to prevent partial matches (e.g. 'degilse_eger' replacing 'degilse')
        sorted_keys = sorted(MAPPING.keys(), key=len, reverse=True)
        lines = code_str.splitlines()
        translated_lines = []
        for line in lines:
            # Skip comments or handle them carefully, but regex with \b is safe enough for fallback
            temp_line = line
            # We want to replace outside of strings if possible, but regex boundary replacement is a solid fallback
            for k in sorted_keys:
                # \b matches word boundaries
                temp_line = re.sub(r'\b' + re.escape(k) + r'\b', MAPPING[k], temp_line)
            translated_lines.append(temp_line)
        return '\n'.join(translated_lines)

def ast_to_dict(node):
    if node is None:
        return None
    
    result = {
        "type": node.__class__.__name__
    }
    
    if hasattr(node, 'lineno'):
        result['lineno'] = node.lineno
        
    for field, value in ast.iter_fields(node):
        if isinstance(value, list):
            result[field] = [ast_to_dict(item) if isinstance(item, ast.AST) else str(item) for item in value]
        elif isinstance(value, ast.AST):
            result[field] = ast_to_dict(value)
        else:
            if value is True:
                result[field] = True
            elif value is False:
                result[field] = False
            else:
                result[field] = str(value) if value is not None else None
            
    return result

def run_code(custom_code):
    translated = translate(custom_code)
    
    ast_json = None
    output = ""
    error = None
    
    try:
        # Parse to Python AST
        tree = ast.parse(translated)
        ast_json = ast_to_dict(tree)
        
        # Compile
        code_obj = compile(tree, filename="<kendi_dil>", mode="exec")
        
        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        
        # Execute in a safe global namespace
        # We can limit builtins if we want to be safe, but a standard exec with standard builtins is fine for coding apps
        global_scope = {"__builtins__": __builtins__}
        
        try:
            exec(code_obj, global_scope)
            error = None
        except Exception as exec_err:
            import traceback
            # Strip internal compiler traceback frames to show only user code errors
            tb_lines = traceback.format_exception(type(exec_err), exec_err, exec_err.__traceback__)
            filtered_lines = []
            for line in tb_lines:
                if "compiler.py" in line or "exec(code_obj" in line:
                    continue
                filtered_lines.append(line)
            error = "".join(filtered_lines)
            
        sys.stdout = old_stdout
        output = mystdout.getvalue()
        
    except SyntaxError as syn_err:
        # Try to map the line number of Python syntax error back to original custom code
        error = f"Yazım Hatası (Syntax Error): {syn_err.msg}\nSatır: {syn_err.lineno}\nKolon: {syn_err.offset}"
        if syn_err.text:
            error += f"\nKod: {syn_err.text.strip()}"
    except Exception as e:
        error = f"Hata: {str(e)}"
        
    return {
        "translated": translated,
        "ast": ast_json,
        "output": output,
        "error": error
    }

if __name__ == '__main__':
    # Read custom code from stdin
    input_data = sys.stdin.read()
    try:
        req = json.loads(input_data)
        code = req.get("code", "")
        result = run_code(code)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({
            "translated": "",
            "ast": None,
            "output": "",
            "error": f"Sistem Hatası: {str(e)}"
        }))
