import React, { useState, useEffect } from "react";
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
  CornerDownRight,
  Sparkle,
  RotateCcw
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
  const [isDark, setIsDark] = useState(false);
  
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

  const handleRunCode = async () => {
    setIsRunning(true);
    setActiveMenu(null);
    if (window.innerWidth < 1024) {
      setSidebarTab(null);
    }
    setPanelHeight("normal");
    setPanelTab("terminal");
    showToast("Kod derleniyor ve çalıştırılıyor...", "info");

    try {
      const response = await fetch("/api/run", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ code })
      });

      if (!response.ok) {
        throw new Error(`HTTP Hatası: ${response.status}`);
      }

      const data: CompilerResult = await response.json();
      setResults(data);
      if (data.error) {
        showToast("Hata ile sonuçlandı!", "error");
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
            if tok.type == tokenize.NAME and tok.string in MAPPING:
                new_tokens.append((tok.type, MAPPING[tok.string], tok.start, tok.end, tok.line))
            else:
                new_tokens.append(tok)
        return tokenize.untokenize(new_tokens).decode('utf-8')
    except Exception:
        # Hata durumunda güvenli regex tabanlı kelime değişimi devralır
        import re
        sorted_keys = sorted(MAPPING.keys(), key=len, reverse=True)
        lines = code_str.splitlines()
        translated_lines = []
        for line in lines:
            temp_line = line
            for k in sorted_keys:
                temp_line = re.sub(r'\\b' + re.escape(k) + r'\\b', MAPPING[k], temp_line)
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

      {/* VS CODE TOP MENU BAR */}
      <header className="h-10 bg-zinc-100 dark:bg-zinc-900 border-b border-zinc-200 dark:border-zinc-850 flex items-center justify-between px-3 shrink-0" id="top-menu-bar">
        <div className="flex items-center gap-2">
          {/* Retro VS Code logo block */}
          <div className="w-5 h-5 rounded bg-indigo-600 flex items-center justify-center text-[10px] text-white font-black tracking-tighter" title="ÖzDil IDE">
            ÖD
          </div>
          
          {/* File, Edit, View lists */}
          <nav className="hidden md:flex items-center gap-1 text-[11px] font-medium text-zinc-600 dark:text-zinc-300">
            {/* File Menu */}
            <div className="relative">
              <button 
                onClick={() => setActiveMenu(activeMenu === "file" ? null : "file")}
                className={`px-2.5 py-1 rounded hover:bg-zinc-200 dark:hover:bg-zinc-800 cursor-pointer ${activeMenu === "file" ? "bg-zinc-200 dark:bg-zinc-800 text-zinc-900 dark:text-white" : ""}`}
              >
                Dosya
              </button>
              {activeMenu === "file" && (
                <div className="absolute top-7 left-0 w-52 bg-white dark:bg-zinc-950 border border-zinc-200 dark:border-zinc-800 rounded-md shadow-lg py-1 z-50 text-[11px]" onMouseLeave={() => setActiveMenu(null)}>
                  <button onClick={() => { openFileTab("kod_alani.oz"); setActiveMenu(null); }} className="w-full text-left px-3 py-1.5 hover:bg-indigo-600 hover:text-white flex items-center justify-between">
                    <span>kod_alani.oz Düzenle</span>
                    <span className="text-zinc-400 text-[10px]">Ctrl+1</span>
                  </button>
                  <button onClick={() => { openFileTab("BENI_OKU.md"); setActiveMenu(null); }} className="w-full text-left px-3 py-1.5 hover:bg-indigo-600 hover:text-white flex items-center justify-between">
                    <span>Beni Oku Kılavuzunu Aç</span>
                    <span className="text-zinc-400 text-[10px]">Ctrl+2</span>
                  </button>
                  <button onClick={() => { openFileTab("ozdil.py"); setActiveMenu(null); }} className="w-full text-left px-3 py-1.5 hover:bg-indigo-600 hover:text-white flex items-center justify-between">
                    <span>ozdil.py Çekirdeği İncele</span>
                    <span className="text-zinc-400 text-[10px]">Ctrl+3</span>
                  </button>
                  <hr className="my-1 border-zinc-150 dark:border-zinc-850" />
                  <button onClick={() => { setCode(""); setActiveMenu(null); showToast("Yazım alanı temizlendi.", "info"); }} className="w-full text-left px-3 py-1.5 hover:bg-indigo-600 hover:text-white flex items-center justify-between text-red-500 dark:text-red-400">
                    <span>Çalışma Alanını Sıfırla</span>
                    <span className="text-zinc-400 text-[10px]"><Trash2 className="w-3 h-3 inline" /></span>
                  </button>
                  <button onClick={handleExportZip} className="w-full text-left px-3 py-1.5 hover:bg-indigo-600 hover:text-white flex items-center justify-between font-bold text-indigo-600 dark:text-indigo-400">
                    <span>Projeyi ZIP Olarak İndir</span>
                    <span className="text-zinc-400 text-[10px]"><Download className="w-3 h-3 inline" /></span>
                  </button>
                </div>
              )}
            </div>

            {/* Edit Menu */}
            <div className="relative">
              <button 
                onClick={() => setActiveMenu(activeMenu === "edit" ? null : "edit")}
                className={`px-2.5 py-1 rounded hover:bg-zinc-200 dark:hover:bg-zinc-800 cursor-pointer ${activeMenu === "edit" ? "bg-zinc-200 dark:bg-zinc-800 text-zinc-900 dark:text-white" : ""}`}
              >
                Düzen
              </button>
              {activeMenu === "edit" && (
                <div className="absolute top-7 left-0 w-48 bg-white dark:bg-zinc-950 border border-zinc-200 dark:border-zinc-800 rounded-md shadow-lg py-1 z-50 text-[11px]" onMouseLeave={() => setActiveMenu(null)}>
                  <button onClick={() => { setSearchQuery(""); toggleSidebarTab("search"); setActiveMenu(null); }} className="w-full text-left px-3 py-1.5 hover:bg-indigo-600 hover:text-white flex items-center justify-between">
                    <span>Sözlükte Ara</span>
                    <span className="text-zinc-400 text-[10px]">Ctrl+F</span>
                  </button>
                  <button onClick={toggleTheme} className="w-full text-left px-3 py-1.5 hover:bg-indigo-600 hover:text-white flex items-center justify-between">
                    <span>Temayı Değiştir</span>
                    <span className="text-zinc-400 text-[10px]">{isDark ? "Açık" : "Koyu"}</span>
                  </button>
                </div>
              )}
            </div>

            {/* Run Menu */}
            <div className="relative">
              <button 
                onClick={() => setActiveMenu(activeMenu === "run" ? null : "run")}
                className={`px-2.5 py-1 rounded hover:bg-zinc-200 dark:hover:bg-zinc-800 cursor-pointer ${activeMenu === "run" ? "bg-zinc-200 dark:bg-zinc-800 text-zinc-900 dark:text-white" : ""}`}
              >
                Çalıştır
              </button>
              {activeMenu === "run" && (
                <div className="absolute top-7 left-0 w-48 bg-white dark:bg-zinc-950 border border-zinc-200 dark:border-zinc-800 rounded-md shadow-lg py-1 z-50 text-[11px]" onMouseLeave={() => setActiveMenu(null)}>
                  <button onClick={handleRunCode} disabled={isRunning} className="w-full text-left px-3 py-1.5 hover:bg-indigo-600 hover:text-white flex items-center justify-between">
                    <span>Hata Ayıklamadan Çalıştır</span>
                    <span className="text-zinc-400 text-[10px]">Ctrl+Enter</span>
                  </button>
                </div>
              )}
            </div>

            {/* Help Menu */}
            <div className="relative">
              <button 
                onClick={() => setActiveMenu(activeMenu === "help" ? null : "help")}
                className={`px-2.5 py-1 rounded hover:bg-zinc-200 dark:hover:bg-zinc-800 cursor-pointer ${activeMenu === "help" ? "bg-zinc-200 dark:bg-zinc-800 text-zinc-900 dark:text-white" : ""}`}
              >
                Yardım
              </button>
              {activeMenu === "help" && (
                <div className="absolute top-7 left-0 w-52 bg-white dark:bg-zinc-950 border border-zinc-200 dark:border-zinc-800 rounded-md shadow-lg py-1 z-50 text-[11px]" onMouseLeave={() => setActiveMenu(null)}>
                  <button onClick={() => { openFileTab("BENI_OKU.md"); setActiveMenu(null); }} className="w-full text-left px-3 py-1.5 hover:bg-indigo-600 hover:text-white">
                    <span>ÖzDil Rehberini Görüntüle</span>
                  </button>
                  <button onClick={() => { toggleSidebarTab("docs"); setActiveMenu(null); }} className="w-full text-left px-3 py-1.5 hover:bg-indigo-600 hover:text-white">
                    <span>Sözlüğü Yan Panelde Aç</span>
                  </button>
                  <hr className="my-1 border-zinc-150 dark:border-zinc-850" />
                  <div className="px-3 py-1 text-[10px] text-zinc-400 dark:text-zinc-500">
                    Sürüm: ÖzDil Web v1.0.0
                  </div>
                </div>
              )}
            </div>
          </nav>
        </div>

        {/* Center: File Name breadcrumb */}
        <div className="text-[11px] font-mono font-medium text-zinc-500 dark:text-zinc-400 select-none hidden lg:block">
          {activeFile} — ÖzDil Web Studio
        </div>

        {/* Right side: Quick Action Buttons */}
        <div className="flex items-center gap-1.5">
          <button
            onClick={handleRunCode}
            disabled={isRunning}
            className={`flex items-center gap-1.5 px-3 py-1 rounded text-[11px] font-bold transition shadow-sm bg-emerald-600 hover:bg-emerald-500 text-white cursor-pointer disabled:opacity-50`}
            id="top-run-btn"
            title="Kodu Çalıştır (Ctrl + Enter)"
          >
            <Play className={`w-3 h-3 ${isRunning ? "animate-spin" : "fill-current"}`} />
            <span className="hidden sm:inline">{isRunning ? "Çalışıyor..." : "Çalıştır"}</span>
          </button>

          <button
            onClick={handleExportZip}
            disabled={isExporting}
            className="flex items-center gap-1 px-2.5 py-1 rounded text-[11px] font-medium border border-zinc-300 dark:border-zinc-800 bg-white hover:bg-zinc-100 dark:bg-zinc-900 dark:hover:bg-zinc-850 cursor-pointer"
            id="top-export-btn"
            title="Çevrimdışı ve Termux İçin Projeyi İndir"
          >
            <Download className="w-3 h-3 text-zinc-500 dark:text-zinc-400" />
            <span className="hidden sm:inline">Projeyi İndir</span>
          </button>

          <span className="w-px h-4 bg-zinc-200 dark:bg-zinc-800 mx-1"></span>

          {/* Quick theme toggle */}
          <button
            onClick={toggleTheme}
            className="p-1.5 text-zinc-500 hover:text-zinc-900 dark:hover:text-white rounded-md hover:bg-zinc-200 dark:hover:bg-zinc-850 transition cursor-pointer"
            title={isDark ? "Açık Tema" : "Karanlık Tema"}
          >
            {isDark ? <Sun className="w-3.5 h-3.5" /> : <Moon className="w-3.5 h-3.5" />}
          </button>
        </div>
      </header>

      {/* VS CODE WORKSPACE CONTAINER (Activity Bar + Sidebar + Main Editor + Bottom Panel) */}
      <div className="flex-1 flex overflow-hidden relative" id="workspace-container">
        
        {/* ACTIVITY BAR (Leftmost strip) */}
        <aside className="hidden lg:flex w-12 bg-zinc-100 dark:bg-zinc-950 border-r border-zinc-200 dark:border-zinc-900 flex-col justify-between py-1 shrink-0 z-10 select-none" id="activity-bar">
          
          {/* Top Icons group */}
          <div className="flex flex-col items-center gap-0.5">
            {/* File Explorer icon */}
            <button
              onClick={() => toggleSidebarTab("explorer")}
              className={`w-11 h-11 flex items-center justify-center relative cursor-pointer group transition-colors ${
                sidebarTab === "explorer"
                  ? "text-indigo-600 dark:text-indigo-400"
                  : "text-zinc-400 dark:text-zinc-650 hover:text-zinc-700 dark:hover:text-zinc-300"
              }`}
              title="Gezgin / Dosya Yapısı"
            >
              <div className={`absolute left-0 w-0.5 h-7 bg-indigo-600 dark:bg-indigo-400 rounded-r transition-all ${sidebarTab === "explorer" ? "opacity-100" : "opacity-0"}`} />
              <FolderOpen className="w-5 h-5" />
            </button>

            {/* Quick Keyword Dictionary Search */}
            <button
              onClick={() => toggleSidebarTab("search")}
              className={`w-11 h-11 flex items-center justify-center relative cursor-pointer group transition-colors ${
                sidebarTab === "search"
                  ? "text-indigo-600 dark:text-indigo-400"
                  : "text-zinc-400 dark:text-zinc-650 hover:text-zinc-700 dark:hover:text-zinc-300"
              }`}
              title="ÖzDil Sözlük Arama"
            >
              <div className={`absolute left-0 w-0.5 h-7 bg-indigo-600 dark:bg-indigo-400 rounded-r transition-all ${sidebarTab === "search" ? "opacity-100" : "opacity-0"}`} />
              <Search className="w-5 h-5" />
            </button>

            {/* Run & Debug tab */}
            <button
              onClick={() => toggleSidebarTab("run")}
              className={`w-11 h-11 flex items-center justify-center relative cursor-pointer group transition-colors ${
                sidebarTab === "run"
                  ? "text-indigo-600 dark:text-indigo-400"
                  : "text-zinc-400 dark:text-zinc-650 hover:text-zinc-700 dark:hover:text-zinc-300"
              }`}
              title="Çalıştır ve Kılavuz"
            >
              <div className={`absolute left-0 w-0.5 h-7 bg-indigo-600 dark:bg-indigo-400 rounded-r transition-all ${sidebarTab === "run" ? "opacity-100" : "opacity-0"}`} />
              <Bug className="w-5 h-5" />
            </button>

            {/* Words dictionary cheat sheet */}
            <button
              onClick={() => toggleSidebarTab("docs")}
              className={`w-11 h-11 flex items-center justify-center relative cursor-pointer group transition-colors ${
                sidebarTab === "docs"
                  ? "text-indigo-600 dark:text-indigo-400"
                  : "text-zinc-400 dark:text-zinc-650 hover:text-zinc-700 dark:hover:text-zinc-300"
              }`}
              title="Tüm Deyimler Listesi"
            >
              <div className={`absolute left-0 w-0.5 h-7 bg-indigo-600 dark:bg-indigo-400 rounded-r transition-all ${sidebarTab === "docs" ? "opacity-100" : "opacity-0"}`} />
              <BookOpen className="w-5 h-5" />
            </button>

            {/* ozpip packages tab */}
            <button
              onClick={() => toggleSidebarTab("packages")}
              className={`w-11 h-11 flex items-center justify-center relative cursor-pointer group transition-colors ${
                sidebarTab === "packages"
                  ? "text-indigo-600 dark:text-indigo-400"
                  : "text-zinc-400 dark:text-zinc-650 hover:text-zinc-700 dark:hover:text-zinc-300"
              }`}
              title="ÖzDil ozpip Kütüphaneleri"
            >
              <div className={`absolute left-0 w-0.5 h-7 bg-indigo-600 dark:bg-indigo-400 rounded-r transition-all ${sidebarTab === "packages" ? "opacity-100" : "opacity-0"}`} />
              <Layers className="w-5 h-5" />
            </button>
          </div>

          {/* Bottom Settings group */}
          <div className="flex flex-col items-center gap-1 mb-2">
            <button
              onClick={toggleTheme}
              className="w-10 h-10 flex items-center justify-center text-zinc-400 dark:text-zinc-600 hover:text-zinc-700 dark:hover:text-zinc-300 transition cursor-pointer"
              title="Tema Değiştir"
            >
              {isDark ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
            </button>
            <button
              onClick={() => { setCode(EXAMPLES[0].code); openFileTab("kod_alani.oz"); showToast("Sıfırlandı ve ana kod şablonu yüklendi.", "info"); }}
              className="w-10 h-10 flex items-center justify-center text-zinc-400 dark:text-zinc-600 hover:text-red-500 transition cursor-pointer"
              title="Tüm Kodları Sıfırla"
            >
              <RotateCcw className="w-4 h-4" />
            </button>
          </div>
        </aside>

        {/* COLLAPSIBLE SIDEBAR PANEL */}
        {sidebarTab && (
          <div 
            className="w-full lg:w-64 bg-zinc-50 dark:bg-zinc-900 border-r border-zinc-200 dark:border-zinc-900 flex flex-col shrink-0 overflow-hidden select-none z-10" 
            id="sidebar-panel"
          >
            {/* Sidebar Title Header */}
            <div className="h-10 px-4 border-b border-zinc-200 dark:border-zinc-850 flex items-center justify-between" id="sidebar-header">
              <span className="text-[11px] font-bold uppercase tracking-wider text-zinc-500 dark:text-zinc-400">
                {sidebarTab === "explorer" && "GEZGİN: ÖZDİL"}
                {sidebarTab === "search" && "SÖZLÜK ARA"}
                {sidebarTab === "run" && "HATA AYIKLAMA"}
                {sidebarTab === "docs" && "ÖZDİL SÖZLÜĞÜ"}
                {sidebarTab === "packages" && "OZPIP KÜTÜPHANELERİ"}
              </span>
              <button 
                onClick={() => setSidebarTab(null)} 
                className="p-1 hover:bg-zinc-200 dark:hover:bg-zinc-800 rounded transition cursor-pointer"
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
                  <div className="border-b border-zinc-200 dark:border-zinc-850/60">
                    <button 
                      onClick={() => setFolderRootExpanded(!folderRootExpanded)}
                      className="w-full px-3 py-1.5 flex items-center gap-1 bg-zinc-100/50 dark:bg-zinc-900/50 text-[10px] font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wide hover:bg-zinc-200/40 dark:hover:bg-zinc-800/40"
                    >
                      {folderRootExpanded ? <ChevronDown className="w-3 h-3" /> : <ChevronRight className="w-3 h-3" />}
                      Açık Editörler
                    </button>
                    {folderRootExpanded && (
                      <div className="py-1 flex flex-col gap-0.5">
                        {openTabs.map((fileName) => (
                          <button
                            key={fileName}
                            onClick={() => openFileTab(fileName)}
                            className={`w-full px-5 py-1.5 flex items-center justify-between text-left ${
                              activeFile === fileName 
                                ? "bg-zinc-200/60 dark:bg-zinc-800 text-indigo-600 dark:text-indigo-400 font-semibold" 
                                : "text-zinc-600 dark:text-zinc-400 hover:bg-zinc-200/30 dark:hover:bg-zinc-850/50"
                            }`}
                          >
                            <span className="flex items-center gap-1.5 truncate">
                              {fileName.endsWith(".oz") && <FileCode2 className="w-3.5 h-3.5 text-indigo-500 shrink-0" />}
                              {fileName.endsWith(".py") && <Code className="w-3.5 h-3.5 text-amber-500 shrink-0" />}
                              {fileName.endsWith(".md") && <Info className="w-3.5 h-3.5 text-emerald-500 shrink-0" />}
                              <span className="truncate">{fileName}</span>
                            </span>
                            {fileName !== "kod_alani.oz" && (
                              <X 
                                onClick={(e) => closeFileTab(e, fileName)}
                                className="w-3 h-3 text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-200 rounded p-px" 
                              />
                            )}
                          </button>
                        ))}
                      </div>
                    )}
                  </div>

                  {/* Collapsible Section: PROJE DOSYALARI */}
                  <div className="border-b border-zinc-200 dark:border-zinc-850/60">
                    <div className="px-3 py-1.5 flex items-center justify-between bg-zinc-100/50 dark:bg-zinc-900/50 text-[10px] font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wide">
                      <span className="flex items-center gap-1">
                        <Folder className="w-3 h-3 text-indigo-500" /> ÖZDİL_PROJESİ
                      </span>
                    </div>
                    
                    {/* Workspace Files hierarchy list */}
                    <div className="py-1.5 flex flex-col gap-0.5">
                      
                      {/* Sub-folder: Şablonlar / Örnekler */}
                      <div>
                        <button 
                          onClick={() => setFolderExamplesExpanded(!folderExamplesExpanded)}
                          className="w-full px-5 py-1 flex items-center gap-1 hover:bg-zinc-200/30 dark:hover:bg-zinc-850/50 text-zinc-600 dark:text-zinc-400 text-left"
                        >
                          {folderExamplesExpanded ? <ChevronDown className="w-3 h-3" /> : <ChevronRight className="w-3 h-3" />}
                          <Folder className="w-3.5 h-3.5 text-amber-500 shrink-0" />
                          <span>örnekler</span>
                        </button>
                        
                        {folderExamplesExpanded && (
                          <div className="pl-8 pr-1 py-0.5 flex flex-col gap-0.5 border-l border-zinc-200 dark:border-zinc-800 ml-6">
                            {EXAMPLES.map((ex) => (
                              <button
                                key={ex.title}
                                onClick={() => handleLoadExample(ex.title, ex.code)}
                                className="w-full text-left px-2 py-1 text-[11px] text-zinc-500 hover:text-indigo-600 dark:text-zinc-400 dark:hover:text-indigo-400 hover:bg-zinc-200/20 dark:hover:bg-zinc-850/20 truncate flex items-center gap-1"
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
                        className={`w-full px-5 py-1 flex items-center gap-1.5 text-left ${
                          activeFile === "kod_alani.oz" 
                            ? "bg-zinc-200/60 dark:bg-zinc-800 text-indigo-600 dark:text-indigo-400 font-semibold" 
                            : "text-zinc-600 dark:text-zinc-400 hover:bg-zinc-200/30 dark:hover:bg-zinc-850/50"
                        }`}
                      >
                        <FileCode2 className="w-3.5 h-3.5 text-indigo-500 shrink-0" />
                        <span className="truncate font-medium">kod_alani.oz</span>
                      </button>

                      <button
                        onClick={() => openFileTab("ozdil.py")}
                        className={`w-full px-5 py-1 flex items-center gap-1.5 text-left ${
                          activeFile === "ozdil.py" 
                            ? "bg-zinc-200/60 dark:bg-zinc-800 text-indigo-600 dark:text-indigo-400 font-semibold" 
                            : "text-zinc-600 dark:text-zinc-400 hover:bg-zinc-200/30 dark:hover:bg-zinc-850/50"
                        }`}
                      >
                        <Code className="w-3.5 h-3.5 text-amber-500 shrink-0" />
                        <span className="truncate">ozdil.py</span>
                      </button>

                      <button
                        onClick={() => openFileTab("BENI_OKU.md")}
                        className={`w-full px-5 py-1 flex items-center gap-1.5 text-left ${
                          activeFile === "BENI_OKU.md" 
                            ? "bg-zinc-200/60 dark:bg-zinc-800 text-indigo-600 dark:text-indigo-400 font-semibold" 
                            : "text-zinc-600 dark:text-zinc-400 hover:bg-zinc-200/30 dark:hover:bg-zinc-850/50"
                        }`}
                      >
                        <Info className="w-3.5 h-3.5 text-emerald-500 shrink-0" />
                        <span className="truncate">BENI_OKU.md</span>
                      </button>

                    </div>
                  </div>

                </div>
              )}

              {/* 2. SEARCH / DICTIONARY PANEL */}
              {sidebarTab === "search" && (
                <div className="p-3 flex flex-col gap-3" id="search-panel-content">
                  <div className="relative">
                    <input
                      type="text"
                      placeholder="Deyim veya karşılık ara..."
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      className="w-full px-2.5 py-1.5 text-xs bg-white dark:bg-zinc-950 border border-zinc-200 dark:border-zinc-850 rounded focus:outline-none focus:border-indigo-500 dark:focus:border-indigo-400 placeholder-zinc-400 font-mono"
                    />
                    {searchQuery && (
                      <button 
                        onClick={() => setSearchQuery("")} 
                        className="absolute right-2 top-2 p-0.5 hover:bg-zinc-100 dark:hover:bg-zinc-800 rounded"
                      >
                        <X className="w-3 h-3 text-zinc-400" />
                      </button>
                    )}
                  </div>

                  <div className="flex flex-col gap-1.5">
                    <span className="text-[10px] font-bold text-zinc-400 uppercase tracking-wider">
                      Sonuçlar ({filteredKeywords.length})
                    </span>

                    <div className="flex flex-col gap-2 max-h-[calc(h-screen-220px)] overflow-y-auto pr-1">
                      {filteredKeywords.map((item) => (
                        <div 
                          key={item.keyword}
                          className="p-2 bg-white dark:bg-zinc-950 border border-zinc-150 dark:border-zinc-850/60 rounded flex flex-col gap-1 text-[11px]"
                        >
                          <div className="flex justify-between items-center">
                            <span className="font-mono font-bold text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-950/20 px-1.5 py-0.5 rounded">
                              {item.keyword}
                            </span>
                            <span className="font-mono text-[10px] text-zinc-400">
                              → {item.pythonEquivalent}
                            </span>
                          </div>
                          <p className="text-zinc-600 dark:text-zinc-400 text-[11px] leading-relaxed">
                            {item.description}
                          </p>
                          <code className="text-[10px] bg-zinc-50 dark:bg-zinc-900 px-1 py-0.5 rounded font-mono border border-zinc-100 dark:border-zinc-850 text-zinc-500 overflow-hidden text-ellipsis">
                            {item.usage}
                          </code>
                          <button
                            onClick={() => handleCopyKeyword(item.keyword)}
                            className="text-left text-[10px] text-indigo-500 hover:text-indigo-600 dark:text-indigo-400 font-bold self-start mt-1 cursor-pointer"
                          >
                            Panoya Kopyala
                          </button>
                        </div>
                      ))}
                      {filteredKeywords.length === 0 && (
                        <span className="text-zinc-400 italic text-center text-xs py-4">Sonuç bulunamadı.</span>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {/* 3. RUN & DEBUG / CONFIG PANEL */}
              {sidebarTab === "run" && (
                <div className="p-4 flex flex-col gap-4 text-xs" id="run-panel-content">
                  <div className="flex flex-col gap-1.5">
                    <span className="text-[10px] font-bold text-zinc-400 uppercase tracking-wider">
                      Çalıştırma Yapılandırması
                    </span>
                    <div className="p-2 bg-white dark:bg-zinc-950 border border-zinc-200 dark:border-zinc-850 rounded flex items-center justify-between font-mono text-[11px]">
                      <span className="text-zinc-600 dark:text-zinc-300">Python: Current File</span>
                      <span className="w-2 h-2 rounded-full bg-emerald-500" />
                    </div>
                  </div>

                  <div className="flex flex-col gap-2">
                    <button
                      onClick={handleRunCode}
                      disabled={isRunning}
                      className="w-full py-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-bold rounded shadow-sm text-xs flex items-center justify-center gap-1.5 cursor-pointer"
                    >
                      <Play className="w-3.5 h-3.5 fill-current" />
                      <span>{isRunning ? "Çalışıyor..." : "Hata Ayıklamayı Başlat"}</span>
                    </button>

                    <button
                      onClick={handleExportZip}
                      disabled={isExporting}
                      className="w-full py-2 bg-zinc-100 hover:bg-zinc-200 dark:bg-zinc-800 dark:hover:bg-zinc-850 border border-zinc-200 dark:border-zinc-750 text-zinc-700 dark:text-zinc-300 font-semibold rounded text-xs flex items-center justify-center gap-1.5 cursor-pointer"
                    >
                      <Download className="w-3.5 h-3.5" />
                      <span>Projeyi İndir (.zip)</span>
                    </button>
                  </div>

                  <hr className="border-zinc-200 dark:border-zinc-800/80" />

                  <div className="flex flex-col gap-2">
                    <span className="text-[10px] font-bold text-zinc-400 uppercase tracking-wider">
                      Klavye Kısayolları
                    </span>
                    <div className="flex flex-col gap-1.5 font-mono text-[10px] text-zinc-500">
                      <div className="flex justify-between">
                        <span>Kodu Çalıştır:</span>
                        <kbd className="bg-zinc-200 dark:bg-zinc-800 px-1 rounded">Ctrl+Enter</kbd>
                      </div>
                      <div className="flex justify-between">
                        <span>Tamamlama:</span>
                        <kbd className="bg-zinc-200 dark:bg-zinc-800 px-1 rounded">Tab / Enter</kbd>
                      </div>
                      <div className="flex justify-between">
                        <span>Pencereyi Kapat:</span>
                        <kbd className="bg-zinc-200 dark:bg-zinc-800 px-1 rounded">Esc</kbd>
                      </div>
                    </div>
                  </div>

                  <hr className="border-zinc-200 dark:border-zinc-800/80" />

                  <div className="p-3 bg-zinc-100/50 dark:bg-zinc-900/50 border border-zinc-150 dark:border-zinc-800/60 rounded-lg flex flex-col gap-1.5">
                    <span className="font-bold flex items-center gap-1 text-[11px] text-indigo-600 dark:text-indigo-400">
                      <Cpu className="w-3.5 h-3.5" /> ÖzDil Runtime
                    </span>
                    <p className="text-[10px] text-zinc-500 leading-relaxed">
                      Sistem, yazdığınız kodu Python'a çevirip izole bir alt işlem (child_process) kullanarak güvenli bir kum havuzunda yürütür.
                    </p>
                  </div>
                </div>
              )}

              {/* 4. REFERENCE LIST PANEL */}
              {sidebarTab === "docs" && (
                <div className="p-3 flex flex-col gap-2" id="reference-panel-content">
                  <span className="text-[10px] font-bold text-zinc-400 uppercase tracking-wider mb-1">
                    Hızlı Başvuru Sözlüğü
                  </span>
                  <div className="flex flex-col gap-1 max-h-[calc(h-screen-160px)] overflow-y-auto">
                    {KEYWORDS.map((item) => (
                      <button
                        key={item.keyword}
                        onClick={() => handleCopyKeyword(item.keyword)}
                        className="w-full text-left p-2 bg-white dark:bg-zinc-950 hover:bg-zinc-100 dark:hover:bg-zinc-850/50 border border-zinc-150 dark:border-zinc-850/60 rounded transition flex justify-between items-center text-[11px] group font-mono"
                      >
                        <div className="flex flex-col">
                          <span className="font-bold text-indigo-600 dark:text-indigo-400">{item.keyword}</span>
                          <span className="text-[9px] text-zinc-400">py: {item.pythonEquivalent}</span>
                        </div>
                        <span className="text-[9px] bg-zinc-100 dark:bg-zinc-900 text-zinc-400 px-1 py-0.5 rounded group-hover:bg-indigo-600 group-hover:text-white transition">Kopyala</span>
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {/* 5. OZPIP PACKAGES PANEL */}
              {sidebarTab === "packages" && (
                <div className="p-3 flex flex-col gap-3 h-full overflow-hidden" id="packages-panel-content">
                  <div className="flex flex-col gap-1 shrink-0">
                    <p className="text-[10px] text-zinc-500 leading-normal">
                      ÖzDil paketlerini <code className="font-mono bg-zinc-200 dark:bg-zinc-800 px-1 rounded">ozpip</code> ile yükleyip yönetin.
                    </p>
                    
                    {/* Search input */}
                    <div className="relative mt-1.5">
                      <input
                        type="text"
                        placeholder="Paket ara..."
                        value={packageSearchQuery}
                        onChange={(e) => setPackageSearchQuery(e.target.value)}
                        className="w-full px-2.5 py-1.5 text-xs bg-white dark:bg-zinc-950 border border-zinc-200 dark:border-zinc-850 rounded focus:outline-none focus:border-indigo-500 dark:focus:border-indigo-400 placeholder-zinc-400 font-sans"
                      />
                      {packageSearchQuery && (
                        <button 
                          onClick={() => setPackageSearchQuery("")} 
                          className="absolute right-2 top-2 p-0.5 hover:bg-zinc-100 dark:hover:bg-zinc-800 rounded"
                        >
                          <X className="w-3 h-3 text-zinc-400" />
                        </button>
                      )}
                    </div>

                    {/* Filter tabs */}
                    <div className="flex bg-zinc-200/60 dark:bg-zinc-950/40 p-0.5 rounded-md mt-2 text-[10px] font-bold">
                      <button
                        onClick={() => setActivePackageTab("all")}
                        className={`flex-1 py-1 rounded-md text-center transition-all ${
                          activePackageTab === "all"
                            ? "bg-white dark:bg-zinc-800 text-indigo-600 dark:text-indigo-400 shadow-sm"
                            : "text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-300"
                        }`}
                      >
                        Tümü ({packages.length})
                      </button>
                      <button
                        onClick={() => setActivePackageTab("installed")}
                        className={`flex-1 py-1 rounded-md text-center transition-all ${
                          activePackageTab === "installed"
                            ? "bg-white dark:bg-zinc-800 text-indigo-600 dark:text-indigo-400 shadow-sm"
                            : "text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-300"
                        }`}
                      >
                        Kurulu ({packages.filter(p => p.installed).length})
                      </button>
                    </div>
                  </div>

                  {/* Packages List */}
                  <div className="flex-1 overflow-y-auto flex flex-col gap-2.5 pr-1 min-h-0">
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
                          className="p-3 bg-white dark:bg-zinc-950 border border-zinc-150 dark:border-zinc-850/60 rounded-lg flex flex-col gap-2 text-[11px] relative shadow-sm"
                        >
                          <div className="flex items-start justify-between gap-1.5">
                            <div className="flex flex-col">
                              <span className="font-mono font-bold text-zinc-800 dark:text-zinc-100 text-xs">
                                {pkg.isim}
                              </span>
                              <span className="text-[9px] text-zinc-400">
                                v{pkg.surum} · {pkg.yazar}
                              </span>
                            </div>
                            
                            {/* Type badge */}
                            <span className={`px-1.5 py-0.5 rounded text-[8px] font-bold uppercase tracking-wider shrink-0 ${
                              pkg.tur === "ozdil"
                                ? "bg-indigo-50 text-indigo-600 dark:bg-indigo-950/20 dark:text-indigo-400 border border-indigo-100 dark:border-indigo-900/40"
                                : "bg-amber-50 text-amber-600 dark:bg-amber-950/20 dark:text-amber-400 border border-amber-100 dark:border-amber-900/40"
                            }`}>
                              {pkg.tur}
                            </span>
                          </div>

                          <p className="text-zinc-600 dark:text-zinc-400 text-[10.5px] leading-relaxed">
                            {pkg.aciklama}
                          </p>

                          {/* Security permissions */}
                          {pkg.izinler && pkg.izinler.length > 0 && (
                            <div className="flex flex-wrap gap-1 items-center mt-0.5">
                              <span className="text-[8px] font-bold text-zinc-400 uppercase tracking-wide">İzinler:</span>
                              {pkg.izinler.map((perm: string) => (
                                <span key={perm} className="bg-zinc-100 dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 text-zinc-500 dark:text-zinc-400 px-1 py-0.5 rounded text-[8px] font-mono">
                                  🛡️ {perm}
                                </span>
                              ))}
                            </div>
                          )}

                          {/* Action Button */}
                          <div className="flex items-center gap-1.5 mt-1 pt-2 border-t border-zinc-100 dark:border-zinc-850/60">
                            {pkg.installed ? (
                              <>
                                <button
                                  onClick={() => handleUninstallPackage(pkg.isim)}
                                  disabled={loadingPackages}
                                  className="flex-1 py-1 bg-red-50 text-red-600 hover:bg-red-100 dark:bg-red-950/10 dark:text-red-400 dark:hover:bg-red-950/20 rounded font-semibold text-[10px] transition text-center cursor-pointer disabled:opacity-50"
                                >
                                  Kaldır
                                </button>
                                <button
                                  onClick={() => handleInstallPackage(pkg.isim)}
                                  disabled={loadingPackages}
                                  className="px-2 py-1 bg-zinc-100 hover:bg-zinc-200 dark:bg-zinc-850 dark:hover:bg-zinc-800 text-zinc-600 dark:text-zinc-400 rounded font-semibold text-[10px] transition text-center cursor-pointer disabled:opacity-50"
                                  title="Paketi Güncelle"
                                >
                                  Güncelle
                                </button>
                              </>
                            ) : (
                              <button
                                onClick={() => handleInstallPackage(pkg.isim)}
                                disabled={loadingPackages}
                                className="flex-1 py-1 bg-indigo-600 hover:bg-indigo-500 text-white rounded font-bold text-[10px] transition text-center cursor-pointer disabled:opacity-50 flex items-center justify-center gap-1"
                              >
                                {loadingPackages ? "Yükleniyor..." : "Kur"}
                              </button>
                            )}
                          </div>
                        </div>
                      ))}
                    {packages.length === 0 && (
                      <div className="flex flex-col items-center justify-center py-8 text-center text-zinc-400 gap-1.5">
                        <RefreshCw className="w-5 h-5 animate-spin text-indigo-500" />
                        <span className="text-xs">Kütüphaneler yükleniyor...</span>
                      </div>
                    )}
                  </div>

                  {/* Interactive ozpip console block */}
                  {packageOutput && (
                    <div className="shrink-0 border-t border-zinc-200 dark:border-zinc-850/80 pt-2 flex flex-col gap-1.5 max-h-[140px]">
                      <div className="flex justify-between items-center">
                        <span className="text-[9px] font-bold text-zinc-400 uppercase tracking-wider">ozpip terminal çıktısı</span>
                        <button onClick={() => setPackageOutput("")} className="text-[9px] text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-200">Temizle</button>
                      </div>
                      <pre className="flex-1 bg-zinc-950 dark:bg-black text-[9px] font-mono text-zinc-300 p-2 rounded-md overflow-y-auto whitespace-pre-wrap leading-tight select-text max-h-[110px] border border-zinc-850">
                        {packageOutput}
                      </pre>
                    </div>
                  )}
                </div>
              )}

            </div>
          </div>
        )}

        {/* MAIN WORKSPACE WRAPPER (Editor Tabs + Active Canvas + Terminal bottom panel) */}
        <main className={`flex-1 flex flex-col overflow-hidden min-w-0 ${sidebarTab ? "hidden lg:flex" : "flex"}`} id="main-editor-pane">
          
          {/* EDITOR TABS BAR */}
          <div className="h-10 bg-zinc-100 dark:bg-zinc-900 border-b border-zinc-200 dark:border-zinc-900 flex items-center justify-between overflow-hidden shrink-0 select-none" id="editor-tabs-bar">
            
            {/* Left side tabs loop */}
            <div className="flex items-end h-full overflow-x-auto overflow-y-hidden scrollbar-none" id="tabs-scroll-container">
              {openTabs.map((fileName) => {
                const isActive = activeFile === fileName;
                return (
                  <button
                    key={fileName}
                    onClick={() => openFileTab(fileName)}
                    className={`h-9 px-4 flex items-center gap-2 border-r border-zinc-200 dark:border-zinc-950 text-xs font-medium cursor-pointer transition-all ${
                      isActive
                        ? "bg-white dark:bg-zinc-950 text-zinc-900 dark:text-white border-t-2 border-indigo-600 dark:border-indigo-500 font-semibold shadow-inner-top"
                        : "bg-zinc-100/60 hover:bg-zinc-200/50 dark:bg-zinc-900/60 dark:hover:bg-zinc-850 text-zinc-500 dark:text-zinc-500"
                    }`}
                  >
                    {fileName.endsWith(".oz") && <FileCode2 className={`w-3.5 h-3.5 ${isActive ? "text-indigo-500" : "text-zinc-400"}`} />}
                    {fileName.endsWith(".py") && <Code className={`w-3.5 h-3.5 ${isActive ? "text-amber-500" : "text-zinc-400"}`} />}
                    {fileName.endsWith(".md") && <Info className={`w-3.5 h-3.5 ${isActive ? "text-emerald-500" : "text-zinc-400"}`} />}
                    
                    <span>{fileName}</span>
                    
                    {fileName !== "kod_alani.oz" && (
                      <X
                        onClick={(e) => closeFileTab(e, fileName)}
                        className="w-3 h-3 text-zinc-400 hover:text-red-500 rounded-full hover:bg-zinc-200 dark:hover:bg-zinc-850 p-px"
                      />
                    )}
                  </button>
                );
              })}
            </div>

            {/* Right side editor layout helper buttons (minimize sidebar, run button preview) */}
            <div className="flex items-center gap-2 px-3 shrink-0">
              <button
                onClick={handleRunCode}
                disabled={isRunning}
                className="p-1 hover:bg-zinc-200 dark:hover:bg-zinc-800 rounded text-zinc-500 hover:text-emerald-600 dark:text-zinc-400 dark:hover:text-emerald-400 cursor-pointer"
                title="Kodu Çalıştır"
              >
                <Play className={`w-4 h-4 ${isRunning ? "animate-spin" : "fill-current"}`} />
              </button>
            </div>
          </div>

          {/* BREADCRUMB STRIP */}
          <div className="h-6 bg-white dark:bg-zinc-950 border-b border-zinc-100 dark:border-zinc-900/40 px-4 flex items-center gap-1 text-[10px] text-zinc-400 select-none uppercase font-mono shrink-0" id="breadcrumbs">
            <span>projemiz</span>
            <ChevronRight className="w-2.5 h-2.5" />
            <span>src</span>
            <ChevronRight className="w-2.5 h-2.5" />
            <span className="text-zinc-600 dark:text-zinc-300 font-bold">{activeFile}</span>
          </div>

          {/* CODE WORKSPACE CANVAS */}
          <div className="flex-1 relative overflow-hidden bg-white dark:bg-zinc-950" id="active-file-canvas">
            
            {/* FILE 1: main user code edit space */}
            {activeFile === "kod_alani.oz" && (
              <CodeEditor
                value={code}
                onChange={setCode}
                onRun={handleRunCode}
                isRunning={isRunning}
                flat={true}
                onCursorChange={(line, col) => setCursorPos({ line, col })}
              />
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
            className={`bg-zinc-950 text-zinc-200 border-t border-zinc-200 dark:border-zinc-900 flex flex-col overflow-hidden transition-all duration-300 relative shrink-0 z-10 select-none ${
              panelHeight === "collapsed" 
                ? "h-9" 
                : panelHeight === "maximized" 
                  ? "flex-1" 
                  : "h-64"
            }`} 
            id="terminal-bottom-panel"
          >
            
            {/* Panel Tabs Header Bar */}
            <div className="h-9 bg-zinc-900 border-b border-zinc-800 flex items-center justify-between px-3 shrink-0" id="panel-tab-headers">
              <div className="flex items-center gap-1 h-full">
                {/* Console Terminal Tab */}
                <button
                  onClick={() => { setPanelTab("terminal"); setPanelHeight("normal"); }}
                  className={`h-full px-3.5 text-[11px] font-bold tracking-wide uppercase transition-all flex items-center gap-1.5 cursor-pointer ${
                    panelTab === "terminal" && panelHeight !== "collapsed"
                      ? "text-indigo-400 border-b-2 border-indigo-500 bg-zinc-950"
                      : "text-zinc-500 hover:text-zinc-300"
                  }`}
                >
                  <Terminal className="w-3.5 h-3.5" />
                  <span>Uçbirim (Terminal)</span>
                </button>

                {/* Python Equivalents Tab */}
                <button
                  onClick={() => { setPanelTab("python"); setPanelHeight("normal"); }}
                  className={`h-full px-3.5 text-[11px] font-bold tracking-wide uppercase transition-all flex items-center gap-1.5 cursor-pointer ${
                    panelTab === "python" && panelHeight !== "collapsed"
                      ? "text-indigo-400 border-b-2 border-indigo-500 bg-zinc-950"
                      : "text-zinc-500 hover:text-zinc-300"
                  }`}
                >
                  <Globe className="w-3.5 h-3.5" />
                  <span>Sözcükler (Lexer)</span>
                </button>

                {/* Python AST Tree Tab */}
                <button
                  onClick={() => { setPanelTab("ast"); setPanelHeight("normal"); }}
                  className={`h-full px-3.5 text-[11px] font-bold tracking-wide uppercase transition-all flex items-center gap-1.5 cursor-pointer ${
                    panelTab === "ast" && panelHeight !== "collapsed"
                      ? "text-indigo-400 border-b-2 border-indigo-500 bg-zinc-950"
                      : "text-zinc-500 hover:text-zinc-300"
                  }`}
                >
                  <Layers className="w-3.5 h-3.5" />
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
                      ) : (results.output || results.error || results.translated) ? (
                        <div className="flex flex-col gap-1">
                          <span className="text-zinc-500">surmert@ozdil-web:~$ python3 ozdil.py kod_alani.oz</span>
                          
                          {results.error ? (
                            <pre className="text-red-400 font-bold whitespace-pre-wrap mt-1 leading-relaxed bg-red-950/20 p-3 rounded border border-red-900/30">
                              {results.error}
                            </pre>
                          ) : (
                            <pre className="text-emerald-400 whitespace-pre-wrap mt-1 leading-relaxed bg-emerald-950/10 p-3 rounded border border-emerald-900/20">
                              {results.output || ">>> [Çıktı Boş: Kod yazdır fonksiyonu içermiyor veya sessiz sonlandı]"}
                            </pre>
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

    </div>
  );
}
