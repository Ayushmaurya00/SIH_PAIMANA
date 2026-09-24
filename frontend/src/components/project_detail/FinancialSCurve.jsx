import React from 'react';
import { ResponsiveContainer, ComposedChart, Area, Line, XAxis, YAxis, Tooltip, Legend, CartesianGrid } from 'recharts';
import { FlaskConical } from 'lucide-react';
import Card from '../Card';

export const FinancialSCurve = ({ sCurveData }) => {
  return (
    <Card
      title="Physical vs Financial S-Curve Progress Trajectory"
      subtitle="12-Month Telemetry Trajectory (Physical Execution vs Cumulative Outlay Burn)"
      headerAction={
        <span className="inline-flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 rounded-full bg-amber-100 text-amber-700 border border-amber-300 select-none">
          <FlaskConical className="w-3 h-3" aria-hidden="true" />
          DEMO — Synthetic Illustration
        </span>
      }
    >
      <div className="h-72 mt-3" role="region" aria-label="Physical vs Financial S-Curve Progress Trajectory Chart">
        <ResponsiveContainer width="100%" height="100%" debounce={50} minWidth={100} minHeight={200}>
          <ComposedChart data={sCurveData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
            <defs>
              <linearGradient id="physGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#2563eb" stopOpacity={0.25} />
                <stop offset="95%" stopColor="#2563eb" stopOpacity={0.0} />
              </linearGradient>
              <linearGradient id="expGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.2} />
                <stop offset="95%" stopColor="#f59e0b" stopOpacity={0.0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
            <XAxis dataKey="month" tick={{ fontSize: 11, fill: '#334155' }} />
            <YAxis domain={[0, 100]} tick={{ fontSize: 11, fill: '#334155' }} unit="%" />
            <Tooltip
              formatter={(val, name) => [`${val}%`, name]}
              contentStyle={{ backgroundColor: '#ffffff', borderRadius: '8px', border: '1px solid #e2e8f0', fontSize: '12px' }}
            />
            <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
            <Area type="monotone" dataKey="Actual Progress (%)" stroke="#2563eb" strokeWidth={2.5} fillOpacity={1} fill="url(#physGrad)" />
            <Area type="monotone" dataKey="Financial Burn (% of Approved)" stroke="#f59e0b" strokeWidth={2} strokeDasharray="4 4" fillOpacity={1} fill="url(#expGrad)" />
            <Line type="monotone" dataKey="Planned Baseline (%)" stroke="#94a3b8" strokeWidth={1.5} strokeDasharray="2 2" dot={false} />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
};

export default FinancialSCurve;
