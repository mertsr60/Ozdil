# -*- coding: utf-8 -*-
import sys
import os
import json
import traceback

from ozdil_core import (
    OzdilError, ReturnException, BreakException, ContinueException, InputRequestException,
    Token, OZDIL_KEYWORDS,
    tokenize_line, lex_ozdil,
    ASTNode, Program, Atama, Eger, Iken, Dongu, Islem, Dondur, Getir,
    IkiliIslem, TekliIslem, Degisken, Deger, Cagir, Nitelik,
    Endeks, Liste, Sozluk, Ifade, DurNode, DevamEtNode,
    Environment, Parser, Interpreter, get_attribute, load_external_package
)

# Derleme Önbelleği (Compilation Cache)
class CompilationCache:
    def __init__(self, max_size=100):
        self.max_size = max_size
        self.cache = {}
        self.order = []

    def get(self, code_str):
        if code_str in self.cache:
            # Move to end (LRU)
            self.order.remove(code_str)
            self.order.append(code_str)
            return self.cache[code_str]
        return None

    def set(self, code_str, data):
        if code_str in self.cache:
            self.order.remove(code_str)
        elif len(self.cache) >= self.max_size:
            # Pop oldest
            oldest = self.order.pop(0)
            del self.cache[oldest]
        self.cache[code_str] = data
        self.order.append(code_str)

_COMPILATION_CACHE = CompilationCache(max_size=100)

def run_code(custom_code, inputs_list=None, trigger_event=None):
    output = ""
    error = None
    ast_dict = None
    translated_tokens_str = ""
    awaiting_input = False
    prompt = ""
    
    import ozdil.plugin_api
    # Temizle ve sıfırla
    ozdil.plugin_api.plugin.clear()
    
    try:
        # Check Compilation Cache
        cached = _COMPILATION_CACHE.get(custom_code)
        if cached:
            tokens, ast_root, ast_dict, translated_tokens_str = cached
        else:
            # Lexer
            tokens = lex_ozdil(custom_code)
            
            # Build friendly Lexer output for the "Sözcükler (Lexer)" tab
            token_lines = []
            for tok in tokens:
                token_lines.append(f"Satır {tok.lineno:2d}, Sütun {tok.col:2d} | Tür: {tok.type:<12} | Değer: {repr(tok.value)}")
            translated_tokens_str = "\n".join(token_lines)
            
            # Parser
            parser = Parser(tokens)
            ast_root = parser.parse_program()
            ast_dict = ast_root.to_dict()
            
            # Cache the compiled data for future runs
            _COMPILATION_CACHE.set(custom_code, (tokens, ast_root, ast_dict, translated_tokens_str))
        
        # Olay tetikle: program_basladi
        ozdil.plugin_api.plugin.trigger_event("program_basladi")
        
        # Interpreter VM
        interpreter = Interpreter(inputs_list=inputs_list)
        interpreter.eval(ast_root, interpreter.global_env)
        
        # Olay tetikle: custom_event
        if trigger_event:
            ozdil.plugin_api.plugin.trigger_event(trigger_event)
            
        # Olay tetikle: program_bitti
        ozdil.plugin_api.plugin.trigger_event("program_bitti")
        
        output = "".join(interpreter.stdout)
        
    except InputRequestException as in_req:
        awaiting_input = True
        prompt = in_req.prompt
        output = "".join(interpreter.stdout)
    except IndentationError as ind_err:
        lines = custom_code.splitlines()
        tb = traceback.extract_tb(sys.exc_info()[2])
        lineno = tb[-1].lineno if tb else 1
        # Try to find the line number of indentation error
        for frame in tb:
            if frame.filename == "<string>" or frame.filename == "<kendi_dil>":
                lineno = frame.lineno
        err_line = lines[lineno - 1].strip() if 1 <= lineno <= len(lines) else "Bilinmiyor"
        error = (
            f"ÖzDil Çalışma Hatası (Girinti Hatası - IndentationError) 🚨\n"
            f"--------------------------------------------------\n"
            f"Açıklama  : Kod bloklarının hizalaması (girintisi) uyuşmuyor.\n"
            f"Satır     : {lineno}\n"
            f"--------------------------------------------------\n"
            f"Hatalı Kod: {err_line}"
        )
        error_details = {
            "type": "IndentationError",
            "friendly_type": "Girinti Hatası (IndentationError)",
            "message": "Kod bloklarının hizalaması (girintisi) uyuşmuyor.",
            "lineno": lineno,
            "col": 1,
            "line_code": err_line,
            "suggested_fix": "Eğer ('eger'), döngü ('dongu') veya işlem ('islem') bloklarının altındaki satırların başına aynı sayıda boşluk/sekme bıraktığınızdan emin olun."
        }
        ozdil.plugin_api.plugin.trigger_event("hata_olustu", error)
    except SyntaxError as syn_err:
        lines = custom_code.splitlines()
        # Retrieve actual or estimated lineno and col
        lineno = 1
        col = 1
        msg = str(syn_err)
        
        # Extract from syn_err tuple if present
        if len(syn_err.args) > 1 and isinstance(syn_err.args[1], tuple):
            lineno = syn_err.args[1][1] or 1
            col = syn_err.args[1][2] or 1
        else:
            # Fallback to scanning tokens
            if 'parser' in locals() and parser.tokens:
                curr_tok = parser.current()
                lineno = curr_tok.lineno
                col = curr_tok.col
                
        err_line = lines[lineno - 1].strip() if 1 <= lineno <= len(lines) else "Bilinmiyor"
        error = (
            f"ÖzDil Çalışma Hatası (Yazım Hatası - SyntaxError) 🚨\n"
            f"--------------------------------------------------\n"
            f"Açıklama  : {msg}\n"
            f"Satır     : {lineno}\n"
            f"Kolon     : {col}\n"
            f"--------------------------------------------------\n"
            f"Hatalı Kod: {err_line}"
        )
        error_details = {
            "type": "SyntaxError",
            "friendly_type": "Yazım Hatası (SyntaxError)",
            "message": msg,
            "lineno": lineno,
            "col": col,
            "line_code": err_line,
            "suggested_fix": "Yazım kurallarını kontrol edin. Parantezlerin kapandığından, iki nokta üst üste (:) işaretinin doğru yerleştirildiğinden ve anahtar kelimelerin doğru yazıldığından emin olun."
        }
        ozdil.plugin_api.plugin.trigger_event("hata_olustu", error)
    except OzdilError as oz_err:
        lines = custom_code.splitlines()
        err_line = lines[oz_err.lineno - 1].strip() if 1 <= oz_err.lineno <= len(lines) else "Bilinmiyor"
        error = (
            f"ÖzDil Çalışma Hatası ({oz_err.friendly_type}) 🚨\n"
            f"--------------------------------------------------\n"
            f"Açıklama  : {oz_err.message}\n"
            f"Satır     : {oz_err.lineno}\n"
            f"--------------------------------------------------\n"
            f"Teknik Hata Detayı:\n"
            f"{oz_err.friendly_type}: {oz_err.message}\n"
            f"Hatalı Kod: {err_line}"
        )
        
        suggested_fix = "Kod mantığını ve değişkenlerin değerlerini kontrol edin."
        ft_lower = oz_err.friendly_type.lower()
        if "tanımlanmamış" in ft_lower or "nameerror" in ft_lower:
            suggested_fix = "Kullanılan değişken veya fonksiyon adını kontrol edin. Doğru tanımlandığından veya büyük-küçük harf hatası olmadığından emin olun."
        elif "sıfıra bölme" in ft_lower or "zerodivisionerror" in ft_lower:
            suggested_fix = "Bir sayıyı sıfıra bölemezsiniz. Lütfen bölme veya mod işlemlerinde payda kısmının sıfır gelmediğinden emin olun."
        elif "tür hatası" in ft_lower or "typeerror" in ft_lower:
            suggested_fix = "Uyumsuz veri türleri arasında işlem yapılmaya çalışıldı. Gerekirse 'metin(...)', 'tam_sayi(...)' gibi tür dönüştürücüleri kullanın."
        elif "dizin hatası" in ft_lower or "indexerror" in ft_lower:
            suggested_fix = "Liste sınırlarının dışına çıkıldı veya geçersiz sözlük anahtarı kullanıldı. Eleman sayısını kontrol etmek için 'uzunluk(...)' fonksiyonundan yararlanabilirsiniz."
        elif "kütüphane" in ft_lower or "importerror" in ft_lower:
            suggested_fix = "İçe aktarılmak istenen kütüphane bulunamadı. ozpip sekmesinden paketin kurulu olduğundan veya adının doğru yazıldığından emin olun."
        elif "sabit" in ft_lower or "constanterror" in ft_lower:
            suggested_fix = "Sabit değişkenlerin (BÜYÜK harfle başlayanlar veya özel tanımlı sabitler) değerleri tanımlandıktan sonra değiştirilemez."
        elif "öznitelik" in ft_lower or "attributeerror" in ft_lower:
            suggested_fix = "Nesnenin sahip olmadığı bir özelliğe (özniteliğe) erişmeye çalıştınız. Özellik adını ve nesnenin yapısını kontrol edin."
        elif "yürütme" in ft_lower or "runtimeerror" in ft_lower:
            suggested_fix = "Kod yürütülürken beklenmedik bir çalışma zamanı hatası oluştu. Verilen parametrelerin ve işlemlerin geçerliliğinden emin olun."

        error_details = {
            "type": "RuntimeError",
            "friendly_type": oz_err.friendly_type,
            "message": oz_err.message,
            "lineno": oz_err.lineno,
            "col": 1,
            "line_code": err_line,
            "suggested_fix": suggested_fix
        }
        ozdil.plugin_api.plugin.trigger_event("hata_olustu", error)
    except Exception as e:
        tb = traceback.extract_tb(sys.exc_info()[2])
        lineno = tb[-1].lineno if tb else 1
        lines = custom_code.splitlines()
        err_line = lines[lineno - 1].strip() if 1 <= lineno <= len(lines) else "Bilinmiyor"
        error = (
            f"ÖzDil Çalışma Hatası (Beklenmeyen Hata) 🚨\n"
            f"--------------------------------------------------\n"
            f"Açıklama  : {str(e)}\n"
            f"Satır     : {lineno}\n"
            f"--------------------------------------------------\n"
            f"Hatalı Kod: {err_line}"
        )
        error_details = {
            "type": "Exception",
            "friendly_type": "Beklenmeyen Hata (SystemException)",
            "message": str(e),
            "lineno": lineno,
            "col": 1,
            "line_code": err_line,
            "suggested_fix": "İşlem yapılırken beklenmeyen bir sistem hatası oluştu. Kodun doğru formatta olduğundan emin olun."
        }
        ozdil.plugin_api.plugin.trigger_event("hata_olustu", error)
        
    import ozdil.plugin_api
    gui_elements = list(ozdil.plugin_api.plugin.gui_elements)
    
    return {
        "translated": translated_tokens_str,
        "ast": ast_dict,
        "output": output,
        "error": error,
        "error_details": error_details if 'error_details' in locals() else None,
        "awaiting_input": awaiting_input,
        "prompt": prompt,
        "gui_elements": gui_elements
    }

if __name__ == '__main__':
    input_data = sys.stdin.read()
    try:
        req = json.loads(input_data)
        code = req.get("code", "")
        inputs = req.get("inputs", [])
        event = req.get("event", None)
        result = run_code(code, inputs_list=inputs, trigger_event=event)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({
            "translated": "",
            "ast": None,
            "output": "",
            "error": f"Sistem Hatası: {str(e)}"
        }))
