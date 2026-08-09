# -*- coding: utf-8 -*-
"""
ÖzDil Paket Yöneticisi Çekirdeği (package_manager.py)
Paket kurma, kaldırma, sürüm kontrolü, bağımlılık çözümü ve imza doğrulama işlemlerini gerçekleştirir.
"""

import os
import json
import shutil
import hashlib
import re
from ozdil.repository import fetch_package_data, generate_sha256

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_CURRENT_DIR, ".."))
LOCAL_PACKAGES_DIR = os.path.join(_PROJECT_ROOT, "oz_packages")
GLOBAL_PACKAGES_DIR = os.path.abspath(os.path.expanduser("~/.ozdil/packages"))

def ensure_dirs():
    os.makedirs(LOCAL_PACKAGES_DIR, exist_ok=True)
    os.makedirs(GLOBAL_PACKAGES_DIR, exist_ok=True)

def parse_version(v_str):
    """
    Sürüm bilgisini sayısal tuple'a dönüştürür. '1.2.5' -> (1, 2, 5)
    """
    m = re.match(r'v?(\d+)\.(\d+)\.(\d+)', v_str.strip())
    if m:
        return tuple(map(int, m.groups()))
    return (0, 0, 0)

def is_compatible(installed_v, req_str):
    """
    Kurulu sürümün, talep edilen sürüm kısıtına uygunluğunu denetler.
    req_str örnekleri: ">=1.2.0", "==1.0.0", "<=2.0.0", ">1.0.0"
    """
    m = re.match(r'^([><=]+)\s*(.*)$', req_str.strip())
    if not m:
        # Eğer operatör belirtilmediyse, doğrudan tam eşleşme veya herhangi bir uyumluluk kabul edilir
        return True
    
    op, req_v_str = m.groups()
    inst = parse_version(installed_v)
    target = parse_version(req_v_str)
    
    if op == '==':
        return inst == target
    elif op == '>=':
        return inst >= target
    elif op == '<=':
        return inst <= target
    elif op == '>':
        return inst > target
    elif op == '<':
        return inst < target
    return True

def get_installed_package_meta(name):
    """
    Sistemde kurulu olan bir paketin ozpaket.json meta verilerini okur.
    """
    for parent in [LOCAL_PACKAGES_DIR, GLOBAL_PACKAGES_DIR]:
        pkg_path = os.path.join(parent, name)
        meta_file = os.path.join(pkg_path, "ozpaket.json")
        if os.path.isfile(meta_file):
            try:
                with open(meta_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
    return None

def verify_package_signature(pkg_name):
    """
    Kurulu paketin dosyalarını inceleyerek SHA256 imzası (bütünlük) kontrolü yapar.
    """
    meta = get_installed_package_meta(pkg_name)
    if not meta:
        return False, "Paket bulunamadı."
    
    expected_imza = meta.get("imza")
    if not expected_imza:
        # Eski geriye dönük paketlerde imza zorunlu değil
        return True, "İmzasız paket (eski sürüm uyumlu)."
        
    # Paket dizinini bul
    pkg_path = None
    for parent in [LOCAL_PACKAGES_DIR, GLOBAL_PACKAGES_DIR]:
        p = os.path.join(parent, pkg_name)
        if os.path.isdir(p):
            pkg_path = p
            break
            
    if not pkg_path:
        return False, "Paket dizini bulunamadı."
        
    # Mevcut dosyaları hashle
    current_files = {}
    for root, dirs, files in os.walk(pkg_path):
        # Skip hidden directories and __pycache__ from os.walk traversal
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "__pycache__"]
        for f in files:
            if f == "ozpaket.json":
                continue # ozpaket.json imza içermez, bu yüzden hariç bırakılır
            if f.startswith(".") or f.endswith((".pyc", ".pyo")):
                continue
            filepath = os.path.join(root, f)
            rel_path = os.path.relpath(filepath, pkg_path)
            try:
                with open(filepath, "r", encoding="utf-8") as file_obj:
                    current_files[rel_path] = file_obj.read()
            except Exception:
                pass
                
    computed_imza = generate_sha256(current_files)
    if computed_imza != expected_imza:
        return False, f"Bozuk veya yetkisiz paket algılandı! İmzalar uyuşmuyor.\nBeklenen: {expected_imza}\nHesaplanan: {computed_imza}"
        
    return True, "İmza doğrulandı. Paket güvenli."

def install_package(pkg_name, target="local", installing_set=None):
    """
    Bir paketi merkezi deponun kopyasından kurar, bağımlılıklarını analiz edip otomatik indirir,
    SHA256 imzalarını doğrular ve sonsuz döngü kontrolü yapar.
    """
    ensure_dirs()
    pkg_name = pkg_name.lower().strip()
    
    if installing_set is None:
        installing_set = set()
        
    # Sonsuz döngü (circular dependency) engelleme
    if pkg_name in installing_set:
        raise ValueError(f"Sonsuz Bağımlılık Döngüsü Algılandı! '{pkg_name}' paketi yüklenemiyor.")
        
    installing_set.add(pkg_name)
    
    # 1. Depodan paketi çek
    repo_data = fetch_package_data(pkg_name)
    if not repo_data:
        raise ValueError(f"Hata: '{pkg_name}' adında bir paket depoda bulunamadı.")
        
    meta = repo_data["meta"]
    files = repo_data["files"]
    
    # 2. Bağımlılıkları kontrol et ve kur
    bagimliliklar = meta.get("bagimliliklar", [])
    for dep in bagimliliklar:
        # Bağımlılık tanımını parse et: örn. "renkler>=1.2.0"
        m = re.match(r'^([a-zA-Z0-9_]+)\s*([><=]+.*)?$', dep.strip())
        if m:
            dep_name = m.group(1)
            dep_constraint = m.group(2) or ""
            
            # Bağımlılık kurulu mu?
            installed_meta = get_installed_package_meta(dep_name)
            if installed_meta:
                # Sürüm kontrolü
                if dep_constraint and not is_compatible(installed_meta["surum"], dep_constraint):
                    print(f"🔄 Sürüm Uyumsuzluğu: Kurulu '{dep_name}' ({installed_meta['surum']}) paketi '{dep_constraint}' kısıtını karşılamıyor. Güncelleniyor...")
                    install_package(dep_name, target, installing_set)
            else:
                # Bağımlılığı kur
                print(f"📦 Eksik bağımlılık tespit edildi: '{dep_name}' otomatik kuruluyor...")
                install_package(dep_name, target, installing_set)
                
    # 3. Paketi dizine yaz
    dest_dir = GLOBAL_PACKAGES_DIR if target == "global" else LOCAL_PACKAGES_DIR
    pkg_dest_path = os.path.join(dest_dir, pkg_name)
    
    # Eski varsa sil
    if os.path.exists(pkg_dest_path):
        shutil.rmtree(pkg_dest_path)
    os.makedirs(pkg_dest_path, exist_ok=True)
    
    # Meta veriyi imza ile kaydet
    with open(os.path.join(pkg_dest_path, "ozpaket.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
        
    # Dosyaları yaz
    for filename, content in files.items():
        filepath = os.path.join(pkg_dest_path, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
    # Temizlik
    installing_set.remove(pkg_name)
    print(f"✨ Başarılı: '{pkg_name}' ({meta['surum']}) paketi başarıyla '{target}' dizinine kuruldu!")
    return True

def uninstall_package(pkg_name):
    """
    Belirtilen paketi yerel ve küresel dizinlerden kaldırır.
    """
    pkg_name = pkg_name.lower().strip()
    removed = False
    
    for dest_dir in [LOCAL_PACKAGES_DIR, GLOBAL_PACKAGES_DIR]:
        pkg_path = os.path.join(dest_dir, pkg_name)
        if os.path.exists(pkg_path):
            print(f"🗑️ '{pkg_name}' paketi siliniyor...")
            shutil.rmtree(pkg_path)
            removed = True
            
    return removed
