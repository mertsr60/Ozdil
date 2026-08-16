# -*- coding: utf-8 -*-
"""
ÖzDil / Varyn Yetkilendirme ve Capability Modeli (capabilities.py)
Bu modül, VM ve interpreter için güvenlik yetki sınırlarını ve misafir ortamı değişkenlerini tanımlar.
"""

from enum import Enum
from .errors import VarynError

class Capability:
    NONE = "hicbiri"
    FILESYSTEM = "dosya_sistemi"
    FILESYSTEM_READ = "dosya_oku"
    FILESYSTEM_WRITE = "dosya_yaz"
    NETWORK = "ag"
    ENV_VARS = "cevre"
    SYSTEM_INFO = "sistem_bilgisi"
    PROCESS = "sistem"

# Varsayılan güvenli misafir ortam değişkenleri (asla host os.environ veya API key sızdırmaz)
DEFAULT_GUEST_ENV = {
    "VARYN_VERSION": "1.0.0",
    "VARYN_ENV": "sandbox",
    "OZ_DIL": "1"
}

class ResourceLimits:
    """
    VM ve Yorumlayıcı için DoS ve kaynak tükenmesini önleme sınırları.
    """
    def __init__(
        self,
        max_instructions=500_000,
        max_call_depth=500,
        max_execution_time_sec=5.0,
        max_string_length=1_000_000,
        max_collection_size=100_000
    ):
        self.max_instructions = max_instructions
        self.max_call_depth = max_call_depth
        self.max_execution_time_sec = max_execution_time_sec
        self.max_string_length = max_string_length
        self.max_collection_size = max_collection_size

class SecurityContext:
    """
    Her VM veya Yorumlayıcı çalıştırması için bağımsız güvenlik ve yetki bağlamı.
    """
    def __init__(self, capabilities=None, limits=None, guest_env=None):
        # Varsayılan olarak tüm tehlikeli yetkiler kapalıdır (DENY ALL BY DEFAULT)
        if capabilities is None:
            self.capabilities = set()
        elif isinstance(capabilities, (list, tuple, set)):
            self.capabilities = set(capabilities)
        elif isinstance(capabilities, str):
            self.capabilities = {capabilities}
        else:
            self.capabilities = set()
            
        self.limits = limits or ResourceLimits()
        self.guest_env = dict(guest_env or DEFAULT_GUEST_ENV)
        
    def has_capability(self, cap):
        if Capability.FILESYSTEM in self.capabilities:
            if cap in (Capability.FILESYSTEM_READ, Capability.FILESYSTEM_WRITE):
                return True
        return cap in self.capabilities
        
    def require_capability(self, cap, lineno=1, action_description="Bu işlem"):
        if not self.has_capability(cap):
            raise VarynError(
                "Yetki Hatası (PermissionError)",
                f"Güvenlik İhlali: {action_description} için '{cap}' izni gereklidir.",
                lineno
            )
