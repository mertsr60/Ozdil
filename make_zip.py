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
    'matematik': 'math',
    'rastgele': 'random',
    'zaman': 'time',
}

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
            if tok.type == tokenize.NAME and tok.string in ('değişken', 'degisken', 'sabit'):
                if i + 1 < n and tokens[i+1].type == tokenize.NAME:
                    i += 1
                    continue
            elif tok.type == tokenize.NAME and tok.string in ('tam_sayı', 'tam_sayi', 'ondalık', 'ondalik', 'metin', 'liste', 'sözlük', 'sozluk', 'mantıksal', 'mantiksal'):
                if i + 1 < n and tokens[i+1].type == tokenize.NAME:
                    if i + 2 < n and tokens[i+2].type in (tokenize.OP, tokenize.NAME) and tokens[i+2].string in ('=', ',', 'in', 'içinde', 'icinde'):
                        i += 1
                        continue
            if tok.type == tokenize.NAME and tok.string in DIRECT_MAPPINGS:
                if is_module_access(new_tokens):
                    mapped_val = MODULE_MEMBER_MAPPINGS[tok.string]
                else:
                    mapped_val = DIRECT_MAPPINGS[tok.string]
                new_tokens.append((tok.type, mapped_val, tok.start, tok.end, tok.line))
            elif tok.type == tokenize.NAME and tok.string in MAPPING:
                new_tokens.append((tok.type, MAPPING[tok.string], tok.start, tok.end, tok.line))
            else:
                new_tokens.append(tok)
            i += 1
        return tokenize.untokenize(new_tokens).decode('utf-8')
    except Exception:
        import re
        sorted_keys = sorted(list(MAPPING.keys()) + list(DIRECT_MAPPINGS.keys()), key=len, reverse=True)
        lines = code_str.splitlines()
        translated_lines = []
        for line in lines:
            temp_line = line
            for k in sorted_keys:
                mapped = DIRECT_MAPPINGS.get(k, MAPPING.get(k))
                temp_line = re.sub(r'\\b' + re.escape(k) + r'\\b', mapped, temp_line)
            translated_lines.append(temp_line)
        return '\\n'.join(translated_lines)

def translate_error(exc_type, exc_value, exc_traceback, filepath):
    exc_name = exc_type.__name__
    import traceback
    tb_list = traceback.extract_tb(exc_traceback)
    user_frames = [f for f in tb_list if f.filename == filepath]
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
        import re
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
        import re
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
        f"ÖzDil Çalışma Hatası ({friendly_type}) \\u26a1\\n"
        f"--------------------------------------------------\\n"
        f"Açıklama  : {explanation}\\n"
        f"Satır     : {lineno}\\n"
        f"--------------------------------------------------\\n"
        f"Teknik Hata Detayı:\\n"
        f"{exc_name}: {msg}"
    )
    return err_msg

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
        import math
        import random
        import time
        global_scope = {
            "__builtins__": __builtins__,
            "math": math,
            "random": random,
            "time": time
        }
        exec(code_obj, global_scope)
    except SyntaxError as syn_err:
        print(f"\\nÖzDil Çalışma Hatası (Yazım Hatası - SyntaxError) \\u26a1")
        print("--------------------------------------------------")
        print(f"Açıklama  : Yazım kuralı ihlali tespit edildi: {syn_err.msg}")
        print(f"Satır     : {syn_err.lineno}")
        print(f"Kolon     : {syn_err.offset}")
        print("--------------------------------------------------")
        if syn_err.text:
            print(f"Hatalı Kod: {syn_err.text.strip()}")
    except Exception as err:
        import sys
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(translate_error(exc_type, exc_value, exc_traceback, filepath))

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
