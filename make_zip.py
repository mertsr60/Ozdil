# -*- coding: utf-8 -*-
import sys
import os
import json
import zipfile

# Clean local CLI entry point for offline/local execution
VARYN_RUNNER_CONTENT = """# -*- coding: utf-8 -*-
\"\"\"
Varyn - Türkçe Programlama Dili Yerel ve Çevrimdışı Çalıştırıcısı
Kullanım: python3 varyn.py <dosya_adi.varyn>
\"\"\"
import sys
import os
import traceback

# Proje dizinini sys.path içerisine ekleyerek varyn ve varyn_core modüllerinin sorunsuz içe aktarılmasını sağlıyoruz
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

try:
    from varyn_core import (
        VarynError, Parser, Interpreter, lex_varyn
    )
except ImportError:
    print("Hata: 'varyn_core' modülü bulunamadı. Lütfen klasör yapısını bozmadığınızdan emin olun.")
    sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Kullanım: python3 varyn.py <dosya_adi.varyn>")
        print("Örnek: python3 varyn.py kodumuz.varyn")
        sys.exit(1)
    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"Hata: '{filepath}' dosyası bulunamadı!")
        sys.exit(1)
    with open(filepath, 'r', encoding='utf-8') as f:
        custom_code = f.read()
        
    try:
        tokens = lex_varyn(custom_code)
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
        print(f"\\nVaryn Çalışma Hatası (Girinti Hatası - IndentationError) 🚨")
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
        print(f"\\nVaryn Çalışma Hatası (Yazım Hatası - SyntaxError) 🚨")
        print("--------------------------------------------------")
        print(f"Açıklama  : {msg}")
        print(f"Satır     : {lineno}")
        print(f"Kolon     : {col}")
        print("--------------------------------------------------")
        print(f"Hatalı Kod: {err_line}")
    except VarynError as varyn_err:
        lines = custom_code.splitlines()
        err_line = lines[varyn_err.lineno - 1].strip() if 1 <= varyn_err.lineno <= len(lines) else "Bilinmiyor"
        print(f"\\nVaryn Çalışma Hatası ({varyn_err.friendly_type}) 🚨")
        print("--------------------------------------------------")
        print(f"Açıklama  : {varyn_err.message}")
        print(f"Satır     : {varyn_err.lineno}")
        print("--------------------------------------------------")
        print("Teknik Hata Detayı:")
        print(f"{varyn_err.friendly_type}: {varyn_err.message}")
        print(f"Hatalı Kod: {err_line}")
    except Exception as e:
        tb = traceback.extract_tb(sys.exc_info()[2])
        lineno = tb[-1].lineno if tb else 1
        lines = custom_code.splitlines()
        err_line = lines[lineno - 1].strip() if 1 <= lineno <= len(lines) else "Bilinmiyor"
        print(f"\\nVaryn Çalışma Hatası (Beklenmeyen Hata) 🚨")
        print("--------------------------------------------------")
        print(f"Açıklama  : {str(e)}")
        print(f"Satır     : {lineno}")
        print("--------------------------------------------------")
        print(f"Hatalı Kod: {err_line}")

if __name__ == '__main__':
    main()
"""

README_CONTENT = """# Varyn - Türkçe Programlama Dili (Yerel / Çevrimdışı Çalıştırıcı)

Tebrikler! Varyn projenizi başarıyla yerel cihazınıza dışa aktardınız.
Artık Varyn kodlarınızı bilgisayarınızda, sunucunuzda veya Android cihazınızda (Termux) çalıştırabilirsiniz!

## Dosya Yapısı

- `varyn.py`: Varyn kodlarını doğrudan sözcük çözücü ve AST yorumlayıcı ile koşturan yerel Varyn VM motoru.
- `varyn_core/`: Varyn'in dil çekirdeği paket modülleri (Lexer, Parser, AST, Interpreter vb.).
- `varyn/`: Paket yöneticisi, sandbox ortamı ve eklenti API'si modülleri.
- `varyn_packages/`: İndirilmiş veya yerel olarak geliştirilmiş Varyn kütüphaneleri (örn: renkler, hesap, matematik vb.).
- `kütüphane.md`: Detaylı Varyn Kütüphane ve Yapay Zekâ Eklentisi Geliştirme Kılavuzu.
- `kodumuz.varyn`: Siteden indirdiğiniz kendi özel kodunuz.
- `README.md`: Bu bilgilendirme dosyası.

## Kurulum ve Çalıştırma

Varyn'i çalıştırmak için bilgisayarınızda veya telefonunuzda **Python 3** kurulu olmalıdır.

### 1. Bilgisayarda Çalıştırma (Windows / MacOS / Linux)

Terminali veya Komut İstemi'ni (CMD) açın, bu dosyaların olduğu klasöre gidin ve şu komutu yazın:

```bash
python3 varyn.py kodumuz.varyn
```

*(Windows kullanıyorsanız `python` veya `py` yazmanız gerekebilir):*
```cmd
python varyn.py kodumuz.varyn
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
   python3 varyn.py kodumuz.varyn
   ```

## Kendi Dosyalarınızı Yazın

Yeni bir dosya oluşturup (örn: `hesapla.varyn`) içine Türkçe Varyn kodlarınızı yazıp çalıştırabilirsiniz:
```bash
python3 varyn.py hesapla.varyn
```

İyi kodlamalar!
"""

def main():
    try:
        input_data = sys.stdin.read()
        req = json.loads(input_data)
        user_code = req.get("code", "")
        
        zip_filename = "varyn_projesi.zip"
        
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 1. Main Runner Entrypoint
            zipf.writestr("varyn.py", VARYN_RUNNER_CONTENT)
            
            # 2. Main user code
            zipf.writestr("kodumuz.varyn", user_code)
            
            # 3. Readme
            zipf.writestr("README.md", README_CONTENT)
            
            # 4. Kütüphane Kılavuzu (kütüphane.md)
            lib_doc_path = "kütüphane.md"
            if os.path.exists(lib_doc_path):
                zipf.write(lib_doc_path, "kütüphane.md")
            
            # 5. Dynamically pack all modules from varyn_core folder on disk
            core_dir = "varyn_core"
            if os.path.exists(core_dir) and os.path.isdir(core_dir):
                for root, _, files in os.walk(core_dir):
                    if "__pycache__" in root:
                        continue
                    for file in files:
                        if file.endswith(".pyc"):
                            continue
                        file_path = os.path.join(root, file)
                        # We want the archive path to be relative, e.g. varyn_core/__init__.py
                        archive_name = os.path.relpath(file_path, start=os.path.dirname(core_dir))
                        zipf.write(file_path, archive_name)
            
            # 6. Dynamically pack all modules from varyn folder on disk (Sandbox / Plugin API)
            varyn_dir = "varyn"
            if os.path.exists(varyn_dir) and os.path.isdir(varyn_dir):
                for root, _, files in os.walk(varyn_dir):
                    if "__pycache__" in root:
                        continue
                    for file in files:
                        if file.endswith(".pyc"):
                            continue
                        file_path = os.path.join(root, file)
                        archive_name = os.path.relpath(file_path, start=os.path.dirname(varyn_dir))
                        zipf.write(file_path, archive_name)
            
            # 7. Dynamically pack all modules from varyn_packages folder on disk (Library Packages)
            packages_dir = "varyn_packages"
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
