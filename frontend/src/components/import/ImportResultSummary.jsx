import React from 'react';
import { CheckCircle2, Sparkles, ArrowRight } from 'lucide-react';

export const ImportResultSummary = ({ result, onClose, handleReset }) => {
  return (
    <div className="py-4 space-y-4">
      <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-900 flex items-start gap-3">
        <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
        <div>
          <h4 className="text-sm font-bold">Ingestion & Telemetry Pipeline Completed</h4>
          <p className="text-xs text-emerald-700 mt-0.5">
            Files parsed, normalized to Unified CUF schema, and re-scored via Machine Learning pipeline.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-center">
        <div className="p-2.5 bg-slate-50 border border-slate-200 rounded-lg">
          <div className="text-[10px] uppercase font-mono text-slate-500">Files Ingested</div>
          <div className="text-lg font-extrabold text-slate-900">{result.files_processed || 1}</div>
        </div>
        <div className="p-2.5 bg-slate-50 border border-slate-200 rounded-lg">
          <div className="text-[10px] uppercase font-mono text-slate-500">Projects Upserted</div>
          <div className="text-lg font-extrabold text-blue-700">{result.projects_upserted || 0}</div>
        </div>
        <div className="p-2.5 bg-slate-50 border border-slate-200 rounded-lg">
          <div className="text-[10px] uppercase font-mono text-slate-500">Snapshots Logged</div>
          <div className="text-lg font-extrabold text-emerald-700">{result.snapshots_inserted || 0}</div>
        </div>
        <div className="p-2.5 bg-slate-50 border border-slate-200 rounded-lg">
          <div className="text-[10px] uppercase font-mono text-slate-500">ML Predictions</div>
          <div className="text-lg font-extrabold text-amber-700">{result.predictions_generated || result.projects_upserted || 0}</div>
        </div>
      </div>

      <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-200">
        <button
          type="button"
          onClick={handleReset}
          className="text-xs px-3 py-1.5 border border-slate-300 rounded-lg hover:bg-slate-50 text-slate-700"
        >
          Import More Files
        </button>
        <button
          type="button"
          onClick={onClose}
          className="btn-primary text-xs flex items-center gap-1.5 py-1.5 px-3 bg-blue-700 text-white rounded-lg"
        >
          <span>View Updated Dashboard</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
};

export default ImportResultSummary;
