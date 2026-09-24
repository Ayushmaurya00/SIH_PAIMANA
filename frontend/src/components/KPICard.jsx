import React from 'react';

export const KPICard = ({
  title,
  value,
  subtitle,
  subValue,
  icon: Icon,
  badgeText
}) => {
  const displaySubtitle = subtitle || subValue;

  return (
    <div className="card p-5 bg-surface-elevated border border-border-rest">
      <div className="flex items-center justify-between gap-3 mb-3">
        <span className="text-xs font-semibold uppercase tracking-wider text-text-secondary">
          {title}
        </span>
        {Icon && (
          <div className="w-8 h-8 rounded-full bg-surface-subtle border border-border-rest flex items-center justify-center text-primary-sovereign shrink-0">
            <Icon className="w-4 h-4" aria-hidden="true" />
          </div>
        )}
      </div>

      <div className="flex items-baseline gap-2 mb-1">
        <span className="text-xl font-extrabold font-mono tracking-tight text-text-primary">
          {value}
        </span>
        {badgeText && (
          <span className="text-[11px] font-medium px-2 py-0.5 rounded bg-surface-subtle text-text-secondary border border-border-rest">
            {badgeText}
          </span>
        )}
      </div>

      {displaySubtitle && (
        <p className="text-[11px] text-slate-700 font-medium truncate mt-1" title={displaySubtitle}>
          {displaySubtitle}
        </p>
      )}
    </div>
  );
};

export default KPICard;
