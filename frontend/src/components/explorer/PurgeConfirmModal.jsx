import React, { useState, useEffect, useRef } from 'react';
import { AlertTriangle, RefreshCw, X, ShieldAlert, CheckCircle2, Lock, Trash2 } from 'lucide-react';
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

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/20 backdrop-blur-md animate-fade-in"
      style={{
        backdropFilter: 'blur(8px)',
        WebkitBackdropFilter: 'blur(8px)'
      }}
      onClick={(e) => { if (e.target === e.currentTarget && !loading) onClose(); }}
      role="alertdialog"
      aria-modal="true"
      aria-labelledby="purge-modal-title"
      aria-describedby="purge-modal-desc"
    >
      <div
        className={`relative w-full max-w-md bg-white rounded-2xl shadow-2xl border border-red-200 overflow-hidden animate-scale-in transition-transform ${
          isShaking ? 'animate-shake' : ''
        }`}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header Alert Strip */}
        <div className="bg-gradient-to-r from-red-600 via-rose-600 to-red-700 px-5 py-4 text-white flex items-start justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-white/15 flex items-center justify-center shrink-0 ring-1 ring-white/30">
              <ShieldAlert className="w-5 h-5 text-amber-300" aria-hidden="true" />
            </div>
            <div>
              <h2 id="purge-modal-title" className="text-sm font-extrabold tracking-tight">
                Irreversible Portfolio Purge
              </h2>
              <p className="text-[11px] text-red-100/90 font-medium">MoSPI Sovereign Database Deletion Protocol</p>
            </div>
          </div>
          <button
            type="button"
            onClick={onClose}
            disabled={loading}
            className="p-1 rounded-lg text-white/80 hover:text-white hover:bg-white/15 cursor-pointer transition-colors"
            aria-label="Close dialog"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Modal Form */}
        <form onSubmit={handleSubmit} className="p-5 space-y-4">
          <div id="purge-modal-desc" className="p-3 rounded-xl bg-red-50 border border-red-200 text-xs text-red-900 flex items-start gap-2.5">
            <AlertTriangle className="w-4 h-4 text-red-600 shrink-0 mt-0.5" aria-hidden="true" />
            <span>This operation will permanently purge all projects, milestones, risk scores, and telemetry. This action <strong>cannot be undone</strong>.</span>
          </div>

          {/* Captcha Target Display */}
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
            <div className="flex items-center justify-between p-3 rounded-xl bg-slate-900 text-white border border-slate-800 shadow-inner">
              <span className="font-mono text-xl sm:text-2xl font-black tracking-widest text-amber-300 select-all px-2">
                {challengeCode}
              </span>
              <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700">
                6 Unique Chars
              </span>
            </div>
          </div>

          {/* Segmented Character Input */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <label htmlFor="purge-input" className="text-xs font-semibold text-slate-700">
                Type the exact 6 characters to unlock:
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
                  ? 'bg-red-600 hover:bg-red-700 text-white shadow-lg shadow-red-600/30 ring-2 ring-red-500 ring-offset-1 cursor-pointer animate-pulse-subtle'
                  : 'bg-red-50/80 border border-red-200 text-red-400 cursor-not-allowed opacity-80'
              }`}
            >
              {loading ? (
                <>
                  <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                  <span>Purging Records...</span>
                </>
              ) : isMatched ? (
                <>
                  <Trash2 className="w-3.5 h-3.5" />
                  <span>Permanently Purge All</span>
                </>
              ) : (
                <>
                  <Lock className="w-3.5 h-3.5 text-red-400" />
                  <span>Enter Code to Unlock</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default PurgeConfirmModal;
