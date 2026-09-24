import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import ActionCard from '../ActionCard';

export const ImmediateAttentionSection = ({ topAtRisk = [] }) => {
  if (!topAtRisk || topAtRisk.length === 0) return null;

  return (
    <section aria-label="Projects Requiring Immediate Attention" className="space-y-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-red-600 shrink-0 animate-pulse" aria-hidden="true" />
          <h2 className="text-base font-bold text-slate-900">
            Projects Requiring Immediate Administrative Attention
          </h2>
        </div>
        <Link
          to="/explorer?risk_level=Critical"
          className="text-xs font-semibold text-blue-700 hover:text-blue-800 flex items-center gap-1"
        >
          <span>View All Escalations</span>
          <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {topAtRisk.slice(0, 6).map((proj) => (
          <ActionCard
            key={proj.project_id}
            project={proj}
            projectId={proj.project_id}
            projectName={proj.project_name}
            ministry={proj.ministry}
            sector={proj.sector}
            approvedCost={proj.approved_cost_cr}
            riskScore={proj.risk_score || proj.score}
            riskLevel={proj.risk_level}
          />
        ))}
      </div>
    </section>
  );
};

export default ImmediateAttentionSection;
