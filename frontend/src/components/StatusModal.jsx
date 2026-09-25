import React, { useEffect } from 'react';
import { createPortal } from 'react-dom';
import { CheckCircle2, AlertCircle, Info, X } from 'lucide-react';

export const StatusModal = ({
  isOpen,
  type = 'success',
  title = 'Confirmation',
  message,
  onClose,
  autoCloseMs = 4000
}) => {
  useEffect(() => {
    if (!isOpen || !autoCloseMs) return;
    const timer = setTimeout(() => {
      onClose();
    }, autoCloseMs);
    return () => clearTimeout(timer);
  }, [isOpen, autoCloseMs, onClose]);

  useEffect(() => {
    if (!isOpen) return;
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const isSuccess = type === 'success';
  const isError = type === 'error';

  return createPortal(
    <div
      className="fixed inset-0 z-[10000] flex items-center justify-center p-4 bg-transparent animate-fade-in"
      onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}
      role="dialog"
      aria-modal="true"
      aria-labelledby="status-modal-title"
    >
      <div
        className="relative w-full max-w-sm bg-white rounded-2xl shadow-2xl border border-slate-200 overflow-hidden animate-scale-in text-slate-800"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="p-5 flex items-start gap-3.5">
          <div
            className={`w-10 h-10 rounded-xl flex items-center justify-center shrink-0 ${
              isSuccess
                ? 'bg-emerald-50 text-emerald-600 border border-emerald-100'
                : isError
                ? 'bg-rose-50 text-rose-600 border border-rose-100'
                : 'bg-blue-50 text-blue-600 border border-blue-100'
            }`}
          >
            {isSuccess && <CheckCircle2 className="w-5 h-5" aria-hidden="true" />}
            {isError && <AlertCircle className="w-5 h-5" aria-hidden="true" />}
            {!isSuccess && !isError && <Info className="w-5 h-5" aria-hidden="true" />}
          </div>

          <div className="flex-1 min-w-0 pt-0.5">
            <h3 id="status-modal-title" className="text-sm font-bold text-slate-900 tracking-tight">
              {title}
            </h3>
            <p className="text-xs text-slate-600 mt-1 leading-relaxed break-words">
              {message}
            </p>
          </div>

          <button
            type="button"
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100 cursor-pointer transition-colors shrink-0"
            aria-label="Dismiss notification"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="px-5 pb-4 pt-1 flex justify-end">
          <button
            type="button"
            onClick={onClose}
            className={`px-4 py-2 text-xs font-semibold rounded-xl text-white transition-colors cursor-pointer shadow-xs ${
              isSuccess
                ? 'bg-emerald-600 hover:bg-emerald-700'
                : isError
                ? 'bg-rose-600 hover:bg-rose-700'
                : 'bg-blue-600 hover:bg-blue-700'
            }`}
          >
            Acknowledge
          </button>
        </div>
      </div>
    </div>,
    document.body
  );
};

export default StatusModal;
