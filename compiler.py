# -*- coding: utf-8 -*-
import sys
import json
import ast
import tokenize
import traceback
import re
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
    # Library names
    'matematik': 'math',
    'rastgele': 'random',
    'zaman': 'time',
}

# Function-to-module mappings for standalone usage
DIRECT_MAPPINGS = {
    'karekok': 'math.sqrt',
    'karekök': 'math.sqrt',
    'faktoriyel': 'math.factorial',
    'faktöriyel': 'math.factorial',
    'sinus': 'math.sin',
    'sinüs': 'math.sin',
    'kosinus': 'math.cos',
    'kosinüs': 'math.cos',
    'tanjant': 'math.tan',
    'radyan': 'math.radians',
    'derece': 'math.degrees',
    'us': 'math.pow',
    'üs': 'math.pow',
    'mutlak': 'math.fabs',
    'asagi_yuvarla': 'math.floor',
    'aşağı_yuvarla': 'math.floor',
    'yukari_yuvarla': 'math.ceil',
    'yukarı_yuvarla': 'math.ceil',
    'ebob': 'math.gcd',
    'en_buyuk_ortak_bolen': 'math.gcd',
    'pi_sayısı': 'math.pi',
    'pi_sayisi': 'math.pi',
    
    'ondalik_sec': 'random.random',
    'ondalık_seç': 'random.random',
    'tamsayi_sec': 'random.randint',
    'tamsayı_seç': 'random.randint',
    'aralikta_sec': 'random.randrange',
    'aralıkta_seç': 'random.randrange',
    'sec': 'random.choice',
    'seç': 'random.choice',
    'karistir': 'random.shuffle',
    'karıştır': 'random.shuffle',
    'ornek_sec': 'random.sample',
    'örnek_seç': 'random.sample',
    
    'bekle': 'time.sleep',
    'yerel_zaman': 'time.localtime',
    'tarih_saat': 'time.ctime',
}

# Standalone name mappings when accessed inside a module (e.g. matematik.karekök -> math.sqrt)
MODULE_MEMBER_MAPPINGS = {
    'karekok': 'sqrt',
    'karekök': 'sqrt',
    'faktoriyel': 'factorial',
    'faktöriyel': 'factorial',
    'sinus': 'sin',
    'sinüs': 'sin',
    'kosinus': 'cos',
    'kosinüs': 'cos',
    'tanjant': 'tan',
    'radyan': 'radians',
    'derece': 'degrees',
    'us': 'pow',
    'üs': 'pow',
    'mutlak': 'fabs',
    'asagi_yuvarla': 'floor',
    'aşağı_yuvarla': 'floor',
    'yukari_yuvarla': 'ceil',
    'yukarı_yuvarla': 'ceil',
    'ebob': 'gcd',
    'en_buyuk_ortak_bolen': 'gcd',
    'pi_sayısı': 'pi',
    'pi_sayisi': 'pi',
    
    'ondalik_sec': 'random',
    'ondalık_seç': 'random',
    'tamsayi_sec': 'randint',
    'tamsayı_seç': 'randint',
    'aralikta_sec': 'randrange',
    'aralıkta_seç': 'randrange',
    'sec': 'choice',
    'seç': 'choice',
    'karistir': 'shuffle',
    'karıştır': 'shuffle',
    'ornek_sec': 'sample',
    'örnek_seç': 'sample',
    
    'bekle': 'sleep',
    'yerel_zaman': 'localtime',
    'tarih_saat': 'ctime',
}

def is_module_access(new_tokens):
    if len(new_tokens) >= 2:
        last_tok = new_tokens[-1]
        second_last_tok = new_tokens[-2]
        if last_tok[0] == tokenize.OP and last_tok[1] == '.':
            if second_last_tok[0] == tokenize.NAME and second_last_tok[1] in ('matematik', 'math', 'rastgele', 'random', 'zaman', 'time'):
                return True
    return False

def translate(code_str):
    if not code_str.strip():
        return ""
        
    try:
        bytes_io = BytesIO(code_str.encode('utf-8'))
        tokens = list(tokenize.tokenize(bytes_io.readline))
        new_tokens = []
        
        i = 0
        n = len(tokens)
        while i < n:
            tok = tokens[i]
            
            # Check if this is a variable declaration keyword
            if tok.type == tokenize.NAME and tok.string in ('değişken', 'degisken', 'sabit'):
                if i + 1 < n and tokens[i+1].type == tokenize.NAME:
                    next_tok = tokens[i+1]
                    # Shift start position of next token to avoid unexpected indentation
                    tokens[i+1] = tokenize.TokenInfo(next_tok.type, next_tok.string, tok.start, next_tok.end, next_tok.line)
                    i += 1
                    continue
            
            # Check if this is a type prefix keyword
            elif tok.type == tokenize.NAME and tok.string in ('tam_sayı', 'tam_sayi', 'ondalık', 'ondalik', 'metin', 'liste', 'sözlük', 'sozluk', 'mantıksal', 'mantiksal'):
                if i + 1 < n and tokens[i+1].type == tokenize.NAME:
                    if i + 2 < n and tokens[i+2].type in (tokenize.OP, tokenize.NAME) and tokens[i+2].string in ('=', ',', 'in', 'içinde', 'icinde'):
                        next_tok = tokens[i+1]
                        # Shift start position of next token to avoid unexpected indentation
                        tokens[i+1] = tokenize.TokenInfo(next_tok.type, next_tok.string, tok.start, next_tok.end, next_tok.line)
                        i += 1
                        continue
            
            # Handle standalone functions (like karekök -> math.sqrt) or module properties
            if tok.type == tokenize.NAME and tok.string in DIRECT_MAPPINGS:
                if is_module_access(new_tokens):
                    mapped_val = MODULE_MEMBER_MAPPINGS[tok.string]
                else:
                    mapped_val = DIRECT_MAPPINGS[tok.string]
                new_tokens.append(tokenize.TokenInfo(tok.type, mapped_val, tok.start, tok.end, tok.line))
            
            # Handle standard keyword mapping
            elif tok.type == tokenize.NAME and tok.string in MAPPING:
                new_tokens.append(tokenize.TokenInfo(tok.type, MAPPING[tok.string], tok.start, tok.end, tok.line))
            else:
                new_tokens.append(tok)
            i += 1
                
        translated = tokenize.untokenize(new_tokens).decode('utf-8')
        return translated
    except Exception as tok_err:
        sorted_keys = sorted(list(MAPPING.keys()) + list(DIRECT_MAPPINGS.keys()), key=len, reverse=True)
        lines = code_str.splitlines()
        translated_lines = []
        for line in lines:
            temp_line = line
            for k in sorted_keys:
                mapped = DIRECT_MAPPINGS.get(k, MAPPING.get(k))
                temp_line = re.sub(r'\b' + re.escape(k) + r'\b', mapped, temp_line)
            translated_lines.append(temp_line)
        return '\n'.join(translated_lines)

def translate_error(exc_type, exc_value, exc_traceback):
    exc_name = exc_type.__name__
    tb_list = traceback.extract_tb(exc_traceback)
    user_frames = [f for f in tb_list if f.filename == "<kendi_dil>"]
    
    lineno = "?"
    if user_frames:
        lineno = user_frames[-1].lineno
    elif hasattr(exc_value, 'lineno') and exc_value.lineno is not None:
        lineno = exc_value.lineno
        
    explanation = "Bilinmeyen bir hata oluştu."
    friendly_type = "Çalışma Zamanı Hatası"
    msg = str(exc_value)
    
    if exc_type is NameError:
        friendly_type = "Tanımlama Hatası (NameError)"
        match = re.search(r"name '([^']+)' is not defined", msg)
        name = match.group(1) if match else "değişken"
        rev_mapping = {v: k for k, v in MAPPING.items()}
        rev_direct = {v.split('.')[-1]: k for k, v in DIRECT_MAPPINGS.items()}
        mapped_name = rev_mapping.get(name, rev_direct.get(name, name))
        explanation = f"'{mapped_name}' adında bir değişken, fonksiyon veya kütüphane bulunamadı. Lütfen adını doğru yazdığınızdan emin olun."
        
    elif exc_type is ZeroDivisionError:
        friendly_type = "Sıfıra Bölme Hatası (ZeroDivisionError)"
        explanation = "Bir sayı sıfıra (0) bölünemez. Lütfen bölen değeri kontrol edin."
        
    elif exc_type is TypeError:
        friendly_type = "Tür Hatası (TypeError)"
        explanation = f"Uyumsuz veri türleri arasında geçersiz bir işlem yapılmaya çalışıldı. Detay: {msg}"
        
    elif exc_type is IndexError:
        friendly_type = "Dizin Hatası (IndexError)"
        explanation = "Listenin sınırları dışındaki bir elemana erişilmeye çalışıldı (Index out of range)."
        
    elif exc_type is KeyError:
        friendly_type = "Anahtar Hatası (KeyError)"
        explanation = f"Sözlükte belirtilen anahtar bulunamadı: {msg}"
        
    elif exc_type is ValueError:
        friendly_type = "Değer Hatası (ValueError)"
        explanation = f"Bir fonksiyona geçersiz veya uyumsuz bir değer gönderildi. Detay: {msg}"
        
    elif exc_type is AttributeError:
        friendly_type = "Öznitelik Hatası (AttributeError)"
        match = re.search(r"attribute '([^']+)'", msg)
        attr = match.group(1) if match else "öznitelik"
        explanation = f"Belirtilen kütüphanede veya nesnede '{attr}' adında bir fonksiyon veya özellik bulunamadı."
        
    elif exc_type is SyntaxError:
        friendly_type = "Yazım Hatası (SyntaxError)"
        explanation = f"Yazım kuralı ihlali tespit edildi. Detay: {msg}"
        lineno = getattr(exc_value, 'lineno', lineno)
        
    else:
        explanation = f"Program yürütülürken hata ile karşılaşıldı: {msg}"

    err_msg = (
        f"ÖzDil Çalışma Hatası ({friendly_type}) 🚨\n"
        f"--------------------------------------------------\n"
        f"Açıklama  : {explanation}\n"
        f"Satır     : {lineno}\n"
        f"--------------------------------------------------\n"
        f"Teknik Hata Detayı:\n"
        f"{exc_name}: {msg}"
    )
    return err_msg

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
        
        # Execute in a safe global namespace pre-populated with standard libraries
        import math
        import random
        import time
        global_scope = {
            "__builtins__": __builtins__,
            "math": math,
            "random": random,
            "time": time
        }
        
        try:
            exec(code_obj, global_scope)
            error = None
        except Exception as exec_err:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            error = translate_error(exc_type, exc_value, exc_traceback)
            
        sys.stdout = old_stdout
        output = mystdout.getvalue()
        
    except SyntaxError as syn_err:
        error = (
            f"ÖzDil Çalışma Hatası (Yazım Hatası - SyntaxError) 🚨\n"
            f"--------------------------------------------------\n"
            f"Açıklama  : Yazım kuralı ihlali tespit edildi: {syn_err.msg}\n"
            f"Satır     : {syn_err.lineno}\n"
            f"Kolon     : {syn_err.offset}\n"
            f"--------------------------------------------------\n"
            f"Hatalı Kod: {syn_err.text.strip() if syn_err.text else 'Bilinmiyor'}"
        )
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
