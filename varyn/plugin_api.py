# -*- coding: utf-8 -*-
"""
Varyn Eklenti ve Olay (Event) API Sistemi (plugin_api.py)
Bu modül, Python eklentilerinin Varyn interpreter'ına dinamik fonksiyon, komut ve
olay dinleyicileri (event handlers) eklemesini sağlayan merkezi plugin arabirimidir.
"""

import sys
import threading

class PluginAPI:
    def __init__(self):
        # Kayıtlı özel fonksiyonlar: Varyn içinden doğrudan çağrılabilir
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
        self.current_program = None

    def fonksiyon_ekle(self, name, func):
        """
        Varyn interpreter'ına yeni bir genel fonksiyon ekler.
        Kullanım: plugin.fonksiyon_ekle("selamla", selamla_fonksiyonu)
        """
        self.functions[name] = func

    def komut_ekle(self, name, func):
        """
        Varyn interpreter'ına yeni bir özel komut ekler.
        """
        self.commands[name] = func

    def event_ekle(self, event_name, func):
        """
        Varyn çalışma zamanı olaylarına dinleyici ekler.
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
                func(*args, **kwargs)

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
        self.current_program = None

class PluginAPIProxy:
    _local = threading.local()

    @classmethod
    def get_current(cls):
        if not hasattr(cls._local, "active_api"):
            cls._local.active_api = PluginAPI()
        return cls._local.active_api

    @classmethod
    def set_current(cls, api):
        cls._local.active_api = api

    def __getattr__(self, name):
        return getattr(self.get_current(), name)

    def __setattr__(self, name, value):
        setattr(self.get_current(), name, value)

# Global proxy nesne. Python eklentileri bu nesneyi 'import plugin_api' diyerek kullanır.
plugin = PluginAPIProxy()
