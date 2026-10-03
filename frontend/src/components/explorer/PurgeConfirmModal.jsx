import React, { useState, useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';
import { AlertTriangle, RefreshCw, X, CheckCircle2, Lock, Trash2, Database } from 'lucide-react';
import { generateSixCharCode } from '../../utils/securityCode';
import SegmentedCodeInput from './SegmentedCodeInput';

export const PurgeConfirmModal = ({ isOpen, onClose, onConfirm, loading = false }) => {
  const [challengeCode, setChallengeCode] = useState('');
  const [userInput, setUserInput] = useState('');
  const [errorMsg, setErrorMsg] = useState('');
  const [isShaking, setIsShaking] = useState(false);
  const inputRef = useRef(null);

  const refreshCode = () => {
    setChallengeCode(generateSixCharCode());
    setUserInput('');
    setErrorMsg('');
    setTimeout(() => inputRef.current?.focus(), 50);
  };

  useEffect(() => {
    if (isOpen) refreshCode();
  }, [isOpen]);

  useEffect(() => {
    if (!isOpen) return;
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && !loading) onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, loading, onClose]);

  if (!isOpen) return null;
  const isMatched = userInput.trim() === challengeCode;

  const triggerShake = (msg) => {
    setErrorMsg(msg);
    setIsShaking(true);
    setTimeout(() => setIsShaking(false), 400);
    inputRef.current?.focus();
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!isMatched) {
      triggerShake('Verification code does not match. Enter the exact 6 characters.');
      return;
    }
    onConfirm();
  };

  return createPortal(
    <div
      className="fixed inset-0 z-[9999] flex items-center justify-center p-4 bg-transparent animate-fade-in"
      onClick={(e) => { if (e.target === e.currentTarget && !loading) onClose(); }}
      role="alertdialog"
      aria-modal="true"
      aria-labelledby="purge-modal-title"
      aria-describedby="purge-modal-desc"
    >
      <div
        className={`relative w-full max-w-md bg-white rounded-2xl shadow-2xl border border-slate-200 overflow-hidden animate-scale-in transition-transform ${
          isShaking ? 'animate-shake' : ''
        }`}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Simple, Clean Header — No Red Gradient */}
        <div className="bg-white px-5 py-4 border-b border-slate-100 flex items-center justify-between text-slate-900">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-slate-100 flex items-center justify-center shrink-0">
              <Database className="w-4 h-4 text-slate-700" aria-hidden="true" />
            </div>
            <div>
              <h2 id="purge-modal-title" className="text-sm font-bold text-slate-900 tracking-tight">
                Confirm Database Purge
              </h2>
              <p className="text-[11px] text-slate-500 font-medium">Verification required before proceeding</p>
            </div>
          </div>
          <button
            type="button"
            onClick={onClose}
            disabled={loading}
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 cursor-pointer transition-colors"
            aria-label="Close dialog"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Modal Form */}
        <form onSubmit={handleSubmit} className="p-5 space-y-4">
          <div id="purge-modal-desc" className="p-3 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-700 flex items-start gap-2.5">
            <AlertTriangle className="w-4 h-4 text-amber-500 shrink-0 mt-0.5" aria-hidden="true" />
            <span>This will permanently purge all projects, milestones, risk scores, and telemetry. This action cannot be undone.</span>
          </div>

          {/* Simple, Light Captcha Display — No Black Color */}
          <div className="space-y-1.5">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-800">Security Verification Code:</span>
              <button
                type="button"
                onClick={refreshCode}
                className="text-[11px] font-semibold text-blue-700 hover:text-blue-900 flex items-center gap-1 cursor-pointer"
                title="Generate new code"
              >
                <RefreshCw className="w-3 h-3" /><span>New code</span>
              </button>
            </div>
            <div className="flex items-center justify-between p-3 rounded-xl bg-slate-100 text-slate-900 border border-slate-200">
              <span className="font-mono text-xl sm:text-2xl font-bold tracking-widest text-slate-900 select-all px-2">
                {challengeCode}
              </span>
              <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded bg-white text-slate-600 border border-slate-200 font-semibold">
                6 Characters
              </span>
            </div>
          </div>

          {/* Segmented Character Input */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <label htmlFor="purge-input" className="text-xs font-semibold text-slate-700">
                Type the 6 characters to unlock:
              </label>
              {isMatched && (
                <span className="flex items-center gap-1 text-emerald-600 text-xs font-bold">
                  <CheckCircle2 className="w-3.5 h-3.5" />Verified
                </span>
              )}
            </div>

            <SegmentedCodeInput
              userInput={userInput}
              onChange={(e) => { setUserInput(e.target.value); setErrorMsg(''); }}
              challengeCode={challengeCode}
              inputRef={inputRef}
            />

            {errorMsg && <p className="text-[11px] font-semibold text-red-600 animate-fade-in">{errorMsg}</p>}
          </div>

          {/* Action Buttons */}
          <div className="pt-2 flex items-center justify-end gap-2.5">
            <button
              type="button"
              onClick={onClose}
              disabled={loading}
              className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 cursor-pointer transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={!isMatched || loading}
              className={`px-4 py-2.5 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 ${
                isMatched && !loading
                  ? 'bg-rose-600 hover:bg-rose-700 text-white shadow-sm cursor-pointer'
                  : 'bg-slate-100 border border-slate-200 text-slate-400 cursor-not-allowed opacity-80'
              }`}
            >
              {loading ? (
                <>
                  <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                  <span>Purging...</span>
                </>
              ) : isMatched ? (
                <>
                  <Trash2 className="w-3.5 h-3.5" />
                  <span>Purge All Data</span>
                </>
              ) : (
                <>
                  <Lock className="w-3.5 h-3.5 text-slate-400" />
                  <span>Locked</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>,
    document.body
  );
};

export default PurgeConfirmModal;
