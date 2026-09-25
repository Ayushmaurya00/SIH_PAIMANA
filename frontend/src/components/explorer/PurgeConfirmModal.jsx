import React, { useState, useEffect } from 'react';
import { AlertTriangle, RefreshCw, X, ShieldAlert, CheckCircle2 } from 'lucide-react';

const SYMBOLS = ['@', '#', '$', '%', '&', '*', '!'];
const NUMBERS = ['2', '3', '4', '5', '6', '7', '8', '9'];
const UPPERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'K', 'M', 'N', 'P', 'R', 'T', 'W', 'X', 'Y', 'Z'];
const LOWERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'k', 'm', 'n', 'p', 'r', 't', 'w', 'x', 'y', 'z'];

export const generateSixCharCode = () => {
  const selected = new Set();
  const pick = (arr) => {
    const valid = arr.filter((ch) => !selected.has(ch));
    const ch = valid[Math.floor(Math.random() * valid.length)];
    selected.add(ch);
    return ch;
  };
  pick(SYMBOLS); pick(NUMBERS); pick(UPPERS); pick(LOWERS);
  const pool = [...SYMBOLS, ...NUMBERS, ...UPPERS, ...LOWERS];
  while (selected.size < 6) pick(pool);

  const arr = Array.from(selected);
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr.join('');
};

export const PurgeConfirmModal = ({ isOpen, onClose, onConfirm, loading = false }) => {
  const [challengeCode, setChallengeCode] = useState('');
  const [userInput, setUserInput] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  const refreshCode = () => {
    setChallengeCode(generateSixCharCode());
    setUserInput('');
    setErrorMsg('');
  };

  useEffect(() => {
    if (isOpen) refreshCode();
  }, [isOpen]);

  if (!isOpen) return null;
  const isMatched = userInput.trim() === challengeCode;

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!isMatched) {
      setErrorMsg('Code does not match. Please enter the exact 6 characters.');
      return;
    }
    onConfirm();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/70 backdrop-blur-xs animate-fade-in" role="dialog" aria-modal="true">
      <div className="relative w-full max-w-md bg-white rounded-2xl shadow-2xl border border-red-200 overflow-hidden animate-scale-in" onClick={(e) => e.stopPropagation()}>
        {/* Header Alert Strip */}
        <div className="bg-gradient-to-r from-red-600 via-rose-600 to-red-700 px-5 py-4 text-white flex items-start justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-white/15 flex items-center justify-center shrink-0 ring-1 ring-white/30">
              <ShieldAlert className="w-5 h-5 text-amber-300" />
            </div>
            <div>
              <h2 className="text-sm font-extrabold tracking-tight">Irreversible Portfolio Purge</h2>
              <p className="text-[11px] text-red-100/90 font-medium">MoSPI Sovereign Database Deletion Protocol</p>
            </div>
          </div>
          <button type="button" onClick={onClose} disabled={loading} className="p-1 rounded-lg text-white/80 hover:text-white hover:bg-white/15 cursor-pointer">
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Modal Form */}
        <form onSubmit={handleSubmit} className="p-5 space-y-4">
          <div className="p-3 rounded-xl bg-red-50 border border-red-200 text-xs text-red-900 flex items-start gap-2.5">
            <AlertTriangle className="w-4 h-4 text-red-600 shrink-0 mt-0.5" />
            <span>This operation will permanently purge all projects, milestones, risk scores, and telemetry. This action <strong>cannot be undone</strong>.</span>
          </div>

          {/* Captcha Display */}
          <div className="space-y-1.5">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-800">Security Verification Code:</span>
              <button type="button" onClick={refreshCode} className="text-[11px] font-semibold text-blue-700 hover:text-blue-900 flex items-center gap-1 cursor-pointer">
                <RefreshCw className="w-3 h-3" /><span>New code</span>
              </button>
            </div>
            <div className="flex items-center justify-between p-3 rounded-xl bg-slate-900 text-white border border-slate-800 shadow-inner">
              <span className="font-mono text-xl sm:text-2xl font-black tracking-widest text-amber-300 select-all px-2">{challengeCode}</span>
              <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700">6 Unique Chars</span>
            </div>
            <p className="text-[10px] text-slate-500">Includes symbol, number, uppercase, and lowercase characters.</p>
          </div>

          {/* User Input */}
          <div className="space-y-1">
            <label htmlFor="purge-input" className="text-xs font-semibold text-slate-700 block">Type the exact 6-character code to unlock:</label>
            <div className="relative">
              <input
                id="purge-input"
                type="text"
                autoComplete="off"
                spellCheck="false"
                maxLength={6}
                value={userInput}
                onChange={(e) => { setUserInput(e.target.value); setErrorMsg(''); }}
                placeholder="Enter 6 characters..."
                className={`w-full px-3.5 py-2.5 text-sm font-mono tracking-widest rounded-xl border transition-all focus:outline-hidden ${
                  isMatched ? 'border-emerald-500 bg-emerald-50/40 text-emerald-950 ring-2 ring-emerald-500/20' : 'border-slate-300 bg-white text-slate-900 focus:border-red-500 focus:ring-2 focus:ring-red-500/20'
                }`}
              />
              {isMatched && (
                <div className="absolute right-3 top-1/2 -translate-y-1/2 flex items-center gap-1 text-emerald-600 text-xs font-bold">
                  <CheckCircle2 className="w-4 h-4" /><span>Verified</span>
                </div>
              )}
            </div>
            {errorMsg && <p className="text-[11px] font-medium text-red-600 mt-1">{errorMsg}</p>}
          </div>

          {/* Buttons */}
          <div className="pt-2 flex items-center justify-end gap-2.5">
            <button type="button" onClick={onClose} disabled={loading} className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 cursor-pointer">
              Cancel
            </button>
            <button
              type="submit"
              disabled={!isMatched || loading}
              className={`px-4 py-2 rounded-xl text-xs font-bold text-white transition-all flex items-center gap-1.5 ${
                isMatched && !loading ? 'bg-red-600 hover:bg-red-700 shadow-sm shadow-red-500/30 cursor-pointer ring-2 ring-red-500/30' : 'bg-slate-300 text-slate-500 cursor-not-allowed opacity-60'
              }`}
            >
              {loading ? (<><RefreshCw className="w-3.5 h-3.5 animate-spin" /><span>Purging...</span></>) : (<span>Permanently Purge All</span>)}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default PurgeConfirmModal;
