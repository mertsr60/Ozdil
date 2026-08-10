# Varyn CPython Bağımlılık Envanteri (CPython Dependency Inventory)

Bu belge, Varyn programlama dilinin mevcut sürümünde CPython çalışma ortamına ve Python standart kütüphanelerine olan tüm bağımlılıklarını detaylı bir şekilde listeler. Varyn'in tamamen bağımsız bir VM ve derleyici mimarisine geçişi (Self-Hosted Compiler & Custom VM) bu envantere dayalı olarak gerçekleştirilecektir.

---

## 1. Çalıştırma Motoru ve Dinamik Kod Çalıştırma (Execution & Dynamic Eval)
Mevcut Varyn yorumlayıcısı, programları doğrudan Python nesneleri ve fonksiyonları olarak yürütür.

*   **`exec()` ve `eval()` Fonksiyonları:**
    *   **Kullanım Amacı:** `getir` (import) anahtar kelimesiyle çağrılan Python tabanlı eklentilerin (`.py` dosyaları) dinamik olarak yüklenmesi ve yürütülmesi için kullanılır.
    *   **Dosya Konumu:** `/varyn_core/interpreter.py` (Satır ~507)
    *   **CPython Bağımlılığı:** Python'ın dahili derleyicisi ve çalışma zamanı (runtime) ortamı.
*   **AST (Abstract Syntax Tree) İşleme:**
    *   **Durum:** Varyn'in parser'ı tamamen `/varyn_core/ast_nodes.py` içinde tanımlanan özel Varyn sınıflarını (`Program`, `Atama`, `Eger` vb.) üretir. CPython'ın `ast` kütüphanesine doğrudan bir bağımlılık yoktur (önceki literal_eval bağımlılıkları tamamen temizlenmiştir).
*   **Geliştirici Sınıf ve Metot Tanımları:**
    *   **Kullanım Amacı:** `OzClass` ve `OzInstance` sınıfları Python'ın `__call__`, `__getattr__` ve `__setattr__` gibi sihirli metotlarına (magic methods) dayanarak çalışır.
    *   **Dosya Konumu:** `/varyn_core/interpreter.py` (Satır ~94-130)

---

## 2. Veri Tipleri ve Değer Temsili (Data Types & Value Models)
Varyn veri tipleri, doğrudan Python'ın temel sınıfları (primitive types) üzerine kuruludur.

*   **Python `int`, `float`, `str`, `bool` Kullanımı:**
    *   `Deger` (Literal) düğümü ve tüm matematiksel/mantıksal işlemler doğrudan Python'ın gömülü sınıflarını kullanır (`float(tok.value)` vb.).
    *   Aritmetik ve mantıksal operatörler (`+`, `-`, `*`, `/`, `veya`, `ve`) Python seviyesindeki işleçlerle çözümlenir.
*   **Python `list` ve `dict` Kullanımı:**
    *   Varyn dizileri (Liste) ve sözlükleri (Sözlük) doğrudan Python `list` ve `dict` veri modellerini kullanır.
    *   `ekle`, `çıkar`, `sırala`, `temizle` gibi yöntemler, Python yansıma (reflection) API'si (`getattr`) ile doğrudan Python listesi/sözlüğü metotlarına yönlendirilir.

---

## 3. Güvenlik, Yalıtım ve İşletim Sistemi Sınırları (Sandbox & OS Isolation)
Varyn, kütüphane ve eklenti paketlerinin güvenliğini sağlamak için CPython ve işletim sistemi yeteneklerini harmanlar.

*   **Subprocess Sandbox (`run_in_subprocess_sandbox`):**
    *   **Kullanım Amacı:** Eklentileri ve güvenli olmayan kodları ayrı bir Python sürecinde (CPython binary) çalıştırarak ana sunucudan yalıtır.
    *   **Kullanılan Kütüphaneler:** `subprocess`, `sys`, `resource` (Unix-specific kaynak sınırlama).
    *   **Dosya Konumu:** `/varyn/sandbox.py` (Satır ~183+)
*   **Kaynak Sınırlama (`resource` modülü):**
    *   **Kullanım Amacı:** CPU zamanı (`RLIMIT_CPU`), Bellek (`RLIMIT_AS`), süreç sayısı (`RLIMIT_NPROC`) ve dosya tanımlayıcı (`RLIMIT_NOFILE`) sınırları koyar. Bu kütüphane tamamen POSIX işletim sistemlerine ve Python'ın bu kütüphaneyi sarmalayan C-bağlantılarına dayanır.
*   **Python AST-tabanlı Güvenlik Süzgeci (`verify_python_code`):**
    *   **Kullanım Amacı:** Eklenti kodlarındaki Python AST'sini (`ast.parse`) inceleyerek `eval`, `exec`, `__subclasses__` gibi yansımaları ve yetkisiz modül yüklemelerini (import os) bloklar.

---

## 4. Paket Yönetimi ve Kriptografik İmzalama (Package Manager & Signing)
Varyn paket sistemi, paketlerin orijinalliğini ve bütünlüğünü doğrulamak için asimetrik şifreleme kullanır.

*   **Kriptografik Araçlar (`hashlib`):**
    *   **Kullanım Amacı:** SHA-256 hash alma ve RSA PKCS#1 v1.5 padding işlemlerinde Python standart `hashlib` kütüphanesini kullanır.
    *   **Dosya Konumu:** `/varyn/repository.py`, `/varyn/package_manager.py`
*   **RSA Asimetrik İmzalama:**
    *   İmzalama ve doğrulama işlemleri büyük tam sayılarla üst alma (`pow(block, RSA_D, RSA_N)`) aritmetiğine dayanır. Bu, Python'ın sınırsız duyarlıklı tam sayı (arbitrary-precision integer) desteğini kullanır.

---

## 5. Standart Kütüphane Bağımlılıkları (Standard Library Dependencies)
Varyn'in yerel kütüphaneleri, CPython standart kütüphanelerinin sarmalanmasıyla oluşturulmuştur.

*   **`matematik` Kütüphanesi:** Python `math` modülüne bağımlıdır (`sin`, `cos`, `sqrt` vb.).
*   **`rastgele` Kütüphanesi:** Python `random` modülüne bağımlıdır (`randint`, `random` vb.).
*   **`zaman` Kütüphanesi:** Python `time` modülüne bağımlıdır (`sleep`, `time` vb.).

---

## 6. Native Runtime Geçiş Planı (Migration Blueprint) - TAMAMLANDI (COMPLETED)
CPython bağımlılığını aşamalı olarak kaldırmak için tasarlanan ve uygulanan mimari başarıyla tamamlanmıştır:

1.  **Aşama 1 (Veri Temsili - TAMAMLANDI):** `/varyn_core/runtime_types.py` dosyası oluşturulmuş; `OzValue` temel sınıfı altında `OzInt`, `OzFloat`, `OzString`, `OzBool`, `OzList`, `OzMap`, `OzFunction`, `OzClass`, `OzInstance`, `OzBoundMethod` ve `OzNativeCallable` sınıfları tasarlanarak tamamen Python nesnelerinden izole edilmiştir.
2.  **Aşama 2 (Yürütme Motoru - TAMAMLANDI):** Varyn AST düğümlerini doğrudan Python yansımalarıyla değil, Varyn'e ait runtime tipleriyle çalıştıran yeni yürütme katmanı tamamlanmıştır.
3.  **Aşama 3 (Environment/Scope - TAMAMLANDI):** `/varyn_core/environment.py` içindeki semantic scope katmanı, hem eski CPython tabanlı yorumlayıcıyı hem de yeni VM'i destekleyecek şekilde güncellenerek lexical scope ve closure davranışları stabilize edilmiştir.
4.  **Aşama 4 (Varyn Bytecode & VM - TAMAMLANDI):**
    *   **Derleyici (`/varyn_core/bytecode_compiler.py`):** AST düğümlerini ziyaret edip optimize edilmiş yığın tabanlı instruction set'e (`LOAD_CONST`, `STORE_VAR`, `CALL`, `JUMP`, `SETUP_EXCEPT` vb.) çeviren bytecode derleyicisi yazılmıştır.
    *   **Sanal Makine (`/varyn_core/vm.py`):** Activation frame'leri, call-stack yapılarını, lokal/global değişken çözümlemelerini ve exception handling mekanizmasını barındıran tam teşekküllü sanal makine (Varyn VM) tamamlanmıştır.
    *   **Çift Yönlü Test Doğrulaması (`/tests/test_interpreter.py`):** Tüm test programları hem eski AST yorumlayıcısı hem de yeni Bytecode VM üzerinde çalıştırılmakta, çıktılar karakteri karakterine doğrulanmaktadır.
    *   **Uyum Katmanı (`/compiler.py`):** Ana CLI ve web arayüzü tetikleyicileri, yeni VM'i varsayılan olarak çalıştıracak şekilde sarmalanmıştır (geriye dönük uyumluluk için `VARYN_USE_LEGACY_INTERPRETER=1` fallback desteği korunmuştur).
