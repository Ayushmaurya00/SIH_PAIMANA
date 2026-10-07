import React from 'react';
import { FlaskConical } from 'lucide-react';
import Card from '../Card';

const STATUS_STYLE = {
  Completed: { dot: 'bg-emerald-500', text: 'text-emerald-700', bar: '#059669', card: 'bg-emerald-50 border-emerald-200' },
  'In Progress': { dot: 'bg-blue-500', text: 'text-blue-700', bar: '#0EA5E9', card: 'bg-blue-50 border-blue-200' },
  Delayed: { dot: 'bg-red-500', text: 'text-red-700', bar: '#EF4444', card: 'bg-red-50 border-red-200' },
  'Not Started': { dot: 'bg-slate-300', text: 'text-slate-500', bar: '#CBD5E1', card: 'bg-slate-50 border-slate-200' },
};

export const PhaseExecutionGantt = ({ phaseData }) => {
  return (
    <Card
      title="Stage-Gate Execution Timeline & Work Breakdown"
      subtitle="5 Statutory Milestone Phases mapped to ground completion metrics"
      headerAction={
        <span className="inline-flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 rounded-full bg-amber-100 text-amber-700 border border-amber-300 select-none">
          <FlaskConical className="w-3 h-3" />
          DEMO — Synthetic Illustration
        </span>
      }
    >
      <div className="space-y-3 mt-3">
        {phaseData.map((ph) => {
          const style = STATUS_STYLE[ph.status] || STATUS_STYLE['Not Started'];
          return (
            <div key={ph.idx} className={`p-3 rounded-lg border ${style.card} flex flex-col sm:flex-row sm:items-center justify-between gap-3`}>
              <div className="flex items-center gap-3">
                <span className={`w-2.5 h-2.5 rounded-full ${style.dot} shrink-0`} />
                <div>
                  <div className="text-xs font-bold text-slate-900">
                    Phase {ph.idx}: {ph.name}
                  </div>
                  <div className="text-[11px] text-slate-500 font-mono mt-0.5">
                    {ph.period} • {ph.weeks} weeks duration
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-3 self-end sm:self-auto">
                <div className="w-24 bg-slate-200 rounded-full h-2 overflow-hidden">
                  <div className="h-full rounded-full transition-all duration-500" style={{ width: `${ph.pct}%`, backgroundColor: style.bar }} />
                </div>
                <span className="text-xs font-bold font-mono text-slate-700 w-10 text-right">{ph.pct}%</span>
                <span className={`text-[10px] font-bold px-2 py-0.5 rounded-md border bg-white ${style.text}`}>
                  {ph.status}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </Card>
  );
};

export default PhaseExecutionGantt;
