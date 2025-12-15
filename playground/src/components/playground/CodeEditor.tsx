'use client';

import React, { useState, useCallback, useEffect } from 'react';
import Editor from '@monaco-editor/react';
import { useCodeExecution } from '@/hooks/useCodeExecution';
import { useEditorStore } from '@/stores/editorStore';
import { Play, Square, Save, Share2, Download } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface CodeEditorProps {
  initialCode?: string;
  onCodeChange?: (code: string) => void;
  height?: string;
}

export function CodeEditor({ initialCode = '', onCodeChange, height = '100%' }: CodeEditorProps) {
  const { code, setCode, isModified } = useEditorStore();
  const { execute, isExecuting, stop } = useCodeExecution();
  const [editorInstance, setEditorInstance] = useState<any>(null);

  // Initialize code
  useEffect(() => {
    if (initialCode && !code) {
      setCode(initialCode);
    }
  }, [initialCode, code, setCode]);

  const handleEditorChange = useCallback(
    (value: string | undefined) => {
      const newCode = value || '';
      setCode(newCode);
      onCodeChange?.(newCode);
    },
    [setCode, onCodeChange]
  );

  const handleRunCode = useCallback(() => {
    if (code && !isExecuting) {
      execute(code);
    }
  }, [code, execute, isExecuting]);

  const handleStopExecution = useCallback(() => {
    stop();
  }, [stop]);

  const handleSave = useCallback(() => {
    // Save to IndexedDB
    const saved = {
      code,
      timestamp: Date.now(),
    };
    localStorage.setItem('playground-code', JSON.stringify(saved));
  }, [code]);

  const handleShare = useCallback(() => {
    // Generate shareable URL with code in URL params (compressed)
    const compressed = btoa(encodeURIComponent(code));
    const shareUrl = `${window.location.origin}/playground?code=${compressed}`;
    navigator.clipboard.writeText(shareUrl);
  }, [code]);

  const handleDownload = useCallback(() => {
    // Download code as .py file
    const blob = new Blob([code], { type: 'text/python' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `houdinis-${Date.now()}.py`;
    a.click();
    URL.revokeObjectURL(url);
  }, [code]);

  return (
    <div className="flex h-full flex-col">
      {/* Toolbar */}
      <div className="flex items-center gap-2 border-b bg-muted/50 px-4 py-2">
        <Button
          size="sm"
          onClick={isExecuting ? handleStopExecution : handleRunCode}
          disabled={!code}
          variant={isExecuting ? 'destructive' : 'default'}
        >
          {isExecuting ? (
            <>
              <Square className="mr-2 h-4 w-4" />
              Stop
            </>
          ) : (
            <>
              <Play className="mr-2 h-4 w-4" />
              Run (Ctrl+Enter)
            </>
          )}
        </Button>

        <div className="flex-1" />

        <Button size="sm" variant="ghost" onClick={handleSave} disabled={!isModified}>
          <Save className="mr-2 h-4 w-4" />
          Save
        </Button>

        <Button size="sm" variant="ghost" onClick={handleShare}>
          <Share2 className="mr-2 h-4 w-4" />
          Share
        </Button>

        <Button size="sm" variant="ghost" onClick={handleDownload}>
          <Download className="mr-2 h-4 w-4" />
          Download
        </Button>
      </div>

      {/* Monaco Editor */}
      <div className="flex-1">
        <Editor
          height={height}
          defaultLanguage="python"
          theme="vs-dark"
          value={code}
          onChange={handleEditorChange}
          onMount={(editor) => setEditorInstance(editor)}
          options={{
            minimap: { enabled: true },
            fontSize: 14,
            lineNumbers: 'on',
            renderLineHighlight: 'all',
            scrollBeyondLastLine: false,
            automaticLayout: true,
            tabSize: 4,
            formatOnPaste: true,
            formatOnType: true,
            suggest: {
              snippetsPreventQuickSuggestions: false,
            },
            quickSuggestions: {
              other: true,
              comments: false,
              strings: true,
            },
          }}
          loading={
            <div className="flex h-full items-center justify-center">
              <div className="animate-pulse text-muted-foreground">Loading editor...</div>
            </div>
          }
        />
      </div>
    </div>
  );
}
