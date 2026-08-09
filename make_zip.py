# -*- coding: utf-8 -*-
import sys
import os
import json
import zipfile

# Clean local CLI entry point for offline/local execution
OZDIL_RUNNER_CONTENT = """# -*- coding: utf-8 -*-
\"\"\"
ÖzDil - Türkçe Programlama Dili Yerel ve Çevrimdışı Çalıştırıcısı
Kullanım: python3 ozdil.py <dosya_adi.oz>
\"\"\"
import sys
import os
import traceback

# Proje dizinini sys.path içerisine ekleyerek ozdil ve ozdil_core modüllerinin sorunsuz içe aktarılmasını sağlıyoruz
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

try:
    from ozdil_core import (
        OzdilError, Parser, Interpreter, lex_ozdil
    )
except ImportError:
    print("Hata: 'ozdil_core' modülü bulunamadı. Lütfen klasör yapısını bozmadığınızdan emin olun.")
    sys.exit(1)

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
        
    try:
        tokens = lex_ozdil(custom_code)
        parser = Parser(tokens)
        ast_root = parser.parse_program()
        
        interpreter = Interpreter()
        interpreter.eval(ast_root, interpreter.global_env)
        
    except IndentationError as ind_err:
        lines = custom_code.splitlines()
        tb = traceback.extract_tb(sys.exc_info()[2])
        lineno = tb[-1].lineno if tb else 1
        for frame in tb:
            if frame.filename == filepath:
                lineno = frame.lineno
        err_line = lines[lineno - 1].strip() if 1 <= lineno <= len(lines) else "Bilinmiyor"
        print(f"\\nÖzDil Çalışma Hatası (Girinti Hatası - IndentationError) 🚨")
        print("--------------------------------------------------")
        print("Açıklama  : Kod bloklarının hizalaması (girintisi) uyuşmuyor.")
        print(f"Satır     : {lineno}")
        print("--------------------------------------------------")
        print(f"Hatalı Kod: {err_line}")
    except SyntaxError as syn_err:
        lines = custom_code.splitlines()
        lineno = 1
        col = 1
        msg = str(syn_err)
        if len(syn_err.args) > 1 and isinstance(syn_err.args[1], tuple):
            lineno = syn_err.args[1][1] or 1
            col = syn_err.args[1][2] or 1
        else:
            if 'parser' in locals() and parser.tokens:
                curr_tok = parser.current()
                lineno = curr_tok.lineno
                col = curr_tok.col
        err_line = lines[lineno - 1].strip() if 1 <= lineno <= len(lines) else "Bilinmiyor"
        print(f"\\nÖzDil Çalışma Hatası (Yazım Hatası - SyntaxError) 🚨")
        print("--------------------------------------------------")
        print(f"Açıklama  : {msg}")
        print(f"Satır     : {lineno}")
        print(f"Kolon     : {col}")
        print("--------------------------------------------------")
        print(f"Hatalı Kod: {err_line}")
    except OzdilError as oz_err:
        lines = custom_code.splitlines()
        err_line = lines[oz_err.lineno - 1].strip() if 1 <= oz_err.lineno <= len(lines) else "Bilinmiyor"
        print(f"\\nÖzDil Çalışma Hatası ({oz_err.friendly_type}) 🚨")
        print("--------------------------------------------------")
        print(f"Açıklama  : {oz_err.message}")
        print(f"Satır     : {oz_err.lineno}")
        print("--------------------------------------------------")
        print("Teknik Hata Detayı:")
        print(f"{oz_err.friendly_type}: {oz_err.message}")
        print(f"Hatalı Kod: {err_line}")
    except Exception as e:
        tb = traceback.extract_tb(sys.exc_info()[2])
        lineno = tb[-1].lineno if tb else 1
        lines = custom_code.splitlines()
        err_line = lines[lineno - 1].strip() if 1 <= lineno <= len(lines) else "Bilinmiyor"
        print(f"\\nÖzDil Çalışma Hatası (Beklenmeyen Hata) 🚨")
        print("--------------------------------------------------")
        print(f"Açıklama  : {str(e)}")
        print(f"Satır     : {lineno}")
        print("--------------------------------------------------")
        print(f"Hatalı Kod: {err_line}")

if __name__ == '__main__':
    main()
"""

README_CONTENT = """# ÖzDil - Türkçe Programlama Dili (Yerel / Çevrimdışı Çalıştırıcı)

Tebrikler! ÖzDil projenizi başarıyla yerel cihazınıza dışa aktardınız.
Artık ÖzDil kodlarınızı bilgisayarınızda, sunucunuzda veya Android cihazınızda (Termux) çalıştırabilirsiniz!

## Dosya Yapısı

- `ozdil.py`: ÖzDil kodlarını doğrudan sözcük çözücü ve AST yorumlayıcı ile koşturan yerel ÖzDil VM motoru.
- `ozdil_core/`: ÖzDil'in dil çekirdeği paket modülleri (Lexer, Parser, AST, Interpreter vb.).
- `ozdil/`: Paket yöneticisi, sandbox ortamı ve eklenti API'si modülleri.
- `oz_packages/`: İndirilmiş veya yerel olarak geliştirilmiş ÖzDil kütüphaneleri (örn: renkler, hesap, matematik vb.).
- `kütüphane.md`: Detaylı ÖzDil Kütüphane ve Yapay Zekâ Eklentisi Geliştirme Kılavuzu.
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

Yeni bir dosya oluşturup (örn: `hesapla.oz`) içine Türkçe ÖzDil kodlarınızı yazıp çalıştırabilirsiniz:
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
        
        zip_filename = "ozdil_projesi.zip"
        
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 1. Main Runner Entrypoint
            zipf.writestr("ozdil.py", OZDIL_RUNNER_CONTENT)
            
            # 2. Main user code
            zipf.writestr("kodumuz.oz", user_code)
            
            # 3. Readme
            zipf.writestr("README.md", README_CONTENT)
            
            # 4. Kütüphane Kılavuzu (kütüphane.md)
            lib_doc_path = "kütüphane.md"
            if os.path.exists(lib_doc_path):
                zipf.write(lib_doc_path, "kütüphane.md")
            
            # 5. Dynamically pack all modules from ozdil_core folder on disk
            core_dir = "ozdil_core"
            if os.path.exists(core_dir) and os.path.isdir(core_dir):
                for root, _, files in os.walk(core_dir):
                    if "__pycache__" in root:
                        continue
                    for file in files:
                        if file.endswith(".pyc"):
                            continue
                        file_path = os.path.join(root, file)
                        # We want the archive path to be relative, e.g. ozdil_core/__init__.py
                        archive_name = os.path.relpath(file_path, start=os.path.dirname(core_dir))
                        zipf.write(file_path, archive_name)
            
            # 6. Dynamically pack all modules from ozdil folder on disk (Sandbox / Plugin API)
            ozdil_dir = "ozdil"
            if os.path.exists(ozdil_dir) and os.path.isdir(ozdil_dir):
                for root, _, files in os.walk(ozdil_dir):
                    if "__pycache__" in root:
                        continue
                    for file in files:
                        if file.endswith(".pyc"):
                            continue
                        file_path = os.path.join(root, file)
                        archive_name = os.path.relpath(file_path, start=os.path.dirname(ozdil_dir))
                        zipf.write(file_path, archive_name)
            
            # 7. Dynamically pack all modules from oz_packages folder on disk (Library Packages)
            packages_dir = "oz_packages"
            if os.path.exists(packages_dir) and os.path.isdir(packages_dir):
                for root, _, files in os.walk(packages_dir):
                    if "__pycache__" in root:
                        continue
                    for file in files:
                        if file.endswith(".pyc"):
                            continue
                        file_path = os.path.join(root, file)
                        archive_name = os.path.relpath(file_path, start=os.path.dirname(packages_dir))
                        zipf.write(file_path, archive_name)
                        
        print(json.dumps({"success": True, "filename": zip_filename}))
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))

if __name__ == '__main__':
    main()
