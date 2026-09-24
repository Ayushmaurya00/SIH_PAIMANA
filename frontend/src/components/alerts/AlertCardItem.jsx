import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldAlert, AlertTriangle, ArrowRight, CheckCircle2, Clock } from 'lucide-react';
import Card from '../Card';

export const AlertCardItem = ({ alert, onReview }) => {
  const isHigh = alert.severity === 'High';
  const isNew = alert.status === 'New';

  return (
    <Card
      padding="p-4"
      className={`border-l-4 transition-shadow hover:shadow-xs ${
        isHigh ? 'border-l-status-critical bg-surface-elevated' : 'border-l-status-warning bg-surface-elevated'
      }`}
    >
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="space-y-1.5 flex-1">
          <div className="flex items-center gap-2 flex-wrap">
            <span
              className={`inline-flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 rounded-full ${
                isHigh ? 'bg-red-50 text-status-critical border border-red-200' : 'bg-amber-50 text-status-warning border border-amber-200'
              }`}
            >
              {isHigh ? <ShieldAlert className="w-3 h-3" aria-hidden="true" /> : <AlertTriangle className="w-3 h-3" aria-hidden="true" />}
              <span>{isHigh ? 'CRITICAL ESCALATION' : 'WATCHLIST WARNING'}</span>
            </span>

            <span className="font-mono text-[10px] text-text-tertiary bg-surface-subtle px-1.5 py-0.5 rounded border border-border-rest">
              {alert.project_id}
            </span>

            <span className="text-xs text-text-secondary font-medium">
              {alert.ministry}
            </span>
          </div>

          <h3 className="text-sm font-bold text-text-primary">
            <Link to={`/projects/${alert.project_id}`} aria-label={`View details for ${alert.project_name} (${alert.project_id})`} className="hover:text-primary-sovereign transition-colors">
              {alert.project_name}
            </Link>
          </h3>

          <p className="text-xs text-text-secondary leading-relaxed">
            {alert.trigger_reason}
          </p>

          {alert.prescriptive_action && (
            <div className="p-2.5 rounded-lg bg-surface-subtle border border-border-rest text-xs text-text-primary mt-2">
              <strong className="text-primary-sovereign">Recommended Playbook:</strong> {alert.prescriptive_action}
            </div>
          )}
        </div>

        <div className="flex md:flex-col items-center md:items-end justify-between gap-2 shrink-0 border-t md:border-t-0 pt-3 md:pt-0 border-border-rest">
          <div className="text-right">
            <span className="text-[10px] text-text-tertiary font-mono block">
              {alert.triggered_at ? new Date(alert.triggered_at).toLocaleDateString('en-IN') : 'Recent'}
            </span>
            <span className={`text-[10px] font-bold px-2 py-0.5 rounded-md mt-1 inline-block ${
              isNew ? 'bg-amber-50 text-amber-700 border border-amber-200' : 'bg-emerald-50 text-emerald-700 border border-emerald-200'
            }`}>
              {alert.status}
            </span>
          </div>

          <div className="flex items-center gap-2">
            {isNew && (
              <button
                type="button"
                onClick={() => onReview(alert.alert_id)}
                aria-label={`Acknowledge escalation alert for ${alert.project_id}`}
                className="text-xs px-2.5 py-1.5 bg-surface-subtle hover:bg-surface-elevated text-text-primary border border-border-rest rounded-lg font-medium transition-colors"
              >
                Acknowledge
              </button>
            )}
            <Link
              to={`/project/${alert.project_id}`}
              aria-label={`Inspect project ${alert.project_name} (${alert.project_id})`}
              className="btn-primary text-xs flex items-center gap-1 py-1.5 px-3"
            >
              <span>Inspect</span>
              <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
            </Link>
          </div>
        </div>
      </div>
    </Card>
  );
};

export default AlertCardItem;
