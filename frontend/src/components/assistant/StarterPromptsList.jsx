import React from 'react';

export const STARTER_PROMPTS = [
  "Which infrastructure sector has the highest cost escalation risk?",
  "Show high-risk projects under Ministry of Railways",
  "Explain the delay factors and land acquisition issues for project PRJ-00004",
  "What are the recommended administrative actions for stalled central sector projects?"
];

export const StarterPromptsList = ({ onSelectPrompt }) => {
  return (
    <div className="px-4 py-2.5 bg-slate-50 border-t border-slate-200">
      <p className="text-[10px] font-bold text-slate-600 uppercase tracking-wider mb-1.5">
        Suggested Administrative Inquiries:
      </p>
      <div className="flex flex-col gap-1">
        {STARTER_PROMPTS.map((prompt, pIdx) => (
          <button
            key={pIdx}
            onClick={() => onSelectPrompt(prompt)}
            className="text-[11px] px-2.5 py-1 rounded-md bg-white hover:bg-slate-100 text-slate-600 hover:text-slate-900 border border-slate-200 transition-colors text-left font-medium truncate w-full"
            title={prompt}
          >
            {prompt}
          </button>
        ))}
      </div>
    </div>
  );
};

export default StarterPromptsList;
