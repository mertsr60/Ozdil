# -*- coding: utf-8 -*-
"""
varynpip CLI (varynpip.py)
Varyn Paket Yöneticisi Komut Satırı Arayüzü.
"""

import sys
import os
import json
import time

from varyn.package_manager import (
    install_package,
    uninstall_package,
    get_installed_package_meta,
    verify_package_signature,
    LOCAL_PACKAGES_DIR,
    GLOBAL_PACKAGES_DIR
)
from varyn.repository import get_repository_json, fetch_package_data

def show_help():
    print("=== varynpip - Varyn Paket Yöneticisi ===")
    print("Kullanım:")
    print("  python3 varynpip.py yükle <paket_adı>    (veya install)   -> Paketi kurar ve bağımlılıklarını çözer")
    print("  python3 varynpip.py kaldır <paket_adı>   (veya uninstall) -> Paketi sistemden kaldırır")
    print("  python3 varynpip.py liste                (veya list)      -> Kurulu paketleri listeler ve imza doğrular")
    print("  python3 varynpip.py bilgi <paket_adı>    (veya info)      -> Paket detaylarını görüntüler")
    print("  python3 varynpip.py güncelle <paket_adı> (veya update)    -> Paketi son sürüme günceller")
    print("  python3 varynpip.py ara <kelime>         (veya search)    -> Paket deposunda arama yapar")
    print("  python3 varynpip.py yardım               (veya help)      -> Bu menüyü gösterir")

def cli_install(name):
    name = name.lower().strip()
    print(f"📦 '{name}' paketi indiriliyor...")
    
    # İndirme animasyonu simülasyonu
    width = 30
    for i in range(width + 1):
        percent = int((i / width) * 100)
        bar = "█" * i + "░" * (width - i)
        print(f"\r[{bar}] {percent}% Tamamlandı", end="", flush=True)
        time.sleep(0.01)
    print()
    
    try:
        install_package(name, target="local")
    except Exception as e:
        print(f"❌ Hata: {str(e)}")
        sys.exit(1)

def cli_uninstall(name):
    name = name.lower().strip()
    if uninstall_package(name):
        print(f"✨ Başarılı: '{name}' paketi sistemden tamamen kaldırıldı.")
    else:
        print(f"⚠️ Hata: Sistemde kurulu '{name}' paketi bulunamadı.")

def cli_list():
    print("=== Kurulu Varyn Paketleri ===")
    print(f"Yerel Dizin  : {LOCAL_PACKAGES_DIR}")
    print(f"Küresel Dizin: {GLOBAL_PACKAGES_DIR}")
    print("-" * 50)
    
    found_any = False
    for parent, label in [(LOCAL_PACKAGES_DIR, "Yerel"), (GLOBAL_PACKAGES_DIR, "Küresel")]:
        if not os.path.exists(parent):
            continue
        folders = [f for f in os.listdir(parent) if os.path.isdir(os.path.join(parent, f))]
        
        for folder in sorted(folders):
            meta = get_installed_package_meta(folder)
            if meta:
                # İmza ve bütünlük doğrulaması
                sig_ok, sig_msg = verify_package_signature(folder)
                sig_badge = "✅ GÜVENLİ" if sig_ok else "🚨 BOZUK/YETKİSİZ"
                
                print(f"📍 [{label}] {meta['isim']} ({meta['surum']}) - Yazar: {meta['yazar']} [{meta['tur'].upper()}] - {sig_badge}")
                print(f"   Açıklama: {meta.get('aciklama', 'Yok')}")
                if meta.get("bagimliliklar"):
                    print(f"   Bağımlılıklar: {', '.join(meta['bagimliliklar'])}")
                if not sig_ok:
                    print(f"   ⚠️  UYARI: {sig_msg}")
                print("-" * 40)
                found_any = True
                
    if not found_any:
        print("ℹ️ Henüz kurulu paket bulunmuyor.")

def cli_info(name):
    name = name.lower().strip()
    
    # Önce kurulu mu kontrol et
    meta = get_installed_package_meta(name)
    is_installed = "Evet" if meta else "Hayır"
    
    # Yoksa depodan oku
    if not meta:
        repo_data = fetch_package_data(name)
        if repo_data:
            meta = repo_data["meta"]
            
    if not meta:
        print(f"❌ Hata: '{name}' adında bir paket bulunamadı.")
        return
        
    print(f"=== Paket Bilgisi: {meta['isim']} ===")
    print(f"Sürüm          : {meta['surum']}")
    print(f"Tür            : {meta['tur'].upper()}")
    print(f"Yazar          : {meta['yazar']}")
    print(f"Sistemde Kurulu: {is_installed}")
    print(f"Açıklama       : {meta.get('aciklama', 'Yok')}")
    if meta.get("bagimliliklar"):
        print(f"Bağımlılıklar  : {', '.join(meta['bagimliliklar'])}")
    if meta.get("izinler"):
        print(f"İzin Yetkileri : {', '.join(meta['izinler'])}")
    if meta.get("imza"):
        print(f"SHA256 İmzası  : {meta['imza']}")
    print("-" * 40)

def cli_update(name):
    name = name.lower().strip()
    print(f"🔄 '{name}' paketi güncelleniyor...")
    uninstall_package(name)
    cli_install(name)

def cli_search(query):
    query = query.lower().strip()
    print(f"=== Paket Arama Sonuçları ('{query}') ===")
    print("-" * 50)
    
    repo_json = get_repository_json()
    found_any = False
    
    for pkg in repo_json["paketler"]:
        if query in pkg["isim"].lower() or query in pkg["aciklama"].lower():
            print(f"📦 {pkg['isim']} ({pkg['surum']}) - Yazar: {pkg['yazar']} [{pkg['tur'].upper()}]")
            print(f"   Açıklama: {pkg['aciklama']}")
            if pkg.get("bagimliliklar"):
                print(f"   Bağımlılıklar: {', '.join(pkg['bagimliliklar'])}")
            print("-" * 40)
            found_any = True
            
    if not found_any:
        print("ℹ️ Eşleşen bir paket bulunamadı.")

def main():
    if len(sys.argv) < 2:
        show_help()
        return
        
    cmd = sys.argv[1].lower().strip()
    
    if cmd in ("yükle", "yukle", "install"):
        if len(sys.argv) < 3:
            print("❌ Hata: Lütfen kurulacak paket adını girin.")
            return
        cli_install(sys.argv[2])
    elif cmd in ("kaldır", "kaldir", "uninstall"):
        if len(sys.argv) < 3:
            print("❌ Hata: Lütfen kaldırılacak paket adını girin.")
            return
        cli_uninstall(sys.argv[2])
    elif cmd in ("liste", "list"):
        cli_list()
    elif cmd in ("bilgi", "info"):
        if len(sys.argv) < 3:
            print("❌ Hata: Lütfen paket adını belirtin.")
            return
        cli_info(sys.argv[2])
    elif cmd in ("güncelle", "guncelle", "update"):
        if len(sys.argv) < 3:
            print("❌ Hata: Lütfen güncellenecek paket adını belirtin.")
            return
        cli_update(sys.argv[2])
    elif cmd in ("ara", "search"):
        q = sys.argv[2] if len(sys.argv) > 2 else ""
        cli_search(q)
    elif cmd in ("yardım", "yardim", "help"):
        show_help()
    else:
        print(f"❌ Hata: Geçersiz komut: '{cmd}'")
        show_help()

if __name__ == "__main__":
    main()
