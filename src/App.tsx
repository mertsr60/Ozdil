import React, { useState, useEffect } from "react";
import {
  Terminal,
  BookOpen,
  Layers,
  Globe,
  RefreshCw,
  CheckCircle2,
  Moon,
  Sun,
  ChevronRight,
  Info,
  X,
  Code,
  Sparkles,
  Play,
  Copy,
  Check,
  Download
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
  const [activeTab, setActiveTab] = useState<"console" | "ast" | "python">("console");
  const [copiedKeyword, setCopiedKeyword] = useState<string | null>(null);
  const [isDark, setIsDark] = useState(false);
  const [showWelcome, setShowWelcome] = useState(true);

  // Mobile Layout Tab selection: "editor", "results", "docs"
  const [mobileTab, setMobileTab] = useState<"editor" | "results" | "docs">("editor");

  // Sync Dark mode
  useEffect(() => {
    // Check local storage or system preference
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark" || (!savedTheme && window.matchMedia("(prefers-color-scheme: dark)").matches)) {
      setIsDark(true);
      document.documentElement.classList.add("dark");
    }
  }, []);

  const toggleTheme = () => {
    if (isDark) {
      setIsDark(false);
      document.documentElement.classList.remove("dark");
      localStorage.setItem("theme", "light");
    } else {
      setIsDark(true);
      document.documentElement.classList.add("dark");
      localStorage.setItem("theme", "dark");
    }
  };

  const handleExportZip = async () => {
    setIsExporting(true);
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
    } catch (err) {
      alert(`Dışa aktarma başarısız oldu: ${(err as Error).message}`);
    } finally {
      setIsExporting(false);
    }
  };

  const handleRunCode = async () => {
    setIsRunning(true);
    // On mobile, switch view automatically to see the terminal output when running!
    if (window.innerWidth < 1024) {
      setMobileTab("results");
    }
    setActiveTab("console");

    try {
      const response = await fetch("/api/run", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ code })
      });

      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status}`);
      }

      const data: CompilerResult = await response.json();
      setResults(data);
    } catch (err) {
      setResults({
        translated: "",
        ast: null,
        output: "",
        error: `Kod çalıştırılırken sunucu hatası oluştu: ${(err as Error).message}`
      });
    } finally {
      setIsRunning(false);
    }
  };

  const handleLoadExample = (exampleCode: string) => {
    setCode(exampleCode);
    setMobileTab("editor");
    // Clear old results
    setResults({
      translated: "",
      ast: null,
      output: "",
      error: null
    });
  };

  const handleCopyKeyword = (keyword: string) => {
    navigator.clipboard.writeText(keyword);
    setCopiedKeyword(keyword);
    setTimeout(() => setCopiedKeyword(null), 1500);
  };

  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950 text-zinc-800 dark:text-zinc-100 transition-colors duration-300 flex flex-col font-sans" id="app-root">
      
      {/* Premium Header */}
      <header className="sticky top-0 z-30 bg-white/80 dark:bg-zinc-900/80 backdrop-blur-md border-b border-zinc-200 dark:border-zinc-850 px-4 py-3.5 lg:px-8 flex items-center justify-between shadow-sm" id="main-header">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-500 dark:from-indigo-500 dark:to-violet-400 flex items-center justify-center text-white font-black text-lg tracking-wider shadow-md shadow-indigo-200 dark:shadow-none" id="logo-icon">
            ÖD
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="font-bold text-base md:text-lg tracking-tight bg-gradient-to-r from-zinc-900 via-indigo-950 to-zinc-900 dark:from-white dark:via-zinc-200 dark:to-white bg-clip-text text-transparent">
                ÖzDil Oyun Alanı
              </h1>
              <span className="flex items-center gap-1.5 px-2 py-0.5 rounded-full bg-emerald-50 dark:bg-emerald-950/40 text-[10px] font-bold text-emerald-600 dark:text-emerald-400 border border-emerald-200/40 select-none">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                Python Sunucusu Bağlı
              </span>
            </div>
            <p className="text-[11px] text-zinc-500 dark:text-zinc-400 hidden sm:block">
              Türkçe kodlama dili ve Python AST derleme simülatörü
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={handleExportZip}
            disabled={isExporting}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-xl text-xs font-bold transition shadow-sm border border-zinc-200 dark:border-zinc-800 ${
              isExporting
                ? "bg-zinc-100 text-zinc-400 dark:bg-zinc-850 cursor-not-allowed"
                : "bg-indigo-50 hover:bg-indigo-100 text-indigo-700 dark:bg-indigo-950/40 dark:hover:bg-indigo-900/60 dark:text-indigo-300"
            }`}
            id="export-zip-btn"
            title="Dili ve Kodları Çevrimdışı/Termux için Dışa Aktar (.zip)"
          >
            <Download className={`w-3.5 h-3.5 ${isExporting ? "animate-bounce" : ""}`} />
            <span className="hidden sm:inline">Dışa Aktar (.zip)</span>
            <span className="sm:hidden">Dışa Aktar</span>
          </button>

          <button
            onClick={toggleTheme}
            className="p-2 text-zinc-600 dark:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-800 rounded-lg transition"
            title={isDark ? "Açık Tema" : "Karanlık Tema"}
            id="theme-toggle"
          >
            {isDark ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
          </button>
        </div>
      </header>

      {/* Main Workspace Frame */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 lg:p-6 flex flex-col gap-5 overflow-hidden" id="workspace-layout">
        
        {/* Welcome Info Card */}
        {showWelcome && (
          <div className="relative bg-gradient-to-r from-indigo-50 via-white to-indigo-50/50 dark:from-indigo-950/20 dark:via-zinc-900 dark:to-indigo-950/10 border border-indigo-100 dark:border-indigo-900/30 rounded-xl p-4 md:p-5 flex gap-4 items-start shadow-sm transition" id="welcome-card">
            <div className="p-2.5 bg-indigo-100 dark:bg-indigo-950/60 text-indigo-600 dark:text-indigo-400 rounded-lg shrink-0">
              <Sparkles className="w-5 h-5" />
            </div>
            <div className="flex-1">
              <h3 className="text-sm font-bold text-indigo-950 dark:text-indigo-200">
                Kendi Türkçe Kodlama Dilinizi Keşfedin!
              </h3>
              <p className="text-xs text-zinc-600 dark:text-zinc-400 mt-1.5 leading-relaxed max-w-4xl">
                ÖzDil, standart Türkçe anahtar kelimeleri doğrudan Python AST (Abstract Syntax Tree) modülüne taşıyan benzersiz bir tasarımdır. Sol kısımdaki editörde kodunuzu yazarken <strong>gelişmiş hayalet tamamlama (ghost suggestions)</strong> desteğinden yararlanabilir, Tab tuşuyla kodunuzu hızlıca tamamlayabilirsiniz. Çalıştırdığınızda kodunuz anında Python AST yapısına ayrıştırılır ve güvenli bir izole alanda çalıştırılır.
              </p>
              
              {/* Keywords summary badges preview */}
              <div className="flex flex-wrap gap-1.5 mt-3.5">
                <span className="text-[10px] font-bold uppercase tracking-wider text-zinc-400 mr-1 self-center">Temel Dönüşümler:</span>
                <span className="px-2 py-0.5 bg-zinc-100 dark:bg-zinc-800 text-[11px] text-zinc-600 dark:text-zinc-400 rounded-md font-mono">yazdir → print</span>
                <span className="px-2 py-0.5 bg-zinc-100 dark:bg-zinc-800 text-[11px] text-zinc-600 dark:text-zinc-400 rounded-md font-mono">eger → if</span>
                <span className="px-2 py-0.5 bg-zinc-100 dark:bg-zinc-800 text-[11px] text-zinc-600 dark:text-zinc-400 rounded-md font-mono">dongu → for</span>
                <span className="px-2 py-0.5 bg-zinc-100 dark:bg-zinc-800 text-[11px] text-zinc-600 dark:text-zinc-400 rounded-md font-mono">fonksiyon → def</span>
                <span className="px-2 py-0.5 bg-zinc-100 dark:bg-zinc-800 text-[11px] text-zinc-600 dark:text-zinc-400 rounded-md font-mono">dene → try</span>
              </div>
            </div>
            <button
              onClick={() => setShowWelcome(false)}
              className="absolute top-3 right-3 p-1 text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-300 rounded-full transition"
              id="close-welcome"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        )}

        {/* Templates selector list */}
        <div className="flex flex-col gap-2" id="examples-block">
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold text-zinc-400 uppercase tracking-wider flex items-center gap-1">
              <Layers className="w-3.5 h-3.5 text-indigo-500" /> Şablon Kütüphanesi
            </span>
            <span className="text-[10px] text-zinc-400">(Tıklayarak editöre yükleyin)</span>
          </div>
          <div className="flex gap-2 overflow-x-auto pb-1 scrollbar-thin select-none" id="examples-list">
            {EXAMPLES.map((ex) => (
              <button
                key={ex.title}
                onClick={() => handleLoadExample(ex.code)}
                className="shrink-0 px-3.5 py-2 bg-white hover:bg-zinc-50 dark:bg-zinc-900 dark:hover:bg-zinc-850 border border-zinc-200 dark:border-zinc-800 rounded-xl text-left transition group cursor-pointer shadow-sm"
              >
                <div className="font-semibold text-xs text-zinc-850 dark:text-zinc-200 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 flex items-center gap-1.5">
                  <Code className="w-3 h-3 text-zinc-400" /> {ex.title}
                </div>
                <p className="text-[10px] text-zinc-400 dark:text-zinc-500 mt-0.5 max-w-[200px] line-clamp-1">
                  {ex.description}
                </p>
              </button>
            ))}
          </div>
        </div>

        {/* Mobile View Navigation Buttons (Only visible on screens &lt; 1024px) */}
        <div className="flex lg:hidden bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 p-1 rounded-xl shadow-sm" id="mobile-navigation">
          <button
            onClick={() => setMobileTab("editor")}
            className={`flex-1 py-2.5 text-xs font-bold rounded-lg transition flex items-center justify-center gap-2 ${
              mobileTab === "editor"
                ? "bg-indigo-600 text-white dark:bg-indigo-500 shadow-sm"
                : "text-zinc-500 hover:bg-zinc-100 dark:hover:bg-zinc-800"
            }`}
          >
            <Code className="w-4 h-4" /> Editör
          </button>
          <button
            onClick={() => setMobileTab("results")}
            className={`flex-1 py-2.5 text-xs font-bold rounded-lg transition flex items-center justify-center gap-2 ${
              mobileTab === "results"
                ? "bg-indigo-600 text-white dark:bg-indigo-500 shadow-sm"
                : "text-zinc-500 hover:bg-zinc-100 dark:hover:bg-zinc-800"
            }`}
          >
            <Terminal className="w-4 h-4" /> Çıktı & AST
          </button>
          <button
            onClick={() => setMobileTab("docs")}
            className={`flex-1 py-2.5 text-xs font-bold rounded-lg transition flex items-center justify-center gap-2 ${
              mobileTab === "docs"
                ? "bg-indigo-600 text-white dark:bg-indigo-500 shadow-sm"
                : "text-zinc-500 hover:bg-zinc-100 dark:hover:bg-zinc-800"
            }`}
          >
            <BookOpen className="w-4 h-4" /> Kılavuz ({KEYWORDS.length})
          </button>
        </div>

        {/* Layout Workspace Grid */}
        <div className="flex-1 grid grid-cols-1 lg:grid-cols-12 gap-5 min-h-[500px] items-stretch overflow-hidden" id="workspace-grid">
          
          {/* Left Block: Editor (Always visible on desktop, tabbed on mobile) */}
          <div className={`lg:col-span-7 flex flex-col h-full ${mobileTab === "editor" ? "flex" : "hidden lg:flex"}`} id="editor-left-block">
            <CodeEditor
              value={code}
              onChange={setCode}
              onRun={handleRunCode}
              isRunning={isRunning}
            />
          </div>

          {/* Right Block: Outputs & Compile analysis (Always visible on desktop, tabbed on mobile) */}
          <div className={`lg:col-span-5 flex flex-col h-full bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl overflow-hidden shadow-sm ${
            mobileTab === "results" ? "flex" : "hidden lg:flex"
          }`} id="results-right-block">
            
            {/* Tab Switches */}
            <div className="flex border-b border-zinc-200 dark:border-zinc-800 bg-zinc-50/50 dark:bg-zinc-900/50 p-1" id="tab-switches">
              <button
                onClick={() => setActiveTab("console")}
                className={`flex-1 py-2 text-xs font-bold rounded-lg transition flex items-center justify-center gap-1.5 ${
                  activeTab === "console"
                    ? "bg-white dark:bg-zinc-800 text-indigo-600 dark:text-indigo-400 shadow-sm"
                    : "text-zinc-500 hover:bg-zinc-100 dark:hover:bg-zinc-800"
                }`}
                id="console-tab-btn"
              >
                <Terminal className="w-3.5 h-3.5" /> Konsol Çıktısı
              </button>
              
              <button
                onClick={() => setActiveTab("ast")}
                className={`flex-1 py-2 text-xs font-bold rounded-lg transition flex items-center justify-center gap-1.5 ${
                  activeTab === "ast"
                    ? "bg-white dark:bg-zinc-800 text-indigo-600 dark:text-indigo-400 shadow-sm"
                    : "text-zinc-500 hover:bg-zinc-100 dark:hover:bg-zinc-800"
                }`}
                id="ast-tab-btn"
              >
                <Layers className="w-3.5 h-3.5" /> Python AST Ağacı
              </button>

              <button
                onClick={() => setActiveTab("python")}
                className={`flex-1 py-2 text-xs font-bold rounded-lg transition flex items-center justify-center gap-1.5 ${
                  activeTab === "python"
                    ? "bg-white dark:bg-zinc-800 text-indigo-600 dark:text-indigo-400 shadow-sm"
                    : "text-zinc-500 hover:bg-zinc-100 dark:hover:bg-zinc-800"
                }`}
                id="python-tab-btn"
              >
                <Globe className="w-3.5 h-3.5" /> Python Karşılığı
              </button>
            </div>

            {/* Tab Contents Frame */}
            <div className="flex-1 p-4 overflow-y-auto" id="tab-contents-frame">
              {activeTab === "console" && (
                <div className="flex flex-col h-full gap-3" id="console-tab-content">
                  {/* Status header */}
                  <div className="flex items-center justify-between text-xs text-zinc-500 dark:text-zinc-400" id="console-header-status">
                    <span className="font-semibold flex items-center gap-1.5 uppercase font-mono tracking-wider">
                      <Terminal className="w-3.5 h-3.5 text-indigo-500" /> terminal_konsolu
                    </span>
                    <div className="flex items-center gap-2">
                      {results.error ? (
                        <span className="px-2 py-0.5 rounded bg-red-50 dark:bg-red-950/20 text-red-600 dark:text-red-400 border border-red-200/20 font-bold">
                          Hata Oluştu
                        </span>
                      ) : results.output || results.translated ? (
                        <span className="px-2 py-0.5 rounded bg-emerald-50 dark:bg-emerald-950/20 text-emerald-600 dark:text-emerald-400 border border-emerald-200/20 font-bold">
                          Derleme Başarılı
                        </span>
                      ) : (
                        <span className="text-zinc-400 italic">Hazır</span>
                      )}
                    </div>
                  </div>

                  {/* Terminal Display Screen */}
                  <div className="flex-1 bg-zinc-950 text-zinc-200 rounded-xl p-4 font-mono text-xs overflow-auto border border-zinc-900 shadow-inner min-h-[300px] flex flex-col" id="terminal-screen">
                    {isRunning ? (
                      <div className="flex-1 flex flex-col items-center justify-center text-zinc-400 gap-3">
                        <RefreshCw className="w-6 h-6 animate-spin text-indigo-500" />
                        <span>Kod güvenli sunucuda çalıştırılıyor...</span>
                      </div>
                    ) : results.error ? (
                      <div className="text-red-400 whitespace-pre-wrap flex-1" id="terminal-error-display">
                        <span className="text-red-500 font-bold">🚨 DERLEME VEYA ÇALIŞMA HATASI:</span>
                        {"\n\n"}{results.error}
                      </div>
                    ) : results.output ? (
                      <div className="whitespace-pre-wrap flex-1 text-emerald-400 selection:bg-emerald-900 selection:text-white" id="terminal-output-display">
                        {results.output}
                        {"\n"}
                        <span className="text-zinc-500 italic text-[10px] select-none block mt-2 border-t border-zinc-900 pt-2">
                          👉 İşlem sıfır hata ile tamamlandı.
                        </span>
                      </div>
                    ) : (
                      <div className="flex-1 flex flex-col items-center justify-center text-zinc-500 text-center px-4" id="terminal-prompt">
                        <Terminal className="w-8 h-8 text-zinc-700 mb-2" />
                        <span className="font-bold text-zinc-400">Konsol Boş</span>
                        <span className="text-[11px] text-zinc-600 mt-1 max-w-xs">
                          Kodunuzun çıktılarını görmek için yukarıdaki "Çalıştır" düğmesine tıklayın ya da <kbd className="bg-zinc-800 text-zinc-400 px-1 rounded font-mono">Ctrl + Enter</kbd> kısayolunu kullanın.
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {activeTab === "ast" && (
                <div className="h-full" id="ast-tab-content">
                  <ASTViewer ast={results.ast} isLoading={isRunning} />
                </div>
              )}

              {activeTab === "python" && (
                <div className="flex flex-col h-full gap-3" id="python-tab-content">
                  <div className="flex items-center justify-between text-xs text-zinc-500 dark:text-zinc-400">
                    <span className="font-semibold uppercase tracking-wider font-mono">
                      python_kod_esdegeri.py
                    </span>
                    <span className="text-[10px] text-zinc-400">Derlenen gerçek Python kodu</span>
                  </div>

                  <div className="flex-1 bg-zinc-50 dark:bg-zinc-950 text-zinc-800 dark:text-zinc-300 rounded-xl p-4 font-mono text-xs overflow-auto border border-zinc-200 dark:border-zinc-900 min-h-[300px]" id="python-code-display">
                    {results.translated ? (
                      <pre className="whitespace-pre-wrap selection:bg-indigo-100 dark:selection:bg-indigo-950">
                        {results.translated}
                      </pre>
                    ) : (
                      <div className="h-full flex flex-col items-center justify-center text-zinc-400 text-center px-4">
                        <Code className="w-8 h-8 text-zinc-300 dark:text-zinc-700 mb-2" />
                        <span className="font-semibold text-zinc-500">Çeviri Bekleniyor</span>
                        <p className="text-[11px] text-zinc-400 mt-1 max-w-xs">
                          Kodunuzu çalıştırdığınızda, Türkçe kelimelerin Python karşılıklarına birebir nasıl dönüştüğünü burada görebilirsiniz.
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Right Block Sidebar - Documentation (Only visible on desktop by default, tabbed on mobile) */}
          <div className={`lg:col-span-12 flex flex-col bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl overflow-hidden shadow-sm p-4 ${
            mobileTab === "docs" ? "flex" : "hidden lg:flex"
          }`} id="docs-sidebar-block">
            <div className="flex items-center justify-between pb-3 border-b border-zinc-200 dark:border-zinc-800" id="docs-header">
              <div className="flex items-center gap-2">
                <BookOpen className="w-4 h-4 text-indigo-500" />
                <h3 className="font-bold text-sm text-zinc-850 dark:text-zinc-100">
                  ÖzDil Türkçe Sözlük & Kod Kılavuzu
                </h3>
              </div>
              <span className="px-2 py-0.5 bg-zinc-100 dark:bg-zinc-800 text-[10px] font-bold rounded-md font-mono text-zinc-500">
                {KEYWORDS.length} Anahtar Kelime
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3.5 mt-4 overflow-y-auto max-h-[400px]" id="docs-keywords-grid">
              {KEYWORDS.map((item) => (
                <div
                  key={item.keyword}
                  className="p-3 bg-zinc-50 hover:bg-zinc-100/50 dark:bg-zinc-950/40 dark:hover:bg-zinc-950/80 border border-zinc-150 dark:border-zinc-800/60 rounded-xl transition flex flex-col justify-between group"
                >
                  <div>
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-mono font-bold text-xs text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-950/30 px-2 py-0.5 rounded">
                        {item.keyword}
                      </span>
                      <span className="text-[10px] font-mono text-zinc-400 italic">
                        python: <strong className="text-zinc-500 dark:text-zinc-300 font-semibold">{item.pythonEquivalent}</strong>
                      </span>
                    </div>
                    <p className="text-xs text-zinc-650 dark:text-zinc-400 mt-1.5 leading-relaxed">
                      {item.description}
                    </p>
                  </div>

                  <div className="mt-3 pt-2.5 border-t border-zinc-200/40 dark:border-zinc-800/40 flex items-center justify-between gap-2">
                    <code className="text-[10px] font-mono text-zinc-500 dark:text-zinc-400 bg-white dark:bg-zinc-900 border border-zinc-100 dark:border-zinc-850 px-1.5 py-0.5 rounded flex-1 truncate">
                      {item.usage}
                    </code>
                    
                    <button
                      onClick={() => handleCopyKeyword(item.keyword)}
                      className="p-1 text-zinc-400 hover:text-indigo-600 dark:hover:text-indigo-400 hover:bg-white dark:hover:bg-zinc-900 border border-transparent hover:border-zinc-200 dark:hover:border-zinc-850 rounded transition shrink-0 cursor-pointer"
                      title="Kodu Kopyala"
                    >
                      {copiedKeyword === item.keyword ? (
                        <Check className="w-3 h-3 text-emerald-500" />
                      ) : (
                        <Copy className="w-3 h-3" />
                      )}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>

        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white dark:bg-zinc-950 border-t border-zinc-200 dark:border-zinc-900 px-4 py-3 text-center text-xs text-zinc-450 dark:text-zinc-500 select-none mt-auto" id="main-footer">
        <p>
          © 2026 Türkçe Programlama Dili • <strong>ÖzDil</strong> Projesi. Python 3.10 AST derleyicisi ile yerel olarak çalışmaktadır.
        </p>
      </footer>
    </div>
  );
}
