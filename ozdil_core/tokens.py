# -*- coding: utf-8 -*-

class Token:
    def __init__(self, type_, value, lineno, col):
        self.type = type_
        self.value = value
        self.lineno = lineno
        self.col = col
        
    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, {self.lineno}:{self.col})"

OZDIL_KEYWORDS = {
    'eğer', 'eger', 'değişken_eğer', 'degilse_eger', 'değilse_eğer', 'degilse_eğer', 'değilse_eger', 
    'değilse', 'degilse', 'iken', 'döngü', 'dongu', 'her', 'işlem', 'islem', 'fonksiyon', 
    'döndür', 'dondur', 'doğru', 'dogru', 'yanlış', 'yanlis', 've', 'veya', 'değil', 'degil', 
    'içinde', 'icinde', 'in', 'getir', 'dur', 'devam_et', 'yok', 'boş', 'bos', 
    'değişken', 'degisken', 'sabit', 'tam_sayı', 'tam_sayi', 'ondalık', 'ondalik', 
    'metin', 'liste', 'sözlük', 'sozluk', 'break', 'continue', 'and', 'or', 'not',
    'sinif', 'sınıf', 'class', 'dene', 'try', 'hata_yakala', 'except', 'olarak', 'as'
}
