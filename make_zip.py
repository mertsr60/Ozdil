# -*- coding: utf-8 -*-
import sys
import os
import json
import zipfile

# The code for ozdil.py runner
OZDIL_RUNNER_CONTENT = """# -*- coding: utf-8 -*-
\"\"\"
ÖzDil - Türkçe Programlama Dili Yerel Çalıştırıcısı
Kullanım: python3 ozdil.py <dosya_adi.oz>
\"\"\"
import sys
import os
import ast
import tokenize
from io import BytesIO

MAPPING = {
    'yazdir': 'print',
    'eger': 'if',
    'degilse_eger': 'elif',
    'degilse': 'else',
    'dongu': 'for',
    'her': 'for',
    'iken': 'while',
    'fonksiyon': 'def',
    'islem': 'def',
    'dondur': 'return',
    'dogru': 'True',
    'yanlis': 'False',
    've': 'and',
    'veya': 'or',
    'degil': 'not',
    'icinde': 'in',
    'sinif': 'class',
    'dene': 'try',
    'hata_yakala': 'except',
    'aralik': 'range',
    'uzunluk': 'len',
    'ekle': 'append',
    'tam_sayi': 'int',
    'metin': 'str',
    'ondalik': 'float',
    'liste': 'list',
    'sozluk': 'dict',
    'olarak': 'as',
    'getir': 'import',
    'dur': 'break',
    'devam_et': 'continue',
    'yok': 'None',
    'bos': 'None',
}

def translate(code_str):
    if not code_str.strip():
        return ""
    try:
        bytes_io = BytesIO(code_str.encode('utf-8'))
        tokens = list(tokenize.tokenize(bytes_io.readline))
        new_tokens = []
        for tok in tokens:
            if tok.type == tokenize.NAME and tok.string in MAPPING:
                new_tokens.append((tok.type, MAPPING[tok.string], tok.start, tok.end, tok.line))
            else:
                new_tokens.append(tok)
        return tokenize.untokenize(new_tokens).decode('utf-8')
    except Exception:
        import re
        sorted_keys = sorted(MAPPING.keys(), key=len, reverse=True)
        lines = code_str.splitlines()
        translated_lines = []
        for line in lines:
            temp_line = line
            for k in sorted_keys:
                temp_line = re.sub(r'\\b' + re.escape(k) + r'\\b', MAPPING[k], temp_line)
            translated_lines.append(temp_line)
        return '\\n'.join(translated_lines)

def main():
    if len(sys.argv) < 2:
        print("Kullanım: python3 ozdil.py <dosya_adi.oz>")
        print("Örnek: python3 ozdil.py kodumuz.oz")
        sys.exit(1)
        
    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"Hata: '{filepath}' dosyası bulunamadı!")
        sys.exit(1)
        
    with open(filepath, 'r', encoding='utf-8') as f:
        custom_code = f.read()
        
    translated = translate(custom_code)
    
    try:
        tree = ast.parse(translated)
        code_obj = compile(tree, filename=filepath, mode="exec")
        global_scope = {"__builtins__": __builtins__}
        exec(code_obj, global_scope)
    except SyntaxError as syn_err:
        print(f"\\nYazım Hatası (Syntax Error): {syn_err.msg}")
        print(f"Satır: {syn_err.lineno}, Kolon: {syn_err.offset}")
        if syn_err.text:
            print(f"Kod: {syn_err.text.strip()}")
    except Exception as err:
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
"""

README_CONTENT = """# ÖzDil - Türkçe Programlama Dili (Yerel / Çevrimdışı Çalıştırıcı)

Tebrikler! ÖzDil projenizi başarıyla yerel cihazınıza dışa aktardınız.
Artık ÖzDil kodlarınızı bilgisayarınızda, sunucunuzda veya Android cihazınızda (Termux) çalıştırabilirsiniz!

## Dosya Yapısı

- `ozdil.py`: Türkçe yazılan kodları Python AST yapısına dönüştürüp çalıştıran ana motor.
- `kodumuz.oz`: Siteden indirdiğiniz kendi özel kodunuz.
- `README.md`: Bu bilgilendirme dosyası.

## Kurulum ve Çalıştırma

ÖzDil'i çalıştırmak için bilgisayarınızda veya telefonunuzda **Python 3** kurulu olmalıdır.

### 1. Bilgisayarda Çalıştırma (Windows / MacOS / Linux)

Terminali veya Komut İstemi'ni (CMD) açın, bu dosyaların olduğu klasöre gidin ve şu komutu yazın:

```bash
python3 ozdil.py kodumuz.oz
```

*(Windows kullanıyorsanız `python` veya `py` yazmanız gerekebilir):*
```cmd
python ozdil.py kodumuz.oz
```

---

### 2. Mobilde / Android'de Çalıştırma (Termux)

Android telefonunuzda kodlarınızı çalıştırmak için **Termux** uygulamasını kullanabilirsiniz:

1. Termux uygulamasını açın.
2. Gerekli paketleri ve Python'u kurun:
   ```bash
   pkg update && pkg upgrade
   pkg install python
   ```
3. Dosyaların bulunduğu dizine gidin (örneğin telefon hafızasındaki Download klasörü):
   ```bash
   termux-setup-storage
   cd /sdcard/Download
   ```
4. Kodunuzu çalıştırın:
   ```bash
   python3 ozdil.py kodumuz.oz
   ```

## Kendi Dosyalarınızı Yazın

Yeni bir dosya oluşturup (örn: `hesapla.oz`) içine Türkçe kodlarınızı yazıp çalıştırabilirsiniz:
```bash
python3 ozdil.py hesapla.oz
```

İyi kodlamalar!
"""

def main():
    try:
        input_data = sys.stdin.read()
        req = json.loads(input_data)
        user_code = req.get("code", "")
        
        # We will create a zip file on disk
        zip_filename = "ozdil_projesi.zip"
        
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.writestr("ozdil.py", OZDIL_RUNNER_CONTENT)
            zipf.writestr("kodumuz.oz", user_code)
            zipf.writestr("README.md", README_CONTENT)
            
        print(json.dumps({"success": True, "filename": zip_filename}))
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))

if __name__ == '__main__':
    main()
