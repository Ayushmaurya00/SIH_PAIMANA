import React from 'react';
import { AlertCircle, AlertTriangle, CheckCircle2 } from 'lucide-react';

export const RiskBadge = ({ score, riskLevel, size = 'md', showScore = true }) => {
  const numScore = score !== undefined && score !== null ? Number(score) : null;
  const safeScore = numScore !== null && Number.isFinite(numScore) ? Math.min(100, Math.max(0, Math.round(numScore))) : null;

  let level = riskLevel;
  if (!level && safeScore !== null) {
    if (safeScore >= 70) level = 'High';
    else if (safeScore >= 40) level = 'Medium';
    else level = 'Low';
  }

  const config = {
    High: {
      label: 'Critical Delay',
      shortLabel: 'Critical',
      icon: AlertCircle,
      dotColor: 'bg-status-critical',
      textColor: 'text-status-critical',
      borderColor: 'border-status-critical/30',
      borderAccent: 'border-l-2 border-l-status-critical',
    },
    Medium: {
      label: 'Watchlist',
      shortLabel: 'Watchlist',
      icon: AlertTriangle,
      dotColor: 'bg-status-warning',
      textColor: 'text-status-warning',
      borderColor: 'border-status-warning/30',
      borderAccent: 'border-l-2 border-l-status-warning',
    },
    Low: {
      label: 'On-Track',
      shortLabel: 'On-Track',
      icon: CheckCircle2,
      dotColor: 'bg-status-healthy',
      textColor: 'text-status-healthy',
      borderColor: 'border-status-healthy/30',
      borderAccent: 'border-l-2 border-l-status-healthy',
    },
  }[level] || {
    label: 'Unassessed',
    shortLabel: 'Unassessed',
    icon: CheckCircle2,
    dotColor: 'bg-text-tertiary',
    textColor: 'text-text-secondary',
    borderColor: 'border-border-rest',
    borderAccent: 'border-l-2 border-l-border-focus',
  };

  const Icon = config.icon;

  // Size SM: Dot + Label only (no background, no border) for tables
  if (size === 'sm') {
    return (
      <span className="inline-flex items-center gap-1.5 text-xs font-medium text-slate-700 whitespace-nowrap">
        <span className={`w-2 h-2 rounded-full ${config.dotColor} shrink-0`} aria-hidden="true" />
        <span>{config.shortLabel}</span>
        {showScore && safeScore !== null && (
          <span className="font-mono text-[11px] text-slate-600 font-semibold">({safeScore})</span>
        )}
      </span>
    );
  }

  // Size LG: Used on Project Detail page
  if (size === 'lg') {
    return (
      <div className={`inline-flex items-center gap-3 p-3 rounded-xl bg-white border ${config.borderColor}`}>
        <div className="p-2 rounded-lg bg-slate-100 text-slate-800">
          <Icon className={`w-5 h-5 ${config.textColor}`} aria-hidden="true" />
        </div>
        <div>
          <p className="text-[11px] font-semibold uppercase tracking-wider text-slate-600">
            Risk Classification
          </p>
          <div className="flex items-center gap-2 mt-0.5">
            <span className={`font-bold text-sm ${config.textColor}`}>{config.label}</span>
            {showScore && safeScore !== null && (
              <span className="text-xs px-2 py-0.5 rounded bg-slate-100 text-slate-800 font-mono font-bold border border-slate-200">
                Index: {safeScore}/100
              </span>
            )}
          </div>
        </div>
      </div>
    );
  }

  // Size MD: Default Pill with white background and subtle border
  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-semibold bg-white border border-slate-200 ${config.borderAccent} ${config.textColor}`}>
      <span className={`w-1.5 h-1.5 rounded-full ${config.dotColor} shrink-0`} aria-hidden="true" />
      <span>{config.label}</span>
      {showScore && safeScore !== null && (
        <span className="font-mono text-[11px] text-slate-600 ml-0.5">
          ({safeScore})
        </span>
      )}
    </span>
  );
};

export default RiskBadge;
