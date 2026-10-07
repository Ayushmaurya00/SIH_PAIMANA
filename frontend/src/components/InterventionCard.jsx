import React from 'react';
import { Building2, Clock, CheckCircle2, ArrowUpRight } from 'lucide-react';

export const InterventionCard = ({ prescription, index = 1 }) => {
  if (!prescription) return null;

  const authority = prescription.authority || 'Nodal Ministry Administrative Wing';
  const timelineDays = prescription.statutory_timeline_days || 30;
  const title = prescription.title || 'Administrative Remediation';
  const action = prescription.recommended_action || 'Review and expedite statutory clearances.';
  const stepNumber = prescription.step || index;

  return (
    <div className="p-4 rounded-xl border border-border-rest bg-surface-elevated hover:border-border-focus transition-colors">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 pb-2.5 border-b border-border-rest">
        <div className="flex items-center gap-2">
          <span className="flex items-center justify-center w-5 h-5 rounded-full bg-primary-sovereign text-white font-mono text-[11px] font-bold shrink-0">
            {stepNumber}
          </span>
          <h4 className="text-sm font-bold text-text-primary">
            {title}
          </h4>
        </div>

        <div className="flex items-center gap-2">
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-md text-xs font-semibold bg-surface-elevated border border-border-rest text-text-secondary">
            <Building2 className="w-3 h-3 text-text-tertiary" aria-hidden="true" />
            {authority}
          </span>
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[11px] font-medium bg-surface-subtle text-text-secondary font-mono border border-border-rest">
            <Clock className="w-3 h-3 text-text-tertiary" aria-hidden="true" />
            {timelineDays} Days
          </span>
        </div>
      </div>

      <div className="mt-3">
        <p className="text-xs text-text-secondary leading-relaxed font-normal">
          {action}
        </p>
      </div>

      <div className="mt-3 pt-2.5 border-t border-border-rest flex items-center justify-between text-[11px] text-text-tertiary">
        <span className="flex items-center gap-1 font-normal">
          <CheckCircle2 className="w-3.5 h-3.5 text-status-healthy" aria-hidden="true" />
          Statutory Compliance: GFR / MoSPI Guidelines
        </span>
        <span className="text-primary-sovereign font-semibold hover:underline cursor-pointer flex items-center gap-0.5">
          Escalation Protocol <ArrowUpRight className="w-3 h-3" aria-hidden="true" />
        </span>
      </div>
    </div>
  );
};

export default InterventionCard;
