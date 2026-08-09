# -*- coding: utf-8 -*-
import unittest
import sys
import os

def run_all_tests():
    print("==================================================")
    print("      ÖzDil Automated Test Suite Runner           ")
    print("==================================================")
    
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=os.path.dirname(__file__), pattern="test_*.py")
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n--------------------------------------------------")
    print(f"Testler Tamamlandı.")
    print(f"Çalıştırılan Test Sayısı: {result.testsRun}")
    print(f"Başarısızlıklar: {len(result.failures)}")
    print(f"Hatalar: {len(result.errors)}")
    print("--------------------------------------------------")
    
    # If successful, exit with code 0, else 1
    if result.wasSuccessful():
        print("✓ BÜTÜN TESTLER BAŞARIYLA GEÇTİ!")
        return True
    else:
        print("🚨 BAZI TESTLER BAŞARISIZ OLDU!")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
