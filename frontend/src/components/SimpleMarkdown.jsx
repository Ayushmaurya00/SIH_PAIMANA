import React from 'react';
import { Link } from 'react-router-dom';

/**
 * SimpleMarkdown — lightweight inline markdown-to-JSX renderer.
 * Handles: ### h3, ## h2, **bold**, *italic*, `code`, > blockquote,
 * - bullets, numbered lists, and bare project ID links.
 */
const sanitizeText = (t) => {
  // Strip dangerous protocols and HTML tags
  return t.replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/javascript:/gi, '').replace(/data:/gi, '');
};
const renderInline = (text) => {
  const safe = sanitizeText(text);
  // Split on **bold**, *italic*, `code`
  const parts = safe.split(/(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)/g);
  return parts.map((part, i) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={i} className="font-bold text-text-primary">{sanitizeText(part.slice(2, -2))}</strong>;
    }
    if (part.startsWith('*') && part.endsWith('*')) {
      return <em key={i} className="italic">{sanitizeText(part.slice(1, -1))}</em>;
    }
    if (part.startsWith('`') && part.endsWith('`')) {
      return <code key={i} className="font-mono text-[10px] px-1 py-0.5 rounded bg-surface-subtle text-primary-sovereign border border-border-rest">{sanitizeText(part.slice(1, -1))}</code>;
    }
    return <span key={i}>{part}</span>;
  });
};

export const SimpleMarkdown = ({ text }) => {
  if (!text) return null;
  const lines = text.split('\n');
  const elements = [];
  let i = 0;
  let listBuffer = [];
  let listType = null; // 'ul' | 'ol'

  const flushList = () => {
    if (listBuffer.length === 0) return;
    if (listType === 'ol') {
      elements.push(
        <ol key={`ol-${i}`} className="list-decimal list-inside space-y-0.5 my-1.5 pl-1">
          {listBuffer.map((item, j) => (
            <li key={j} className="text-xs text-text-secondary leading-relaxed">{renderInline(item)}</li>
          ))}
        </ol>
      );
    } else {
      elements.push(
        <ul key={`ul-${i}`} className="space-y-0.5 my-1.5 pl-1">
          {listBuffer.map((item, j) => (
            <li key={j} className="flex items-start gap-1.5 text-xs text-text-secondary leading-relaxed">
              <span className="mt-1.5 w-1 h-1 rounded-full bg-text-tertiary shrink-0" />
              <span>{renderInline(item)}</span>
            </li>
          ))}
        </ul>
      );
    }
    listBuffer = [];
    listType = null;
  };

  while (i < lines.length) {
    const line = lines[i];
    const trimmed = line.trim();

    // Blank line
    if (trimmed === '') {
      flushList();
      i++;
      continue;
    }

    // H3
    if (trimmed.startsWith('### ')) {
      flushList();
      elements.push(
        <h3 key={i} className="text-xs font-bold text-slate-900 mt-3 mb-1 border-b border-slate-100 pb-1">
          {renderInline(trimmed.slice(4))}
        </h3>
      );
      i++;
      continue;
    }

    // H2
    if (trimmed.startsWith('## ')) {
      flushList();
      elements.push(
        <h2 key={i} className="text-[13px] font-bold text-slate-900 mt-3 mb-1">
          {renderInline(trimmed.slice(3))}
        </h2>
      );
      i++;
      continue;
    }

    // H1
    if (trimmed.startsWith('# ')) {
      flushList();
      elements.push(
        <h2 key={i} className="text-sm font-extrabold text-slate-900 mt-3 mb-1.5">
          {renderInline(trimmed.slice(2))}
        </h2>
      );
      i++;
      continue;
    }

    // Horizontal rule
    if (trimmed === '---' || trimmed === '***') {
      flushList();
      elements.push(<hr key={i} className="my-2 border-slate-200" />);
      i++;
      continue;
    }

    // Blockquote
    if (trimmed.startsWith('> ')) {
      flushList();
      elements.push(
        <blockquote key={i} className="border-l-2 border-slate-300 pl-3 py-0.5 my-1.5 text-[11px] text-slate-500 italic bg-slate-50 rounded-r">
          {renderInline(trimmed.slice(2))}
        </blockquote>
      );
      i++;
      continue;
    }

    // Unordered list item
    if (/^[-•]\s/.test(trimmed)) {
      if (listType !== 'ul') { flushList(); listType = 'ul'; }
      listBuffer.push(trimmed.replace(/^[-•]\s+/, ''));
      i++;
      continue;
    }

    // Ordered list item
    if (/^\d+\.\s/.test(trimmed)) {
      if (listType !== 'ol') { flushList(); listType = 'ol'; }
      listBuffer.push(trimmed.replace(/^\d+\.\s+/, ''));
      i++;
      continue;
    }

    // Regular paragraph
    flushList();
    elements.push(
      <p key={i} className="text-xs text-slate-700 leading-relaxed my-0.5">
        {renderInline(trimmed)}
      </p>
    );
    i++;
  }
  flushList();

  return <div className="space-y-0.5">{elements}</div>;
};

export default SimpleMarkdown;
