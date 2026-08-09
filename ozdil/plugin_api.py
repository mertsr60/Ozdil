# -*- coding: utf-8 -*-
"""
ÖzDil Eklenti ve Olay (Event) API Sistemi (plugin_api.py)
Bu modül, Python eklentilerinin ÖzDil interpreter'ına dinamik fonksiyon, komut ve
olay dinleyicileri (event handlers) eklemesini sağlayan merkezi plugin arabirimidir.
"""

import sys

class PluginAPI:
    def __init__(self):
        # Kayıtlı özel fonksiyonlar: ÖzDil içinden doğrudan çağrılabilir
        self.functions = {}
        # Kayıtlı özel komutlar
        self.commands = {}
        # Olay (Event) dinleyicileri
        self.events = {
            "program_basladi": [],
            "paket_yuklendi": [],
            "hata_olustu": [],
            "program_bitti": []
        }
        # Telefon GUI Elementleri
        self.gui_elements = []
        self.current_page = None

    def fonksiyon_ekle(self, name, func):
        """
        ÖzDil interpreter'ına yeni bir genel fonksiyon ekler.
        Kullanım: plugin.fonksiyon_ekle("selamla", selamla_fonksiyonu)
        """
        self.functions[name] = func

    def komut_ekle(self, name, func):
        """
        ÖzDil interpreter'ına yeni bir özel komut ekler.
        """
        self.commands[name] = func

    def event_ekle(self, event_name, func):
        """
        ÖzDil çalışma zamanı olaylarına dinleyici ekler.
        """
        if event_name not in self.events:
            self.events[event_name] = []
        self.events[event_name].append(func)

    def trigger_event(self, event_name, *args, **kwargs):
        """
        Kayıtlı olay tetikleyicilerini sırayla çalıştırır.
        """
        if event_name in self.events:
            for func in self.events[event_name]:
                try:
                    func(*args, **kwargs)
                except Exception as e:
                    print(f"[Plugin API Hata] '{event_name}' olayı tetiklenirken hata oluştu: {str(e)}", file=sys.stderr)

    def clear(self):
        """
        Her yeni program çalışmasında eklentileri temizler/resetler.
        """
        self.functions.clear()
        self.commands.clear()
        for k in self.events.keys():
            self.events[k] = []
        self.gui_elements.clear()
        self.current_page = None

# Global tekil (singleton) nesne. Python eklentileri bu nesneyi 'import plugin_api' diyerek kullanır.
plugin = PluginAPI()
