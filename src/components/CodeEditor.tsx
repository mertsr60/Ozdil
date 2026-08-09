import React, { useState, useEffect, useRef } from "react";
import { Play, RotateCcw, HelpCircle, Code, Eye, FileCode2 } from "lucide-react";
import { KeywordInfo } from "../types";
import { KEYWORDS } from "../constants";

interface CodeEditorProps {
  value: string;
  onChange: (val: string) => void;
  onRun: () => void;
  isRunning: boolean;
  flat?: boolean;
  onCursorChange?: (line: number, col: number) => void;
}

export default function CodeEditor({ value, onChange, onRun, isRunning, flat = false, onCursorChange }: CodeEditorProps) {
  const [cursorPos, setCursorPos] = useState({ line: 1, col: 1 });
  const [selectionStart, setSelectionStart] = useState(0);
  const [suggestions, setSuggestions] = useState<KeywordInfo[]>([]);
  const [selectedSuggestionIndex, setSelectedSuggestionIndex] = useState(0);
  const [ghostText, setGhostText] = useState("");
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [popupPos, setPopupPos] = useState({ top: 0, left: 0 });

  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const highlightRef = useRef<HTMLPreElement>(null);

  // Auto-resize / sync scroll
  const handleScroll = (e: React.UIEvent<HTMLTextAreaElement>) => {
    if (highlightRef.current) {
      highlightRef.current.scrollTop = e.currentTarget.scrollTop;
      highlightRef.current.scrollLeft = e.currentTarget.scrollLeft;
    }
  };

  // Sync cursor position tracking & autocomplete logic
  const handleCursorMove = () => {
    const textarea = textareaRef.current;
    if (!textarea) return;

    const start = textarea.selectionStart;
    setSelectionStart(start);

    // Track line/col for info bar
    const textBeforeCursor = value.slice(0, start);
    const lines = textBeforeCursor.split("\n");
    const currentLine = lines[lines.length - 1];
    const newPos = {
      line: lines.length,
      col: currentLine.length + 1
    };
    
    setCursorPos(newPos);
    if (onCursorChange) {
      onCursorChange(newPos.line, newPos.col);
    }

    // Extract word being typed
    const wordMatch = currentLine.match(/[a-zA-Z0-9_ğüşöçİĞÜŞÖÇ]+$/);
    const word = wordMatch ? wordMatch[0] : "";

    if (word && word.length >= 1) {
      // Find matching keywords
      const lowerWord = word.toLowerCase();
      const filtered = KEYWORDS.filter((kw) =>
        kw.keyword.toLowerCase().startsWith(lowerWord) &&
        kw.keyword.toLowerCase() !== lowerWord
      );

      setSuggestions(filtered);
      setSelectedSuggestionIndex(0);

      if (filtered.length > 0) {
        setShowSuggestions(true);
        // Calculate ghost text for the top suggestion
        const topMatch = filtered[0].keyword;
        setGhostText(topMatch.slice(word.length));

        // Position popup based on line and character width
        // Monospace font character is approx 8.2px wide, line height is 24px (1.5rem)
        const lineIdx = lines.length - 1;
        const colIdx = currentLine.length - word.length;
        
        // Ensure within bounds
        const computedTop = (lineIdx * 24) + 48; // line height * idx + padding
        const computedLeft = (colIdx * 8.2) + 24;

        setPopupPos({
          top: computedTop - textarea.scrollTop,
          left: Math.max(16, computedLeft - textarea.scrollLeft)
        });
      } else {
        setShowSuggestions(false);
        setGhostText("");
      }
    } else {
      setShowSuggestions(false);
      setSuggestions([]);
      setGhostText("");
    }
  };

  const insertText = (insert: string, replaceWordLength = 0) => {
    const textarea = textareaRef.current;
    if (!textarea) return;

    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;

    // Replace the word currently being typed with the full keyword
    const newValue =
      value.slice(0, start - replaceWordLength) +
      insert +
      value.slice(end);

    onChange(newValue);

    // Reposition cursor
    const newCursorPos = start - replaceWordLength + insert.length;
    setTimeout(() => {
      textarea.focus();
      textarea.setSelectionRange(newCursorPos, newCursorPos);
      handleCursorMove();
    }, 0);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    const textarea = textareaRef.current;
    if (!textarea) return;

    // Run code shortcut: Ctrl + Enter or Cmd + Enter
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
      e.preventDefault();
      onRun();
      return;
    }

    // Handle suggestions popup keys
    if (showSuggestions && suggestions.length > 0) {
      if (e.key === "ArrowDown") {
        e.preventDefault();
        setSelectedSuggestionIndex((prev) => (prev + 1) % suggestions.length);
        const nextWord = suggestions[(selectedSuggestionIndex + 1) % suggestions.length].keyword;
        // Update ghost text to match selection
        const wordBeingTyped = value.slice(0, selectionStart).split(/[^a-zA-Z0-9_ğüşöçİĞÜŞÖÇ]/).pop() || "";
        setGhostText(nextWord.slice(wordBeingTyped.length));
        return;
      }

      if (e.key === "ArrowUp") {
        e.preventDefault();
        setSelectedSuggestionIndex((prev) => (prev - 1 + suggestions.length) % suggestions.length);
        const prevWord = suggestions[(selectedSuggestionIndex - 1 + suggestions.length) % suggestions.length].keyword;
        // Update ghost text to match selection
        const wordBeingTyped = value.slice(0, selectionStart).split(/[^a-zA-Z0-9_ğüşöçİĞÜŞÖÇ]/).pop() || "";
        setGhostText(prevWord.slice(wordBeingTyped.length));
        return;
      }

      if (e.key === "Tab" || e.key === "Enter") {
        e.preventDefault();
        const wordBeingTyped = value.slice(0, selectionStart).split(/[^a-zA-Z0-9_ğüşöçİĞÜŞÖÇ]/).pop() || "";
        insertText(suggestions[selectedSuggestionIndex].keyword, wordBeingTyped.length);
        setShowSuggestions(false);
        setGhostText("");
        return;
      }

      if (e.key === "Escape") {
        e.preventDefault();
        setShowSuggestions(false);
        setGhostText("");
        return;
      }
    }

    // If suggestions are NOT showing but Tab is pressed, insert 4 spaces instead of tab-focus out
    if (e.key === "Tab") {
      e.preventDefault();
      // If there's a single ghost text option available even if suggestions are closed, or let's just insert spaces
      insertText("    ");
      return;
    }

    // Auto brackets/quotes closing
    const bracketPairs: { [key: string]: string } = {
      "(": ")",
      "[": "]",
      "{": "}",
      '"': '"',
      "'": "'"
    };

    if (bracketPairs[e.key] !== undefined) {
      e.preventDefault();
      const closingChar = bracketPairs[e.key];
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;

      const newValue = value.slice(0, start) + e.key + closingChar + value.slice(end);
      onChange(newValue);

      setTimeout(() => {
        textarea.setSelectionRange(start + 1, start + 1);
        handleCursorMove();
      }, 0);
    }
  };

  const highlight = (codeText: string) => {
    // Escape HTML entities to prevent rendering bugs
    let html = codeText
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");

    // Highlight strings in green
    html = html.replace(/("(?:\\.|[^"\\])*")/g, '<span class="text-emerald-600 dark:text-emerald-400">$1</span>');
    html = html.replace(/('(?:\\.|[^'\\])*')/g, '<span class="text-emerald-600 dark:text-emerald-400">$1</span>');

    // Highlight comments in gray/italics
    html = html.replace(/(#[^\n]*)/g, '<span class="text-zinc-400 dark:text-zinc-500 italic">$1</span>');

    // Highlight control keywords (blue)
    const controlKeywords = ['eger', 'degilse_eger', 'degilse', 'dongu', 'her', 'iken', 'dene', 'hata_yakala', 'sinif'];
    controlKeywords.forEach(kw => {
      const regex = new RegExp(`\\b${kw}\\b`, 'g');
      html = html.replace(regex, `<span class="text-indigo-600 dark:text-indigo-400 font-semibold">${kw}</span>`);
    });

    // Highlight builtins/standard variables (amber)
    const builtinKeywords = ['yazdir', 'fonksiyon', 'islem', 'dondur', 'dogru', 'yanlis', 've', 'veya', 'degil', 'icinde', 'aralik', 'uzunluk', 'ekle', 'tam_sayi', 'metin', 'ondalik', 'liste', 'sozluk', 'olarak', 'getir', 'dur', 'devam_et', 'yok', 'bos'];
    builtinKeywords.forEach(kw => {
      const regex = new RegExp(`\\b${kw}\\b`, 'g');
      html = html.replace(regex, `<span class="text-amber-600 dark:text-amber-400 font-medium">${kw}</span>`);
    });

    return html;
  };

  const getHighlightedContent = () => {
    if (!ghostText) {
      return highlight(value);
    }

    const leftPart = value.slice(0, selectionStart);
    const rightPart = value.slice(selectionStart);

    return (
      highlight(leftPart) +
      `<span class="text-zinc-400 dark:text-zinc-500/60 font-medium select-none pointer-events-none italic animate-pulse bg-zinc-100 dark:bg-zinc-800/50 px-0.5 rounded">${ghostText}</span>` +
      highlight(rightPart)
    );
  };

  const lineCount = value.split("\n").length;

  return (
    <div className={`flex flex-col h-full overflow-hidden ${
      flat 
        ? "bg-white dark:bg-zinc-950 w-full" 
        : "bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800 shadow-sm"
    }`} id="editor-container">
      
      {/* Editor Toolbar (hidden in flat/VS Code mode) */}
      {!flat && (
        <div className="flex items-center justify-between px-4 py-3 bg-zinc-50 dark:bg-zinc-900/50 border-b border-zinc-200 dark:border-zinc-800" id="editor-toolbar">
          <div className="flex items-center gap-2">
            <div className="flex gap-1.5">
              <span className="w-3 h-3 rounded-full bg-red-400"></span>
              <span className="w-3 h-3 rounded-full bg-amber-400"></span>
              <span className="w-3 h-3 rounded-full bg-green-400"></span>
            </div>
            <span className="text-xs font-semibold tracking-wider text-zinc-500 dark:text-zinc-400 ml-2 flex items-center gap-1.5 uppercase font-mono">
              <FileCode2 className="w-3.5 h-3.5" /> kod_alani.oz
            </span>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => onChange("")}
              className="p-1.5 text-zinc-500 hover:text-red-600 hover:bg-zinc-100 dark:hover:bg-zinc-800 rounded-md transition"
              title="Temizle"
              id="clear-btn"
            >
              <RotateCcw className="w-4 h-4" />
            </button>
            
            <button
              onClick={onRun}
              disabled={isRunning}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-semibold transition shadow-sm ${
                isRunning
                  ? "bg-zinc-100 text-zinc-400 dark:bg-zinc-800 cursor-not-allowed"
                  : "bg-indigo-600 hover:bg-indigo-500 text-white dark:bg-indigo-50 dark:hover:bg-indigo-400"
              }`}
              id="run-btn"
            >
              <Play className={`w-4 h-4 ${isRunning ? "animate-spin" : "fill-current"}`} />
              {isRunning ? "Çalışıyor..." : "Çalıştır"}
            </button>
          </div>
        </div>
      )}

      {/* Code Editor Workspace */}
      <div className="flex-1 flex relative overflow-hidden font-mono text-sm leading-relaxed" id="editor-workspace">
        {/* Line Numbers */}
        <div className={`w-12 py-4 select-none text-right pr-3 text-zinc-400 border-r font-mono text-xs leading-relaxed ${
          flat
            ? "bg-zinc-50/50 dark:bg-zinc-900/20 border-zinc-100 dark:border-zinc-800/30"
            : "bg-zinc-50 dark:bg-zinc-900/40 border-zinc-100 dark:border-zinc-800/40"
        }`} id="line-numbers">
          {Array.from({ length: lineCount }).map((_, i) => (
            <div key={i} className="h-6">
              {i + 1}
            </div>
          ))}
        </div>

        {/* Overlapping Editor Component */}
        <div className="flex-1 relative overflow-auto h-full" id="overlapping-editor">
          {/* Syntax Highlighted Underlay */}
          <pre
            ref={highlightRef}
            className="absolute inset-0 p-4 font-mono text-sm leading-relaxed text-zinc-800 dark:text-zinc-200 pointer-events-none overflow-hidden whitespace-pre break-normal"
            style={{ margin: 0 }}
            dangerouslySetInnerHTML={{ __html: getHighlightedContent() }}
            id="syntax-highlighted-underlay"
          />

          {/* Interactive Textarea Overlay */}
          <textarea
            ref={textareaRef}
            value={value}
            onChange={(e) => {
              onChange(e.target.value);
              // Trigger autocomplete updates right away
              setTimeout(handleCursorMove, 0);
            }}
            onScroll={handleScroll}
            onKeyDown={handleKeyDown}
            onKeyUp={handleCursorMove}
            onClick={handleCursorMove}
            onFocus={handleCursorMove}
            onBlur={() => {
              // Gracefully close autocomplete on blur, but delay so clicks inside popup can register
              setTimeout(() => {
                setShowSuggestions(false);
                setGhostText("");
              }, 150);
            }}
            className="absolute inset-0 w-full h-full p-4 font-mono text-sm leading-relaxed bg-transparent text-transparent caret-zinc-900 dark:caret-zinc-100 border-none outline-none resize-none overflow-auto whitespace-pre break-normal"
            style={{ margin: 0 }}
            placeholder="# Buraya Türkçe kod yazın...&#10;# Örn: yazdir('Merhaba Dünya!')"
            id="textarea-editor"
            spellCheck={false}
          />

          {/* Autocomplete Suggestions Popup */}
          {showSuggestions && suggestions.length > 0 && (
            <div
              className="absolute z-20 bg-white dark:bg-zinc-950 border border-zinc-200 dark:border-zinc-800 rounded-lg shadow-xl max-w-xs overflow-hidden"
              style={{
                top: `${popupPos.top}px`,
                left: `${popupPos.left}px`
              }}
              id="autocomplete-popup"
            >
              <div className="px-2 py-1.5 bg-zinc-100 dark:bg-zinc-900 border-b border-zinc-200 dark:border-zinc-800 text-[10px] uppercase font-bold text-zinc-400 flex justify-between items-center select-none">
                <span>Otomatik Tamamlama</span>
                <span>[Tab / Enter]</span>
              </div>
              <div className="max-h-48 overflow-y-auto">
                {suggestions.map((item, idx) => (
                  <button
                    key={item.keyword}
                    onClick={() => insertText(item.keyword, value.slice(0, selectionStart).split(/[^a-zA-Z0-9_ğüşöçİĞÜŞÖÇ]/).pop()?.length || 0)}
                    className={`w-full text-left px-3 py-2 text-xs flex flex-col transition border-b border-zinc-100 dark:border-zinc-900/40 last:border-b-0 ${
                      idx === selectedSuggestionIndex
                        ? "bg-indigo-50 dark:bg-indigo-950/40 text-indigo-900 dark:text-indigo-200"
                        : "text-zinc-700 dark:text-zinc-300 hover:bg-zinc-50 dark:hover:bg-zinc-900"
                    }`}
                  >
                    <div className="flex justify-between items-center w-full">
                      <span className="font-bold">{item.keyword}</span>
                      <span className="text-[10px] text-zinc-400 font-mono italic">
                        python: {item.pythonEquivalent}
                      </span>
                    </div>
                    <span className="text-[10px] text-zinc-500 dark:text-zinc-400 mt-0.5 line-clamp-1">
                      {item.description}
                    </span>
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Editor Info Bar / Metadata footer (hidden in flat/VS Code mode) */}
      {!flat && (
        <div className="flex items-center justify-between px-4 py-1.5 bg-zinc-50 dark:bg-zinc-900/30 border-t border-zinc-100 dark:border-zinc-800 text-xs text-zinc-500 dark:text-zinc-400" id="editor-infobar">
          <div className="flex items-center gap-4">
            <span>Satır: <strong>{cursorPos.line}</strong>, Sütun: <strong>{cursorPos.col}</strong></span>
            {ghostText && (
              <span className="hidden md:inline text-indigo-500 animate-pulse text-[11px] font-medium bg-indigo-50 dark:bg-indigo-950/30 px-2 py-0.5 rounded">
                Tab / Sağ Yön Tuşu ile Tamamla ({ghostText})
              </span>
            )}
          </div>
          <div className="text-[10px] tracking-wider uppercase font-semibold text-zinc-400">
            ÖzDil v1.0 • Python Çalışma Ortamı
          </div>
        </div>
      )}
    </div>
  );
}
