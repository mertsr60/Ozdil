# -*- coding: utf-8 -*-
"""
ÖzDil Geliştirici Araçları (ozpaket.py)
Paket oluşturma, test etme ve yayınlama öncesi zip paketleme araçlarını sağlar.
"""

import os
import sys
import json
import zipfile
import hashlib
import traceback

def show_help():
    print("=== ozpaket - ÖzDil Eklenti Geliştirici Araçları ===")
    print("Kullanım:")
    print("  python3 ozpaket.py oluştur <paket_adı> -> Yeni bir eklenti şablonu oluşturur")
    print("  python3 ozpaket.py test                -> Mevcut dizindeki test.oz dosyasını çalıştırarak paketi test eder")
    print("  python3 ozpaket.py paketle             -> Paketi yayınlanmaya hazır .zip dosyası haline getirir")
    print("  python3 ozpaket.py yardım              -> Yardım menüsünü gösterir")

def cmd_create(name):
    name = name.lower().strip()
    if os.path.exists(name):
        print(f"❌ Hata: '{name}' dizini zaten mevcut!")
        return
        
    os.makedirs(name, exist_ok=True)
    
    # 1. ozpaket.json
    meta = {
        "isim": name,
        "surum": "1.0.0",
        "yazar": "gelistirici",
        "tur": "python",
        "aciklama": "Yeni oluşturulmuş harika bir ÖzDil eklentisi.",
        "izinler": [],
        "bagimliliklar": []
    }
    with open(os.path.join(name, "ozpaket.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
        
    # 2. main.py
    main_py_content = f"""# -*- coding: utf-8 -*-
# {name} Eklentisi Giriş Dosyası
import plugin_api

def selam_ver(isim):
    \"\"\"
    ÖzDil içinden doğrudan 'selam_ver(\"Ahmet\")' olarak çağrılabilir.
    \"\"\"
    print(f"[Eklenti] Merhaba, {{isim}}!")
    return f"Selamla: {{isim}}"

def plugin():
    # Eklenti API'sine ekliyoruz
    plugin_api.plugin.fonksiyon_ekle("selam_ver", selam_ver)
    return {{
        "selam_ver": selam_ver
    }}
"""
    with open(os.path.join(name, "main.py"), "w", encoding="utf-8") as f:
        f.write(main_py_content)
        
    # 3. README.md
    readme_content = f"""# {name} ÖzDil Eklentisi

Bu eklenti ÖzDil eklenti ekosistemi için otomatik olarak oluşturulmuştur.

## Kullanım:

```ozdil
getir {name}

değişken sonuc = selam_ver("Dünya")
yazdır(sonuc)
```
"""
    with open(os.path.join(name, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)
        
    # 4. test.oz
    test_oz_content = f"""# {name} Eklentisi Otomatik Test Dosyası
getir {name}

değişken sonuc = selam_ver("ÖzDil Test")
yazdır("Dönen Değer: " + sonuc)
"""
    with open(os.path.join(name, "test.oz"), "w", encoding="utf-8") as f:
        f.write(test_oz_content)
        
    print(f"✨ Başarılı: '{name}' eklenti şablonu ve dosyaları başarıyla oluşturuldu!")

def cmd_test():
    if not os.path.isfile("ozpaket.json"):
        print("❌ Hata: Mevcut dizinde 'ozpaket.json' bulunamadı! Lütfen bir paket dizininde olduğunuzdan emin olun.")
        return
        
    if not os.path.isfile("test.oz"):
        print("❌ Hata: Test için 'test.oz' dosyası bulunamadı!")
        return
        
    print("🧪 Paket test ediliyor...")
    
    # ÖzDil interpreter'ını dinamik çağır
    try:
        # sys.path'e çalışma dizinini ekle
        sys.path.insert(0, os.path.abspath(".."))
        sys.path.insert(0, os.path.abspath("."))
        
        # compiler.py'ı import et
        import compiler
        
        with open("test.oz", "r", encoding="utf-8") as f:
            test_code = f.read()
            
        print("--- Çalıştırılan ÖzDil Test Kodu ---")
        print(test_code)
        print("-----------------------------------")
        
        res = compiler.run_code(test_code)
        if res.get("error"):
            print("❌ Test Başarısız Oldu!")
            print(res["error"])
        else:
            print("🟢 Test Başarıyla Tamamlandı!")
            print("Konsol Çıktısı:")
            print(res.get("output", ""))
            
    except Exception as e:
        print(f"❌ Test çalıştırılırken sistem hatası: {str(e)}")
        traceback.print_exc()

def cmd_pack():
    if not os.path.isfile("ozpaket.json"):
        print("❌ Hata: Mevcut dizinde 'ozpaket.json' bulunamadı!")
        return
        
    try:
        with open("ozpaket.json", "r", encoding="utf-8") as f:
            meta = json.load(f)
    except Exception as e:
        print(f"❌ Hata: 'ozpaket.json' okunamadı: {str(e)}")
        return
        
    name = meta.get("isim", "isimsiz")
    version = meta.get("surum", "1.0.0")
    zip_name = f"{name}-{version}.zip"
    
    print(f"📦 '{name}' paketi '{zip_name}' olarak paketleniyor...")
    
    # İmza hesapla
    sha = hashlib.sha256()
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, _, files in os.walk('.'):
            for file in files:
                if file == zip_name:
                    continue
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, '.')
                zip_file.write(file_path, rel_path)
                
                # Dosya içeriğini hashle (imza doğrulaması için)
                if file != "ozpaket.json":
                    try:
                        with open(file_path, "rb") as bf:
                            sha.update(rel_path.encode('utf-8'))
                            sha.update(bf.read())
                    except Exception:
                        pass
                        
    print(f"🔒 SHA256 İmzası: {sha.hexdigest()}")
    print(f"✨ Başarılı: Paket '{zip_name}' olarak başarıyla oluşturuldu! Dağıtıma hazır.")

def main():
    if len(sys.argv) < 2:
        show_help()
        return
        
    cmd = sys.argv[1].lower().strip()
    
    if cmd in ("oluştur", "olustur", "create"):
        if len(sys.argv) < 3:
            print("❌ Hata: Lütfen paket adını belirtin.")
            return
        cmd_create(sys.argv[2])
    elif cmd in ("test", "run"):
        cmd_test()
    elif cmd in ("paketle", "pack"):
        cmd_pack()
    elif cmd in ("yardım", "yardim", "help"):
        show_help()
    else:
        print(f"❌ Hata: Bilinmeyen komut: '{cmd}'")
        show_help()

if __name__ == "__main__":
    main()
