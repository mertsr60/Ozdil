import React, { useState, useEffect, useRef } from "react";
import {
  Terminal,
  BookOpen,
  Layers,
  Globe,
  RefreshCw,
  Moon,
  Sun,
  ChevronRight,
  ChevronDown,
  Info,
  X,
  Code,
  Sparkles,
  Play,
  Copy,
  Check,
  Download,
  Settings,
  Search,
  Folder,
  FolderOpen,
  FileCode2,
  Trash2,
  Maximize2,
  Minimize2,
  HelpCircle,
  Bug,
  Cpu,
  AlertTriangle,
  Lightbulb,
  CornerDownRight,
  Sparkle,
  RotateCcw,
  Menu,
  Smartphone,
  ToggleLeft,
  Home,
  User,
  Heart,
  Bell,
  Trash,
  Mail,
  Star,
  MapPin,
  Camera,
  Calendar,
  Compass,
  ShoppingCart,
  Video,
  Music
} from "lucide-react";
import CodeEditor from "./components/CodeEditor";
import ASTViewer from "./components/ASTViewer";
import { KEYWORDS, EXAMPLES } from "./constants";
import { CompilerResult } from "./types";

export default function App() {
  const [code, setCode] = useState<string>(EXAMPLES[0].code);
  const [results, setResults] = useState<CompilerResult>({
    translated: "",
    ast: null,
    output: "",
    error: null
  });
  const [isRunning, setIsRunning] = useState(false);
  const [isExporting, setIsExporting] = useState(false);
  const [showExportDropdown, setShowExportDropdown] = useState(false);
  const [isDark, setIsDark] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  
  // VS Code IDE State managers
  const [sidebarTab, setSidebarTab] = useState<"explorer" | "search" | "run" | "docs" | "packages" | null>("explorer");
  const [panelTab, setPanelTab] = useState<"terminal" | "python" | "ast">("terminal");
  const [panelHeight, setPanelHeight] = useState<"collapsed" | "normal" | "maximized">("normal");
  
  // ozpip package manager state
  const [packages, setPackages] = useState<any[]>([]);
  const [loadingPackages, setLoadingPackages] = useState(false);
  const [packageOutput, setPackageOutput] = useState<string>("");
  const [packageSearchQuery, setPackageSearchQuery] = useState("");
  const [activePackageTab, setActivePackageTab] = useState<"all" | "installed">("all");
  
  // File System State (Open tabs in the editor)
  const [openTabs, setOpenTabs] = useState<string[]>(["kod_alani.oz", "BENI_OKU.md"]);
  const [activeFile, setActiveFile] = useState<string>("kod_alani.oz");
  
  // Sidebar folders toggle
  const [folderExamplesExpanded, setFolderExamplesExpanded] = useState(true);
  const [folderRootExpanded, setFolderRootExpanded] = useState(true);
  
  // Search state inside ÖzDil Dictionary
  const [searchQuery, setSearchQuery] = useState("");
  
  // Cursor position tracking
  const [cursorPos, setCursorPos] = useState({ line: 1, col: 1 });
  
  // Copied keyword visual feedback state
  const [copiedKeyword, setCopiedKeyword] = useState<string | null>(null);
  
  // Dropdown menu toggle states
  const [activeMenu, setActiveMenu] = useState<string | null>(null);
  
  // Simple toast status system
  const [toast, setToast] = useState<{ message: string; type: "success" | "error" | "info" } | null>(null);

  // Terminal Interactive Input States
  const [runInputs, setRunInputs] = useState<string[]>([]);
  const [terminalInputValue, setTerminalInputValue] = useState<string>("");

  // Phone Preview States
  const [showPhonePreview, setShowPhonePreview] = useState<boolean>(true);
  const [phoneAlert, setPhoneAlert] = useState<string | null>(null);
  const [activePageIndex, setActivePageIndex] = useState<number>(0);

  useEffect(() => {
    setActivePageIndex(0);
  }, [results]);

  // Sync Dark mode
  useEffect(() => {
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark" || (!savedTheme && window.matchMedia("(prefers-color-scheme: dark)").matches)) {
      setIsDark(true);
      document.documentElement.classList.add("dark");
    } else {
      setIsDark(false);
      document.documentElement.classList.remove("dark");
    }
  }, []);

  const fetchPackages = async () => {
    setLoadingPackages(true);
    try {
      const res = await fetch("/api/packages");
      const data = await res.json();
      if (data.success) {
        setPackages(data.packages);
      }
    } catch (err) {
      console.error("Paketler yüklenemedi:", err);
    } finally {
      setLoadingPackages(false);
    }
  };

  const handleInstallPackage = async (name: string) => {
    setLoadingPackages(true);
    setPackageOutput(`ozpip install ${name}\nSistem kuruluyor, lütfen bekleyin...\n`);
    showToast(`'${name}' kuruluyor...`, "info");
    try {
      const response = await fetch("/api/packages/install", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name })
      });
      const data = await response.json();
      if (data.success) {
        setPackageOutput(prev => prev + data.output + "\n✨ Kurulum başarıyla tamamlandı!");
        showToast(`'${name}' paketi başarıyla kuruldu!`, "success");
        fetchPackages();
      } else {
        setPackageOutput(prev => prev + (data.output || "") + `\nHata: ${data.error || "Bilinmeyen hata"}`);
        showToast(`Kurulum hatası: ${data.error || "Bilinmeyen hata"}`, "error");
      }
    } catch (err) {
      setPackageOutput(prev => prev + `\nHata: ${(err as Error).message}`);
      showToast("Kurulum sırasında bağlantı hatası oluştu.", "error");
    } finally {
      setLoadingPackages(false);
    }
  };

  const handleUninstallPackage = async (name: string) => {
    setLoadingPackages(true);
    setPackageOutput(`ozpip uninstall ${name}\nPaket kaldırılıyor...\n`);
    showToast(`'${name}' kaldırılıyor...`, "info");
    try {
      const response = await fetch("/api/packages/uninstall", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name })
      });
      const data = await response.json();
      if (data.success) {
        setPackageOutput(prev => prev + data.output + "\n✨ Paket başarıyla kaldırıldı!");
        showToast(`'${name}' paketi sistemden kaldırıldı.`, "success");
        fetchPackages();
      } else {
        setPackageOutput(prev => prev + (data.output || "") + `\nHata: ${data.error || "Bilinmeyen hata"}`);
        showToast(`Kaldırma hatası: ${data.error || "Bilinmeyen hata"}`, "error");
      }
    } catch (err) {
      setPackageOutput(prev => prev + `\nHata: ${(err as Error).message}`);
      showToast("Kaldırma sırasında bağlantı hatası oluştu.", "error");
    } finally {
      setLoadingPackages(false);
    }
  };

  useEffect(() => {
    fetchPackages();
  }, [sidebarTab]);

  const toggleTheme = () => {
    if (isDark) {
      setIsDark(false);
      document.documentElement.classList.remove("dark");
      localStorage.setItem("theme", "light");
      showToast("Açık tema aktif edildi", "info");
    } else {
      setIsDark(true);
      document.documentElement.classList.add("dark");
      localStorage.setItem("theme", "dark");
      showToast("Karanlık tema aktif edildi", "info");
    }
    setActiveMenu(null);
  };

  const showToast = (message: string, type: "success" | "error" | "info" = "success") => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 3000);
  };

  const handleExportZip = async () => {
    setIsExporting(true);
    setActiveMenu(null);
    setShowExportDropdown(false);
    showToast("ÖzDil projesi sıkıştırılıyor...", "info");
    try {
      const response = await fetch("/api/export", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ code })
      });

      if (!response.ok) {
        throw new Error(`İndirme Hatası: ${response.status}`);
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "ozdil_projesi.zip";
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
      showToast("Dışa aktarma başarıyla tamamlandı!", "success");
    } catch (err) {
      showToast(`Dışa aktarma başarısız oldu: ${(err as Error).message}`, "error");
    } finally {
      setIsExporting(false);
    }
  };

  const handleExportOzOnly = () => {
    setActiveMenu(null);
    setShowExportDropdown(false);
    try {
      const blob = new Blob([code], { type: "text/plain;charset=utf-8" });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "kodumuz.oz";
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
      showToast("ÖzDil kod dosyası (.oz) indirildi!", "success");
    } catch (err) {
      showToast(`İndirme başarısız: ${(err as Error).message}`, "error");
    }
  };

  const handleExportPythonOnly = () => {
    setActiveMenu(null);
    setShowExportDropdown(false);
    if (!results.translated) {
      showToast("Lütfen önce kodunuzu çalıştırarak Python'a çevrilmesini sağlayın.", "error");
      return;
    }
    try {
      const blob = new Blob([results.translated], { type: "text/plain;charset=utf-8" });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "kodumuz.py";
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
      showToast("Çevrilmiş Python dosyası (.py) indirildi!", "success");
    } catch (err) {
      showToast(`İndirme başarısız: ${(err as Error).message}`, "error");
    }
  };

  const handleRunCode = async (customInputs?: string[]) => {
    setIsRunning(true);
    setActiveMenu(null);
    if (window.innerWidth < 1024) {
      setSidebarTab(null);
    }
    setPanelHeight("normal");
    setPanelTab("terminal");

    const inputsToUse = Array.isArray(customInputs) ? customInputs : [];
    if (inputsToUse.length === 0) {
      setRunInputs([]);
      setTerminalInputValue("");
      showToast("Kod derleniyor ve çalıştırılıyor...", "info");
    }

    try {
      const response = await fetch("/api/run", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ code, inputs: inputsToUse })
      });

      if (!response.ok) {
        throw new Error(`HTTP Hatası: ${response.status}`);
      }

      const data: CompilerResult = await response.json();
      setResults(data);
      if (data.gui_elements && data.gui_elements.length > 0) {
        setShowPhonePreview(true);
        setPhoneAlert(null);
      }
      if (data.error) {
        showToast("Hata ile sonuçlandı!", "error");
      } else if (data.awaiting_input) {
        showToast("Girdi bekleniyor...", "info");
      } else {
        showToast("İşlem başarıyla tamamlandı!", "success");
      }
    } catch (err) {
      setResults({
        translated: "",
        ast: null,
        output: "",
        error: `Kod çalıştırılırken sunucu hatası oluştu: ${(err as Error).message}`
      });
      showToast("Sunucu bağlantı hatası!", "error");
    } finally {
      setIsRunning(false);
    }
  };

  const handlePhoneButtonPress = async (action?: string, buttonName?: string) => {
    if (!action) return;
    
    setPhoneAlert(`"${buttonName}" tıklandı, "${action}" olayı tetikleniyor...`);
    setIsRunning(true);
    
    try {
      const response = await fetch("/api/run", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ code, inputs: runInputs, event: action })
      });

      if (!response.ok) {
        throw new Error(`HTTP Hatası: ${response.status}`);
      }

      const data: CompilerResult = await response.json();
      setResults(data);
      if (data.gui_elements && data.gui_elements.length > 0) {
        setShowPhonePreview(true);
        if (data.error) {
          setPhoneAlert(`Hata oluştu: ${data.error}`);
        } else {
          setPhoneAlert(`"${buttonName}" başarıyla tetiklendi!`);
        }
      }
    } catch (err) {
      setPhoneAlert(`Bağlantı hatası: ${(err as Error).message}`);
    } finally {
      setIsRunning(false);
    }
  };

  const handleTerminalInputSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const nextInputs = [...runInputs, terminalInputValue];
    setRunInputs(nextInputs);
    setTerminalInputValue("");
    handleRunCode(nextInputs);
  };

  const handleLoadExample = (exampleTitle: string, exampleCode: string) => {
    setCode(exampleCode);
    openFileTab("kod_alani.oz");
    // Clear old results
    setResults({
      translated: "",
      ast: null,
      output: "",
      error: null
    });
    if (exampleCode.includes("telefon")) {
      setShowPhonePreview(true);
    }
    if (window.innerWidth < 1024) {
      setSidebarTab(null);
    }
    showToast(`"${exampleTitle}" şablonu yüklendi.`, "success");
  };

  const handleCopyKeyword = (keyword: string) => {
    navigator.clipboard.writeText(keyword);
    setCopiedKeyword(keyword);
    showToast(`"${keyword}" panoya kopyalandı.`);
    setTimeout(() => setCopiedKeyword(null), 1500);
  };

  // Switch or open a file tab in our virtual environment
  const openFileTab = (filename: string) => {
    if (!openTabs.includes(filename)) {
      setOpenTabs([...openTabs, filename]);
    }
    setActiveFile(filename);
    if (window.innerWidth < 1024) {
      setSidebarTab(null);
    }
  };

  const closeFileTab = (e: React.MouseEvent, filename: string) => {
    e.stopPropagation();
    if (filename === "kod_alani.oz") return; // Primary file cannot be closed
    
    const remaining = openTabs.filter(t => t !== filename);
    setOpenTabs(remaining);
    
    if (activeFile === filename) {
      setActiveFile(remaining[remaining.length - 1] || "kod_alani.oz");
    }
  };

  // Toggle active sidebar tab (collapse if clicked again)
  const toggleSidebarTab = (tab: "explorer" | "search" | "run" | "docs" | "packages") => {
    if (sidebarTab === tab) {
      setSidebarTab(null);
    } else {
      setSidebarTab(tab);
      if (window.innerWidth < 1024) {
        setPanelHeight("collapsed");
      }
    }
  };

  // Normalize Turkish text to ASCII characters for accent-insensitive search
  const normalizeTurkish = (str: string) => {
    return str
      .toLowerCase()
      .replace(/ı/g, "i")
      .replace(/ş/g, "s")
      .replace(/ğ/g, "g")
      .replace(/ç/g, "c")
      .replace(/ö/g, "o")
      .replace(/ü/g, "u");
  };

  // Filter keywords in dictionary based on query
  const filteredKeywords = KEYWORDS.filter((kw) => {
    const query = normalizeTurkish(searchQuery);
    return (
      normalizeTurkish(kw.keyword).includes(query) ||
      normalizeTurkish(kw.pythonEquivalent).includes(query) ||
      normalizeTurkish(kw.description).includes(query)
    );
  });

  // Content for read-only runner script file "ozdil.py"
  const ozdilPyContent = `# -*- coding: utf-8 -*-
"""
ÖzDil Türkçe Programlama Dili - Çekirdek Çevirici Motoru (v1.0)
Bu kod, .oz uzantılı Türkçe kodlarınızı Python AST yapısına dönüştürür.
"""
import sys
import os
import ast
import tokenize
from io import BytesIO

# Türkçe kelimelerden Python karşılıklarına birebir haritalama tablosu
MAPPING = {
    'yazdir': 'print',
    'yazdır': 'print',
    'eger': 'if',
    'eğer': 'if',
    'degilse_eger': 'elif',
    'değilse_eğer': 'elif',
    'degilse_eğer': 'elif',
    'değilse_eger': 'elif',
    'degilse': 'else',
    'değilse': 'else',
    'dongu': 'for',
    'döngü': 'for',
    'her': 'for',
    'iken': 'while',
    'fonksiyon': 'def',
    'islem': 'def',
    'işlem': 'def',
    'dondur': 'return',
    'dogru': 'True',
    'doğru': 'True',
    'yanlis': 'False',
    'yanlış': 'False',
    've': 'and',
    'veya': 'or',
    'degil': 'not',
    'değil': 'not',
    'icinde': 'in',
    'içinde': 'in',
    'sinif': 'class',
    'sınıf': 'class',
    'dene': 'try',
    'hata_yakala': 'except',
    'aralik': 'range',
    'aralık': 'range',
    'uzunluk': 'len',
    'ekle': 'append',
    'tam_sayi': 'int',
    'tam_sayı': 'int',
    'metin': 'str',
    'ondalik': 'float',
    'ondalık': 'float',
    'liste': 'list',
    'sozluk': 'dict',
    'sözlük': 'dict',
    'olarak': 'as',
    'getir': 'import',
    'dur': 'break',
    'devam_et': 'continue',
    'yok': 'None',
    'bos': 'None',
    'boş': 'None',
}

# Regex patterns compiled once at module load to avoid recreation overhead
import re
_SORTED_MAPPING_KEYS = sorted(MAPPING.keys(), key=len, reverse=True)
_REGEX_PATTERNS = {k: re.compile(r'\\b' + re.escape(k) + r'\\b') for k in MAPPING}
_MAPPING_KEYS_SET = set(MAPPING.keys())

def translate(code_str):
    """
    Türkçe anahtar kelimeleri token bazında analiz edip Python karşılığına çevirir.
    String'leri ve yorum satırlarını bozmadan sadece kod deyimlerini hedefler.
    """
    try:
        bytes_io = BytesIO(code_str.encode('utf-8'))
        tokens = list(tokenize.tokenize(bytes_io.readline))
        new_tokens = []
        for tok in tokens:
            if tok.type == tokenize.NAME and tok.string in _MAPPING_KEYS_SET:
                new_tokens.append((tok.type, MAPPING[tok.string], tok.start, tok.end, tok.line))
            else:
                new_tokens.append(tok)
        return tokenize.untokenize(new_tokens).decode('utf-8')
    except Exception:
        # Hata durumunda önceden derlenmiş yüksek performanslı regex değişimi devralır
        lines = code_str.splitlines()
        translated_lines = []
        for line in lines:
            temp_line = line
            for k in _SORTED_MAPPING_KEYS:
                temp_line = _REGEX_PATTERNS[k].sub(MAPPING[k], temp_line)
            translated_lines.append(temp_line)
        return '\\n'.join(translated_lines)

print("✓ ÖzDil Modülü Başarıyla Yüklendi.")`;

  return (
    <div className="h-screen w-screen flex flex-col bg-zinc-50 dark:bg-zinc-950 text-zinc-800 dark:text-zinc-200 overflow-hidden font-sans select-none" id="app-root">
      
      {/* Toast Notification */}
      {toast && (
        <div 
          className={`fixed top-14 right-5 z-50 flex items-center gap-2.5 px-4 py-3 rounded-lg shadow-xl text-xs font-semibold animate-in fade-in slide-in-from-top-4 duration-200 border ${
            toast.type === "success" 
              ? "bg-emerald-500 text-white border-emerald-400" 
              : toast.type === "error" 
                ? "bg-red-500 text-white border-red-400" 
                : "bg-indigo-600 text-white border-indigo-500"
          }`}
          id="toast-notification"
        >
          <Sparkles className="w-4 h-4 animate-pulse" />
          <span>{toast.message}</span>
        </div>
      )}

      {/* ULTRA-PREMIUM MODERN STUDIO TOP HEADER */}
      <header className="h-14 bg-white dark:bg-zinc-950 border-b border-zinc-200/80 dark:border-zinc-900/80 flex items-center justify-between px-4 shrink-0 shadow-sm relative z-30 select-none" id="top-menu-bar">
        <div className="flex items-center gap-3">
          {/* Mobile hamburger menu button */}
          <button
            onClick={() => setIsMobileMenuOpen(true)}
            className="flex md:hidden p-2 hover:bg-zinc-100 dark:hover:bg-zinc-900 rounded-lg text-zinc-600 dark:text-zinc-400 transition cursor-pointer"
            title="Menüyü Aç"
          >
            <Menu className="w-4 h-4" />
          </button>

          {/* Premium customized badge logo */}
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-xs text-white font-extrabold shadow-md shadow-indigo-600/10 tracking-wider hover:scale-105 transition duration-150" title="ÖzDil IDE">
              ÖD
            </div>
            <div className="flex flex-col select-none">
              <span className="font-bold text-xs tracking-tight text-zinc-900 dark:text-zinc-50 leading-tight">ÖzDil</span>
              <span className="text-[10px] text-zinc-400 dark:text-zinc-500 font-medium leading-none">Türkçe Programlama</span>
            </div>
          </div>
          
          <span className="hidden md:inline-block w-px h-5 bg-zinc-200 dark:bg-zinc-900/60 mx-1"></span>

          {/* Elegant menus dropdown block */}
          <nav className="hidden md:flex items-center gap-1.5 text-xs font-semibold text-zinc-600 dark:text-zinc-300">
            {/* File Menu */}
            <div className="relative">
              <button 
                onClick={() => setActiveMenu(activeMenu === "file" ? null : "file")}
                className={`px-3 py-1.5 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-900 cursor-pointer transition ${activeMenu === "file" ? "bg-zinc-100 dark:bg-zinc-900 text-zinc-900 dark:text-white" : ""}`}
              >
                Dosya
              </button>
              {activeMenu === "file" && (
                <div className="absolute top-9 left-0 w-60 bg-white dark:bg-zinc-950 border border-zinc-200/80 dark:border-zinc-850 rounded-xl shadow-xl py-1.5 z-50 text-[11px] animate-in fade-in slide-in-from-top-2 duration-150" onMouseLeave={() => setActiveMenu(null)}>
                  <div className="px-3 py-1 text-[9px] font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider select-none">Çalışma Sayfaları</div>
                  <button onClick={() => { openFileTab("kod_alani.oz"); setActiveMenu(null); }} className="w-full text-left px-3 py-2 hover:bg-indigo-50 dark:hover:bg-indigo-950/40 hover:text-indigo-600 dark:hover:text-indigo-400 flex items-center justify-between transition text-zinc-700 dark:text-zinc-300">
                    <span className="font-medium">kod_alani.oz Düzenle</span>
                    <span className="text-zinc-400 font-mono text-[9px]">Ctrl+1</span>
                  </button>
                  <button onClick={() => { openFileTab("BENI_OKU.md"); setActiveMenu(null); }} className="w-full text-left px-3 py-2 hover:bg-indigo-50 dark:hover:bg-indigo-950/40 hover:text-indigo-600 dark:hover:text-indigo-400 flex items-center justify-between transition text-zinc-700 dark:text-zinc-300">
                    <span className="font-medium">Beni Oku Kılavuzunu Aç</span>
                    <span className="text-zinc-400 font-mono text-[9px]">Ctrl+2</span>
                  </button>
                  <button onClick={() => { openFileTab("ozdil.py"); setActiveMenu(null); }} className="w-full text-left px-3 py-2 hover:bg-indigo-50 dark:hover:bg-indigo-950/40 hover:text-indigo-600 dark:hover:text-indigo-400 flex items-center justify-between transition text-zinc-700 dark:text-zinc-300">
                    <span className="font-medium">ozdil.py Çekirdeği İncele</span>
                    <span className="text-zinc-400 font-mono text-[9px]">Ctrl+3</span>
                  </button>
                  <hr className="my-1.5 border-zinc-100 dark:border-zinc-900" />
                  <div className="px-3 py-1 text-[9px] font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider select-none">Proje Sıfırlama</div>
                  <button onClick={() => { setCode(""); setActiveMenu(null); showToast("Yazım alanı temizlendi.", "info"); }} className="w-full text-left px-3 py-2 hover:bg-red-50 dark:hover:bg-red-950/20 flex items-center justify-between text-red-500 dark:text-red-400 transition font-medium">
                    <span>Çalışma Alanını Sıfırla</span>
                    <span><Trash2 className="w-3.5 h-3.5" /></span>
                  </button>
                </div>
              )}
            </div>

            {/* Edit Menu */}
            <div className="relative">
              <button 
                onClick={() => setActiveMenu(activeMenu === "edit" ? null : "edit")}
                className={`px-3 py-1.5 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-900 cursor-pointer transition ${activeMenu === "edit" ? "bg-zinc-100 dark:bg-zinc-900 text-zinc-900 dark:text-white" : ""}`}
              >
                Düzen
              </button>
              {activeMenu === "edit" && (
                <div className="absolute top-9 left-0 w-52 bg-white dark:bg-zinc-950 border border-zinc-200/80 dark:border-zinc-850 rounded-xl shadow-xl py-1.5 z-50 text-[11px] animate-in fade-in slide-in-from-top-2 duration-150" onMouseLeave={() => setActiveMenu(null)}>
                  <button onClick={() => { setSearchQuery(""); toggleSidebarTab("search"); setActiveMenu(null); }} className="w-full text-left px-3 py-2 hover:bg-indigo-50 dark:hover:bg-indigo-950/40 hover:text-indigo-600 dark:hover:text-indigo-400 flex items-center justify-between transition text-zinc-700 dark:text-zinc-300">
                    <span className="font-medium">Sözlükte Ara</span>
                    <span className="text-zinc-400 font-mono text-[9px]">Ctrl+F</span>
                  </button>
                  <button onClick={toggleTheme} className="w-full text-left px-3 py-2 hover:bg-indigo-50 dark:hover:bg-indigo-950/40 hover:text-indigo-600 dark:hover:text-indigo-400 flex items-center justify-between transition text-zinc-700 dark:text-zinc-300">
                    <span className="font-medium">Temayı Değiştir</span>
                    <span className="text-indigo-500 dark:text-indigo-400 font-semibold">{isDark ? "Açık Tema" : "Karanlık Tema"}</span>
                  </button>
                </div>
              )}
            </div>

            {/* Run Menu */}
            <div className="relative">
              <button 
                onClick={() => setActiveMenu(activeMenu === "run" ? null : "run")}
                className={`px-3 py-1.5 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-900 cursor-pointer transition ${activeMenu === "run" ? "bg-zinc-100 dark:bg-zinc-900 text-zinc-900 dark:text-white" : ""}`}
              >
                Çalıştır
              </button>
              {activeMenu === "run" && (
                <div className="absolute top-9 left-0 w-56 bg-white dark:bg-zinc-950 border border-zinc-200/80 dark:border-zinc-850 rounded-xl shadow-xl py-1.5 z-50 text-[11px] animate-in fade-in slide-in-from-top-2 duration-150" onMouseLeave={() => setActiveMenu(null)}>
                  <button onClick={() => { handleRunCode(); setActiveMenu(null); }} disabled={isRunning} className="w-full text-left px-3 py-2 hover:bg-indigo-50 dark:hover:bg-indigo-950/40 hover:text-indigo-600 dark:hover:text-indigo-400 flex items-center justify-between transition text-zinc-700 dark:text-zinc-300 disabled:opacity-50">
                    <span className="font-medium">Hata Ayıklamadan Çalıştır</span>
                    <span className="text-zinc-400 font-mono text-[9px]">Ctrl+Enter</span>
                  </button>
                </div>
              )}
            </div>

            {/* Help Menu */}
            <div className="relative">
              <button 
                onClick={() => setActiveMenu(activeMenu === "help" ? null : "help")}
                className={`px-3 py-1.5 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-900 cursor-pointer transition ${activeMenu === "help" ? "bg-zinc-100 dark:bg-zinc-900 text-zinc-900 dark:text-white" : ""}`}
              >
                Yardım
              </button>
              {activeMenu === "help" && (
                <div className="absolute top-9 left-0 w-56 bg-white dark:bg-zinc-950 border border-zinc-200/80 dark:border-zinc-850 rounded-xl shadow-xl py-1.5 z-50 text-[11px] animate-in fade-in slide-in-from-top-2 duration-150" onMouseLeave={() => setActiveMenu(null)}>
                  <button onClick={() => { openFileTab("BENI_OKU.md"); setActiveMenu(null); }} className="w-full text-left px-3 py-2 hover:bg-indigo-50 dark:hover:bg-indigo-950/40 hover:text-indigo-600 dark:hover:text-indigo-400 transition text-zinc-700 dark:text-zinc-300 font-medium">
                    <span>ÖzDil Rehberini Görüntüle</span>
                  </button>
                  <button onClick={() => { toggleSidebarTab("docs"); setActiveMenu(null); }} className="w-full text-left px-3 py-2 hover:bg-indigo-50 dark:hover:bg-indigo-950/40 hover:text-indigo-600 dark:hover:text-indigo-400 transition text-zinc-700 dark:text-zinc-300 font-medium">
                    <span>Sözlüğü Yan Panelde Aç</span>
                  </button>
                  <hr className="my-1.5 border-zinc-100 dark:border-zinc-900" />
                  <div className="px-3 py-1 text-[9px] text-zinc-400 dark:text-zinc-500 font-semibold select-none">
                    Sürüm: ÖzDil Web v1.1.0
                  </div>
                </div>
              )}
            </div>
          </nav>
        </div>

        {/* Center: File Name breadcrumb */}
        <div className="text-xs font-mono font-semibold text-zinc-500 dark:text-zinc-400 select-none hidden lg:flex items-center gap-2 bg-zinc-50 dark:bg-zinc-900 px-3.5 py-1.5 rounded-full border border-zinc-200/30 dark:border-zinc-800/30">
          <span className="w-1.5 h-1.5 rounded-full bg-indigo-500"></span>
          <span>{activeFile}</span>
          <span className="text-[10px] text-zinc-400 font-light">•</span>
          <span className="text-[10px] text-indigo-500 font-bold uppercase tracking-wide">Stüdyo</span>
        </div>

        {/* Right side: Quick Action Buttons */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => handleRunCode()}
            disabled={isRunning}
            className={`flex items-center gap-1.5 px-4 py-2 rounded-lg text-xs font-bold transition shadow-md shadow-emerald-600/10 bg-emerald-600 hover:bg-emerald-500 text-white cursor-pointer disabled:opacity-50 active:scale-95 duration-100`}
            id="top-run-btn"
            title="Kodu Çalıştır (Ctrl + Enter)"
          >
            <Play className={`w-3.5 h-3.5 ${isRunning ? "animate-spin" : "fill-current"}`} />
            <span>{isRunning ? "Çalışıyor..." : "Çalıştır"}</span>
          </button>

          <div className="relative">
            <button
              onClick={() => setShowExportDropdown(!showExportDropdown)}
              className="flex items-center gap-1.5 px-3.5 py-2 rounded-lg text-xs font-semibold border border-zinc-200 dark:border-zinc-800 bg-white hover:bg-zinc-50 dark:bg-zinc-900 dark:hover:bg-zinc-850 cursor-pointer text-zinc-700 dark:text-zinc-300 transition shadow-sm active:scale-95 duration-100"
              id="top-export-btn"
              title="Kodu veya Projeyi Çevrimdışı Kullanım İçin İndir"
            >
              <Download className="w-3.5 h-3.5 text-zinc-500 dark:text-zinc-400" />
              <span>Dışa Aktar</span>
              <ChevronDown className="w-3 h-3 text-zinc-400" />
            </button>
            {showExportDropdown && (
              <div 
                className="absolute right-0 top-10 w-64 bg-white dark:bg-zinc-950 border border-zinc-200/80 dark:border-zinc-850 rounded-xl shadow-xl py-1.5 z-50 text-[11px] flex flex-col animate-in fade-in slide-in-from-top-2 duration-150"
                onMouseLeave={() => setShowExportDropdown(false)}
              >
                <div className="px-3 py-1 text-[9px] font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider border-b border-zinc-100 dark:border-zinc-900/60 mb-1.5 select-none">
                  İndirme Seçenekleri
                </div>
                <button 
                  onClick={() => { handleExportZip(); setShowExportDropdown(false); }} 
                  disabled={isExporting}
                  className="w-full text-left px-3 py-2 hover:bg-indigo-50 dark:hover:bg-indigo-950/40 hover:text-indigo-600 dark:hover:text-indigo-400 flex items-center justify-between text-zinc-850 dark:text-zinc-200 font-semibold disabled:opacity-50 transition"
                >
                  <span className="flex items-center gap-2">
                    <Download className="w-3.5 h-3.5 text-indigo-500 shrink-0" />
                    <span>ÖzDil Projesi (ZIP)</span>
                  </span>
                  <span className="text-zinc-400 dark:text-zinc-500 text-[9px] font-mono">Tümü</span>
                </button>
                <button 
                  onClick={() => { handleExportOzOnly(); setShowExportDropdown(false); }} 
                  className="w-full text-left px-3 py-2 hover:bg-indigo-50 dark:hover:bg-indigo-950/40 hover:text-indigo-600 dark:hover:text-indigo-400 flex items-center justify-between text-zinc-850 dark:text-zinc-200 transition"
                >
                  <span className="flex items-center gap-2">
                    <FileCode2 className="w-3.5 h-3.5 text-amber-500 shrink-0" />
                    <span>Sadece ÖzDil Kodu (.oz)</span>
                  </span>
                  <span className="text-zinc-400 dark:text-zinc-500 text-[9px] font-mono">Kaynak</span>
                </button>
                <button 
                  onClick={() => { handleExportPythonOnly(); setShowExportDropdown(false); }} 
                  className="w-full text-left px-3 py-2 hover:bg-indigo-50 dark:hover:bg-indigo-950/40 hover:text-indigo-600 dark:hover:text-indigo-400 flex items-center justify-between text-zinc-850 dark:text-zinc-200 transition"
                >
                  <span className="flex items-center gap-2">
                    <Code className="w-3.5 h-3.5 text-emerald-500 shrink-0" />
                    <span>Python Çevirisi (.py)</span>
                  </span>
                  <span className="text-zinc-400 dark:text-zinc-500 text-[9px] font-mono">Çeviri</span>
                </button>
              </div>
            )}
          </div>

          <span className="w-px h-5 bg-zinc-200 dark:bg-zinc-900/60 mx-1"></span>

          {/* Quick theme toggle */}
          <button
            onClick={toggleTheme}
            className="p-2 text-zinc-500 hover:text-zinc-900 dark:hover:text-white rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-900 transition cursor-pointer active:scale-95 duration-100"
            title={isDark ? "Açık Tema" : "Karanlık Tema"}
          >
            {isDark ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
          </button>
        </div>
      </header>

      {/* VS CODE WORKSPACE CONTAINER (Activity Bar + Sidebar + Main Editor + Bottom Panel) */}
      <div className="flex-1 flex overflow-hidden relative" id="workspace-container">

        {/* ACTIVITY BAR (Leftmost strip) */}
        <aside className="hidden lg:flex w-14 bg-zinc-50 dark:bg-[#0c0d10] border-r border-zinc-200/80 dark:border-zinc-900/80 flex-col justify-between py-2 shrink-0 z-10 select-none" id="activity-bar">
          
          {/* Top Icons group */}
          <div className="flex flex-col items-center gap-1.5 px-1.5">
            {/* File Explorer icon */}
            <button
              onClick={() => toggleSidebarTab("explorer")}
              className={`w-11 h-11 flex items-center justify-center rounded-xl relative cursor-pointer group transition-all duration-200 ${
                sidebarTab === "explorer"
                  ? "text-indigo-600 bg-indigo-50 dark:text-indigo-400 dark:bg-indigo-950/40"
                  : "text-zinc-400 dark:text-zinc-650 hover:text-zinc-700 dark:hover:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-900/40"
              }`}
              title="Gezgin / Dosya Yapısı"
            >
              <FolderOpen className="w-5 h-5 transition-transform group-hover:scale-105" />
            </button>

            {/* Quick Keyword Dictionary Search */}
            <button
              onClick={() => toggleSidebarTab("search")}
              className={`w-11 h-11 flex items-center justify-center rounded-xl relative cursor-pointer group transition-all duration-200 ${
                sidebarTab === "search"
                  ? "text-indigo-600 bg-indigo-50 dark:text-indigo-400 dark:bg-indigo-950/40"
                  : "text-zinc-400 dark:text-zinc-650 hover:text-zinc-700 dark:hover:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-900/40"
              }`}
              title="ÖzDil Sözlük Arama"
            >
              <Search className="w-5 h-5 transition-transform group-hover:scale-105" />
            </button>

            {/* Run & Debug tab */}
            <button
              onClick={() => toggleSidebarTab("run")}
              className={`w-11 h-11 flex items-center justify-center rounded-xl relative cursor-pointer group transition-all duration-200 ${
                sidebarTab === "run"
                  ? "text-indigo-600 bg-indigo-50 dark:text-indigo-400 dark:bg-indigo-950/40"
                  : "text-zinc-400 dark:text-zinc-650 hover:text-zinc-700 dark:hover:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-900/40"
              }`}
              title="Çalıştır ve Kılavuz"
            >
              <Bug className="w-5 h-5 transition-transform group-hover:scale-105" />
            </button>

            {/* Words dictionary cheat sheet */}
            <button
              onClick={() => toggleSidebarTab("docs")}
              className={`w-11 h-11 flex items-center justify-center rounded-xl relative cursor-pointer group transition-all duration-200 ${
                sidebarTab === "docs"
                  ? "text-indigo-600 bg-indigo-50 dark:text-indigo-400 dark:bg-indigo-950/40"
                  : "text-zinc-400 dark:text-zinc-650 hover:text-zinc-700 dark:hover:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-900/40"
              }`}
              title="Tüm Deyimler Listesi"
            >
              <BookOpen className="w-5 h-5 transition-transform group-hover:scale-105" />
            </button>

            {/* ozpip packages tab */}
            <button
              onClick={() => toggleSidebarTab("packages")}
              className={`w-11 h-11 flex items-center justify-center rounded-xl relative cursor-pointer group transition-all duration-200 ${
                sidebarTab === "packages"
                  ? "text-indigo-600 bg-indigo-50 dark:text-indigo-400 dark:bg-indigo-950/40"
                  : "text-zinc-400 dark:text-zinc-650 hover:text-zinc-700 dark:hover:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-900/40"
              }`}
              title="ÖzDil ozpip Kütüphaneleri"
            >
              <Layers className="w-5 h-5 transition-transform group-hover:scale-105" />
            </button>
          </div>

          {/* Bottom Settings group */}
          <div className="flex flex-col items-center gap-1.5 px-1.5 mb-2">
            <button
              onClick={toggleTheme}
              className="w-10 h-10 flex items-center justify-center rounded-lg text-zinc-400 dark:text-zinc-600 hover:text-zinc-700 dark:hover:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-900/40 transition cursor-pointer"
              title="Tema Değiştir"
            >
              {isDark ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
            </button>
            <button
              onClick={() => { setCode(EXAMPLES[0].code); openFileTab("kod_alani.oz"); showToast("Sıfırlandı ve ana kod şablonu yüklendi.", "info"); }}
              className="w-10 h-10 flex items-center justify-center rounded-lg text-zinc-400 dark:text-zinc-600 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-950/20 transition cursor-pointer"
              title="Tüm Kodları Sıfırla"
            >
              <RotateCcw className="w-4 h-4" />
            </button>
          </div>
        </aside>

        {/* COLLAPSIBLE SIDEBAR PANEL */}
        {sidebarTab && (
          <>
            {/* Mobile backdrop for the sidebar drawer */}
            <div 
              className="lg:hidden fixed inset-0 bg-black/40 dark:bg-black/70 backdrop-blur-[2px] z-30 top-14 bottom-14" 
              onClick={() => setSidebarTab(null)}
              id="sidebar-mobile-backdrop"
            />
            
            <div 
              className="fixed lg:relative top-14 bottom-14 lg:top-0 lg:bottom-0 left-0 z-40 w-72 lg:w-64 bg-white dark:bg-[#111216] border-r border-zinc-200/80 dark:border-zinc-900/80 flex flex-col shrink-0 overflow-hidden select-none shadow-xl lg:shadow-none" 
              id="sidebar-panel"
            >
            {/* Sidebar Title Header */}
            <div className="h-12 px-4 border-b border-zinc-200/60 dark:border-zinc-900/60 flex items-center justify-between bg-zinc-50/50 dark:bg-zinc-950/20" id="sidebar-header">
              <span className="text-[10px] font-extrabold uppercase tracking-widest text-zinc-500 dark:text-zinc-450">
                {sidebarTab === "explorer" && "GEZGİN: ÖZDİL"}
                {sidebarTab === "search" && "SÖZLÜK ARA"}
                {sidebarTab === "run" && "HATA AYIKLAMA"}
                {sidebarTab === "docs" && "ÖZDİL SÖZLÜĞÜ"}
                {sidebarTab === "packages" && "OZPIP KÜTÜPHANELERİ"}
              </span>
              <button 
                onClick={() => setSidebarTab(null)} 
                className="p-1 hover:bg-zinc-150 dark:hover:bg-zinc-900 rounded-md transition cursor-pointer"
                title="Paneli Kapat"
              >
                <X className="w-3.5 h-3.5 text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-300" />
              </button>
            </div>

            {/* Sidebar Content area */}
            <div className="flex-1 overflow-y-auto" id="sidebar-content">
              
              {/* 1. EXPLORER SECTION */}
              {sidebarTab === "explorer" && (
                <div className="flex flex-col text-xs" id="explorer-panel-content">
                  
                  {/* Collapsible Section: AÇIK EDİTÖRLER */}
                  <div className="border-b border-zinc-150 dark:border-zinc-900/60">
                    <button 
                      onClick={() => setFolderRootExpanded(!folderRootExpanded)}
                      className="w-full px-3 py-2 flex items-center gap-1.5 bg-zinc-50/50 dark:bg-zinc-950/25 text-[9px] font-extrabold text-zinc-500 dark:text-zinc-400 uppercase tracking-widest hover:bg-zinc-100 dark:hover:bg-zinc-900/40 transition duration-150"
                    >
                      {folderRootExpanded ? <ChevronDown className="w-3 h-3 text-zinc-400" /> : <ChevronRight className="w-3 h-3 text-zinc-400" />}
                      <span>Açık Editörler</span>
                    </button>
                    {folderRootExpanded && (
                      <div className="py-1 flex flex-col gap-0.5 px-1.5">
                        {openTabs.map((fileName) => (
                          <button
                            key={fileName}
                            onClick={() => openFileTab(fileName)}
                            className={`w-full px-3 py-2 rounded-lg flex items-center justify-between text-left transition duration-150 ${
                              activeFile === fileName 
                                ? "bg-indigo-50/70 dark:bg-indigo-950/30 text-indigo-600 dark:text-indigo-400 font-bold" 
                                : "text-zinc-600 dark:text-zinc-450 hover:bg-zinc-100/50 dark:hover:bg-zinc-900/30"
                            }`}
                          >
                            <span className="flex items-center gap-2 truncate">
                              {fileName.endsWith(".oz") && <FileCode2 className="w-3.5 h-3.5 text-indigo-500 shrink-0" />}
                              {fileName.endsWith(".py") && <Code className="w-3.5 h-3.5 text-amber-500 shrink-0" />}
                              {fileName.endsWith(".md") && <Info className="w-3.5 h-3.5 text-emerald-500 shrink-0" />}
                              <span className="truncate">{fileName}</span>
                            </span>
                            {fileName !== "kod_alani.oz" && (
                              <X 
                                onClick={(e) => closeFileTab(e, fileName)}
                                className="w-3 h-3 text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-200 rounded p-px transition" 
                              />
                            )}
                          </button>
                        ))}
                      </div>
                    )}
                  </div>

                  {/* Collapsible Section: PROJE DOSYALARI */}
                  <div className="border-b border-zinc-150 dark:border-zinc-900/60">
                    <div className="px-3 py-2 flex items-center justify-between bg-zinc-50/50 dark:bg-zinc-950/25 text-[9px] font-extrabold text-zinc-500 dark:text-zinc-400 uppercase tracking-widest select-none">
                      <span className="flex items-center gap-1.5">
                        <Folder className="w-3.5 h-3.5 text-indigo-500" /> <span>ÖZDİL_PROJESİ</span>
                      </span>
                    </div>
                    
                    {/* Workspace Files hierarchy list */}
                    <div className="py-1 px-1.5 flex flex-col gap-0.5">
                      
                      {/* Sub-folder: Şablonlar / Örnekler */}
                      <div className="mb-0.5">
                        <button 
                          onClick={() => setFolderExamplesExpanded(!folderExamplesExpanded)}
                          className="w-full px-3 py-1.5 flex items-center gap-1.5 rounded-lg hover:bg-zinc-100/50 dark:hover:bg-zinc-900/30 text-zinc-600 dark:text-zinc-450 text-left transition duration-150"
                        >
                          {folderExamplesExpanded ? <ChevronDown className="w-3 h-3 text-zinc-400" /> : <ChevronRight className="w-3 h-3 text-zinc-400" />}
                          <Folder className="w-3.5 h-3.5 text-amber-500 shrink-0" />
                          <span className="font-medium">örnekler</span>
                        </button>
                        
                        {folderExamplesExpanded && (
                          <div className="pl-4 pr-1 py-0.5 flex flex-col gap-0.5 border-l border-zinc-200 dark:border-zinc-800 ml-[23px] my-0.5">
                            {EXAMPLES.map((ex) => (
                              <button
                                key={ex.title}
                                onClick={() => handleLoadExample(ex.title, ex.code)}
                                className="w-full text-left px-2.5 py-1.5 text-[11px] rounded-md text-zinc-500 hover:text-indigo-600 dark:text-zinc-400 dark:hover:text-indigo-400 hover:bg-zinc-100/40 dark:hover:bg-zinc-900/30 truncate flex items-center gap-1.5 transition duration-150"
                                title={ex.description}
                              >
                                <FileCode2 className="w-3 h-3 text-indigo-400 shrink-0" />
                                <span className="truncate">{ex.title.replace(/\s+/g, "")}.oz</span>
                              </button>
                            ))}
                          </div>
                        )}
                      </div>

                      {/* Main workspace files */}
                      <button
                        onClick={() => openFileTab("kod_alani.oz")}
                        className={`w-full px-3 py-2 flex items-center gap-2 rounded-lg text-left transition duration-150 ${
                          activeFile === "kod_alani.oz" 
                            ? "bg-indigo-50/70 dark:bg-indigo-950/30 text-indigo-600 dark:text-indigo-400 font-bold" 
                            : "text-zinc-600 dark:text-zinc-450 hover:bg-zinc-100/50 dark:hover:bg-zinc-900/30"
                        }`}
                      >
                        <FileCode2 className="w-3.5 h-3.5 text-indigo-500 shrink-0" />
                        <span className="truncate font-medium">kod_alani.oz</span>
                      </button>

                      <button
                        onClick={() => openFileTab("ozdil.py")}
                        className={`w-full px-3 py-2 flex items-center gap-2 rounded-lg text-left transition duration-150 ${
                          activeFile === "ozdil.py" 
                            ? "bg-indigo-50/70 dark:bg-indigo-950/30 text-indigo-600 dark:text-indigo-400 font-bold" 
                            : "text-zinc-600 dark:text-zinc-450 hover:bg-zinc-100/50 dark:hover:bg-zinc-900/30"
                        }`}
                      >
                        <Code className="w-3.5 h-3.5 text-amber-500 shrink-0" />
                        <span className="truncate font-medium">ozdil.py</span>
                      </button>

                      <button
                        onClick={() => openFileTab("BENI_OKU.md")}
                        className={`w-full px-3 py-2 flex items-center gap-2 rounded-lg text-left transition duration-150 ${
                          activeFile === "BENI_OKU.md" 
                            ? "bg-indigo-50/70 dark:bg-indigo-950/30 text-indigo-600 dark:text-indigo-400 font-bold" 
                            : "text-zinc-600 dark:text-zinc-450 hover:bg-zinc-100/50 dark:hover:bg-zinc-900/30"
                        }`}
                      >
                        <Info className="w-3.5 h-3.5 text-emerald-500 shrink-0" />
                        <span className="truncate font-medium">BENI_OKU.md</span>
                      </button>

                    </div>
                  </div>

                </div>
              )}

              {/* 2. SEARCH / DICTIONARY PANEL */}
              {sidebarTab === "search" && (
                <div className="p-3.5 flex flex-col gap-4" id="search-panel-content">
                  <div className="relative">
                    <input
                      type="text"
                      placeholder="Deyim veya karşılık ara..."
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      className="w-full px-3 py-2 text-xs bg-zinc-50 dark:bg-zinc-950 border border-zinc-200 dark:border-zinc-800 rounded-lg focus:outline-none focus:border-indigo-500 dark:focus:border-indigo-400 placeholder-zinc-400 font-mono shadow-inner transition duration-150"
                    />
                    {searchQuery ? (
                      <button 
                        onClick={() => setSearchQuery("")} 
                        className="absolute right-2.5 top-2.5 p-0.5 hover:bg-zinc-200 dark:hover:bg-zinc-800 rounded"
                      >
                        <X className="w-3 h-3 text-zinc-400" />
                      </button>
                    ) : (
                      <Search className="w-3.5 h-3.5 text-zinc-400 absolute right-3 top-2.5" />
                    )}
                  </div>

                  <div className="flex flex-col gap-2">
                    <span className="text-[9px] font-extrabold text-zinc-400 uppercase tracking-widest border-b border-zinc-100 dark:border-zinc-900/60 pb-1 select-none">
                      Arama Sonuçları ({filteredKeywords.length})
                    </span>

                    <div className="flex flex-col gap-2 max-h-[calc(100vh-230px)] overflow-y-auto pr-0.5">
                      {filteredKeywords.map((item, index) => (
                        <div 
                          key={`${item.keyword}-${item.pythonEquivalent}-${index}`}
                          className="p-3 bg-zinc-50/50 dark:bg-zinc-950 border border-zinc-200/80 dark:border-zinc-900/80 rounded-xl flex flex-col gap-1.5 text-xs transition hover:border-zinc-300 dark:hover:border-zinc-800"
                        >
                          <div className="flex justify-between items-center">
                            <span className="font-mono font-bold text-indigo-600 dark:text-indigo-400 bg-indigo-50/70 dark:bg-indigo-950/40 px-2 py-0.5 rounded-lg text-[11px]">
                              {item.keyword}
                            </span>
                            <span className="font-mono text-[10px] text-zinc-400 font-medium">
                              → {item.pythonEquivalent}
                            </span>
                          </div>
                          <p className="text-zinc-600 dark:text-zinc-450 text-[11px] leading-relaxed">
                            {item.description}
                          </p>
                          <code className="text-[10px] bg-zinc-100 dark:bg-zinc-900 px-2 py-1 rounded-md font-mono border border-zinc-200/60 dark:border-zinc-850/60 text-zinc-500 overflow-hidden text-ellipsis whitespace-nowrap block">
                            {item.usage}
                          </code>
                          <button
                            onClick={() => handleCopyKeyword(item.keyword)}
                            className="text-left text-[10px] text-indigo-500 hover:text-indigo-600 dark:text-indigo-400 font-bold self-start mt-0.5 cursor-pointer active:scale-95 transition"
                          >
                            Panoya Kopyala
                          </button>
                        </div>
                      ))}
                      {filteredKeywords.length === 0 && (
                        <span className="text-zinc-400 italic text-center text-xs py-6 font-medium">Uyan deyim bulunamadı.</span>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {/* 3. RUN & DEBUG / CONFIG PANEL */}
              {sidebarTab === "run" && (
                <div className="p-4 flex flex-col gap-5 text-xs" id="run-panel-content">
                  <div className="flex flex-col gap-2">
                    <span className="text-[9px] font-extrabold text-zinc-400 uppercase tracking-widest">
                      Çalıştırma Yapılandırması
                    </span>
                    <div className="p-3 bg-zinc-50/70 dark:bg-zinc-950 border border-zinc-200/80 dark:border-zinc-900/80 rounded-xl flex items-center justify-between font-mono text-xs shadow-sm">
                      <span className="text-zinc-700 dark:text-zinc-300 font-medium">Python: Current File</span>
                      <span className="flex items-center gap-1.5">
                        <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                        <span className="text-[10px] text-zinc-400">Aktif</span>
                      </span>
                    </div>
                  </div>

                  <div className="flex flex-col gap-2.5">
                    <button
                      onClick={() => handleRunCode()}
                      disabled={isRunning}
                      className="w-full py-2.5 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-bold rounded-lg shadow-md shadow-indigo-600/10 text-xs flex items-center justify-center gap-2 cursor-pointer active:scale-95 transition duration-150"
                    >
                      <Play className="w-3.5 h-3.5 fill-current" />
                      <span>{isRunning ? "Çalışıyor..." : "Derle ve Çalıştır"}</span>
                    </button>

                    <div className="flex flex-col gap-2 mt-2 border-t border-zinc-200/50 dark:border-zinc-800/50 pt-4">
                      <span className="text-[9px] font-extrabold text-zinc-400 uppercase tracking-widest mb-1 select-none">
                        Dışa Aktar & İndir
                      </span>
                      
                      <button
                        onClick={handleExportZip}
                        disabled={isExporting}
                        className="w-full py-2 bg-zinc-50 hover:bg-zinc-100 dark:bg-zinc-950 dark:hover:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 text-zinc-700 dark:text-zinc-300 font-bold rounded-lg text-[11px] flex items-center justify-center gap-1.5 cursor-pointer disabled:opacity-50 transition active:scale-95 duration-100"
                      >
                        <Download className="w-3.5 h-3.5 text-indigo-500" />
                        <span>Tüm Projeyi İndir (.zip)</span>
                      </button>

                      <button
                        onClick={handleExportOzOnly}
                        className="w-full py-2 bg-zinc-50 hover:bg-zinc-100 dark:bg-zinc-950 dark:hover:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 text-zinc-700 dark:text-zinc-300 font-bold rounded-lg text-[11px] flex items-center justify-center gap-1.5 cursor-pointer transition active:scale-95 duration-100"
                      >
                        <FileCode2 className="w-3.5 h-3.5 text-amber-500" />
                        <span>Sadece ÖzDil Kodu (.oz)</span>
                      </button>

                      <button
                        onClick={handleExportPythonOnly}
                        className="w-full py-2 bg-zinc-50 hover:bg-zinc-100 dark:bg-zinc-950 dark:hover:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 text-zinc-700 dark:text-zinc-300 font-bold rounded-lg text-[11px] flex items-center justify-center gap-1.5 cursor-pointer transition active:scale-95 duration-100"
                      >
                        <Code className="w-3.5 h-3.5 text-emerald-500" />
                        <span>Python Koduna Çevir (.py)</span>
                      </button>
                    </div>
                  </div>

                  <hr className="border-zinc-150 dark:border-zinc-900/60" />

                  <div className="flex flex-col gap-2.5">
                    <span className="text-[9px] font-extrabold text-zinc-400 uppercase tracking-widest select-none">
                      Klavye Kısayolları
                    </span>
                    <div className="flex flex-col gap-2 font-mono text-[10px] text-zinc-500">
                      <div className="flex justify-between items-center">
                        <span>Kodu Çalıştır:</span>
                        <kbd className="bg-zinc-100 dark:bg-zinc-950 border border-zinc-200 dark:border-zinc-850 px-1.5 py-0.5 rounded text-zinc-600 dark:text-zinc-400 shadow-sm">Ctrl+Enter</kbd>
                      </div>
                      <div className="flex justify-between items-center">
                        <span>Tamamlama:</span>
                        <kbd className="bg-zinc-100 dark:bg-zinc-950 border border-zinc-200 dark:border-zinc-850 px-1.5 py-0.5 rounded text-zinc-600 dark:text-zinc-400 shadow-sm">Tab / Enter</kbd>
                      </div>
                      <div className="flex justify-between items-center">
                        <span>Menü Kapat:</span>
                        <kbd className="bg-zinc-100 dark:bg-zinc-950 border border-zinc-200 dark:border-zinc-850 px-1.5 py-0.5 rounded text-zinc-600 dark:text-zinc-400 shadow-sm">Esc</kbd>
                      </div>
                    </div>
                  </div>

                  <hr className="border-zinc-150 dark:border-zinc-900/60" />

                  <div className="p-3.5 bg-zinc-50/50 dark:bg-zinc-950/40 border border-zinc-200/80 dark:border-zinc-900/80 rounded-xl flex flex-col gap-1.5">
                    <span className="font-bold flex items-center gap-1.5 text-[11px] text-indigo-600 dark:text-indigo-400 select-none">
                      <Cpu className="w-4 h-4" /> <span>ÖzDil Çalışma Alanı</span>
                    </span>
                    <p className="text-[10px] text-zinc-500 leading-relaxed font-medium">
                      Yazdığınız kodlar sunucuda Türkçe token filtresinden geçirilerek güvenli bir Python alt işlemi (subprocess) ile yürütülür.
                    </p>
                  </div>
                </div>
              )}

              {/* 4. REFERENCE LIST PANEL */}
              {sidebarTab === "docs" && (
                <div className="p-3.5 flex flex-col gap-3" id="reference-panel-content">
                  <span className="text-[9px] font-extrabold text-zinc-400 uppercase tracking-widest mb-1 border-b border-zinc-100 dark:border-zinc-900/60 pb-1 select-none">
                    Tüm Deyimler Listesi
                  </span>
                  <div className="flex flex-col gap-1.5 max-h-[calc(100vh-170px)] overflow-y-auto pr-0.5">
                    {KEYWORDS.map((item, index) => (
                      <button
                        key={`${item.keyword}-${item.pythonEquivalent}-${index}`}
                        onClick={() => handleCopyKeyword(item.keyword)}
                        className="w-full text-left p-2.5 bg-zinc-50/50 dark:bg-zinc-950 hover:bg-zinc-100 dark:hover:bg-zinc-900 border border-zinc-200/60 dark:border-zinc-850/60 rounded-xl transition flex justify-between items-center text-xs group font-mono active:scale-[0.98] duration-100"
                      >
                        <div className="flex flex-col">
                          <span className="font-bold text-indigo-600 dark:text-indigo-400 text-[11px]">{item.keyword}</span>
                          <span className="text-[9px] text-zinc-400 font-medium">py: {item.pythonEquivalent}</span>
                        </div>
                        <span className="text-[9px] font-bold bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 text-zinc-400 px-1.5 py-0.5 rounded-lg group-hover:bg-indigo-600 group-hover:text-white group-hover:border-indigo-600 transition duration-150">Kopyala</span>
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {/* 5. OZPIP PACKAGES PANEL */}
              {sidebarTab === "packages" && (
                <div className="p-3.5 flex flex-col gap-3 h-full overflow-hidden" id="packages-panel-content">
                  <div className="flex flex-col gap-1.5 shrink-0">
                    <p className="text-[10px] text-zinc-500 leading-relaxed font-medium">
                      Eklentileri <code className="font-mono bg-zinc-100 dark:bg-zinc-950 px-1.5 py-0.5 border border-zinc-200/60 dark:border-zinc-850/60 rounded text-[9px] text-indigo-500">ozpip</code> ile tek tıkla yükleyebilirsiniz.
                    </p>
                    
                    {/* Search input */}
                    <div className="relative mt-1">
                      <input
                        type="text"
                        placeholder="Paket ara..."
                        value={packageSearchQuery}
                        onChange={(e) => setPackageSearchQuery(e.target.value)}
                        className="w-full px-3 py-2 text-xs bg-zinc-50 dark:bg-zinc-950 border border-zinc-200 dark:border-zinc-800 rounded-lg focus:outline-none focus:border-indigo-500 dark:focus:border-indigo-400 placeholder-zinc-400 font-sans shadow-inner transition duration-150"
                      />
                      {packageSearchQuery ? (
                        <button 
                          onClick={() => setPackageSearchQuery("")} 
                          className="absolute right-2.5 top-2.5 p-0.5 hover:bg-zinc-200 dark:hover:bg-zinc-800 rounded"
                        >
                          <X className="w-3 h-3 text-zinc-400" />
                        </button>
                      ) : (
                        <Search className="w-3.5 h-3.5 text-zinc-400 absolute right-3 top-2.5" />
                      )}
                    </div>

                    {/* Filter tabs */}
                    <div className="flex bg-zinc-100 dark:bg-zinc-950 border border-zinc-200/60 dark:border-zinc-800 p-0.5 rounded-lg mt-2 text-[10px] font-bold shadow-inner">
                      <button
                        onClick={() => setActivePackageTab("all")}
                        className={`flex-1 py-1 rounded-md text-center transition-all duration-150 ${
                          activePackageTab === "all"
                            ? "bg-white dark:bg-zinc-850 text-indigo-600 dark:text-indigo-400 shadow-sm"
                            : "text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-350"
                        }`}
                      >
                        Tümü ({packages.length})
                      </button>
                      <button
                        onClick={() => setActivePackageTab("installed")}
                        className={`flex-1 py-1 rounded-md text-center transition-all duration-150 ${
                          activePackageTab === "installed"
                            ? "bg-white dark:bg-zinc-850 text-indigo-600 dark:text-indigo-400 shadow-sm"
                            : "text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-350"
                        }`}
                      >
                        Kurulu ({packages.filter(p => p.installed).length})
                      </button>
                    </div>
                  </div>

                  {/* Packages List */}
                  <div className="flex-1 overflow-y-auto flex flex-col gap-3 pr-0.5 min-h-0">
                    {packages
                      .filter(pkg => {
                        const matchesQuery = pkg.isim.toLowerCase().includes(packageSearchQuery.toLowerCase()) ||
                          pkg.aciklama.toLowerCase().includes(packageSearchQuery.toLowerCase());
                        const matchesTab = activePackageTab === "all" || pkg.installed;
                        return matchesQuery && matchesTab;
                      })
                      .map((pkg) => (
                        <div 
                          key={pkg.isim}
                          className="p-3 bg-zinc-50/50 dark:bg-zinc-950 border border-zinc-200/80 dark:border-zinc-900/80 rounded-xl flex flex-col gap-2.5 text-[11px] relative shadow-sm"
                        >
                          <div className="flex items-start justify-between gap-2">
                            <div className="flex flex-col">
                              <span className="font-mono font-bold text-zinc-900 dark:text-zinc-50 text-xs">
                                {pkg.isim}
                              </span>
                              <span className="text-[9px] text-zinc-400 font-semibold mt-0.5">
                                v{pkg.surum} · {pkg.yazar}
                              </span>
                            </div>
                            
                            {/* Type badge */}
                            <span className={`px-2 py-0.5 rounded-full text-[8px] font-bold uppercase tracking-wider shrink-0 border ${
                              pkg.tur === "ozdil"
                                ? "bg-indigo-50 text-indigo-600 dark:bg-indigo-950/20 dark:text-indigo-400 border-indigo-100/45 dark:border-indigo-900/40"
                                : "bg-amber-50 text-amber-600 dark:bg-amber-950/20 dark:text-amber-400 border-amber-100/45 dark:border-amber-900/40"
                            }`}>
                              {pkg.tur}
                            </span>
                          </div>

                          <p className="text-zinc-650 dark:text-zinc-400 text-[10.5px] leading-relaxed">
                            {pkg.aciklama}
                          </p>

                          {/* Security permissions */}
                          {pkg.izinler && pkg.izinler.length > 0 && (
                            <div className="flex flex-wrap gap-1 items-center mt-0.5">
                              {pkg.izinler.map((perm: string) => (
                                <span key={perm} className="bg-emerald-50 text-emerald-600 dark:bg-emerald-950/20 dark:text-emerald-400 border border-emerald-100/40 px-1.5 py-0.5 rounded text-[8px] font-mono leading-none">
                                  🛡️ {perm}
                                </span>
                              ))}
                            </div>
                          )}

                          {/* Action Button */}
                          <div className="flex items-center gap-1.5 mt-1 pt-2.5 border-t border-zinc-200/50 dark:border-zinc-850/60">
                            {pkg.installed ? (
                              <>
                                <button
                                  onClick={() => handleUninstallPackage(pkg.isim)}
                                  disabled={loadingPackages}
                                  className="flex-1 py-1.5 bg-red-50 text-red-600 hover:bg-red-100 dark:bg-red-950/10 dark:text-red-400 dark:hover:bg-red-950/20 rounded-lg font-bold text-[10px] transition text-center cursor-pointer disabled:opacity-50"
                                >
                                  Kaldır
                                </button>
                                <button
                                  onClick={() => handleInstallPackage(pkg.isim)}
                                  disabled={loadingPackages}
                                  className="px-2.5 py-1.5 bg-zinc-100 hover:bg-zinc-200 dark:bg-zinc-850 dark:hover:bg-zinc-800 text-zinc-600 dark:text-zinc-400 rounded-lg font-bold text-[10px] transition text-center cursor-pointer disabled:opacity-50"
                                  title="Paketi Güncelle"
                                >
                                  Güncelle
                                </button>
                              </>
                            ) : (
                              <button
                                onClick={() => handleInstallPackage(pkg.isim)}
                                disabled={loadingPackages}
                                className="flex-1 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg font-bold text-[10px] transition text-center cursor-pointer disabled:opacity-50 flex items-center justify-center gap-1"
                              >
                                {loadingPackages ? "Yükleniyor..." : "Kur"}
                              </button>
                            )}
                          </div>
                        </div>
                      ))}
                    {packages.length === 0 && (
                      <div className="flex flex-col items-center justify-center py-10 text-center text-zinc-400 gap-2">
                        <RefreshCw className="w-5 h-5 animate-spin text-indigo-500" />
                        <span className="text-xs font-semibold">Kütüphaneler yükleniyor...</span>
                      </div>
                    )}
                  </div>

                  {/* Interactive ozpip console block */}
                  {packageOutput && (
                    <div className="shrink-0 border-t border-zinc-200/60 dark:border-zinc-850/80 pt-2.5 flex flex-col gap-1.5 max-h-[140px]">
                      <div className="flex justify-between items-center">
                        <span className="text-[9px] font-extrabold text-zinc-400 dark:text-zinc-500 uppercase tracking-widest">ozpip terminal çıktısı</span>
                        <button onClick={() => setPackageOutput("")} className="text-[9px] text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-200 font-bold">Temizle</button>
                      </div>
                      <pre className="flex-1 bg-zinc-950 dark:bg-black text-[9px] font-mono text-zinc-300 p-2.5 rounded-lg overflow-y-auto whitespace-pre-wrap leading-tight select-text max-h-[110px] border border-zinc-850">
                        {packageOutput}
                      </pre>
                    </div>
                  )}
                </div>
              )}

            </div>
          </div>
          </>
        )}

        {/* MAIN WORKSPACE WRAPPER (Editor Tabs + Active Canvas + Terminal bottom panel) */}
        <main className="flex-1 flex flex-col overflow-hidden min-w-0" id="main-editor-pane">
          
          {/* EDITOR TABS BAR */}
          <div className="h-12 bg-zinc-50 dark:bg-[#0c0d10] border-b border-zinc-200/80 dark:border-zinc-900/80 flex items-center justify-between overflow-hidden shrink-0 select-none" id="editor-tabs-bar">
            
            {/* Left side tabs loop */}
            <div className="flex items-end h-full overflow-x-auto overflow-y-hidden scrollbar-none" id="tabs-scroll-container">
              {openTabs.map((fileName) => {
                const isActive = activeFile === fileName;
                return (
                  <button
                    key={fileName}
                    onClick={() => openFileTab(fileName)}
                    className={`h-12 px-5 flex items-center gap-2 border-r border-zinc-200/60 dark:border-zinc-900/60 text-xs font-semibold cursor-pointer transition-all duration-150 ${
                      isActive
                        ? "bg-white dark:bg-[#111216] text-indigo-600 dark:text-indigo-400 border-t-[3px] border-indigo-600 dark:border-indigo-500 font-bold"
                        : "bg-zinc-50/50 hover:bg-zinc-100/60 dark:bg-[#0a0b0d] dark:hover:bg-zinc-900/30 text-zinc-500 dark:text-zinc-500"
                    }`}
                  >
                    {fileName.endsWith(".oz") && <FileCode2 className={`w-4 h-4 ${isActive ? "text-indigo-500" : "text-zinc-400"}`} />}
                    {fileName.endsWith(".py") && <Code className={`w-4 h-4 ${isActive ? "text-amber-500" : "text-zinc-400"}`} />}
                    {fileName.endsWith(".md") && <Info className={`w-4 h-4 ${isActive ? "text-emerald-500" : "text-zinc-400"}`} />}
                    
                    <span>{fileName}</span>
                    
                    {fileName !== "kod_alani.oz" && (
                      <X
                        onClick={(e) => closeFileTab(e, fileName)}
                        className="w-3.5 h-3.5 text-zinc-400 hover:text-red-500 rounded-md hover:bg-zinc-150 dark:hover:bg-zinc-900/60 p-0.5 transition"
                      />
                    )}
                  </button>
                );
              })}
            </div>

            {/* Right side editor layout helper buttons (minimize sidebar, run button preview) */}
            <div className="flex items-center gap-2 px-4 shrink-0">
              {activeFile === "kod_alani.oz" && (
                <button
                  onClick={() => setShowPhonePreview(!showPhonePreview)}
                  className={`px-3 py-1.5 rounded-lg flex items-center gap-1.5 cursor-pointer text-xs font-bold transition-all duration-150 ${
                    showPhonePreview
                      ? "bg-indigo-50 text-indigo-600 dark:bg-indigo-950/40 dark:text-indigo-400 border border-indigo-100/40 dark:border-indigo-900/30 shadow-sm"
                      : "text-zinc-500 hover:text-zinc-700 dark:text-zinc-400 dark:hover:text-zinc-200 border border-transparent hover:bg-zinc-100 dark:hover:bg-zinc-900/40"
                  }`}
                  title="Telefon Arayüzünü Göster/Gizle"
                >
                  <Smartphone className="w-4 h-4" />
                  <span className="hidden md:inline">Telefon Ekranı</span>
                </button>
              )}
              <button
                onClick={handleRunCode}
                disabled={isRunning}
                className="p-1.5 hover:bg-zinc-100 dark:hover:bg-zinc-900/40 rounded-lg text-zinc-500 hover:text-emerald-600 dark:text-zinc-400 dark:hover:text-emerald-400 cursor-pointer transition active:scale-95 duration-100"
                title="Kodu Çalıştır"
              >
                <Play className={`w-4.5 h-4.5 ${isRunning ? "animate-spin" : "fill-current"}`} />
              </button>
            </div>
          </div>

          {/* BREADCRUMB STRIP */}
          <div className="h-7 bg-white dark:bg-[#111216] border-b border-zinc-200/60 dark:border-zinc-900/60 px-4 flex items-center gap-1.5 text-[10px] text-zinc-400 select-none uppercase font-mono shrink-0" id="breadcrumbs">
            <span>projemiz</span>
            <ChevronRight className="w-2.5 h-2.5 text-zinc-400/60" />
            <span>src</span>
            <ChevronRight className="w-2.5 h-2.5 text-zinc-400/60" />
            <span className="text-zinc-700 dark:text-zinc-300 font-extrabold">{activeFile}</span>
          </div>

          {/* CODE WORKSPACE CANVAS */}
          <div className="flex-1 relative overflow-hidden bg-white dark:bg-[#111216]" id="active-file-canvas">
            
            {/* FILE 1: main user code edit space */}
            {activeFile === "kod_alani.oz" && (
              <div className="w-full h-full flex flex-col lg:flex-row overflow-hidden">
                <div className="flex-1 min-w-0 h-full">
                  <CodeEditor
                    value={code}
                    onChange={(newVal) => {
                      setCode(newVal);
                      if (results.error) {
                        setResults(prev => ({ ...prev, error: null, error_details: null }));
                      }
                    }}
                    onRun={handleRunCode}
                    isRunning={isRunning}
                    flat={true}
                    onCursorChange={(line, col) => setCursorPos({ line, col })}
                    errorLine={results.error_details?.lineno}
                  />
                </div>
                
                {showPhonePreview && (
                  <div className="w-full lg:w-[380px] shrink-0 h-full bg-zinc-50 dark:bg-zinc-900 border-t lg:border-t-0 lg:border-l border-zinc-200 dark:border-zinc-850 flex flex-col overflow-hidden relative">
                    {/* Header bar */}
                    <div className="h-9 border-b border-zinc-200 dark:border-zinc-800/80 px-3 flex items-center justify-between shrink-0 bg-white dark:bg-zinc-950">
                      <span className="text-[10px] font-bold text-zinc-500 uppercase tracking-wider flex items-center gap-1.5 font-mono">
                        <span className="w-2 h-2 rounded-full bg-indigo-500 animate-pulse"></span>
                        Mobil Arayüz Simülatörü
                      </span>
                      <button 
                        onClick={() => setShowPhonePreview(false)}
                        className="text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-250 text-[10px] font-bold tracking-wide uppercase font-mono"
                      >
                        Kapat
                      </button>
                    </div>

                    {/* Phone Body Wrapper */}
                    <div className="flex-1 overflow-auto p-4 flex justify-center items-start bg-zinc-100/50 dark:bg-zinc-950/30">
                      {/* Virtual Phone Container */}
                      <div className="w-[300px] h-[520px] rounded-[36px] bg-zinc-900 border-[10px] border-zinc-800 dark:border-zinc-850 shadow-2xl relative flex flex-col overflow-hidden text-zinc-800 dark:text-zinc-200 select-text font-sans">
                        
                        {/* Dynamic Island / Notch */}
                        <div className="absolute top-2.5 left-1/2 -translate-x-1/2 w-28 h-5 rounded-full bg-black z-20 flex items-center justify-between px-3 text-white text-[8px] font-bold">
                          <span className="text-[8px] opacity-80">09:41</span>
                          <div className="w-3.5 h-3.5 rounded-full bg-zinc-900 border border-zinc-800 flex items-center justify-center">
                            <div className="w-1.5 h-1.5 rounded-full bg-indigo-900/60 animate-pulse"></div>
                          </div>
                          <span className="text-[8px] text-emerald-400">5G</span>
                        </div>

                        {/* Screen Content */}
                        <div className={`flex-1 flex flex-col overflow-hidden pt-9 pb-4 px-4 ${
                          results.gui_elements?.some(e => e.type === "arka_plan" && e.val === "gok_mavisi") ? "bg-sky-50 dark:bg-sky-950 text-sky-900 dark:text-sky-100" :
                          results.gui_elements?.some(e => e.type === "arka_plan" && e.val === "gece_mavisi") ? "bg-slate-900 text-zinc-100" :
                          results.gui_elements?.some(e => e.type === "arka_plan" && e.val === "kirli_beyaz") ? "bg-stone-50 dark:bg-stone-900 text-stone-900 dark:text-stone-100" :
                          "bg-white dark:bg-zinc-900"
                        }`}>
                          
                          {/* Inner Alert Popups */}
                          {phoneAlert && (
                            <div className="absolute inset-x-4 top-16 z-30 bg-indigo-600 text-white rounded-2xl p-4 shadow-lg border border-indigo-400/20 text-xs flex flex-col gap-2 animate-in fade-in slide-in-from-top-4 duration-200">
                              <div className="flex justify-between items-center">
                                <span className="font-bold flex items-center gap-1">🔔 Bildirim</span>
                                <button onClick={() => setPhoneAlert(null)} className="text-white hover:text-zinc-200 font-bold p-1">✕</button>
                              </div>
                              <p className="leading-relaxed text-[11px] font-sans">{phoneAlert}</p>
                            </div>
                          )}

                          {/* Render Elements Loop */}
                          {results.gui_elements && results.gui_elements.length > 0 ? (
                            <div className="flex-1 overflow-y-auto pr-0.5 space-y-3.5 pb-2 scrollbar-thin flex flex-col">
                              
                              {/* Title Header inside Phone Screen if defined */}
                              {results.gui_elements.filter(e => e.type === "baslik").map((e, idx) => (
                                <div key={idx} className="border-b border-zinc-200 dark:border-zinc-800 pb-2 mb-3 mt-1 text-center shrink-0">
                                  <h3 className="text-sm font-black tracking-tight">{e.val}</h3>
                                </div>
                              ))}

                              {/* Multi-page Tab Switcher */}
                              {(() => {
                                const pages = results.gui_elements.filter(e => e.type === "sayfa") || [];
                                const hasPages = pages.length > 0;
                                if (!hasPages) return null;

                                return (
                                  <div className="flex gap-1.5 overflow-x-auto pb-2 border-b border-zinc-200 dark:border-zinc-800 mb-3 scrollbar-none shrink-0">
                                    {pages.map((p, pIdx) => {
                                      const isActive = activePageIndex === pIdx;
                                      return (
                                        <button
                                          key={pIdx}
                                          onClick={() => setActivePageIndex(pIdx)}
                                          className={`px-3 py-1.5 text-[10px] font-extrabold rounded-full transition-all whitespace-nowrap active:scale-95 cursor-pointer ${
                                            isActive
                                              ? "bg-indigo-600 text-white shadow-sm"
                                              : "bg-zinc-100 dark:bg-zinc-800 text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-300 border border-zinc-200/50 dark:border-zinc-700/50"
                                          }`}
                                        >
                                          {p.val}
                                        </button>
                                      );
                                    })}
                                  </div>
                                );
                              })()}

                              {/* Dynamic Elements Mapping */}
                              {(() => {
                                const pages = results.gui_elements.filter(e => e.type === "sayfa") || [];
                                const hasPages = pages.length > 0;
                                const elementsToRender = hasPages
                                  ? (pages[activePageIndex]?.elements || [])
                                  : (results.gui_elements.filter(e => e.type !== "baslik" && e.type !== "arka_plan" && e.type !== "sayfa") || []);

                                return elementsToRender.map((e: any, idx: number) => {
                                  switch (e.type) {
                                    case "yazi": {
                                      const isObjectStyle = typeof e.style === "object" && e.style !== null;
                                      if (isObjectStyle) {
                                        const styleObj = e.style;
                                        const size = styleObj.size || styleObj.boyut || styleObj.fontSize;
                                        const bold = styleObj.bold || styleObj.kalin;
                                        const color = styleObj.color || styleObj.renk;
                                        const align = styleObj.align || styleObj.hizala;
                                        
                                        const textStyle: React.CSSProperties = {};
                                        if (size) {
                                          textStyle.fontSize = typeof size === "number" ? `${size}px` : size;
                                        }
                                        if (color) {
                                          textStyle.color = color;
                                        }
                                        
                                        let classNames = "font-sans leading-relaxed text-[11px] text-zinc-600 dark:text-zinc-300";
                                        if (bold) {
                                          classNames += " font-extrabold";
                                        }
                                        if (align === "center" || align === "ortala") {
                                          classNames += " text-center";
                                        } else if (align === "right" || align === "sag") {
                                          classNames += " text-right";
                                        } else {
                                          classNames += " text-left";
                                        }
                                        return <p key={idx} className={classNames} style={textStyle}>{e.val}</p>;
                                      }

                                      if (e.style === "baslik") {
                                        return <h4 key={idx} className="text-base font-extrabold tracking-tight mt-2 text-center">{e.val}</h4>;
                                      } else if (e.style === "alt_baslik") {
                                        return <p key={idx} className="text-[11px] text-zinc-500 dark:text-zinc-400 leading-normal text-center -mt-1.5">{e.val}</p>;
                                      } else if (e.style === "uyari") {
                                        return <div key={idx} className="p-2.5 bg-red-50 dark:bg-red-950/20 border border-red-100 dark:border-red-900/40 text-red-700 dark:text-red-400 rounded-xl text-[10.5px] leading-relaxed font-semibold">{e.val}</div>;
                                      } else if (e.style === "basarili") {
                                        return <div key={idx} className="p-2.5 bg-emerald-50 dark:bg-emerald-950/20 border border-emerald-100 dark:border-emerald-900/40 text-emerald-700 dark:text-emerald-400 rounded-xl text-[10.5px] leading-relaxed font-semibold">{e.val}</div>;
                                      } else if (e.style === "derece") {
                                        return <span key={idx} className="block text-4xl font-black tracking-tighter text-center py-2">{e.val}</span>;
                                      }
                                      return <p key={idx} className="text-[11px] leading-relaxed text-zinc-600 dark:text-zinc-300 font-sans">{e.val}</p>;
                                    }

                                    case "buton":
                                      return (
                                        <button
                                          key={idx}
                                          onClick={() => {
                                            if (e.action) {
                                              handlePhoneButtonPress(e.action, e.val);
                                            } else {
                                              setPhoneAlert(`"${e.val}" butonuna tıklandı!`);
                                            }
                                          }}
                                          className="w-full py-2 bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 text-white font-bold text-xs rounded-xl shadow-md cursor-pointer transition-all duration-150 flex items-center justify-center gap-1.5 border border-indigo-500/20"
                                        >
                                          <span>{e.val}</span>
                                        </button>
                                      );

                                    case "girdi":
                                      return (
                                        <div key={idx} className="flex flex-col gap-1 text-left">
                                          <label className="text-[10px] font-bold text-zinc-400 uppercase tracking-wide px-1">{e.val}</label>
                                          <input
                                            type="text"
                                            disabled
                                            placeholder={`${e.val} buraya girilecek...`}
                                            className="w-full bg-zinc-50 dark:bg-zinc-850 border border-zinc-200 dark:border-zinc-800 rounded-xl px-3 py-1.5 text-xs text-zinc-400 outline-none"
                                          />
                                        </div>
                                      );

                                    case "kart":
                                      return (
                                        <div key={idx} className="p-3 bg-zinc-50 dark:bg-zinc-850/60 border border-zinc-200 dark:border-zinc-800 rounded-2xl shadow-sm text-left flex flex-col gap-1">
                                          <span className="font-extrabold text-[11px] text-indigo-600 dark:text-indigo-400 font-sans uppercase tracking-wide">{e.title}</span>
                                          <p className="text-[11px] leading-relaxed text-zinc-600 dark:text-zinc-300">{e.content}</p>
                                        </div>
                                      );

                                    case "resim":
                                      return (
                                        <div key={idx} className="w-full flex justify-center py-1.5">
                                          <img
                                            src={e.val}
                                            alt="Mobil GUI Görsel"
                                            referrerPolicy="no-referrer"
                                            className="w-16 h-16 rounded-full object-cover shadow-md border-2 border-indigo-500"
                                          />
                                        </div>
                                      );

                                    case "liste":
                                      return (
                                        <div key={idx} className="border border-zinc-200 dark:border-zinc-800 rounded-xl divide-y divide-zinc-200 dark:divide-zinc-800 overflow-hidden shadow-sm bg-white dark:bg-zinc-950/20 text-left">
                                          {e.items.map((item: string, listIdx: number) => (
                                            <div key={listIdx} className="p-2.5 text-[10.5px] text-zinc-700 dark:text-zinc-300 font-medium hover:bg-zinc-50 dark:hover:bg-zinc-900 transition flex items-center gap-2">
                                              <span className="w-1.5 h-1.5 rounded-full bg-indigo-500"></span>
                                              <span>{item}</span>
                                            </div>
                                          ))}
                                        </div>
                                      );

                                    case "ilerleme":
                                      return (
                                        <div key={idx} className="flex flex-col gap-1.5 py-1 text-left">
                                          <div className="w-full bg-zinc-200 dark:bg-zinc-800 rounded-full h-2 overflow-hidden shadow-inner">
                                            <div className="bg-indigo-600 h-full rounded-full transition-all duration-300" style={{ width: `${Math.min(100, Math.max(0, e.val))}%` }}></div>
                                          </div>
                                        </div>
                                      );

                                    case "anahtar":
                                      return (
                                        <div key={idx} className="flex items-center justify-between p-2.5 bg-zinc-50 dark:bg-zinc-850/60 border border-zinc-150 dark:border-zinc-800 rounded-xl text-left shadow-sm">
                                          <span className="text-[11px] font-bold text-zinc-700 dark:text-zinc-300">{e.val}</span>
                                          <div 
                                            onClick={() => handlePhoneButtonPress(e.val, e.val)}
                                            className={`w-8 h-4.5 rounded-full p-0.5 transition-colors cursor-pointer ${e.checked ? "bg-indigo-600" : "bg-zinc-300 dark:bg-zinc-700"}`}
                                          >
                                            <div className={`bg-white w-3.5 h-3.5 rounded-full shadow-md transform duration-200 ${e.checked ? "translate-x-3.5" : "translate-x-0"}`}></div>
                                          </div>
                                        </div>
                                      );

                                    case "video": {
                                      const isYoutube = e.val.includes("youtube.com") || e.val.includes("youtu.be");
                                      if (isYoutube) {
                                        let embedUrl = e.val;
                                        if (e.val.includes("watch?v=")) {
                                          embedUrl = e.val.replace("watch?v=", "embed/");
                                        } else if (e.val.includes("youtu.be/")) {
                                          embedUrl = e.val.replace("youtu.be/", "youtube.com/embed/");
                                        }
                                        return (
                                          <div key={idx} className="w-full aspect-video rounded-xl overflow-hidden shadow-md border border-zinc-200 dark:border-zinc-800 shrink-0">
                                            <iframe src={embedUrl} className="w-full h-full border-0" allowFullScreen referrerPolicy="no-referrer" />
                                          </div>
                                        );
                                      }
                                      return (
                                        <div key={idx} className="w-full aspect-video bg-zinc-950 rounded-xl overflow-hidden shadow-md relative group shrink-0">
                                          <video src={e.val} controls className="w-full h-full object-cover" preload="metadata" />
                                        </div>
                                      );
                                    }

                                    case "kamera":
                                      return <PhoneCameraComponent key={idx} />;

                                    case "harita": {
                                      const isCoords = e.lat !== undefined && e.lng !== undefined;
                                      const mapQuery = isCoords ? `${e.lat},${e.lng}` : encodeURIComponent(e.val);
                                      const mapUrl = `https://maps.google.com/maps?q=${mapQuery}&t=&z=13&ie=UTF8&iwloc=&output=embed`;
                                      return (
                                        <div key={idx} className="flex flex-col gap-1.5 text-left shrink-0">
                                          <label className="text-[10px] font-bold text-zinc-400 uppercase tracking-wide px-1">📍 Harita: {isCoords ? "Koordinat" : e.val}</label>
                                          <div className="w-full h-36 bg-zinc-100 dark:bg-zinc-850 border border-zinc-200 dark:border-zinc-800 rounded-xl overflow-hidden shadow-sm">
                                            <iframe src={mapUrl} className="w-full h-full border-0 filter dark:invert dark:hue-rotate-180" loading="lazy" />
                                          </div>
                                        </div>
                                      );
                                    }

                                    case "ikon":
                                      return (
                                        <div key={idx} className="w-full flex justify-center py-1">
                                          <div className="p-2.5 bg-indigo-50 dark:bg-indigo-950/40 text-indigo-600 dark:text-indigo-400 rounded-full shadow-sm flex items-center justify-center shrink-0">
                                            {getIconComponent(e.val)}
                                          </div>
                                        </div>
                                      );

                                    case "menu":
                                      return (
                                        <div key={idx} className="flex flex-col gap-1 text-left bg-zinc-50 dark:bg-zinc-850/40 border border-zinc-150 dark:border-zinc-800 rounded-2xl p-2 shadow-sm shrink-0">
                                          {e.items.map((item: string, menuIdx: number) => (
                                            <button 
                                              key={menuIdx} 
                                              onClick={() => handlePhoneButtonPress(item, item)}
                                              className="w-full text-left p-2.5 text-[11px] text-zinc-700 dark:text-zinc-300 font-bold hover:bg-indigo-500 hover:text-white rounded-xl transition flex items-center justify-between group active:scale-[0.98] cursor-pointer"
                                            >
                                              <span>{item}</span>
                                              <ChevronRight className="w-3.5 h-3.5 opacity-50 group-hover:opacity-100 transition" />
                                            </button>
                                          ))}
                                        </div>
                                      );

                                    case "sekme":
                                      return (
                                        <div key={idx} className="w-full bg-zinc-100 dark:bg-zinc-800/80 p-1 rounded-xl flex gap-1 shadow-inner overflow-x-auto scrollbar-none shrink-0">
                                          {e.items.map((item: string, tabIdx: number) => {
                                            const isActive = e.active_index === tabIdx;
                                            return (
                                              <button
                                                key={tabIdx}
                                                onClick={() => handlePhoneButtonPress(`tab_${item}`, item)}
                                                className={`flex-1 py-1.5 px-3 text-[10px] font-extrabold rounded-lg whitespace-nowrap transition cursor-pointer ${
                                                  isActive 
                                                    ? "bg-white dark:bg-zinc-700 text-indigo-600 dark:text-white shadow-sm" 
                                                    : "text-zinc-500 hover:text-zinc-800 dark:text-zinc-400"
                                                }`}
                                              >
                                                {item}
                                              </button>
                                            );
                                          })}
                                        </div>
                                      );

                                    case "kaydirici":
                                      return (
                                        <div key={idx} className="flex flex-col gap-1 text-left bg-zinc-50 dark:bg-zinc-850/40 border border-zinc-150 dark:border-zinc-800 rounded-xl p-3 shadow-sm shrink-0">
                                          <div className="flex justify-between items-center px-1">
                                            <span className="text-[10px] font-extrabold text-zinc-700 dark:text-zinc-300">{e.val}</span>
                                            <span className="text-[10px] font-bold text-indigo-600 dark:text-indigo-400">{e.value}</span>
                                          </div>
                                          <input 
                                            type="range" 
                                            min={e.min} 
                                            max={e.max} 
                                            defaultValue={e.value} 
                                            onChange={(event) => handlePhoneButtonPress(`${e.val}_degisti`, `${e.val}: ${event.target.value}`)}
                                            className="w-full h-1 bg-zinc-200 dark:bg-zinc-700 rounded-lg appearance-none cursor-pointer accent-indigo-600"
                                          />
                                        </div>
                                      );

                                    case "resim_yukle":
                                      return (
                                        <div key={idx} className="flex flex-col gap-1 text-left shrink-0">
                                          <label className="text-[10px] font-bold text-zinc-400 uppercase tracking-wide px-1">{e.val}</label>
                                          <div className="w-full border-2 border-dashed border-zinc-200 dark:border-zinc-800 hover:border-indigo-500/50 dark:hover:border-indigo-500/50 bg-zinc-50 dark:bg-zinc-850/40 rounded-xl p-4 flex flex-col items-center justify-center gap-1.5 transition cursor-pointer">
                                            <Download className="w-5 h-5 text-zinc-400" />
                                            <span className="text-[9.5px] font-extrabold text-zinc-600 dark:text-zinc-300">Bir dosya seçin veya sürükleyin</span>
                                            <span className="text-[8px] text-zinc-400">PNG, JPG, GIF (Maks. 5MB)</span>
                                          </div>
                                        </div>
                                      );

                                    case "ses":
                                      return <PhoneAudioPlayer key={idx} url={e.val} />;

                                    default:
                                      return null;
                                  }
                                });
                              })()}

                            </div>
                          ) : (
                            <div className="flex-1 flex flex-col justify-center items-center text-center p-4 text-zinc-400 dark:text-zinc-500 gap-2 font-sans select-none">
                              <Smartphone className="w-8 h-8 text-indigo-400 dark:text-indigo-500/60 animate-pulse" />
                              <h5 className="font-bold text-[11px] text-zinc-600 dark:text-zinc-400">Telefon GUI Aktif Değil</h5>
                              <p className="text-[10px] leading-normal max-w-[190px]">
                                Kodunuzda <code>getir telefon</code> kütüphanesini kullanın ve arayüz elemanları (yazi, buton, kart) ekleyin.
                              </p>
                              <button
                                onClick={() => handleLoadExample("Mobil Telefon GUI Tasarımı", `getir telefon\n\ntelefon.ornekler("profil")\n`)}
                                className="mt-2 text-[10px] bg-indigo-600/10 hover:bg-indigo-600/20 text-indigo-500 font-bold px-3 py-1.5 rounded-lg transition"
                              >
                                Profil Örneğini Yükle
                              </button>
                            </div>
                          )}

                          {/* Home Indicator */}
                          <div className="absolute bottom-1 left-1/2 -translate-x-1/2 w-28 h-1 rounded-full bg-zinc-300 dark:bg-zinc-700"></div>

                        </div>
                      </div>
                    </div>

                  </div>
                )}
              </div>
            )}

            {/* FILE 2: read-only translator source code */}
            {activeFile === "ozdil.py" && (
              <div className="w-full h-full flex flex-col font-mono text-xs overflow-hidden bg-zinc-50 dark:bg-zinc-950" id="ozdil-py-view">
                <div className="p-3.5 bg-zinc-100/50 dark:bg-zinc-900/30 border-b border-zinc-200 dark:border-zinc-900 flex items-center justify-between text-zinc-500">
                  <span className="flex items-center gap-1.5"><Code className="w-4 h-4 text-amber-500" /> ozdil.py (Salt Okunur Çekirdek Kodları)</span>
                  <span className="text-[10px] tracking-wider uppercase font-bold bg-amber-500/10 text-amber-600 dark:text-amber-400 px-2 py-0.5 rounded">Python Motoru</span>
                </div>
                <div className="flex-1 overflow-auto p-4 select-text">
                  <pre className="text-zinc-800 dark:text-zinc-300 whitespace-pre-wrap">{ozdilPyContent}</pre>
                </div>
              </div>
            )}

            {/* FILE 3: read-only rich BENI_OKU.md document */}
            {activeFile === "BENI_OKU.md" && (
              <div className="w-full h-full flex flex-col overflow-auto bg-white dark:bg-zinc-950 p-6 lg:p-8" id="readme-view">
                <div className="max-w-3xl mx-auto flex flex-col gap-5 text-sm select-text" id="readme-content">
                  
                  {/* Markdown header */}
                  <div className="border-b border-zinc-200 dark:border-zinc-850 pb-4">
                    <div className="flex items-center gap-2 text-indigo-600 dark:text-indigo-400 font-bold uppercase text-[10px] tracking-widest font-mono">
                      <Sparkle className="w-4 h-4 animate-pulse" /> ÖZDİL TÜRKÇE PROGRAMLAMA DİLİ
                    </div>
                    <h2 className="text-2xl font-black tracking-tight text-zinc-900 dark:text-white mt-1">
                      ÖzDil - Türkçe Kodlama & AST Derleyici
                    </h2>
                    <p className="text-zinc-500 dark:text-zinc-400 text-xs mt-2 leading-relaxed">
                      ÖzDil, yabancı dildeki kod bloklarını Türkçe doğal kod yapısına dönüştüren, Python Abstract Syntax Tree (AST) modülünü temel alan yerel bir derleme simülatörüdür.
                    </p>
                  </div>

                  {/* Section 1: Nasıl Çalışır */}
                  <section className="flex flex-col gap-2">
                    <h3 className="text-xs font-bold text-zinc-400 uppercase tracking-wider flex items-center gap-1.5 font-mono">
                      <CornerDownRight className="w-3.5 h-3.5 text-indigo-500" /> 1. Çalışma Mantığı Nedir?
                    </h3>
                    <p className="text-zinc-600 dark:text-zinc-400 leading-relaxed text-xs">
                      Editöre yazdığınız Türkçe kodlar, sunucudaki token-çözümleyici (lexer) tarafından taranır. Yorumlar, sayılar ve string ifadeler dışındaki Türkçe anahtar kelimeler, Python'daki muadillerine birebir çevrilir. Ardından Python <code>ast.parse()</code> ile Soyut Sözdizimi Ağacı'na ayrıştırılır ve güvenli bir izole alanda koşturulur.
                    </p>
                  </section>

                  {/* Section 2: Temel Kelimeler */}
                  <section className="flex flex-col gap-2">
                    <h3 className="text-xs font-bold text-zinc-400 uppercase tracking-wider flex items-center gap-1.5 font-mono">
                      <CornerDownRight className="w-3.5 h-3.5 text-indigo-500" /> 2. En Sık Kullanılan Deyimler
                    </h3>
                    
                    {/* Small comparison grid */}
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-2.5 mt-1 font-mono text-[11px]">
                      <div className="p-2.5 bg-zinc-50 dark:bg-zinc-900 border border-zinc-150 dark:border-zinc-850 rounded flex flex-col">
                        <span className="font-bold text-indigo-600 dark:text-indigo-400">yazdir(...)</span>
                        <span className="text-[10px] text-zinc-400">print(...)</span>
                      </div>
                      <div className="p-2.5 bg-zinc-50 dark:bg-zinc-900 border border-zinc-150 dark:border-zinc-850 rounded flex flex-col">
                        <span className="font-bold text-indigo-600 dark:text-indigo-400">eger ...:</span>
                        <span className="text-[10px] text-zinc-400">if ...:</span>
                      </div>
                      <div className="p-2.5 bg-zinc-50 dark:bg-zinc-900 border border-zinc-150 dark:border-zinc-850 rounded flex flex-col">
                        <span className="font-bold text-indigo-600 dark:text-indigo-400">dongu i ...:</span>
                        <span className="text-[10px] text-zinc-400">for i ...:</span>
                      </div>
                      <div className="p-2.5 bg-zinc-50 dark:bg-zinc-900 border border-zinc-150 dark:border-zinc-850 rounded flex flex-col">
                        <span className="font-bold text-indigo-600 dark:text-indigo-400">fonksiyon ...:</span>
                        <span className="text-[10px] text-zinc-400">def ...:</span>
                      </div>
                    </div>
                  </section>

                  {/* Section 3: Offline zip explanation */}
                  <section className="p-4 bg-indigo-50/50 dark:bg-indigo-950/20 border border-indigo-100 dark:border-indigo-900/30 rounded-xl flex gap-3.5 items-start">
                    <Download className="w-5 h-5 text-indigo-600 dark:text-indigo-400 shrink-0 mt-0.5" />
                    <div>
                      <h4 className="font-bold text-zinc-900 dark:text-indigo-300 text-xs">
                        Bu Projeyi Bilgisayarınızda veya Telefonunuzda Çalıştırın!
                      </h4>
                      <p className="text-zinc-600 dark:text-zinc-400 text-xs mt-1.5 leading-relaxed">
                        Sağ üst köşedeki <strong>"Projeyi İndir"</strong> butonunu kullanarak ÖzDil interpreter paketini yerel bilgisayarınıza alabilirsiniz. Zip dosyası içerisinde Türkçe kod motorunu çalıştıran <code>ozdil.py</code>, kendi yazdığınız <code>kodumuz.oz</code> ve detaylı offline çalıştırma kılavuzu (README) yer almaktadır.
                      </p>
                    </div>
                  </section>

                  {/* Section 4: Mobile instructions */}
                  <section className="flex flex-col gap-2">
                    <h3 className="text-xs font-bold text-zinc-400 uppercase tracking-wider flex items-center gap-1.5 font-mono">
                      <CornerDownRight className="w-3.5 h-3.5 text-indigo-500" /> 3. Mobilde Çalıştırma (Android Termux)
                    </h3>
                    <p className="text-zinc-600 dark:text-zinc-400 leading-relaxed text-xs">
                      ÖzDil yerel kod motoru tamamen bağımsızdır ve ek bir kütüphaneye ihtiyaç duymaz. Android telefonunuzda çalıştırmak için:
                    </p>
                    <ol className="list-decimal list-inside pl-2 py-1 text-xs text-zinc-500 dark:text-zinc-400 flex flex-col gap-1.5 font-mono">
                      <li>Google Play veya F-Droid üzerinden <strong>Termux</strong> kurun.</li>
                      <li>Python'u yükleyin: <code>pkg install python</code></li>
                      <li>Projeyi Download dizinine çıkarıp gidin: <code>cd /sdcard/Download</code></li>
                      <li>Kodunuzu çalıştırın: <code>python3 ozdil.py kodumuz.oz</code></li>
                    </ol>
                  </section>

                  {/* Action row to go to editor directly */}
                  <button
                    onClick={() => openFileTab("kod_alani.oz")}
                    className="mt-4 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold rounded-lg self-start cursor-pointer shadow-sm flex items-center gap-1.5"
                  >
                    <Code className="w-4 h-4" />
                    <span>Hemen Kodlamaya Başla!</span>
                  </button>

                </div>
              </div>
            )}

          </div>

          {/* BOTTOM TERMINAL PANEL (Console output, Python output, AST tree) */}
          <div 
            className={`bg-[#0c0d10] text-zinc-150 border-t border-zinc-200 dark:border-zinc-900/85 flex flex-col overflow-hidden transition-all duration-300 relative shrink-0 z-10 select-none ${
              panelHeight === "collapsed" 
                ? "h-10" 
                : panelHeight === "maximized" 
                  ? "flex-1" 
                  : "h-48 md:h-64"
            }`} 
            id="terminal-bottom-panel"
          >
            
            {/* Panel Tabs Header Bar */}
            <div className="h-10 bg-zinc-900/40 dark:bg-[#08090c] border-b border-zinc-200/40 dark:border-zinc-900/60 flex items-center justify-between px-4 shrink-0" id="panel-tab-headers">
              <div className="flex items-center gap-1.5 h-full">
                {/* Console Terminal Tab */}
                <button
                  onClick={() => { setPanelTab("terminal"); setPanelHeight("normal"); }}
                  className={`h-full px-4 text-[10px] font-bold tracking-widest uppercase transition-all duration-200 flex items-center gap-2 cursor-pointer ${
                    panelTab === "terminal" && panelHeight !== "collapsed"
                      ? "text-indigo-400 border-b-2 border-indigo-500 bg-[#0c0d10]"
                      : "text-zinc-500 hover:text-zinc-300"
                  }`}
                >
                  <Terminal className="w-4 h-4" />
                  <span>Uçbirim (Terminal)</span>
                </button>

                {/* Python Equivalents Tab */}
                <button
                  onClick={() => { setPanelTab("python"); setPanelHeight("normal"); }}
                  className={`h-full px-4 text-[10px] font-bold tracking-widest uppercase transition-all duration-200 flex items-center gap-2 cursor-pointer ${
                    panelTab === "python" && panelHeight !== "collapsed"
                      ? "text-indigo-400 border-b-2 border-indigo-500 bg-[#0c0d10]"
                      : "text-zinc-500 hover:text-zinc-300"
                  }`}
                >
                  <Globe className="w-4 h-4" />
                  <span>Sözcükler (Lexer)</span>
                </button>

                {/* Python AST Tree Tab */}
                <button
                  onClick={() => { setPanelTab("ast"); setPanelHeight("normal"); }}
                  className={`h-full px-4 text-[10px] font-bold tracking-widest uppercase transition-all duration-200 flex items-center gap-2 cursor-pointer ${
                    panelTab === "ast" && panelHeight !== "collapsed"
                      ? "text-indigo-400 border-b-2 border-indigo-500 bg-[#0c0d10]"
                      : "text-zinc-500 hover:text-zinc-300"
                  }`}
                >
                  <Layers className="w-4 h-4" />
                  <span>ÖzDil AST Ağacı</span>
                </button>
              </div>

              {/* Panel Layout/Action Controls */}
              <div className="flex items-center gap-2 text-zinc-500">
                {/* Clear terminal logs */}
                <button
                  onClick={() => {
                    setResults({ ...results, output: "", error: null });
                    showToast("Terminal konsol çıktısı temizlendi.", "info");
                  }}
                  className="p-1 hover:text-zinc-300 rounded hover:bg-zinc-800 cursor-pointer"
                  title="Konsolu Temizle"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
                
                {/* Collapse / Normal height */}
                {panelHeight === "collapsed" ? (
                  <button
                    onClick={() => setPanelHeight("normal")}
                    className="p-1 hover:text-zinc-300 rounded hover:bg-zinc-800 cursor-pointer"
                    title="Paneli Genişlet"
                  >
                    <ChevronDown className="w-3.5 h-3.5 rotate-180" />
                  </button>
                ) : (
                  <button
                    onClick={() => setPanelHeight("collapsed")}
                    className="p-1 hover:text-zinc-300 rounded hover:bg-zinc-800 cursor-pointer"
                    title="Paneli Gizle"
                  >
                    <ChevronDown className="w-3.5 h-3.5" />
                  </button>
                )}

                {/* Maximize / Normal toggle */}
                {panelHeight === "maximized" ? (
                  <button
                    onClick={() => setPanelHeight("normal")}
                    className="p-1 hover:text-zinc-300 rounded hover:bg-zinc-800 cursor-pointer"
                    title="Normal Boyut"
                  >
                    <Minimize2 className="w-3.5 h-3.5" />
                  </button>
                ) : (
                  <button
                    onClick={() => setPanelHeight("maximized")}
                    className="p-1 hover:text-zinc-300 rounded hover:bg-zinc-800 cursor-pointer"
                    title="Ekranı Kapla"
                  >
                    <Maximize2 className="w-3.5 h-3.5" />
                  </button>
                )}
              </div>
            </div>

            {/* Panel Tab Content screen */}
            {panelHeight !== "collapsed" && (
              <div className="flex-1 p-4 overflow-auto font-mono text-[11px]" id="panel-tab-content-container">
                
                {/* 1. Terminal screen output */}
                {panelTab === "terminal" && (
                  <div className="h-full flex flex-col justify-between" id="terminal-screen-block">
                    <div className="flex-1 overflow-auto select-text selection:bg-zinc-800">
                      
                      {/* Virtual system intro */}
                      <div className="text-zinc-500 mb-2 leading-relaxed">
                        ÖzDil Web Term [Sürüm 1.0.0]<br />
                        Sistem Bağımlılıkları: Python 3.10.12 • GCC 11.4.0<br />
                        surmert@ozdil-web:~$ # Projenizi yerel ortamda çalıştırmak için yukarıdaki 'Çalıştır' butonuna tıklayabilir ya da Ctrl + Enter kombinasyonunu kullanabilirsiniz.
                      </div>

                      {/* Execution feedback log */}
                      {isRunning ? (
                        <div className="flex items-center gap-2 text-indigo-400 py-2">
                          <RefreshCw className="w-4 h-4 animate-spin" />
                          <span>surmert@ozdil-web:~$ python3 ozdil.py kod_alani.oz</span>
                        </div>
                      ) : (results.output || results.error || results.translated || results.awaiting_input) ? (
                        <div className="flex flex-col gap-1">
                          <span className="text-zinc-500">surmert@ozdil-web:~$ python3 ozdil.py kod_alani.oz</span>
                          
                          {results.error ? (
                            results.error_details ? (
                              <div className="mt-3 border border-red-500/30 rounded-lg bg-red-500/5 overflow-hidden font-sans text-left" id="rich-error-report">
                                <div className="bg-red-500/10 px-4 py-2.5 border-b border-red-500/20 flex items-center gap-2 select-none">
                                  <AlertTriangle className="w-4 h-4 text-red-500 animate-pulse animate-bounce" />
                                  <span className="font-bold text-red-600 dark:text-red-400 text-xs tracking-wide uppercase">
                                    {results.error_details.friendly_type || "Çalışma Zamanı Hatası (Runtime Error)"}
                                  </span>
                                  <span className="ml-auto text-[10px] bg-red-500/20 text-red-600 dark:text-red-400 font-mono px-2 py-0.5 rounded font-bold">
                                    Satır: {results.error_details.lineno}
                                  </span>
                                </div>
                                <div className="p-4 flex flex-col gap-3">
                                  <div>
                                    <span className="text-[10px] font-bold text-zinc-400 uppercase tracking-wider block mb-1">Hata Açıklaması</span>
                                    <p className="text-zinc-700 dark:text-zinc-300 text-xs font-semibold leading-relaxed font-sans">
                                      {results.error_details.message}
                                    </p>
                                  </div>
                                  
                                  <div>
                                    <span className="text-[10px] font-bold text-zinc-400 uppercase tracking-wider block mb-1">Hatalı Kod Satırı</span>
                                    <div className="flex bg-zinc-950 border border-red-500/30 rounded overflow-hidden font-mono text-xs">
                                      <div className="bg-red-500/10 border-r border-red-500/20 px-3 py-2 text-red-500 text-right select-none font-bold min-w-[36px]">
                                        {results.error_details.lineno}
                                      </div>
                                      <div className="px-4 py-2 text-zinc-200 overflow-x-auto whitespace-pre w-full flex items-center justify-between">
                                        <span className="font-bold">{results.error_details.line_code || "..."}</span>
                                        <span className="text-[9px] bg-red-500/20 text-red-400 border border-red-500/30 px-1.5 py-0.5 rounded ml-2 select-none uppercase font-sans shrink-0 animate-pulse">
                                          Hata Burada!
                                        </span>
                                      </div>
                                    </div>
                                  </div>

                                  {results.error_details.suggested_fix && (
                                    <div className="bg-amber-500/5 border border-amber-500/20 rounded p-3 flex items-start gap-2.5">
                                      <Lightbulb className="w-4 h-4 text-amber-500 shrink-0 mt-0.5" />
                                      <div>
                                        <span className="text-[10px] font-bold text-amber-600 dark:text-amber-400 uppercase tracking-wider block mb-0.5">Çözüm Önerisi</span>
                                        <p className="text-zinc-600 dark:text-zinc-300 text-[11px] leading-relaxed font-sans">
                                          {results.error_details.suggested_fix}
                                        </p>
                                      </div>
                                    </div>
                                  )}
                                </div>
                              </div>
                            ) : (
                              <pre className="text-red-400 font-bold whitespace-pre-wrap mt-1 leading-relaxed bg-red-950/20 p-3 rounded border border-red-900/30">
                                {results.error}
                              </pre>
                            )
                          ) : (
                            <pre className="text-emerald-400 whitespace-pre-wrap mt-1 leading-relaxed bg-emerald-950/10 p-3 rounded border border-emerald-900/20">
                              {results.output || ">>> [Çıktı Boş: Kod yazdır fonksiyonu içermiyor veya sessiz sonlandı]"}
                            </pre>
                          )}

                          {results.awaiting_input && (
                            <form onSubmit={handleTerminalInputSubmit} className="flex items-center gap-2 mt-2 bg-indigo-950/20 p-2.5 rounded border border-indigo-900/30 text-indigo-400">
                              <span className="font-mono text-[11px] animate-pulse shrink-0">⚡ Girdi bekleniyor:</span>
                              <span className="font-mono text-[11px] font-semibold text-zinc-300 shrink-0">{results.prompt}</span>
                              <input
                                type="text"
                                autoFocus
                                value={terminalInputValue}
                                onChange={(e) => setTerminalInputValue(e.target.value)}
                                className="flex-1 bg-zinc-950/80 dark:bg-zinc-950/80 border border-indigo-500/40 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500/50 rounded px-2.5 py-1 text-[11px] text-zinc-100 font-mono outline-none min-w-[80px]"
                                placeholder="Değer yazıp Enter'a basın..."
                              />
                              <button
                                type="submit"
                                className="bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 text-white font-sans text-[10px] font-bold px-3 py-1 rounded transition shadow-sm"
                              >
                                Gönder
                              </button>
                            </form>
                          )}
                        </div>
                      ) : (
                        <div className="text-zinc-600 italic py-3">Uçbirim boş. Kodunuzu koşturmak için yukarıdaki 'Çalıştır' butonunu kullanın.</div>
                      )}
                    </div>
                  </div>
                )}

                {/* 2. Lexer Tokens screen */}
                {panelTab === "python" && (
                  <div className="h-full flex flex-col select-text" id="python-screen-block">
                    <div className="text-zinc-500 mb-2 text-[10px] font-sans font-semibold uppercase tracking-wider">
                      # ÖzDil Sözcük Çözümleyici (Lexer) Tarafından Çözümlenen Token Listesi
                    </div>
                    {results.translated ? (
                      <pre className="text-zinc-300 whitespace-pre-wrap bg-zinc-950/40 p-3 rounded border border-zinc-900 leading-relaxed">
                        {results.translated}
                      </pre>
                    ) : (
                      <div className="text-zinc-600 italic py-2">Henüz çözümlenmiş sözcük (token) yok. Lütfen önce kodunuzu koşturun.</div>
                    )}
                  </div>
                )}

                {/* 3. AST viewer block */}
                {panelTab === "ast" && (
                  <div className="h-full overflow-auto" id="ast-screen-block">
                    <ASTViewer ast={results.ast} isLoading={isRunning} />
                  </div>
                )}

              </div>
            )}
          </div>

        </main>
      </div>

      {/* MOBILE COMPACT NAVIGATION TAB BAR (Only shown on < 1024px screens) */}
      <nav className="flex lg:hidden bg-zinc-100 dark:bg-zinc-900 border-t border-zinc-200 dark:border-zinc-850 p-1 shrink-0 z-20 select-none" id="mobile-nav-bar">
        <button
          onClick={() => { setSidebarTab(null); setPanelHeight("collapsed"); }}
          className={`flex-1 py-2.5 text-xs font-bold rounded-lg transition flex flex-col items-center gap-1 ${
            !sidebarTab && panelHeight === "collapsed"
              ? "bg-indigo-600 text-white dark:bg-indigo-500 shadow-sm"
              : "text-zinc-500 hover:bg-zinc-200 dark:hover:bg-zinc-850"
          }`}
        >
          <Code className="w-4 h-4" />
          <span>Editör</span>
        </button>

        <button
          onClick={() => {
            if (sidebarTab === "explorer") {
              setSidebarTab(null);
            } else {
              setSidebarTab("explorer");
              setPanelHeight("collapsed");
            }
          }}
          className={`flex-1 py-2.5 text-xs font-bold rounded-lg transition flex flex-col items-center gap-1 ${
            sidebarTab === "explorer"
              ? "bg-indigo-600 text-white dark:bg-indigo-500 shadow-sm"
              : "text-zinc-500 hover:bg-zinc-200 dark:hover:bg-zinc-850"
          }`}
        >
          <Folder className="w-4 h-4" />
          <span>Gezgin</span>
        </button>

        <button
          onClick={() => {
            if (sidebarTab === "search") {
              setSidebarTab(null);
            } else {
              setSidebarTab("search");
              setPanelHeight("collapsed");
            }
          }}
          className={`flex-1 py-2.5 text-xs font-bold rounded-lg transition flex flex-col items-center gap-1 ${
            sidebarTab === "search"
              ? "bg-indigo-600 text-white dark:bg-indigo-500 shadow-sm"
              : "text-zinc-500 hover:bg-zinc-200 dark:hover:bg-zinc-850"
          }`}
        >
          <Search className="w-4 h-4" />
          <span>Sözlük</span>
        </button>

        <button
          onClick={() => {
            if (panelHeight !== "collapsed" && !sidebarTab) {
              setPanelHeight("collapsed");
            } else {
              setSidebarTab(null);
              setPanelHeight("normal");
              setPanelTab("terminal");
            }
          }}
          className={`flex-1 py-2.5 text-xs font-bold rounded-lg transition flex flex-col items-center gap-1 ${
            panelHeight !== "collapsed" && !sidebarTab
              ? "bg-indigo-600 text-white dark:bg-indigo-500 shadow-sm"
              : "text-zinc-500 hover:bg-zinc-200 dark:hover:bg-zinc-850"
          }`}
        >
          <Terminal className="w-4 h-4" />
          <span>Konsol</span>
        </button>

        <button
          onClick={handleRunCode}
          disabled={isRunning}
          className="flex-1 py-2.5 text-xs font-bold rounded-lg transition flex flex-col items-center gap-1 bg-emerald-600 text-white hover:bg-emerald-500 active:bg-emerald-700 disabled:opacity-50"
        >
          <Play className="w-4 h-4 fill-current" />
          <span>Çalıştır</span>
        </button>
      </nav>

      {/* VS CODE BOTTOM STATUS BAR */}
      <footer className="h-6 bg-indigo-600 text-white dark:bg-zinc-950 dark:text-zinc-400 text-[11px] px-3 flex items-center justify-between border-t border-indigo-700 dark:border-zinc-900 shrink-0 select-none" id="status-bar">
        
        {/* Left indicators */}
        <div className="flex items-center gap-3">
          <span className="flex items-center gap-1 hover:bg-indigo-700 dark:hover:bg-zinc-850 px-1.5 h-full transition duration-150 cursor-pointer font-bold">
            <svg className="w-3 h-3 inline" viewBox="0 0 16 16" fill="currentColor">
              <path fillRule="evenodd" d="M11.5 7a4.499 4.499 0 11-8.998 0A4.499 4.499 0 0111.5 7zm-.82 4.74a6 6 0 111.06-1.06l3.04 3.04a.75.75 0 11-1.06 1.06l-3.04-3.04z" />
            </svg>
            <span>main</span>
          </span>
          <span className="hidden sm:inline font-mono">
            {isRunning ? "⚡ Çalıştırılıyor..." : "✓ Hazır"}
          </span>
        </div>

        {/* Center: System status notifications */}
        <div className="text-[10px] tracking-wide select-none hidden md:block">
          ÖzDil Web Studio v1.0.0
        </div>

        {/* Right formatting status */}
        <div className="flex items-center gap-3">
          <span className="hover:bg-indigo-700 dark:hover:bg-zinc-850 px-1.5 h-full flex items-center transition duration-150 cursor-pointer">
            Satır {cursorPos.line}, Sütun {cursorPos.col}
          </span>
          <span className="hidden sm:inline hover:bg-indigo-700 dark:hover:bg-zinc-850 px-1.5 h-full flex items-center transition duration-150 cursor-pointer">
            Girinti: 4 Boşluk
          </span>
          <span className="hidden md:inline hover:bg-indigo-700 dark:hover:bg-zinc-850 px-1.5 h-full flex items-center transition duration-150 cursor-pointer">
            UTF-8
          </span>
          <span className="hover:bg-indigo-700 dark:hover:bg-zinc-850 px-1.5 h-full flex items-center transition duration-150 cursor-pointer font-bold text-indigo-100 dark:text-indigo-400">
            ÖzDil
          </span>
        </div>
      </footer>

      {/* MOBILE MENU SLIDE-OVER DRAWER */}
      {isMobileMenuOpen && (
        <div className="fixed inset-0 z-50 flex md:hidden" id="mobile-menu-drawer">
          {/* Backdrop */}
          <div 
            className="fixed inset-0 bg-black/50 dark:bg-black/75 backdrop-blur-[2px] transition-opacity duration-200" 
            onClick={() => setIsMobileMenuOpen(false)}
          />
          {/* Drawer Panel content */}
          <div className="relative w-72 max-w-[85vw] bg-white dark:bg-zinc-950 h-full shadow-2xl flex flex-col z-50 animate-in slide-in-from-left duration-200 text-xs">
            {/* Drawer Header */}
            <div className="h-14 border-b border-zinc-200 dark:border-zinc-850 px-4 flex items-center justify-between bg-zinc-50 dark:bg-zinc-900">
              <div className="flex items-center gap-2">
                <div className="w-5 h-5 rounded bg-indigo-600 flex items-center justify-center text-[10px] text-white font-black">
                  ÖD
                </div>
                <span className="font-bold text-zinc-800 dark:text-white">ÖzDil Menü</span>
              </div>
              <button 
                onClick={() => setIsMobileMenuOpen(false)}
                className="p-1.5 hover:bg-zinc-200 dark:hover:bg-zinc-800 rounded text-zinc-500 cursor-pointer"
                title="Menüyü Kapat"
              >
                <X className="w-4 h-4 text-zinc-400" />
              </button>
            </div>
            
            {/* Drawer Body Items list */}
            <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-5">
              
              {/* Dosya list section */}
              <div className="flex flex-col gap-1.5">
                <span className="text-[10px] font-bold text-zinc-400 uppercase tracking-wider flex items-center gap-1">
                  <Folder className="w-3.5 h-3.5 text-indigo-500" /> Dosya İşlemleri
                </span>
                <div className="flex flex-col bg-zinc-50 dark:bg-zinc-900/40 rounded-lg border border-zinc-150 dark:border-zinc-850 divide-y divide-zinc-150 dark:divide-zinc-850 overflow-hidden">
                  <button 
                    onClick={() => { openFileTab("kod_alani.oz"); setIsMobileMenuOpen(false); }} 
                    className="w-full text-left px-3 py-2.5 hover:bg-zinc-100 dark:hover:bg-zinc-800 flex items-center justify-between text-zinc-700 dark:text-zinc-300 cursor-pointer"
                  >
                    <span>kod_alani.oz Düzenle</span>
                    <FileCode2 className="w-3.5 h-3.5 text-indigo-500 opacity-80" />
                  </button>
                  <button 
                    onClick={() => { openFileTab("BENI_OKU.md"); setIsMobileMenuOpen(false); }} 
                    className="w-full text-left px-3 py-2.5 hover:bg-zinc-100 dark:hover:bg-zinc-800 flex items-center justify-between text-zinc-700 dark:text-zinc-300 cursor-pointer"
                  >
                    <span>Beni Oku Kılavuzu</span>
                    <Info className="w-3.5 h-3.5 text-emerald-500 opacity-80" />
                  </button>
                  <button 
                    onClick={() => { openFileTab("ozdil.py"); setIsMobileMenuOpen(false); }} 
                    className="w-full text-left px-3 py-2.5 hover:bg-zinc-100 dark:hover:bg-zinc-800 flex items-center justify-between text-zinc-700 dark:text-zinc-300 cursor-pointer"
                  >
                    <span>ozdil.py Çekirdeği İncele</span>
                    <Code className="w-3.5 h-3.5 text-amber-500 opacity-80" />
                  </button>
                  <button 
                    onClick={() => { setCode(""); setIsMobileMenuOpen(false); showToast("Yazım alanı temizlendi.", "info"); }} 
                    className="w-full text-left px-3 py-2.5 hover:bg-red-50 dark:hover:bg-red-950/20 flex items-center justify-between text-red-600 dark:text-red-400 font-semibold cursor-pointer"
                  >
                    <span>Çalışma Alanını Sıfırla</span>
                    <Trash2 className="w-3.5 h-3.5 text-red-500" />
                  </button>
                </div>
              </div>

              {/* Dışa aktar / İndir section */}
              <div className="flex flex-col gap-1.5">
                <span className="text-[10px] font-bold text-zinc-400 uppercase tracking-wider flex items-center gap-1">
                  <Download className="w-3.5 h-3.5 text-indigo-500" /> Dışa Aktar & İndir
                </span>
                <div className="flex flex-col bg-zinc-50 dark:bg-zinc-900/40 rounded-lg border border-zinc-150 dark:border-zinc-850 divide-y divide-zinc-150 dark:divide-zinc-850 overflow-hidden">
                  <button 
                    onClick={() => { handleExportZip(); setIsMobileMenuOpen(false); }} 
                    className="w-full text-left px-3 py-2.5 hover:bg-zinc-100 dark:hover:bg-zinc-800 flex items-center justify-between text-zinc-700 dark:text-zinc-300 font-semibold cursor-pointer"
                  >
                    <span className="flex items-center gap-1.5">
                      <Download className="w-3.5 h-3.5 text-indigo-500" />
                      <span>Projeyi İndir (ZIP)</span>
                    </span>
                    <span className="text-zinc-400 text-[10px]">Tüm Proje</span>
                  </button>
                  <button 
                    onClick={() => { handleExportOzOnly(); setIsMobileMenuOpen(false); }} 
                    className="w-full text-left px-3 py-2.5 hover:bg-zinc-100 dark:hover:bg-zinc-800 flex items-center justify-between text-zinc-700 dark:text-zinc-300 cursor-pointer"
                  >
                    <span className="flex items-center gap-1.5">
                      <FileCode2 className="w-3.5 h-3.5 text-amber-500" />
                      <span>Sadece ÖzDil Kodu (.oz)</span>
                    </span>
                  </button>
                  <button 
                    onClick={() => { handleExportPythonOnly(); setIsMobileMenuOpen(false); }} 
                    className="w-full text-left px-3 py-2.5 hover:bg-zinc-100 dark:hover:bg-zinc-800 flex items-center justify-between text-zinc-700 dark:text-zinc-300 cursor-pointer"
                  >
                    <span className="flex items-center gap-1.5">
                      <Code className="w-3.5 h-3.5 text-emerald-500" />
                      <span>Python Çevirisi (.py)</span>
                    </span>
                  </button>
                </div>
              </div>

              {/* Görünüm & Yardım section */}
              <div className="flex flex-col gap-1.5">
                <span className="text-[10px] font-bold text-zinc-400 uppercase tracking-wider flex items-center gap-1">
                  <Settings className="w-3.5 h-3.5 text-indigo-500" /> Görünüm & Yardım
                </span>
                <div className="flex flex-col bg-zinc-50 dark:bg-zinc-900/40 rounded-lg border border-zinc-150 dark:border-zinc-850 divide-y divide-zinc-150 dark:divide-zinc-850 overflow-hidden">
                  <button 
                    onClick={() => { toggleTheme(); setIsMobileMenuOpen(false); }} 
                    className="w-full text-left px-3 py-2.5 hover:bg-zinc-100 dark:hover:bg-zinc-800 flex items-center justify-between text-zinc-700 dark:text-zinc-300 cursor-pointer"
                  >
                    <span>Tema: {isDark ? "Açık Tema" : "Karanlık Tema"}</span>
                    {isDark ? <Sun className="w-4 h-4 text-amber-500" /> : <Moon className="w-4 h-4 text-indigo-500" />}
                  </button>
                </div>
              </div>

            </div>

            {/* Footer */}
            <div className="p-4 border-t border-zinc-200 dark:border-zinc-850 bg-zinc-50 dark:bg-zinc-900 text-center text-[10px] text-zinc-400">
              ÖzDil Web Studio v1.0.0 · surmert@ozdil-web
            </div>
          </div>
        </div>
      )}

    </div>
  );
}

// Sub-components for expanded ÖzDil Mobile GUI
const PhoneCameraComponent = () => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [captured, setCaptured] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const startCamera = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" } });
      setStream(mediaStream);
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
    } catch (err) {
      setError("Kamera izni verilmedi veya desteklenmiyor.");
    }
  };

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
    }
  };

  const takePhoto = () => {
    if (videoRef.current) {
      const canvas = document.createElement("canvas");
      canvas.width = videoRef.current.videoWidth || 640;
      canvas.height = videoRef.current.videoHeight || 480;
      const ctx = canvas.getContext("2d");
      if (ctx) {
        ctx.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
        setCaptured(canvas.toDataURL("image/png"));
        stopCamera();
      }
    }
  };

  useEffect(() => {
    return () => {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
    };
  }, [stream]);

  return (
    <div className="p-3 bg-zinc-50 dark:bg-zinc-850/60 border border-zinc-150 dark:border-zinc-800 rounded-2xl flex flex-col gap-2">
      <span className="text-[10px] font-bold text-zinc-400 uppercase tracking-wide flex items-center gap-1">📸 Canlı Kamera Eklentisi</span>
      {captured ? (
        <div className="relative rounded-xl overflow-hidden shadow-inner aspect-video">
          <img src={captured} className="w-full h-full object-cover" alt="Captured" />
          <button 
            onClick={() => { setCaptured(null); startCamera(); }}
            className="absolute bottom-2 right-2 bg-indigo-600 text-white font-bold text-[9px] px-2.5 py-1 rounded-lg"
          >
            Yeniden Çek
          </button>
        </div>
      ) : stream ? (
        <div className="relative rounded-xl overflow-hidden shadow-inner aspect-video bg-black">
          <video ref={videoRef} autoPlay playsInline className="w-full h-full object-cover" />
          <button 
            onClick={takePhoto}
            className="absolute bottom-2 left-1/2 -translate-x-1/2 w-8 h-8 rounded-full border-2 border-white bg-red-600 flex items-center justify-center shadow-lg active:scale-95 transition"
          />
        </div>
      ) : (
        <div className="aspect-video bg-zinc-200 dark:bg-zinc-800 rounded-xl flex flex-col items-center justify-center text-center gap-2 p-4">
          {error ? (
            <span className="text-[9px] text-red-500 font-medium">{error}</span>
          ) : (
            <>
              <span className="text-[9px] text-zinc-500">Kamera kapalı</span>
              <button 
                onClick={startCamera}
                className="bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-[9px] px-3 py-1.5 rounded-lg active:scale-95 transition"
              >
                Kamerayı Aç
              </button>
            </>
          )}
        </div>
      )}
    </div>
  );
};

const PhoneAudioPlayer = ({ url }: { url: string; key?: any }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  return (
    <div className="p-3 bg-zinc-50 dark:bg-zinc-850/60 border border-zinc-150 dark:border-zinc-800 rounded-2xl flex items-center justify-between gap-3 shadow-sm text-left">
      <button 
        onClick={() => setIsPlaying(!isPlaying)}
        className="w-8 h-8 rounded-full bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 text-white flex items-center justify-center shadow transition-all shrink-0"
      >
        {isPlaying ? <span className="text-[10px] font-bold">⏸</span> : <span className="text-[10px] font-bold pl-0.5">▶</span>}
      </button>
      <div className="flex-1 flex flex-col gap-1 min-w-0">
        <span className="text-[10px] font-bold text-zinc-700 dark:text-zinc-300 truncate">Ses Çalar: {url.split("/").pop()}</span>
        <div className="flex gap-0.5 items-end h-4">
          {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18].map((i) => (
            <div 
              key={i} 
              className={`bg-indigo-500 rounded-full w-1 transition-all duration-300`} 
              style={{ 
                height: isPlaying ? `${Math.floor(Math.random() * 12) + 4}px` : "4px",
              }}
            />
          ))}
        </div>
      </div>
      <span className="text-[8px] text-zinc-400 self-end">00:15</span>
    </div>
  );
};

const getIconComponent = (name: string) => {
  const iconName = name.toLowerCase().trim();
  switch (iconName) {
    case "ev":
    case "home":
      return <Home className="w-5 h-5" />;
    case "profil":
    case "kullanici":
    case "user":
      return <User className="w-5 h-5" />;
    case "ayarlar":
    case "settings":
      return <Settings className="w-5 h-5" />;
    case "kalp":
    case "heart":
      return <Heart className="w-5 h-5" />;
    case "bildirim":
    case "zil":
    case "bell":
      return <Bell className="w-5 h-5" />;
    case "cop":
    case "trash":
      return <Trash className="w-5 h-5" />;
    case "eposta":
    case "mail":
      return <Mail className="w-5 h-5" />;
    case "yildiz":
    case "star":
      return <Star className="w-5 h-5" />;
    case "harita":
    case "pin":
    case "map":
      return <MapPin className="w-5 h-5" />;
    case "kamera":
    case "camera":
      return <Camera className="w-5 h-5" />;
    case "video":
      return <Video className="w-5 h-5" />;
    case "ses":
    case "muzik":
    case "music":
      return <Music className="w-5 h-5" />;
    case "takvim":
    case "calendar":
      return <Calendar className="w-5 h-5" />;
    case "pusula":
    case "compass":
      return <Compass className="w-5 h-5" />;
    case "sepet":
    case "cart":
    case "shopping-cart":
      return <ShoppingCart className="w-5 h-5" />;
    case "arama":
    case "search":
      return <Search className="w-5 h-5" />;
    case "bilgi":
    case "info":
      return <Info className="w-5 h-5" />;
    default:
      return <Sparkles className="w-5 h-5" />;
  }
};
