import React from 'react';
import { Zap, AlertCircle, TrendingUp, ShieldAlert } from 'lucide-react';
import Card from '../Card';

export const PredictiveTelemetry = ({ project, costDelta, costDeltaPct, expPct }) => {
  const costOverrunProb = project.cost_overrun_prob != null ? (project.cost_overrun_prob * 100).toFixed(1) : null;
  const timeOverrunProb = project.time_overrun_prob != null ? (project.time_overrun_prob * 100).toFixed(1) : null;
  const costPredLower = project.cost_overrun_pct_lower != null ? project.cost_overrun_pct_lower.toFixed(1) : null;
  const costPredUpper = project.cost_overrun_pct_upper != null ? project.cost_overrun_pct_upper.toFixed(1) : null;
  const timePredLower = project.time_delay_lower_months != null ? project.time_delay_lower_months.toFixed(1) : null;
  const timePredUpper = project.time_delay_upper_months != null ? project.time_delay_upper_months.toFixed(1) : null;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Key Financial Health KPI */}
      <Card title="Financial Sanctions & Expenditure" subtitle="Authorized Outlays vs Cumulative Drawdowns">
        <div className="space-y-3 mt-1">
          <div className="flex justify-between items-center py-1.5 border-b border-slate-100 text-xs">
            <span className="text-slate-600 font-medium">Sanctioned Outlay:</span>
            <span className="font-bold text-slate-800">₹{project.approved_cost_cr?.toLocaleString('en-IN')} Cr</span>
          </div>
          <div className="flex justify-between items-center py-1.5 border-b border-slate-100 text-xs">
            <span className="text-slate-600 font-medium">Latest Revised Estimate:</span>
            <span className="font-bold text-slate-900">₹{project.revised_cost_cr?.toLocaleString('en-IN')} Cr</span>
          </div>
          <div className="flex justify-between items-center py-1.5 border-b border-slate-100 text-xs">
            <span className="text-slate-600 font-medium">Variance / Escalation:</span>
            <span className={`font-bold ${costDelta > 0 ? 'text-red-600' : 'text-emerald-600'}`}>
              {costDelta > 0 ? `+₹${costDelta.toLocaleString('en-IN')} Cr (+${costDeltaPct.toFixed(1)}%)` : '₹0.00 (On Budget)'}
            </span>
          </div>
          <div className="flex justify-between items-center py-1.5 text-xs">
            <span className="text-slate-600 font-medium">Cumulative Expenditure:</span>
            <span className="font-bold text-blue-700">₹{project.cumulative_expenditure_cr?.toLocaleString('en-IN')} Cr ({expPct}%)</span>
          </div>
        </div>
      </Card>

      {/* ML Cost Overrun Forecast Card */}
      <Card title="Predictive Cost Forecast" subtitle="Calibrated 90% Conformal Prediction Intervals">
        <div className="space-y-3 mt-1">
          <div className="flex justify-between items-center py-1.5 border-b border-slate-100 text-xs">
            <span className="text-slate-600 font-medium">Overrun Likelihood:</span>
            <span className="font-bold text-slate-900">{costOverrunProb ? `${costOverrunProb}%` : 'Low Risk'}</span>
          </div>
          <div className="flex justify-between items-center py-1.5 border-b border-slate-100 text-xs">
            <span className="text-slate-600 font-medium">Point Estimate Escalation:</span>
            <span className="font-bold text-amber-700">
              {project.cost_overrun_pct_pred != null ? `+${project.cost_overrun_pct_pred.toFixed(1)}%` : '0.0%'}
            </span>
          </div>
          <div className="flex justify-between items-center py-1.5 text-xs">
            <span className="text-slate-600 font-medium">90% Confidence Interval:</span>
            <span className="font-bold text-slate-900 font-mono">
              {costPredLower && costPredUpper ? `+${costPredLower}% → +${costPredUpper}%` : '±3.5%'}
            </span>
          </div>
        </div>
      </Card>

      {/* ML Time Delay Forecast Card */}
      <Card title="Predictive Schedule Horizon" subtitle="Quantile Delay Estimation in Calendar Months">
        <div className="space-y-3 mt-1">
          <div className="flex justify-between items-center py-1.5 border-b border-slate-100 text-xs">
            <span className="text-slate-600 font-medium">Delay Probability:</span>
            <span className="font-bold text-slate-900">{timeOverrunProb ? `${timeOverrunProb}%` : 'Low Risk'}</span>
          </div>
          <div className="flex justify-between items-center py-1.5 border-b border-slate-100 text-xs">
            <span className="text-slate-600 font-medium">Predicted Schedule Delay:</span>
            <span className="font-bold text-red-600">
              {project.time_overrun_months_pred != null ? `+${project.time_overrun_months_pred.toFixed(1)} months` : '0 months'}
            </span>
          </div>
          <div className="flex justify-between items-center py-1.5 text-xs">
            <span className="text-slate-600 font-medium">90% Delay Interval:</span>
            <span className="font-bold text-slate-900 font-mono">
              {timePredLower && timePredUpper ? `+${timePredLower}m → +${timePredUpper}m` : '0-2 months'}
            </span>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default PredictiveTelemetry;
