import React, { useState } from "react";
import { ChevronDown, ChevronRight, Folder, File, Code, HelpCircle } from "lucide-react";

interface ASTNodeProps {
  nodeName: string;
  nodeValue: any;
  depth: number;
  key?: any;
}

function ASTNode({ nodeName, nodeValue, depth }: ASTNodeProps) {
  const [isOpen, setIsOpen] = useState(depth < 2); // Auto-expand top levels

  if (nodeValue === null || nodeValue === undefined) {
    return (
      <div className="flex items-center gap-1.5 py-1 text-xs text-zinc-400 font-mono" style={{ paddingLeft: `${depth * 16}px` }}>
        <span className="font-semibold text-zinc-500">{nodeName}:</span>
        <span className="italic">bos</span>
      </div>
    );
  }

  // If nodeValue is a primitive
  if (typeof nodeValue !== "object") {
    let colorClass = "text-zinc-700 dark:text-zinc-300";
    if (typeof nodeValue === "boolean") {
      colorClass = "text-indigo-600 dark:text-indigo-400 font-semibold";
    } else if (!isNaN(Number(nodeValue))) {
      colorClass = "text-amber-600 dark:text-amber-400";
    } else if (typeof nodeValue === "string") {
      colorClass = "text-emerald-600 dark:text-emerald-400";
    }

    return (
      <div className="flex items-center gap-1.5 py-0.5 text-xs font-mono" style={{ paddingLeft: `${depth * 16}px` }}>
        <span className="text-zinc-500 font-medium">{nodeName}:</span>
        <span className={`px-1.5 py-0.2 bg-zinc-50 dark:bg-zinc-800/40 rounded ${colorClass}`}>
          {String(nodeValue)}
        </span>
      </div>
    );
  }

  // If nodeValue is an array
  if (Array.isArray(nodeValue)) {
    if (nodeValue.length === 0) {
      return (
        <div className="flex items-center gap-1.5 py-0.5 text-xs text-zinc-400 font-mono" style={{ paddingLeft: `${depth * 16}px` }}>
          <span className="text-zinc-500 font-medium">{nodeName}:</span>
          <span className="italic bg-zinc-100 dark:bg-zinc-800/40 px-1 py-0.2 rounded text-[10px]">boş liste []</span>
        </div>
      );
    }

    return (
      <div className="flex flex-col py-0.5" id={`ast-array-${nodeName}`}>
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="flex items-center gap-1 hover:bg-zinc-100 dark:hover:bg-zinc-800/50 py-0.5 text-xs font-mono font-medium text-zinc-700 dark:text-zinc-300 rounded cursor-pointer self-start select-none"
          style={{ marginLeft: `${depth * 16}px` }}
        >
          {isOpen ? <ChevronDown className="w-3.5 h-3.5 text-zinc-400" /> : <ChevronRight className="w-3.5 h-3.5 text-zinc-400" />}
          <span className="text-zinc-500">{nodeName}:</span>
          <span className="text-indigo-500 dark:text-indigo-400 font-bold text-[10px] bg-indigo-50 dark:bg-indigo-950/40 px-1.5 py-0.2 rounded-full">
            {nodeValue.length} elemanlı liste
          </span>
        </button>

        {isOpen && (
          <div className="flex flex-col mt-0.5 border-l border-zinc-100 dark:border-zinc-800/40 ml-[7px] pl-[9px]" style={{ marginLeft: `${depth * 16 + 7}px` }}>
            {nodeValue.map((item, idx) => (
              <ASTNode
                key={idx}
                nodeName={`[${idx}]`}
                nodeValue={item}
                depth={1} // reset base relative to the border indent
              />
            ))}
          </div>
        )}
      </div>
    );
  }

  // If nodeValue is a nested object / AST node
  const isASTNode = typeof nodeValue.type === "string";
  const displayLabel = isASTNode ? nodeValue.type : nodeName;

  return (
    <div className="flex flex-col py-0.5" id={`ast-node-${displayLabel}`}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-1.5 hover:bg-zinc-100 dark:hover:bg-zinc-800/50 py-1 text-xs font-mono rounded cursor-pointer self-start select-none"
        style={{ marginLeft: `${depth * 16}px` }}
      >
        {isOpen ? <ChevronDown className="w-3.5 h-3.5 text-zinc-400" /> : <ChevronRight className="w-3.5 h-3.5 text-zinc-400" />}
        {!isASTNode && <span className="text-zinc-500">{nodeName}: </span>}
        <span className={`px-2 py-0.5 rounded font-bold text-[11px] tracking-wide ${
          isASTNode
            ? "bg-indigo-100 dark:bg-indigo-950/50 text-indigo-700 dark:text-indigo-300 border border-indigo-200/40 dark:border-indigo-900/40"
            : "bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300"
        }`}>
          {isASTNode ? nodeValue.type : "Obje"}
        </span>
        {nodeValue.lineno && (
          <span className="text-[10px] text-zinc-400">
            (Satır: {nodeValue.lineno})
          </span>
        )}
      </button>

      {isOpen && (
        <div className="flex flex-col mt-0.5 border-l border-zinc-100 dark:border-zinc-800/40 pl-3" style={{ marginLeft: `${depth * 16 + 7}px` }}>
          {Object.entries(nodeValue)
            .filter(([key]) => key !== "type" && key !== "lineno")
            .map(([key, val]) => (
              <ASTNode
                key={key}
                nodeName={key}
                nodeValue={val}
                depth={1} // Reset relative indent
              />
            ))}
        </div>
      )}
    </div>
  );
}

interface ASTViewerProps {
  ast: any;
  isLoading: boolean;
}

export default function ASTViewer({ ast, isLoading }: ASTViewerProps) {
  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center py-12 px-4" id="ast-loading">
        <div className="w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-3 font-medium">AST Ağacı Oluşturuluyor...</p>
      </div>
    );
  }

  if (!ast) {
    return (
      <div className="flex flex-col items-center justify-center py-12 px-6 text-center border-2 border-dashed border-zinc-100 dark:border-zinc-800 rounded-xl" id="ast-empty">
        <div className="p-3 bg-zinc-50 dark:bg-zinc-900 rounded-xl text-zinc-400 dark:text-zinc-600 mb-3">
          <Code className="w-6 h-6" />
        </div>
        <h4 className="text-sm font-semibold text-zinc-700 dark:text-zinc-300">AST İzleme Hazır</h4>
        <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1 max-w-xs">
          Kodunuzu çalıştırdığınızda, Python derleme aşamasında oluşturulan Soyut Sözdizimi Ağacı (Abstract Syntax Tree) burada görüntülenecektir.
        </p>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full bg-white dark:bg-zinc-950/20 rounded-xl border border-zinc-100 dark:border-zinc-900/60 p-4 overflow-y-auto" id="ast-viewer-container">
      <div className="flex items-center gap-2 mb-4 pb-2 border-b border-zinc-100 dark:border-zinc-900" id="ast-viewer-header">
        <span className="px-2 py-1 bg-indigo-50 dark:bg-indigo-950/40 text-indigo-600 dark:text-indigo-400 rounded-md font-bold text-xs font-mono uppercase tracking-wider">
          AST Görüntüleyici
        </span>
        <span className="text-xs text-zinc-500 dark:text-zinc-400">
          Python Abstract Syntax Tree
        </span>
      </div>

      <div className="flex-1 overflow-x-auto" id="ast-node-tree-root">
        <ASTNode nodeName="Kök (Root)" nodeValue={ast} depth={0} />
      </div>
    </div>
  );
}
