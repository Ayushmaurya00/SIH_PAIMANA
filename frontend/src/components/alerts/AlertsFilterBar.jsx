import React from 'react';
import Card from '../Card';

export const AlertsFilterBar = ({ severityFilter, setSeverityFilter, statusFilter, setStatusFilter }) => {
  return (
    <Card padding="p-4" className="bg-surface-elevated border border-border-rest">
      <div className="flex flex-wrap items-center gap-x-6 gap-y-3">
        <div className="flex flex-wrap items-center gap-2 text-xs">
          <span className="text-text-secondary font-semibold text-[11px] uppercase tracking-wider">Severity:</span>
          {['All', 'High', 'Medium'].map((sev) => (
            <button
              key={sev}
              onClick={() => setSeverityFilter(sev)}
              className={`px-3 py-1 rounded-md font-semibold transition-colors ${
                severityFilter === sev
                  ? 'bg-primary-sovereign text-white'
                  : 'bg-surface-subtle text-text-secondary hover:bg-border-rest'
              }`}
            >
              {sev === 'High' ? 'Critical' : sev === 'Medium' ? 'Watchlist' : 'All Severities'}
            </button>
          ))}
        </div>

        <div className="hidden sm:block w-px h-5 bg-border-rest shrink-0" />

        <div className="flex flex-wrap items-center gap-2 text-xs">
          <span className="text-text-secondary font-semibold text-[11px] uppercase tracking-wider">Status:</span>
          {['All', 'New', 'Reviewed'].map((st) => (
            <button
              key={st}
              onClick={() => setStatusFilter(st)}
              className={`px-3 py-1 rounded-md font-semibold transition-colors ${
                statusFilter === st
                  ? 'bg-primary-sovereign text-white'
                  : 'bg-surface-subtle text-text-secondary hover:bg-border-rest'
              }`}
            >
              {st === 'All' ? 'All Statuses' : st === 'New' ? 'Unreviewed (Action Required)' : 'Acknowledged'}
            </button>
          ))}
        </div>
      </div>
    </Card>
  );
};

export default AlertsFilterBar;
