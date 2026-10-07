import React from 'react';
import { Calendar, AlertCircle, CheckCircle, Clock } from 'lucide-react';

export const MilestoneGantt = ({ milestones = [] }) => {
  if (!milestones || milestones.length === 0) {
    return (
      <div className="p-4 rounded-lg bg-surface-subtle text-xs text-text-tertiary border border-border-rest">
        No operational milestones logged for this central sector project.
      </div>
    );
  }

  // Calculate timeline bounds
  const dates = [];
  milestones.forEach((m) => {
    if (m.planned_date) dates.push(new Date(m.planned_date).getTime());
    if (m.achieved_date) dates.push(new Date(m.achieved_date).getTime());
  });

  const minTime = dates.length ? Math.min(...dates) : Date.now();
  const maxTime = dates.length ? Math.max(...dates) : Date.now() + 86400000 * 365;
  const timeSpan = Math.max(1, maxTime - minTime);

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between text-xs text-text-tertiary border-b border-border-rest pb-2">
        <div className="flex items-center gap-4">
          <span className="flex items-center gap-1.5 font-medium text-text-secondary">
            <span className="w-2.5 h-2.5 rounded bg-primary border border-primary-sovereign" aria-hidden="true" />
            Planned Timeline
          </span>
          <span className="flex items-center gap-1.5 font-medium text-text-secondary">
            <span className="w-2.5 h-2.5 rounded bg-status-healthy border border-status-healthy" aria-hidden="true" />
            Achieved Milestone
          </span>
          <span className="flex items-center gap-1.5 font-medium text-text-secondary">
            <span className="w-2.5 h-2.5 rounded bg-status-critical border border-status-critical" aria-hidden="true" />
            Slippage / Delay
          </span>
        </div>
        <span className="font-mono text-[11px] font-bold text-status-critical bg-status-critical/10 px-2 py-0.5 rounded border border-status-critical/20">
          {milestones.filter((m) => m.is_delayed).length} Stages Delayed
        </span>
      </div>

      <div className="space-y-2.5">
        {milestones.map((m, idx) => {
          const plannedTime = new Date(m.planned_date).getTime();
          const achievedTime = m.achieved_date ? new Date(m.achieved_date).getTime() : null;

          const plannedOffset = ((plannedTime - minTime) / timeSpan) * 100;
          const isDelayed = m.is_delayed;
          const isDone = !!m.achieved_date;

          return (
            <div key={m.milestone_id || idx} className="p-3 rounded-lg bg-surface-subtle border border-border-rest space-y-2 hover:border-border-focus transition-colors">
              <div className="flex items-center justify-between text-xs">
                <div className="flex items-center gap-2">
                  <span className="font-mono text-[11px] font-bold text-text-tertiary">{idx + 1}.</span>
                  <span className="font-bold text-primary-sovereign">{m.milestone_name}</span>
                </div>
                <div className="flex items-center gap-2">
                  {isDelayed ? (
                    <span className="px-2 py-0.5 rounded-md text-[10px] font-bold bg-status-critical/10 text-status-critical border border-status-critical/20 flex items-center gap-1">
                      <AlertCircle className="w-3 h-3 text-status-critical" aria-hidden="true" />
                      Delayed
                    </span>
                  ) : isDone ? (
                    <span className="px-2 py-0.5 rounded-md text-[10px] font-bold bg-status-healthy/10 text-status-healthy border border-status-healthy/20 flex items-center gap-1">
                      <CheckCircle className="w-3 h-3 text-status-healthy" aria-hidden="true" />
                      Achieved
                    </span>
                  ) : (
                    <span className="px-2 py-0.5 rounded-md text-[10px] font-semibold bg-surface-elevated text-text-secondary border border-border-rest flex items-center gap-1">
                      <Clock className="w-3 h-3 text-text-tertiary" aria-hidden="true" />
                      In Progress
                    </span>
                  )}
                </div>
              </div>

              {/* Gantt Bar Visualization */}
              <div className="relative w-full h-2.5 bg-border-rest rounded-full overflow-hidden">
                {/* Planned Bar */}
                <div
                  className="absolute h-full rounded-full bg-primary/30"
                  style={{
                    left: `${Math.max(0, plannedOffset - 15)}%`,
                    width: '30%',
                  }}
                />

                {/* Actual / Delayed Indicator Marker */}
                {isDelayed ? (
                  <div
                    className="absolute h-full bg-status-critical rounded-full"
                    style={{
                      left: `${Math.max(0, plannedOffset - 5)}%`,
                      width: '40%',
                    }}
                  />
                ) : isDone ? (
                  <div
                    className="absolute h-full bg-status-healthy rounded-full"
                    style={{
                      left: `${Math.max(0, plannedOffset - 15)}%`,
                      width: '30%',
                    }}
                  />
                ) : null}
              </div>

              <div className="flex items-center justify-between text-[11px] font-mono text-text-tertiary">
                <span>Planned Target: <strong className="text-primary-sovereign">{m.planned_date}</strong></span>
                <span>
                  {m.achieved_date ? (
                    <>Actual Date: <strong className={isDelayed ? "text-status-critical font-bold" : "text-status-healthy font-bold"}>{m.achieved_date}</strong></>
                  ) : (
                    <span className="text-text-tertiary">Awaiting Completion</span>
                  )}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default MilestoneGantt;
