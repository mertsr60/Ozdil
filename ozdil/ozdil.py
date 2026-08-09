# -*- coding: utf-8 -*-
"""
ÖzDil Interpreter Köprüsü (ozdil.py)
Bu dosya, kök dizindeki compiler.py modülüne bağlanarak ÖzDil dilinin tüm çekirdek
bileşenlerini tek bir yerden paket halinde dışa aktarır.
"""

import sys
import os

# Kök dizini sys.path içerisine ekleyerek compiler.py'a erişimi sağlıyoruz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    import compiler
    
    # Tüm çekirdek sınıfları ve fonksiyonları dışa aktarıyoruz
    OzdilError = compiler.OzdilError
    run_code = compiler.run_code
    Interpreter = compiler.Interpreter
    Parser = compiler.Parser
    lex_ozdil = compiler.lex_ozdil
    Token = compiler.Token
    Environment = compiler.Environment
except ImportError:
    pass
