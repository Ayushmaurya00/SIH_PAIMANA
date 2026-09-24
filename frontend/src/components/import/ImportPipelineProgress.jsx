import React from 'react';
import { RefreshCw, CheckCircle2 } from 'lucide-react';

export const PIPELINE_STAGES = [
  { id: 1, label: 'Document Validation & Integrity Check', targetPct: 18, desc: 'Verifying file signatures and header structure...' },
  { id: 2, label: 'Table Extraction (Tables 6, 3 & 4)', targetPct: 45, desc: 'Extracting ongoing outlays, expenditure, and physical progress...' },
  { id: 3, label: 'CUF Schema Normalization & Snapshots', targetPct: 70, desc: 'Deduplicating project IDs and logging monthly telemetry...' },
  { id: 4, label: 'Dual ML Conformal Inference (XGBoost)', targetPct: 88, desc: 'Generating 90% confidence bounds and SHAP drivers...' },
  { id: 5, label: 'Risk Scoring & Early Warning Alerts', targetPct: 98, desc: 'Triaging composite 0–100 risk indices and prescriptive playbooks...' },
];

export const ImportPipelineProgress = ({ progressPct, currentStageIdx }) => {
  return (
    <div className="py-6 space-y-5">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <RefreshCw className="w-4 h-4 text-blue-600 animate-spin" />
          <span className="text-xs font-bold text-slate-800">
            {PIPELINE_STAGES[currentStageIdx]?.label}
          </span>
        </div>
        <span className="text-xs font-bold font-mono text-blue-600">{progressPct}%</span>
      </div>

      <div className="w-full bg-slate-100 rounded-full h-2 overflow-hidden border border-slate-200">
        <div
          className="bg-blue-600 h-full rounded-full transition-all duration-300"
          style={{ width: `${progressPct}%` }}
        />
      </div>

      <div className="space-y-2 pt-2">
        {PIPELINE_STAGES.map((stg, i) => {
          const isDone = i < currentStageIdx || progressPct === 100;
          const isCurrent = i === currentStageIdx && progressPct < 100;
          return (
            <div key={stg.id} className="flex items-center gap-2.5 text-xs">
              {isDone ? (
                <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
              ) : isCurrent ? (
                <div className="w-4 h-4 rounded-full border-2 border-blue-600 border-t-transparent animate-spin shrink-0" />
              ) : (
                <div className="w-4 h-4 rounded-full bg-slate-200 shrink-0" />
              )}
              <span className={isDone ? 'text-slate-700 font-medium' : isCurrent ? 'text-blue-700 font-bold' : 'text-slate-400'}>
                {stg.label}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ImportPipelineProgress;
