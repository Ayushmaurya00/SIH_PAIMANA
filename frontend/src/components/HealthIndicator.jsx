import React from 'react';

export const HealthIndicator = ({ highCount = 0, mediumCount = 0, lowCount = 0, totalProjects = 0 }) => {
  const total = totalProjects || (highCount + mediumCount + lowCount) || 1;
  const highPct = Math.round((highCount / total) * 100);
  const medPct = Math.round((mediumCount / total) * 100);
  // Absorb rounding remainder into the green segment so bar always sums to 100%
  const lowPct = Math.max(0, 100 - highPct - medPct);

  return (
    <div className="card p-5 bg-surface-elevated border border-border-rest">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 pb-3 border-b border-border-rest">
        <div>
          <h2 className="text-base font-bold text-text-primary tracking-tight">
            Portfolio Health Status
          </h2>
        </div>

        {highCount > 0 && (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-semibold bg-surface-elevated border border-status-critical/30 text-status-critical">
            <span className="w-2 h-2 rounded-full bg-status-critical shrink-0" aria-hidden="true" />
            {highCount} Projects Need Urgent Review
          </span>
        )}
      </div>

      {/* Tri-color Status Progress Bar */}
      <div className="mt-4">
        <div className="w-full h-2.5 bg-surface-subtle rounded-full overflow-hidden flex gap-0.5 p-0.5 border border-border-rest">
          <div
            style={{ width: `${highPct}%` }}
            className="bg-status-critical rounded-l-full transition-all duration-300"
            title={`Critical Delay: ${highCount} (${highPct}%)`}
          />
          <div
            style={{ width: `${medPct}%` }}
            className="bg-status-warning transition-all duration-300"
            title={`Watchlist: ${mediumCount} (${medPct}%)`}
          />
          <div
            style={{ width: `${lowPct}%` }}
            className="bg-status-healthy rounded-r-full transition-all duration-300"
            title={`On-Track: ${lowCount} (${lowPct}%)`}
          />
        </div>

        {/* Legend Indicators */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mt-4">
          <div className="flex items-center justify-between p-3 rounded-lg bg-surface-elevated border border-border-rest">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-status-critical shrink-0" aria-hidden="true" />
              <span className="text-xs font-medium text-text-secondary">Critical Delay</span>
            </div>
            <div className="flex items-baseline gap-1.5">
              <span className="text-sm font-bold text-text-primary font-mono">{highCount}</span>
              <span className="text-[11px] text-slate-700 font-medium">({highPct}%)</span>
            </div>
          </div>

          <div className="flex items-center justify-between p-3 rounded-lg bg-surface-elevated border border-border-rest">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-status-warning shrink-0" aria-hidden="true" />
              <span className="text-xs font-medium text-text-secondary">Watchlist / Escalation</span>
            </div>
            <div className="flex items-baseline gap-1.5">
              <span className="text-sm font-bold text-text-primary font-mono">{mediumCount}</span>
              <span className="text-[11px] text-slate-700 font-medium">({medPct}%)</span>
            </div>
          </div>

          <div className="flex items-center justify-between p-3 rounded-lg bg-surface-elevated border border-border-rest">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-status-healthy shrink-0" aria-hidden="true" />
              <span className="text-xs font-medium text-text-secondary">On-Track</span>
            </div>
            <div className="flex items-baseline gap-1.5">
              <span className="text-sm font-bold text-text-primary font-mono">{lowCount}</span>
              <span className="text-[11px] text-slate-700 font-medium">({lowPct}%)</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HealthIndicator;
