import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import RiskBadge from './RiskBadge';
import { formatCurrency } from '../utils/cn';

export const ActionCard = (props) => {
  const p = props.project || props;
  const pid = p.project_id || props.projectId;
  if (!pid) return null;

  const pname = p.project_name || props.projectName || 'Infrastructure Project';
  const ministry = p.ministry || props.ministry || 'Central Ministry';
  const sector = p.sector || props.sector || 'Infrastructure';
  const agency = p.implementing_agency || props.agency || 'Central Agency';
  const state = p.state || props.state || 'National';
  const cost = p.approved_cost_cr || props.approvedCost || 0;
  const score = p.risk_score || p.score || props.riskScore || 0;
  const riskLevel = p.risk_level || props.riskLevel || (score >= 70 ? 'High' : score >= 40 ? 'Medium' : 'Low');

  return (
    <div className="card p-5 bg-surface-elevated border border-border-rest transition-colors hover:border-border-focus rounded-xl shadow-xs">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 pb-2">
        <div className="flex items-center gap-2">
          <span className="font-mono text-[11px] font-bold px-2 py-0.5 rounded bg-surface-subtle text-text-primary border border-border-rest">
            {pid}
          </span>
          <h3 className="text-sm font-bold text-text-primary hover:text-primary-sovereign transition-colors line-clamp-1">
            <Link to={`/project/${pid}`} aria-label={`View project details for ${pname} (${pid})`}>
              {pname}
            </Link>
          </h3>
        </div>
        <RiskBadge score={score} riskLevel={riskLevel} size="sm" />
      </div>

      <div className="flex flex-wrap items-center gap-x-4 gap-y-1.5 text-xs pt-1 text-slate-600">
        <span>Ministry: <strong className="text-slate-900 font-semibold">{ministry}</strong></span>
        <span>Sector: <strong className="text-slate-900 font-semibold">{sector}</strong></span>
        <span>Agency: <strong className="text-slate-900 font-semibold">{agency}</strong></span>
        <span>State: <strong className="text-slate-900 font-semibold">{state}</strong></span>
        <span>Outlay: <strong className="text-slate-900 font-mono font-semibold">{formatCurrency(cost)}</strong></span>
      </div>

      <div className="flex items-center justify-end pt-3 border-t border-slate-100 mt-3">
        <Link
          to={`/project/${pid}`}
          aria-label={`Examine project ${pname} (${pid})`}
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-blue-700 hover:text-blue-800 transition-colors"
        >
          <span>Examine Project</span>
          <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
        </Link>
      </div>
    </div>
  );
};

export default ActionCard;
