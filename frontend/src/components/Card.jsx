import React from 'react';

export const Card = ({
  title,
  subtitle,
  children,
  className = '',
  hover = false,
  padding = 'p-5',
  action,
  ...props
}) => {
  return (
    <div
      className={`card ${padding} ${hover ? 'hover:border-slate-300' : ''} ${className}`}
      {...props}
    >
      {(title || action) && (
        <div className="flex items-start justify-between gap-3 pb-3 mb-4 border-b border-slate-100">
          <div>
            {title && <h2 className="text-base font-bold text-slate-900">{title}</h2>}
            {subtitle && <p className="text-xs text-slate-600 mt-0.5">{subtitle}</p>}
          </div>
          {action && <div className="shrink-0">{action}</div>}
        </div>
      )}
      {children}
    </div>
  );
};

export default Card;
