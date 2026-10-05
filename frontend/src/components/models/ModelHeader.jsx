import React from 'react';
import { GitCompare, Award } from 'lucide-react';

export const ModelHeader = () => {
  return (
    <div className="space-y-4">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-border-rest pb-3">
        <div>
          <h1 className="text-xl font-extrabold text-text-primary tracking-tight flex items-center gap-2">
            <GitCompare className="w-5 h-5 text-primary-sovereign" />
            <span>Model Comparison & Feature Ablation (SIH Technical Dimension)</span>
          </h1>
          <p className="text-xs text-text-tertiary mt-0.5">
            Empirical benchmarking of <code className="text-primary-sovereign font-mono font-bold">model_bundle_cuf_only.joblib</code> vs <code className="text-status-healthy font-mono font-bold">model_bundle_cuf_plus_extra.joblib</code> across out-of-time temporal cohorts
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold px-2.5 py-1 rounded-md bg-surface-elevated border border-border-rest text-text-secondary">
            Validation Protocol: <strong>Chronological Out-of-Time (80/20 Cohort)</strong>
          </span>
        </div>
      </div>

      <div className="p-4 rounded-xl bg-surface-subtle border border-border-rest text-text-secondary">
        <div className="flex items-start gap-3">
          <Award className="w-5 h-5 text-primary-sovereign shrink-0 mt-0.5" />
          <div className="text-xs leading-relaxed">
            <strong className="text-text-primary font-bold">SIH Technical Evaluation Dimension:</strong>
            {" "}The Smart India Hackathon problem statement specifically tasks participants to evaluate whether auxiliary variables beyond the standard Ministry Common Unified Framework (CUF) outlays enhance early warning detection.
            Our dual-pipeline architecture trains and evaluates both bundles side-by-side to prove the empirical predictive lift of stage-gate milestone friction, cash-flow burn velocity, and domain complexity indices.
          </div>
        </div>
      </div>
    </div>
  );
};

export default ModelHeader;
