import React from 'react';

export const SegmentedCodeInput = ({
  userInput,
  onChange,
  challengeCode,
  inputRef
}) => {
  return (
    <div className="relative">
      {/* Visual 6-box Segmented Display */}
      <div
        className="grid grid-cols-6 gap-2 cursor-text select-none"
        onClick={() => inputRef.current?.focus()}
      >
        {[0, 1, 2, 3, 4, 5].map((idx) => {
          const char = userInput[idx] || '';
          const target = challengeCode[idx] || '';
          const isFilled = char !== '';
          const isCorrect = isFilled && char === target;
          const isCurrent = idx === userInput.length;

          return (
            <div
              key={idx}
              className={`h-11 rounded-xl flex items-center justify-center font-mono text-base font-bold border transition-all ${
                isCorrect
                  ? 'bg-emerald-50 border-emerald-500 text-emerald-800 ring-2 ring-emerald-500/20'
                  : isFilled
                  ? 'bg-red-50 border-red-400 text-red-700'
                  : isCurrent
                  ? 'border-blue-500 ring-2 ring-blue-500/20 bg-white'
                  : 'border-slate-200 bg-slate-50 text-slate-400'
              }`}
            >
              {char || (isCurrent ? <span className="w-1.5 h-4 bg-blue-500 animate-pulse rounded-full" /> : '')}
            </div>
          );
        })}
      </div>

      {/* Accessible native input element capturing keystrokes */}
      <input
        ref={inputRef}
        id="purge-input"
        type="text"
        autoComplete="off"
        spellCheck="false"
        maxLength={6}
        value={userInput}
        onChange={onChange}
        className="sr-only"
        aria-label="Enter 6-character security verification code"
      />
    </div>
  );
};

export default SegmentedCodeInput;
