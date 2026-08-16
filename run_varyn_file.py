# -*- coding: utf-8 -*-
import sys
import json
from compiler import run_code

if len(sys.argv) < 2:
    print("Kullanım: python3 run_varyn_file.py <dosya_adı.varyn>")
    sys.exit(1)

filename = sys.argv[1]
try:
    with open(filename, 'r', encoding='utf-8') as f:
        code = f.read()
except Exception as e:
    print(f"Dosya okuma hatası: {e}")
    sys.exit(1)

result = run_code(code)
if result.get("output"):
    print("--- ÇIKTI ---")
    print(result["output"])
if result.get("error"):
    print("--- HATA ---")
    print(result["error"])
