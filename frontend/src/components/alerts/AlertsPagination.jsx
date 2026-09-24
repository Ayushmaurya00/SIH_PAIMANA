import React from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

export const AlertsPagination = ({ page, totalCount, chunkSize = 30, setPage }) => {
  const totalPages = Math.ceil(totalCount / chunkSize);
  if (totalPages <= 1) return null;

  const start = page * chunkSize + 1;
  const end = Math.min((page + 1) * chunkSize, totalCount);

  // Generate a sliding window of page numbers
  const pagesToShow = [];
  const maxButtons = 5;
  let startPage = Math.max(0, page - Math.floor(maxButtons / 2));
  let endPage = Math.min(totalPages - 1, startPage + maxButtons - 1);
  if (endPage - startPage + 1 < maxButtons) {
    startPage = Math.max(0, endPage - maxButtons + 1);
  }
  for (let i = startPage; i <= endPage; i++) {
    pagesToShow.push(i);
  }

  return (
    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs text-text-secondary pt-3 border-t border-border-rest select-none">
      <div>
        Showing <strong className="text-text-primary font-semibold">{start}</strong> to{' '}
        <strong className="text-text-primary font-semibold">{end}</strong> of{' '}
        <strong className="text-text-primary font-semibold">{totalCount}</strong> alerts
        <span className="ml-1 text-[11px] text-text-tertiary">({chunkSize} per chunk)</span>
      </div>

      <div className="flex items-center gap-1.5 self-center sm:self-auto">
        <button
          type="button"
          disabled={page === 0}
          onClick={() => { setPage(page - 1); window.scrollTo({ top: 0, behavior: 'smooth' }); }}
          className="p-1.5 rounded-lg border border-border-rest bg-surface-elevated hover:bg-surface-subtle disabled:opacity-40 transition-colors cursor-pointer"
          title="Previous chunk"
          aria-label="Previous chunk"
        >
          <ChevronLeft className="w-4 h-4" />
        </button>

        {pagesToShow.map((p) => (
          <button
            key={p}
            type="button"
            onClick={() => { setPage(p); window.scrollTo({ top: 0, behavior: 'smooth' }); }}
            className={`min-w-[32px] h-8 px-2 rounded-lg font-mono text-xs font-semibold transition-colors cursor-pointer ${
              p === page
                ? 'bg-primary-sovereign text-white shadow-xs'
                : 'border border-border-rest bg-surface-elevated hover:bg-surface-subtle text-text-primary'
            }`}
          >
            {p + 1}
          </button>
        ))}

        <button
          type="button"
          disabled={page >= totalPages - 1}
          onClick={() => { setPage(page + 1); window.scrollTo({ top: 0, behavior: 'smooth' }); }}
          className="p-1.5 rounded-lg border border-border-rest bg-surface-elevated hover:bg-surface-subtle disabled:opacity-40 transition-colors cursor-pointer"
          title="Next chunk"
          aria-label="Next chunk"
        >
          <ChevronRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};

export default AlertsPagination;
