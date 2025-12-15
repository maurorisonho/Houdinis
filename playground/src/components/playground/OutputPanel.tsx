/**
 * Houdinis Playground - Output Panel Component
 * Desenvolvido: Lógica e Codificação por Humano e AI Assistida (Claude Sonnet 4.5)
 */
'use client';

import React, { useEffect, useRef } from 'react';
import { useExecutionStore } from '@/stores/executionStore';
import { Terminal, CheckCircle, XCircle, Clock } from 'lucide-react';
import { ScrollArea } from '@/components/ui/scroll-area';
import { cn } from '@/lib/utils';

export function OutputPanel() {
  const { output, error, executionTime, isExecuting } = useExecutionStore();
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new output arrives
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [output, error]);

  const hasOutput = output.length > 0 || error;

  return (
    <div className="flex h-full flex-col">
      {/* Header */}
      <div className="flex items-center gap-2 border-b bg-muted/50 px-4 py-2">
        <Terminal className="h-4 w-4" />
        <span className="text-sm font-medium">Output</span>

        {isExecuting && (
          <div className="ml-auto flex items-center gap-2 text-sm text-muted-foreground">
            <div className="h-2 w-2 animate-pulse rounded-full bg-green-500" />
            Running...
          </div>
        )}

        {!isExecuting && executionTime !== null && (
          <div className="ml-auto flex items-center gap-2 text-sm text-muted-foreground">
            <Clock className="h-3 w-3" />
            {executionTime.toFixed(2)}s
          </div>
        )}
      </div>

      {/* Output Content */}
      <ScrollArea className="flex-1" ref={scrollRef}>
        <div className="p-4">
          {!hasOutput && !isExecuting && (
            <div className="flex h-full items-center justify-center text-center">
              <div className="text-muted-foreground">
                <Terminal className="mx-auto mb-2 h-12 w-12 opacity-50" />
                <p className="text-sm">Run your code to see output here</p>
                <p className="mt-1 text-xs">Press Ctrl+Enter or click the Run button</p>
              </div>
            </div>
          )}

          {isExecuting && !hasOutput && (
            <div className="flex items-center gap-2 text-sm">
              <div className="h-2 w-2 animate-pulse rounded-full bg-blue-500" />
              <span className="text-muted-foreground">Initializing Python kernel...</span>
            </div>
          )}

          {/* Standard Output */}
          {output.map((line, index) => (
            <OutputLine key={index} type="stdout" content={line} />
          ))}

          {/* Error Output */}
          {error && (
            <div className="mt-4 rounded-lg border border-red-500/50 bg-red-500/10 p-4">
              <div className="mb-2 flex items-center gap-2 text-red-500">
                <XCircle className="h-4 w-4" />
                <span className="font-semibold">Error</span>
              </div>
              <pre className="overflow-x-auto text-sm text-red-400">{error}</pre>
            </div>
          )}

          {/* Success Message */}
          {!isExecuting && hasOutput && !error && (
            <div className="mt-4 flex items-center gap-2 text-sm text-green-500">
              <CheckCircle className="h-4 w-4" />
              <span>Execution completed successfully</span>
            </div>
          )}
        </div>
      </ScrollArea>
    </div>
  );
}

interface OutputLineProps {
  type: 'stdout' | 'stderr';
  content: string;
}

function OutputLine({ type, content }: OutputLineProps) {
  return (
    <div
      className={cn(
        'font-mono text-sm',
        type === 'stdout' ? 'text-foreground' : 'text-red-400'
      )}
    >
      {content}
    </div>
  );
}
