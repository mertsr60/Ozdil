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

export interface CompilerResult {
  translated: string;
  ast: any; // Can be a nested AST node dictionary or null
  output: string;
  error: string | null;
}

export interface ASTNodeProps {
  name: string;
  value: any;
  depth: number;
}
