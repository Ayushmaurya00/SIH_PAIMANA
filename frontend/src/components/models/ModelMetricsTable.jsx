import React from 'react';
import { Sliders } from 'lucide-react';

export const ModelMetricsTable = ({ metrics, featureSetFilter, setFeatureSetFilter }) => {
  const displayMetrics = metrics.filter(m => {
    if (featureSetFilter === 'all') return true;
    return m.feature_set === featureSetFilter;
  });

  return (
    <div className="bg-surface-elevated rounded-xl border border-border-rest shadow-xs overflow-hidden">
      <div className="p-4 border-b border-border-rest flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-surface-subtle/50">
        <div>
          <h2 className="text-sm font-bold text-text-primary">Comprehensive Out-of-Time Metric Audit Table</h2>
          <p className="text-xs text-text-tertiary mt-0.5">Statistical benchmarks computed on held-out temporal cohorts</p>
        </div>
        <div className="flex items-center gap-2">
          <Sliders className="w-3.5 h-3.5 text-text-tertiary" />
          <span className="text-xs text-text-secondary">Feature Set:</span>
          <select
            value={featureSetFilter}
            onChange={(e) => setFeatureSetFilter(e.target.value)}
            className="text-xs bg-surface-elevated border border-border-rest rounded-lg px-2.5 py-1 text-text-primary font-medium focus:ring-1 focus:ring-primary-sovereign"
          >
            <option value="all">All Feature Sets (Side-by-Side)</option>
            <option value="cuf_only">CUF-Only (10 Features)</option>
            <option value="cuf_plus_extra">CUF + Extra (25 Features)</option>
          </select>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="border-b border-border-rest bg-surface-subtle font-mono text-[11px] text-text-secondary uppercase">
              <th className="py-2.5 px-4">Feature Set</th>
              <th className="py-2.5 px-4">Model Algorithm</th>
              <th className="py-2.5 px-4">Prediction Target</th>
              <th className="py-2.5 px-4 text-right">Accuracy / R²</th>
              <th className="py-2.5 px-4 text-right">F1-Score / RMSE</th>
              <th className="py-2.5 px-4 text-right">Lead Time (Mos)</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border-rest">
            {displayMetrics.map((m, idx) => (
              <tr key={idx} className="hover:bg-surface-subtle/40 transition-colors">
                <td className="py-2.5 px-4 font-mono font-medium">
                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                    m.feature_set === 'cuf_plus_extra'
                      ? 'bg-status-healthy/10 text-status-healthy border border-status-healthy/30'
                      : 'bg-surface-subtle text-text-secondary border border-border-rest'
                  }`}>
                    {m.feature_set}
                  </span>
                </td>
                <td className="py-2.5 px-4 font-semibold text-text-primary">{m.model_name}</td>
                <td className="py-2.5 px-4 text-text-secondary">{m.target}</td>
                <td className="py-2.5 px-4 text-right font-mono font-bold">
                  {m.accuracy != null ? `${(m.accuracy * 100).toFixed(1)}%` : (m.r2 != null ? `${(m.r2 * 100).toFixed(1)}%` : '-')}
                </td>
                <td className="py-2.5 px-4 text-right font-mono">
                  {m.f1_score != null ? m.f1_score.toFixed(3) : (m.rmse != null ? `±${m.rmse.toFixed(2)}` : '-')}
                </td>
                <td className="py-2.5 px-4 text-right font-mono font-bold text-primary-sovereign">
                  {m.lead_time_months ? `${m.lead_time_months.toFixed(1)} mos` : '-'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ModelMetricsTable;
