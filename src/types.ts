export interface KeywordInfo {
  keyword: string;
  pythonEquivalent: string;
  description: string;
  usage: string;
}

export interface ExampleCode {
  title: string;
  description: string;
  code: string;
}

export interface ErrorDetails {
  type: string;
  friendly_type: string;
  message: string;
  lineno: number;
  col: number;
  line_code: string;
  suggested_fix: string;
}

export interface CompilerResult {
  translated: string;
  ast: any; // Can be a nested AST node dictionary or null
  output: string;
  error: string | null;
  error_details?: ErrorDetails | null;
  awaiting_input?: boolean;
  prompt?: string;
  gui_elements?: any[];
}

export interface ASTNodeProps {
  name: string;
  value: any;
  depth: number;
}
