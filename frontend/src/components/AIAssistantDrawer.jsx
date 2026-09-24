import React, { useState, useRef, useEffect } from 'react';
import { X, Send, Bot, Landmark } from 'lucide-react';
import { queryAIAssistant } from '../api/client';
import { ChatMessageItem } from './assistant/ChatMessageItem';
import { StarterPromptsList } from './assistant/StarterPromptsList';

export const AIAssistantDrawer = ({ isOpen, onClose, contextProjectId = null }) => {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      text: 'Namaste! I am the **PAIMANA Decision Support Assistant**.\n\nI provide grounded analytical insights directly derived from MoSPI Central Sector project monitoring data, expenditure S-curves, and operational delay models.\n\nHow may I assist your portfolio review or project briefing today?',
      sources: []
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    if (isOpen) {
      chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isOpen]);

  const handleSend = async (questionText = null) => {
    const textToSend = questionText || input.trim();
    if (!textToSend || loading) return;

    const newMessages = [...messages, { role: 'user', text: textToSend }];
    setMessages(newMessages);
    setInput('');
    setLoading(true);

    try {
      const res = await queryAIAssistant(textToSend, contextProjectId);
      setMessages([
        ...newMessages,
        {
          role: 'assistant', text: res.answer, sources: res.sources || [],
          confidence: res.confidence, fallback_mode: res.fallback_mode,
          mode: res.mode, model_used: res.model_used
        }
      ]);
    } catch {
      setMessages([
        ...newMessages,
        { role: 'assistant', text: '⚠️ Unable to complete request. Ensure backend service is accessible.', sources: [] }
      ]);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-hidden bg-slate-950/20 backdrop-blur-xs flex justify-end transition-opacity animate-in fade-in duration-200">
      <div className="w-full max-w-lg bg-white border-l border-slate-200 flex flex-col h-full shadow-lg animate-in slide-in-from-right duration-200" onClick={(e) => e.stopPropagation()}>
        {/* Drawer Header */}
        <div className="p-4 border-b border-slate-200 flex items-center justify-between bg-white">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-primary-sovereign flex items-center justify-center text-white shrink-0">
              <Landmark className="w-4 h-4 text-white" aria-hidden="true" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-text-primary flex items-center gap-2">
                PAIMANA Decision Assistant
                <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-surface-subtle text-text-secondary border border-border-rest font-semibold">
                  MoSPI RAG
                </span>
              </h3>
              <p className="text-[11px] text-text-tertiary font-normal">Decision-Support Intelligence for Review Authorities</p>
            </div>
          </div>
          <button
            onClick={onClose}
            aria-label="Close Assistant Drawer"
            className="p-1.5 rounded-lg bg-surface-elevated hover:bg-surface-subtle text-slate-600 hover:text-text-primary border border-border-rest transition-colors cursor-pointer"
          >
            <X className="w-4 h-4 text-slate-600 hover:text-text-primary" aria-hidden="true" />
          </button>
        </div>

        {/* Message Stream */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-surface-subtle">
          {messages.map((msg, idx) => (
            <ChatMessageItem key={idx} msg={msg} onClose={onClose} />
          ))}

          {loading && (
            <div className="flex gap-3 justify-start animate-fade-in">
              <div className="w-7 h-7 rounded-full bg-[#0F2B5B] text-white flex items-center justify-center shrink-0">
                <Bot className="w-4 h-4 animate-spin" aria-hidden="true" />
              </div>
              <div className="bg-white border border-slate-200 rounded-xl p-3 text-xs text-slate-600 flex items-center gap-2.5">
                <div className="flex gap-1 items-center">
                  <span className="w-1.5 h-1.5 rounded-full bg-[#0F2B5B] animate-bounce [animation-delay:-0.3s]" aria-hidden="true" />
                  <span className="w-1.5 h-1.5 rounded-full bg-[#0F2B5B] animate-bounce [animation-delay:-0.15s]" aria-hidden="true" />
                  <span className="w-1.5 h-1.5 rounded-full bg-[#0F2B5B] animate-bounce" aria-hidden="true" />
                </div>
                <span className="text-[11px] font-medium">Querying MoSPI project database and calculating risk trajectory...</span>
              </div>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>

        <StarterPromptsList onSelectPrompt={handleSend} />

        {/* Input Bar */}
        <div className="p-3 border-t border-slate-200 bg-white">
          <form onSubmit={(e) => { e.preventDefault(); handleSend(); }} className="flex items-center gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Inquire on statutory delays, ministry outlays, milestone slip..."
              aria-label="Inquire on statutory delays, ministry outlays, milestone slip"
              className="input-gov flex-1 text-xs"
            />
            <button
              type="submit"
              disabled={!input.trim() || loading}
              aria-label="Send message to Assistant"
              className="p-2 bg-primary-sovereign text-white rounded-lg hover:bg-primary-sovereign/90 disabled:opacity-50 transition-colors shadow-xs"
            >
              <Send className="w-4 h-4" aria-hidden="true" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default AIAssistantDrawer;
