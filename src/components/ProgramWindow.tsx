import React, { useState } from "react";
import {
  X,
  Minus,
  Square,
  Layout,
  Terminal,
  Play,
  Save,
  FileText,
  Settings,
  Plus,
  RefreshCw,
  Table as TableIcon,
  CheckSquare,
  Sliders,
  Code as CodeIcon,
  AlertCircle,
  CheckCircle2,
  Info,
  Layers,
  ChevronRight,
  FolderOpen,
  Sparkles
} from "lucide-react";

interface ProgramWindowProps {
  windowData: {
    title: string;
    width?: number;
    height?: number;
    theme?: string;
    icon?: string;
    elements: any[];
  };
  onAction?: (actionName: string, payload?: any) => void;
}

export const ProgramWindow: React.FC<ProgramWindowProps> = ({ windowData, onAction }) => {
  const [activeTab, setActiveTab] = useState(0);
  const [formValues, setFormValues] = useState<Record<string, any>>({});
  const [activeNotification, setActiveNotification] = useState<{
    title: string;
    message: string;
    type: string;
  } | null>(null);

  const isDark = windowData.theme !== "aydinlik" && windowData.theme !== "light";
  const elements = windowData.elements || [];

  const handleInputChange = (key: string, val: any) => {
    setFormValues((prev) => ({ ...prev, [key]: val }));
  };

  const handleButtonClick = (action: string, label: string) => {
    if (onAction) {
      onAction(action, { formValues, label });
    }
    setActiveNotification({
      title: "İşlem Tetiklendi",
      message: `"${label}" butonu çalıştırıldı. (Eylem: ${action})`,
      type: "basari"
    });
  };

  // Find menubar and toolbar if any
  const menuBarElem = elements.find((e) => e.type === "menu_cubugu");
  const toolBarElem = elements.find((e) => e.type === "arac_cubugu");
  const statusBarElem = elements.find((e) => e.type === "durum_cubugu");
  const tabGroupElem = elements.find((e) => e.type === "sekme_grubu");

  // Filter main body elements
  const bodyElements = elements.filter(
    (e) => e.type !== "menu_cubugu" && e.type !== "arac_cubugu" && e.type !== "durum_cubugu" && e.type !== "sekme_grubu"
  );

  return (
    <div
      className={`w-full max-w-full rounded-2xl border shadow-2xl overflow-hidden flex flex-col transition-all duration-300 font-sans ${
        isDark
          ? "bg-[#16181D] border-zinc-800 text-zinc-100 shadow-black/60"
          : "bg-white border-zinc-250 text-zinc-900 shadow-zinc-400/30"
      }`}
      style={{ minHeight: "440px" }}
    >
      {/* WINDOW TITLEBAR */}
      <div
        className={`h-10 px-3.5 flex items-center justify-between border-b select-none shrink-0 ${
          isDark
            ? "bg-[#111216] border-zinc-800/90 text-zinc-300"
            : "bg-zinc-100 border-zinc-200 text-zinc-700"
        }`}
      >
        {/* Window controls (macOS style dots) */}
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-rose-500 hover:bg-rose-600 transition cursor-pointer flex items-center justify-center group shadow-xs">
            <X className="w-2 h-2 text-rose-950 opacity-0 group-hover:opacity-100 transition" />
          </div>
          <div className="w-3 h-3 rounded-full bg-amber-500 hover:bg-amber-600 transition cursor-pointer flex items-center justify-center group shadow-xs">
            <Minus className="w-2 h-2 text-amber-950 opacity-0 group-hover:opacity-100 transition" />
          </div>
          <div className="w-3 h-3 rounded-full bg-emerald-500 hover:bg-emerald-600 transition cursor-pointer flex items-center justify-center group shadow-xs">
            <Square className="w-1.5 h-1.5 text-emerald-950 opacity-0 group-hover:opacity-100 transition" />
          </div>
        </div>

        {/* Window Title & Badge */}
        <div className="flex items-center gap-2 text-xs font-semibold tracking-wide">
          <Layout className="w-3.5 h-3.5 text-indigo-400" />
          <span className="truncate max-w-[220px]">{windowData.title || "Varyn Uygulama Penceresi"}</span>
          <span
            className={`text-[9px] px-1.5 py-0.5 rounded font-mono font-bold uppercase tracking-wider ${
              isDark ? "bg-indigo-950/80 text-indigo-300 border border-indigo-800/50" : "bg-indigo-50 text-indigo-700 border border-indigo-200"
            }`}
          >
            ÖzDil Program
          </span>
        </div>

        {/* Window info right */}
        <div className="text-[10px] font-mono text-zinc-400 flex items-center gap-1.5">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>Çalışıyor</span>
        </div>
      </div>

      {/* MENUBAR (If defined) */}
      {menuBarElem && (
        <div
          className={`h-7 px-3 flex items-center gap-4 text-xs font-medium border-b select-none shrink-0 ${
            isDark ? "bg-[#181A20] border-zinc-800 text-zinc-400" : "bg-zinc-50 border-zinc-200 text-zinc-600"
          }`}
        >
          {menuBarElem.items?.map((m: string, i: number) => (
            <button
              key={i}
              className="hover:text-indigo-400 hover:bg-zinc-800/40 dark:hover:bg-zinc-800 px-1.5 py-0.5 rounded transition cursor-pointer"
              onClick={() =>
                setActiveNotification({
                  title: "Menü Seçildi",
                  message: `"${m}" menüsü açıldı.`,
                  type: "bilgi"
                })
              }
            >
              {m}
            </button>
          ))}
        </div>
      )}

      {/* TOOLBAR (If defined) */}
      {toolBarElem && (
        <div
          className={`h-9 px-3 flex items-center gap-1.5 border-b overflow-x-auto select-none shrink-0 scrollbar-none ${
            isDark ? "bg-[#14151A] border-zinc-800" : "bg-zinc-100/70 border-zinc-200"
          }`}
        >
          {toolBarElem.items?.map((item: string, i: number) => (
            <button
              key={i}
              onClick={() => handleButtonClick(`toolbar_${item}`, item)}
              className={`px-2.5 py-1 text-[11px] font-medium rounded-lg flex items-center gap-1.5 transition active:scale-95 cursor-pointer border ${
                isDark
                  ? "bg-zinc-800/80 hover:bg-zinc-700 text-zinc-200 border-zinc-700/60"
                  : "bg-white hover:bg-zinc-50 text-zinc-800 border-zinc-250 shadow-2xs"
              }`}
            >
              <Sparkles className="w-3 h-3 text-indigo-400" />
              <span>{item}</span>
            </button>
          ))}
        </div>
      )}

      {/* TAB BAR (If defined) */}
      {tabGroupElem && (
        <div
          className={`px-3 pt-2 flex items-center gap-1 border-b overflow-x-auto select-none shrink-0 ${
            isDark ? "bg-[#14151A] border-zinc-800" : "bg-zinc-50 border-zinc-200"
          }`}
        >
          {tabGroupElem.items?.map((tab: string, idx: number) => {
            const isTabActive = activeTab === idx;
            return (
              <button
                key={idx}
                onClick={() => setActiveTab(idx)}
                className={`px-3.5 py-1.5 text-xs font-semibold rounded-t-lg transition border-t border-x cursor-pointer ${
                  isTabActive
                    ? isDark
                      ? "bg-[#16181D] text-indigo-400 border-zinc-700 border-b-transparent"
                      : "bg-white text-indigo-600 border-zinc-250 border-b-transparent shadow-xs"
                    : isDark
                    ? "bg-transparent text-zinc-400 border-transparent hover:text-zinc-200"
                    : "bg-transparent text-zinc-500 border-transparent hover:text-zinc-800"
                }`}
              >
                {tab}
              </button>
            );
          })}
        </div>
      )}

      {/* MODAL / TOAST NOTIFICATION */}
      {activeNotification && (
        <div className="mx-4 mt-3 p-3 rounded-xl bg-indigo-600/90 backdrop-blur-md text-white text-xs flex items-center justify-between shadow-lg border border-indigo-400/30 animate-in fade-in duration-200">
          <div className="flex items-center gap-2">
            <Info className="w-4 h-4 text-indigo-200 shrink-0" />
            <div>
              <span className="font-bold">{activeNotification.title}: </span>
              <span>{activeNotification.message}</span>
            </div>
          </div>
          <button
            onClick={() => setActiveNotification(null)}
            className="text-white hover:text-indigo-200 font-bold p-1 cursor-pointer"
          >
            ✕
          </button>
        </div>
      )}

      {/* WINDOW MAIN BODY / CANVAS */}
      <div className="flex-1 p-4 overflow-y-auto space-y-4">
        {bodyElements.length === 0 ? (
          <div className="h-48 flex flex-col items-center justify-center text-zinc-400 text-center gap-2">
            <Layout className="w-8 h-8 opacity-40" />
            <p className="text-xs">Pencere hazır. 'program' komutları ile bileşen ekleyin.</p>
          </div>
        ) : (
          bodyElements.map((elem: any, idx: number) => {
            switch (elem.type) {
              case "program_baslik":
                return (
                  <div key={idx} className="border-b border-zinc-700/40 pb-2 mb-2">
                    <h2
                      className={`font-black tracking-tight ${
                        elem.level === 2 ? "text-base" : "text-lg text-indigo-400"
                      }`}
                    >
                      {elem.title}
                    </h2>
                    {elem.subtitle && (
                      <p className="text-xs text-zinc-400 mt-0.5">{elem.subtitle}</p>
                    )}
                  </div>
                );

              case "program_yazi": {
                let styleClass = "text-xs leading-relaxed ";
                if (elem.style === "vurgulu") styleClass += "font-bold text-indigo-300";
                else if (elem.style === "basarili") styleClass += "text-emerald-400 font-semibold";
                else if (elem.style === "uyari") styleClass += "text-amber-400 font-semibold";
                else if (elem.style === "hata") styleClass += "text-rose-400 font-semibold";
                else if (elem.style === "bilgi") styleClass += "text-sky-400";
                else if (elem.style === "kod") styleClass += "font-mono bg-zinc-800/80 px-1.5 py-0.5 rounded text-amber-300";
                else styleClass += isDark ? "text-zinc-300" : "text-zinc-700";

                return (
                  <p
                    key={idx}
                    className={styleClass}
                    style={{ textAlign: elem.align === "orta" || elem.align === "center" ? "center" : "left" }}
                  >
                    {elem.text}
                  </p>
                );
              }

              case "metin_kutusu":
                return (
                  <div key={idx} className="flex flex-col gap-1.5">
                    <label className="text-xs font-semibold text-zinc-400">{elem.label}</label>
                    <input
                      type="text"
                      value={formValues[elem.label] !== undefined ? formValues[elem.label] : elem.value}
                      onChange={(e) => handleInputChange(elem.label, e.target.value)}
                      placeholder={elem.placeholder}
                      className={`w-full px-3 py-2 rounded-xl text-xs outline-none transition border ${
                        isDark
                          ? "bg-[#1D2027] border-zinc-700/80 text-zinc-100 focus:border-indigo-500"
                          : "bg-zinc-50 border-zinc-300 text-zinc-900 focus:border-indigo-500"
                      }`}
                    />
                  </div>
                );

              case "sayi_kutusu":
                return (
                  <div key={idx} className="flex flex-col gap-1.5">
                    <div className="flex justify-between items-center text-xs font-semibold text-zinc-400">
                      <span>{elem.label}</span>
                      <span className="font-mono text-indigo-400">
                        {formValues[elem.label] !== undefined ? formValues[elem.label] : elem.value}
                      </span>
                    </div>
                    <input
                      type="number"
                      min={elem.min}
                      max={elem.max}
                      value={formValues[elem.label] !== undefined ? formValues[elem.label] : elem.value}
                      onChange={(e) => handleInputChange(elem.label, parseFloat(e.target.value) || 0)}
                      className={`w-full px-3 py-2 rounded-xl text-xs outline-none transition border font-mono ${
                        isDark
                          ? "bg-[#1D2027] border-zinc-700/80 text-zinc-100 focus:border-indigo-500"
                          : "bg-zinc-50 border-zinc-300 text-zinc-900 focus:border-indigo-500"
                      }`}
                    />
                  </div>
                );

              case "program_buton": {
                let btnStyle = "bg-indigo-600 hover:bg-indigo-500 text-white shadow-indigo-900/30";
                if (elem.style === "basari") btnStyle = "bg-emerald-600 hover:bg-emerald-500 text-white shadow-emerald-900/30";
                else if (elem.style === "tehlike") btnStyle = "bg-rose-600 hover:bg-rose-500 text-white shadow-rose-900/30";
                else if (elem.style === "uyari") btnStyle = "bg-amber-600 hover:bg-amber-500 text-white shadow-amber-900/30";
                else if (elem.style === "ikincil") btnStyle = isDark ? "bg-zinc-800 hover:bg-zinc-700 text-zinc-200 border border-zinc-700" : "bg-zinc-200 hover:bg-zinc-300 text-zinc-800";

                return (
                  <button
                    key={idx}
                    onClick={() => handleButtonClick(elem.action, elem.label)}
                    className={`w-full py-2.5 px-4 rounded-xl text-xs font-bold transition-all active:scale-[0.98] cursor-pointer shadow-md flex items-center justify-center gap-2 ${btnStyle}`}
                  >
                    <Play className="w-3.5 h-3.5 fill-current" />
                    <span>{elem.label}</span>
                  </button>
                );
              }

              case "onay_kutusu": {
                const checked = formValues[elem.label] !== undefined ? formValues[elem.label] : elem.checked;
                return (
                  <div
                    key={idx}
                    onClick={() => handleInputChange(elem.label, !checked)}
                    className={`flex items-center justify-between p-3 rounded-xl border transition cursor-pointer ${
                      isDark ? "bg-[#1B1D23] border-zinc-800 hover:border-zinc-700" : "bg-zinc-50 border-zinc-250 hover:border-zinc-300"
                    }`}
                  >
                    <span className="text-xs font-semibold">{elem.label}</span>
                    <div
                      className={`w-5 h-5 rounded-md flex items-center justify-center transition ${
                        checked ? "bg-indigo-600 text-white" : isDark ? "border border-zinc-600 bg-zinc-800" : "border border-zinc-400 bg-white"
                      }`}
                    >
                      {checked && <CheckCircle2 className="w-3.5 h-3.5" />}
                    </div>
                  </div>
                );
              }

              case "secim_kutusu":
                return (
                  <div key={idx} className="flex flex-col gap-1.5">
                    <label className="text-xs font-semibold text-zinc-400">{elem.label}</label>
                    <select
                      value={formValues[elem.label] !== undefined ? formValues[elem.label] : elem.selected}
                      onChange={(e) => handleInputChange(elem.label, e.target.value)}
                      className={`w-full px-3 py-2 rounded-xl text-xs outline-none transition border cursor-pointer ${
                        isDark
                          ? "bg-[#1D2027] border-zinc-700/80 text-zinc-100"
                          : "bg-zinc-50 border-zinc-300 text-zinc-900"
                      }`}
                    >
                      {elem.options?.map((opt: string, optIdx: number) => (
                        <option key={optIdx} value={opt}>
                          {opt}
                        </option>
                      ))}
                    </select>
                  </div>
                );

              case "program_kaydirici": {
                const sliderVal = formValues[elem.label] !== undefined ? formValues[elem.label] : elem.value;
                return (
                  <div key={idx} className="flex flex-col gap-1.5 p-3 rounded-xl border bg-[#1B1D23] border-zinc-800">
                    <div className="flex justify-between items-center text-xs">
                      <span className="font-semibold text-zinc-300">{elem.label}</span>
                      <span className="font-mono font-bold text-indigo-400">{sliderVal}</span>
                    </div>
                    <input
                      type="range"
                      min={elem.min}
                      max={elem.max}
                      value={sliderVal}
                      onChange={(e) => handleInputChange(elem.label, parseFloat(e.target.value))}
                      className="w-full accent-indigo-500 cursor-pointer"
                    />
                  </div>
                );
              }

              case "program_kart":
                return (
                  <div
                    key={idx}
                    className={`p-3.5 rounded-2xl border flex items-start justify-between gap-3 shadow-xs ${
                      isDark ? "bg-[#1B1D24] border-zinc-800/80" : "bg-zinc-50 border-zinc-200"
                    }`}
                  >
                    <div className="flex flex-col gap-1">
                      <span className="text-xs font-bold text-indigo-400">{elem.title}</span>
                      <span className="text-sm font-extrabold">{elem.content}</span>
                    </div>
                    {elem.badge && (
                      <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-indigo-950/80 text-indigo-300 border border-indigo-800">
                        {elem.badge}
                      </span>
                    )}
                  </div>
                );

              case "program_tablo":
                return (
                  <div
                    key={idx}
                    className={`rounded-xl border overflow-hidden shadow-xs text-xs ${
                      isDark ? "border-zinc-800 bg-[#171920]" : "border-zinc-200 bg-white"
                    }`}
                  >
                    <div className="overflow-x-auto">
                      <table className="w-full text-left border-collapse">
                        <thead>
                          <tr className={`border-b font-bold ${isDark ? "bg-[#121318] border-zinc-800 text-zinc-300" : "bg-zinc-100 border-zinc-200 text-zinc-700"}`}>
                            {elem.headers?.map((h: string, hIdx: number) => (
                              <th key={hIdx} className="py-2.5 px-3 uppercase tracking-wider text-[10px]">
                                {h}
                              </th>
                            ))}
                          </tr>
                        </thead>
                        <tbody className={`divide-y ${isDark ? "divide-zinc-800/60" : "divide-zinc-150"}`}>
                          {elem.rows?.map((row: string[], rIdx: number) => (
                            <tr
                              key={rIdx}
                              className={`transition ${
                                isDark ? "hover:bg-zinc-800/40" : "hover:bg-zinc-50"
                              }`}
                            >
                              {row.map((cell: string, cIdx: number) => (
                                <td key={cIdx} className="py-2 px-3 font-mono text-[11px]">
                                  {cell}
                                </td>
                              ))}
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                );

              case "kod_kutusu":
                return (
                  <div key={idx} className="rounded-xl border border-zinc-800 bg-[#101116] p-3 font-mono text-xs overflow-x-auto shadow-inner text-amber-200">
                    <pre className="whitespace-pre-wrap">{elem.code}</pre>
                  </div>
                );

              case "terminal_kutusu":
                return (
                  <div key={idx} className="rounded-xl border border-zinc-800 bg-black/90 p-3 font-mono text-[11px] text-emerald-400 space-y-1 shadow-inner">
                    <div className="flex items-center gap-1.5 text-zinc-500 pb-1.5 border-b border-zinc-800 text-[10px]">
                      <Terminal className="w-3 h-3" />
                      <span>Konsol & Log Çıktısı</span>
                    </div>
                    {elem.logs?.map((log: string, lIdx: number) => (
                      <div key={lIdx} className="leading-relaxed">
                        {log}
                      </div>
                    ))}
                  </div>
                );

              case "program_ilerleme":
                return (
                  <div key={idx} className="space-y-1.5">
                    <div className="flex justify-between text-xs font-semibold text-zinc-400">
                      <span>{elem.status || "İlerleme"}</span>
                      <span className="font-mono text-indigo-400">%{elem.percent}</span>
                    </div>
                    <div className="w-full bg-zinc-800 rounded-full h-2 overflow-hidden shadow-inner">
                      <div
                        className="bg-indigo-500 h-full rounded-full transition-all duration-500 shadow-sm"
                        style={{ width: `${elem.percent}%` }}
                      ></div>
                    </div>
                  </div>
                );

              case "program_bildirim":
                return (
                  <div
                    key={idx}
                    className={`p-3 rounded-xl border flex items-start gap-2.5 text-xs ${
                      elem.alert_type === "hata"
                        ? "bg-rose-950/30 border-rose-800 text-rose-300"
                        : elem.alert_type === "uyari"
                        ? "bg-amber-950/30 border-amber-800 text-amber-300"
                        : elem.alert_type === "basari"
                        ? "bg-emerald-950/30 border-emerald-800 text-emerald-300"
                        : "bg-sky-950/30 border-sky-800 text-sky-300"
                    }`}
                  >
                    <Info className="w-4 h-4 shrink-0 mt-0.5" />
                    <div>
                      <h4 className="font-bold">{elem.title}</h4>
                      <p className="opacity-90 mt-0.5">{elem.message}</p>
                    </div>
                  </div>
                );

              default:
                return null;
            }
          })
        )}
      </div>

      {/* WINDOW STATUSBAR (Pinned at bottom) */}
      <div
        className={`h-7 px-3 flex items-center justify-between border-t text-[10px] font-mono select-none shrink-0 ${
          isDark ? "bg-[#111216] border-zinc-800 text-zinc-400" : "bg-zinc-100 border-zinc-200 text-zinc-600"
        }`}
      >
        <div className="flex items-center gap-1.5">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
          <span>{statusBarElem ? statusBarElem.left : "Hazır"}</span>
        </div>
        <div className="flex items-center gap-3 opacity-80">
          <span>{statusBarElem ? statusBarElem.right : "v1.0.0 | UTF-8"}</span>
        </div>
      </div>
    </div>
  );
};
