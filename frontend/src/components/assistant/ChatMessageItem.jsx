import React from 'react';
import { Link } from 'react-router-dom';
import { Bot, User, ArrowRight } from 'lucide-react';
import SimpleMarkdown from '../SimpleMarkdown';

export const ChatMessageItem = ({ msg, onClose }) => {
  return (
    <div className={`flex gap-3 animate-fade-in ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
      {msg.role === 'assistant' && (
        <div className="w-7 h-7 rounded-full bg-primary-sovereign text-white flex items-center justify-center shrink-0 mt-0.5">
          <Bot className="w-4 h-4" aria-hidden="true" />
        </div>
      )}
      <div
        className={`max-w-[85%] rounded-xl p-3.5 text-xs leading-relaxed ${
          msg.role === 'user'
            ? 'bg-primary-sovereign text-white font-medium'
            : 'bg-surface-elevated border border-border-rest text-text-primary'
        }`}
      >
        <div>
          {msg.role === 'assistant' ? (
            <SimpleMarkdown text={msg.text} />
          ) : (
            <span className="whitespace-pre-line">{msg.text}</span>
          )}
        </div>

        {msg.role === 'assistant' && (msg.fallback_mode !== undefined || msg.mode) && (
          <div className="mt-2.5 pt-2 border-t border-border-rest flex items-center gap-1.5 text-[10px] text-text-tertiary font-mono">
            <span className={`w-1.5 h-1.5 rounded-full ${msg.fallback_mode ? 'bg-status-warning' : 'bg-status-healthy'}`} aria-hidden="true" />
            <span>{msg.fallback_mode ? 'Deterministic Administrative Grounding' : `AI Engine: ${msg.model_used || 'Gemini 3.6 Flash'}`}</span>
          </div>
        )}

        {msg.sources && msg.sources.length > 0 && (
          <div className="mt-3 pt-2 border-t border-border-rest">
            <p className="text-[10px] font-bold uppercase tracking-wider text-text-tertiary mb-1.5">
              Grounding Project Records:
            </p>
            <div className="flex flex-wrap gap-1.5">
              {msg.sources.map((s, sIdx) => (
                <Link
                  key={sIdx}
                  to={`/projects/${s.project_id}`}
                  onClick={onClose}
                  aria-label={`View grounded project ${s.project_id}`}
                  className="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-surface-subtle hover:bg-primary-sovereign hover:text-white border border-border-rest text-text-secondary text-[11px] font-mono transition-colors font-medium"
                >
                  <span>{s.project_id}</span>
                  <ArrowRight className="w-2.5 h-2.5" aria-hidden="true" />
                </Link>
              ))}
            </div>
          </div>
        )}
      </div>
      {msg.role === 'user' && (
        <div className="w-7 h-7 rounded-full bg-border-rest text-text-secondary flex items-center justify-center shrink-0 mt-0.5">
          <User className="w-4 h-4" aria-hidden="true" />
        </div>
      )}
    </div>
  );
};

export default ChatMessageItem;
