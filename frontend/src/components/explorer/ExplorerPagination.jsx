import React from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

export const ExplorerPagination = ({ page, totalPages, total, pageSize, setPage }) => {
  if (totalPages <= 1) return null;

  return (
    <div className="flex items-center justify-between text-xs text-text-secondary pt-2">
      <div>
        Showing <strong className="text-text-primary">{page * pageSize + 1}</strong> to{' '}
        <strong className="text-text-primary">{Math.min((page + 1) * pageSize, total)}</strong> of{' '}
        <strong className="text-text-primary">{total}</strong> projects
      </div>

      <div className="flex items-center gap-1.5">
        <button
          type="button"
          disabled={page === 0}
          onClick={() => setPage(page - 1)}
          className="p-1.5 rounded-lg border border-border-rest bg-surface-elevated hover:bg-surface-subtle disabled:opacity-40 transition-colors"
        >
          <ChevronLeft className="w-4 h-4" />
        </button>

        <span className="px-3 py-1 font-mono text-xs font-semibold">
          Page {page + 1} of {totalPages}
        </span>

        <button
          type="button"
          disabled={page >= totalPages - 1}
          onClick={() => setPage(page + 1)}
          className="p-1.5 rounded-lg border border-border-rest bg-surface-elevated hover:bg-surface-subtle disabled:opacity-40 transition-colors"
        >
          <ChevronRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};

export default ExplorerPagination;
