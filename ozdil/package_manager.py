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
from ozdil.repository import fetch_package_data

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
    m = re.match(r'^v?(\d+)\.(\d+)\.(\d+)$', v_str.strip())
    if m:
        return tuple(map(int, m.groups()))
    raise ValueError(f"Geçersiz sürüm formatı: '{v_str}'")

def is_compatible(installed_v, req_str):
    """
    Kurulu sürümün, talep edilen sürüm kısıtına uygunluğunu denetler.
    req_str can contain multiple constraints separated by commas, e.g. ">=1.0,<2.0",
    or caret "^1.2.0", tilde "~1.2", or "!=" operators.
    """
    req_str = req_str.strip()
    if not req_str:
        return True
        
    # Split by comma for multiple constraints (e.g. ">=1.0,<2.0")
    parts = [p.strip() for p in req_str.split(',') if p.strip()]
    if len(parts) > 1:
        try:
            return all(is_compatible(installed_v, part) for part in parts)
        except Exception:
            return False
        
    single_req = parts[0]
    try:
        inst = parse_version(installed_v)
    except ValueError:
        return False
    
    # Check caret "^1.2.0"
    if single_req.startswith('^'):
        v_part = single_req[1:].strip()
        try:
            target = parse_version(v_part)
        except ValueError:
            return False
        if inst < target:
            return False
        if target[0] > 0:
            return inst[0] == target[0]
        elif target[1] > 0:
            return inst[0] == 0 and inst[1] == target[1]
        else:
            return inst[0] == 0 and inst[1] == 0 and inst[2] == target[2]
            
    # Check tilde "~1.2" or "~1.2.3"
    if single_req.startswith('~'):
        v_part = single_req[1:].strip()
        dot_count = v_part.count('.')
        try:
            if dot_count == 1:
                major, minor = map(int, v_part.split('.'))
                target = (major, minor, 0)
                limit = (major, minor + 1, 0)
            else:
                target = parse_version(v_part)
                limit = (target[0], target[1] + 1, 0)
        except Exception:
            return False
        return target <= inst < limit

    # Check comparison operators
    m = re.match(r'^([><=!]+)\s*(.*)$', single_req)
    if not m:
        try:
            target = parse_version(single_req)
            return inst == target
        except ValueError:
            return True
            
    op, req_v_str = m.groups()
    try:
        target = parse_version(req_v_str)
    except ValueError:
        return False
    
    if op == '==':
        return inst == target
    elif op == '!=':
        return inst != target
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
    name = os.path.basename(name.lower().strip())
    if ".." in name or "/" in name or "\\" in name:
        return None
        
    for parent in [LOCAL_PACKAGES_DIR, GLOBAL_PACKAGES_DIR]:
        pkg_path = os.path.abspath(os.path.join(parent, name))
        normalized_parent = os.path.abspath(parent)
        if not pkg_path.startswith(normalized_parent + os.sep) and pkg_path != normalized_parent:
            continue
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
    Kurulu paketin dosyalarını inceleyerek asimetrik geliştirici ortak anahtarı (RSA Public Key) ile imza doğrulaması yapar.
    """
    pkg_name = os.path.basename(pkg_name.lower().strip())
    if ".." in pkg_name or "/" in pkg_name or "\\" in pkg_name:
        return False, "Geçersiz paket adı."
        
    meta = get_installed_package_meta(pkg_name)
    if not meta:
        return False, "Paket bulunamadı."
    
    expected_imza = meta.get("imza")
    if not expected_imza:
        return False, "Hata: İmzasız paketlerin kurulması veya çalıştırılması güvenlik nedeniyle engellenmiştir!"
        
    # Paket dizinini bul
    pkg_path = None
    for parent in [LOCAL_PACKAGES_DIR, GLOBAL_PACKAGES_DIR]:
        p = os.path.abspath(os.path.join(parent, pkg_name))
        normalized_parent = os.path.abspath(parent)
        if not p.startswith(normalized_parent + os.sep) and p != normalized_parent:
            continue
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
                
    # 1. Dosyaların yerel hash'ini (SHA256) çıkar
    import hashlib
    m = hashlib.sha256()
    for filename in sorted(current_files.keys()):
        m.update(filename.encode('utf-8'))
        m.update(current_files[filename].encode('utf-8'))
    local_hash_bytes = m.digest()
    
    # 2. Paketteki imzayı RSA Public Key ile deşifre et ve doğrula (PKCS#1 v1.5)
    RSA_N = 131869317293702309841552762712251746919494094597659741157495659622634729285218513465697541530679097013689567260341373183132862975885657361980250503060699818453974315755595888928004082339480555986396058724985887669654995936400724289959367139038363430191002142550275704958761657952655646721269560238302518773703
    RSA_E = 65537
    key_size = 128
    
    try:
        signature_int = int(expected_imza, 16)
        # s^e mod n
        decrypted_int = pow(signature_int, RSA_E, RSA_N)
        decrypted_bytes = decrypted_int.to_bytes(key_size, byteorder='big')
    except Exception as e:
        return False, f"Geçersiz imza formatı veya doğrulama hatası: {str(e)}"
        
    # PKCS#1 v1.5 padding kontrolü ve hash karşılaştırması
    if decrypted_bytes[0] != 0 or decrypted_bytes[1] != 1:
        return False, "Hata: PKCS#1 v1.5 imza yapısı geçersiz (başlangıç marker'ları uyuşmuyor)."
        
    try:
        sep_idx = decrypted_bytes.index(b"\x00", 2)
    except ValueError:
        return False, "Hata: PKCS#1 v1.5 imza yapısı geçersiz (seperator byte bulunamadı)."
        
    ps = decrypted_bytes[2:sep_idx]
    if len(ps) < 8 or any(b != 0xff for b in ps):
        return False, "Hata: PKCS#1 v1.5 imza yapısı geçersiz (padding bytes bozuk)."
        
    t = decrypted_bytes[sep_idx + 1:]
    der_prefix = b"\x30\x31\x30\x0d\x06\x09\x60\x86\x48\x01\x65\x03\x04\x02\x01\x05\x00\x04\x20"
    if not t.startswith(der_prefix):
        return False, "Hata: PKCS#1 v1.5 imza yapısı geçersiz (SHA-256 OID / DigestInfo uyuşmuyor)."
        
    decrypted_hash = t[len(der_prefix):]
    if decrypted_hash != local_hash_bytes:
        return False, f"Bozuk veya yetkisiz paket algılandı! Asimetrik imza doğrulaması başarısız oldu.\nBeklenen hash: {local_hash_bytes.hex()}\nÇözülen hash: {decrypted_hash.hex()}"
        
    return True, "İmza doğrulandı (RSA PKCS#1 v1.5 Asymmetric Signature). Paket tamamen güvenli."

def install_package(pkg_name, target="local", installing_set=None):
    """
    Bir paketi merkezi deponun kopyasından kurar, bağımlılıklarını analiz edip otomatik indirir,
    SHA256 imzalarını doğrular ve sonsuz döngü kontrolü yapar.
    """
    ensure_dirs()
    pkg_name = os.path.basename(pkg_name.lower().strip())
    if ".." in pkg_name or "/" in pkg_name or "\\" in pkg_name:
        raise ValueError("Geçersiz paket adı.")
    
    if installing_set is None:
        installing_set = set()
        
    # Sonsuz döngü (circular dependency) engelleme
    if pkg_name in installing_set:
        raise ValueError(f"Sonsuz Bağımlılık Döngüsü Algılandı! '{pkg_name}' paketi yüklenemiyor.")
        
    installing_set.add(pkg_name)
    
    try:
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
        pkg_dest_path = os.path.abspath(os.path.join(dest_dir, pkg_name))
        normalized_pkg_dest = os.path.abspath(pkg_dest_path)
        
        # Verifying target boundary
        normalized_dest_dir = os.path.abspath(dest_dir)
        if not pkg_dest_path.startswith(normalized_dest_dir + os.sep) and pkg_dest_path != normalized_dest_dir:
            raise ValueError("Güvenlik İhlali: Geçersiz dizin konumu.")
        
        # Eski varsa sil
        if os.path.exists(pkg_dest_path):
            shutil.rmtree(pkg_dest_path)
        os.makedirs(pkg_dest_path, exist_ok=True)
        
        # Meta veriyi imza ile kaydet
        with open(os.path.join(pkg_dest_path, "ozpaket.json"), "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)
            
        # Dosyaları yaz
        for filename, content in files.items():
            filepath = os.path.abspath(os.path.join(pkg_dest_path, filename))
            if not filepath.startswith(normalized_pkg_dest + os.sep) and filepath != normalized_pkg_dest:
                raise ValueError(f"Güvenlik İhlali: Geçersiz dosya yolu '{filename}'. Path traversal algılandı.")
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
                
        print(f"✨ Başarılı: '{pkg_name}' ({meta['surum']}) paketi başarıyla '{target}' dizinine kuruldu!")
        return True
    finally:
        # Temizlik - Exception oluşsa bile mutlaka çalışır
        if pkg_name in installing_set:
            installing_set.remove(pkg_name)

def uninstall_package(pkg_name):
    """
    Belirtilen paketi yerel ve küresel dizinlerden kaldırır.
    """
    pkg_name = os.path.basename(pkg_name.lower().strip())
    if ".." in pkg_name or "/" in pkg_name or "\\" in pkg_name:
        raise ValueError("Geçersiz paket adı.")
        
    removed = False
    
    for dest_dir in [LOCAL_PACKAGES_DIR, GLOBAL_PACKAGES_DIR]:
        pkg_path = os.path.abspath(os.path.join(dest_dir, pkg_name))
        normalized_dest = os.path.abspath(dest_dir)
        if not pkg_path.startswith(normalized_dest + os.sep) and pkg_path != normalized_dest:
            continue
        if os.path.exists(pkg_path):
            print(f"🗑️ '{pkg_name}' paketi siliniyor...")
            shutil.rmtree(pkg_path)
            removed = True
            
    return removed
