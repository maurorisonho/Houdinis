'use client';

import React from 'react';
import { CodeEditor } from '@/components/playground/CodeEditor';
import { OutputPanel } from '@/components/playground/OutputPanel';
import { CircuitViewer } from '@/components/playground/CircuitViewer';
import { TemplateSelector } from '@/components/playground/TemplateSelector';
import { ResizablePanelGroup, ResizablePanel, ResizableHandle } from '@/components/ui/resizable';

export default function PlaygroundPage() {
  return (
    <div className="flex h-screen flex-col">
      {/* Header */}
      <header className="flex items-center justify-between border-b px-6 py-3">
        <div className="flex items-center gap-4">
          <h1 className="text-xl font-bold">Houdinis Playground</h1>
          <TemplateSelector />
        </div>

        <div className="flex items-center gap-4">
          <a
            href="https://docs.houdinis.dev"
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-muted-foreground hover:text-foreground"
          >
            Documentation
          </a>
          <a
            href="https://github.com/maurorisonho/Houdinis"
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-muted-foreground hover:text-foreground"
          >
            GitHub
          </a>
        </div>
      </header>

      {/* Main Content - 3 Panel Layout */}
      <main className="flex-1 overflow-hidden">
        <ResizablePanelGroup direction="horizontal">
          {/* Code Editor Panel */}
          <ResizablePanel defaultSize={40} minSize={30}>
            <CodeEditor />
          </ResizablePanel>

          <ResizableHandle />

          {/* Output Panel */}
          <ResizablePanel defaultSize={30} minSize={25}>
            <OutputPanel />
          </ResizablePanel>

          <ResizableHandle />

          {/* Circuit Visualization Panel */}
          <ResizablePanel defaultSize={30} minSize={25}>
            <CircuitViewer />
          </ResizablePanel>
        </ResizablePanelGroup>
      </main>

      {/* Footer */}
      <footer className="border-t px-6 py-2 text-center text-xs text-muted-foreground">
        Powered by JupyterLite + Pyodide | Houdinis Framework v1.0.0 | MIT License
      </footer>
    </div>
  );
}
