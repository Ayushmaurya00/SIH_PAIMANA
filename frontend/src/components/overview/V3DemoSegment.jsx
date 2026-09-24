import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  ResponsiveContainer, BarChart, Bar, LineChart, Line, XAxis, YAxis, Tooltip, Legend, CartesianGrid
} from 'recharts';
import { Sparkles, BarChart3, TrendingUp, ArrowRight, ShieldAlert, CheckCircle2 } from 'lucide-react';
import Card from '../Card';

const DEMO_BAR_DATA = [
  { stage: 'Land Acquisition', baseline: 120, simulatedOverrun: 185, acceleratedMitigation: 135 },
  { stage: 'Forest Clearances', baseline: 80, simulatedOverrun: 140, acceleratedMitigation: 95 },
  { stage: 'Engineering Design', baseline: 210, simulatedOverrun: 230, acceleratedMitigation: 215 },
  { stage: 'Civil Construction', baseline: 650, simulatedOverrun: 920, acceleratedMitigation: 710 },
  { stage: 'Commissioning & Trial', baseline: 150, simulatedOverrun: 260, acceleratedMitigation: 170 },
];

const DEMO_LINE_DATA = [
  { month: "Q1'25", plannedBaseline: 15, simulatedActual: 14, upperBand: 18, lowerBand: 12 },
  { month: "Q2'25", plannedBaseline: 32, simulatedActual: 27, upperBand: 36, lowerBand: 24 },
  { month: "Q3'25", plannedBaseline: 50, simulatedActual: 39, upperBand: 55, lowerBand: 35 },
  { month: "Q4'25", plannedBaseline: 68, simulatedActual: 48, upperBand: 74, lowerBand: 44 },
  { month: "Q1'26", plannedBaseline: 82, simulatedActual: 58, upperBand: 89, lowerBand: 52 },
  { month: "Q2'26", plannedBaseline: 100, simulatedActual: 67, upperBand: 110, lowerBand: 60 },
];

export const V3DemoSegment = () => {
  const [activeScenario, setActiveScenario] = useState('simulatedOverrun');

  return (
    <div className="p-5 rounded-2xl bg-gradient-to-br from-purple-950/20 via-surface-elevated to-surface-elevated border border-purple-500/40 space-y-4 shadow-sm animate-fade-in">
      {/* V.3 Sandbox Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 border-b border-purple-200/40 pb-3">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-purple-700 text-white flex items-center justify-center shadow-xs">
            <Sparkles className="w-4 h-4 text-purple-200" aria-hidden="true" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-sm font-extrabold text-purple-950 tracking-tight">
                V.3 Demonstration Sandbox & Simulated Analytics
              </h2>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-purple-100 text-purple-800 border border-purple-200 font-bold">
                v.3@gmail.com Exclusive
              </span>
            </div>
            <p className="text-[11px] text-slate-600">
              Interactive scenario modeling & demonstration graphs. Regular dashboard shows only authentic MoSPI data.
            </p>
          </div>
        </div>

        {/* Showcase Links */}
        <div className="flex items-center gap-2 text-xs">
          <span className="text-[11px] text-slate-600 font-mono">Demo Scenarios:</span>
          <Link
            to="/explorer?status=Delayed"
            className="px-2.5 py-1 rounded-md bg-purple-50 hover:bg-purple-100 border border-purple-200 text-purple-800 text-[11px] font-bold flex items-center gap-1 transition-colors"
          >
            <ShieldAlert className="w-3.5 h-3.5 text-red-600" aria-hidden="true" />
            <span>Overrun Slip</span>
          </Link>
          <Link
            to="/explorer?status=On%20Track"
            className="px-2.5 py-1 rounded-md bg-purple-50 hover:bg-purple-100 border border-purple-200 text-purple-800 text-[11px] font-bold flex items-center gap-1 transition-colors"
          >
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" aria-hidden="true" />
            <span>On-Track Standard</span>
          </Link>
        </div>
      </div>

      {/* Demo Visualizations Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Demo Bar Graph */}
        <Card
          title="Demo Bar Graph: Stage-Wise Outlay Escalation (₹ Cr)"
          subtitle="Simulated capital absorption variance across critical execution stages"
        >
          <div className="h-56 mt-2" role="region" aria-label="Demo Bar Graph: Stage-Wise Outlay Escalation">
            <ResponsiveContainer width="100%" height="100%" debounce={50} minWidth={100} minHeight={200}>
              <BarChart data={DEMO_BAR_DATA} margin={{ top: 10, right: 15, left: -15, bottom: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="stage" tick={{ fontSize: 10, fill: '#334155' }} interval={0} angle={-10} textAnchor="end" />
                <YAxis tick={{ fontSize: 10, fill: '#334155' }} unit=" Cr" />
                <Tooltip formatter={(val) => [`₹${val} Cr`, '']} contentStyle={{ backgroundColor: '#ffffff', borderRadius: '8px', border: '1px solid #e2e8f0', fontSize: '12px' }} />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '8px' }} />
                <Bar dataKey="baseline" name="Baseline Sanction" fill="#94a3b8" radius={[3, 3, 0, 0]} />
                <Bar dataKey="simulatedOverrun" name="Simulated Overrun" fill="#ef4444" radius={[3, 3, 0, 0]} />
                <Bar dataKey="acceleratedMitigation" name="Mitigated Trajectory" fill="#8b5cf6" radius={[3, 3, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>

        {/* Demo Line Graph */}
        <Card
          title="Demo Line Graph: Projected S-Curve & Confidence Band (%)"
          subtitle="Chronological expenditure forecast with 90% uncertainty envelopes"
        >
          <div className="h-56 mt-2" role="region" aria-label="Demo Line Graph: Projected S-Curve & Confidence Band">
            <ResponsiveContainer width="100%" height="100%" debounce={50} minWidth={100} minHeight={200}>
              <LineChart data={DEMO_LINE_DATA} margin={{ top: 10, right: 15, left: -15, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="month" tick={{ fontSize: 10, fill: '#334155' }} />
                <YAxis domain={[0, 120]} tick={{ fontSize: 10, fill: '#334155' }} unit="%" />
                <Tooltip formatter={(val) => [`${val}%`, '']} contentStyle={{ backgroundColor: '#ffffff', borderRadius: '8px', border: '1px solid #e2e8f0', fontSize: '12px' }} />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '8px' }} />
                <Line type="monotone" dataKey="plannedBaseline" name="Planned Baseline" stroke="#94a3b8" strokeWidth={2} strokeDasharray="3 3" dot={false} />
                <Line type="monotone" dataKey="simulatedActual" name="Simulated Burn" stroke="#8b5cf6" strokeWidth={2.5} dot={{ r: 3 }} />
                <Line type="monotone" dataKey="upperBand" name="90% Upper Bound" stroke="#f43f5e" strokeWidth={1} strokeDasharray="2 2" dot={false} />
                <Line type="monotone" dataKey="lowerBand" name="90% Lower Bound" stroke="#10b981" strokeWidth={1} strokeDasharray="2 2" dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default V3DemoSegment;
