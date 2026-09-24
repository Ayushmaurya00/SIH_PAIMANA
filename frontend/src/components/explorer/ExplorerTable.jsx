import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowUpDown, ArrowRight, Trash2 } from 'lucide-react';
import RiskBadge from '../RiskBadge';

export const ExplorerTable = ({
  projects,
  sortBy,
  sortOrder,
  setSortBy,
  setSortOrder,
  handleDeleteProject
}) => {
  const handleSort = (field) => {
    if (sortBy === field) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(field);
      setSortOrder('desc');
    }
  };

  const getStatusDot = (projStatus) => {
    if (projStatus === 'Delayed') return 'bg-status-warning';
    if (projStatus === 'Stalled') return 'bg-status-critical';
    if (projStatus === 'Completed') return 'bg-primary';
    return 'bg-status-healthy';
  };

  return (
    <div className="bg-surface-elevated rounded-xl border border-border-rest shadow-xs overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="border-b border-border-rest bg-surface-subtle font-mono text-[11px] text-text-secondary uppercase">
              <th className="py-2.5 px-3">Project ID / Title</th>
              <th className="py-2.5 px-3">Ministry & Sector</th>
              <th className="py-2.5 px-3 cursor-pointer hover:text-text-primary" onClick={() => handleSort('cost')}>
                <div className="flex items-center gap-1">
                  <span>Outlay (₹ Cr)</span>
                  <ArrowUpDown className="w-3 h-3" aria-hidden="true" />
                </div>
              </th>
              <th className="py-2.5 px-3 cursor-pointer hover:text-text-primary" onClick={() => handleSort('progress')}>
                <div className="flex items-center gap-1">
                  <span>Progress</span>
                  <ArrowUpDown className="w-3 h-3" aria-hidden="true" />
                </div>
              </th>
              <th className="py-2.5 px-3">Status</th>
              <th className="py-2.5 px-3 cursor-pointer hover:text-text-primary text-right" onClick={() => handleSort('score')}>
                <div className="flex items-center justify-end gap-1">
                  <span>Risk Score</span>
                  <ArrowUpDown className="w-3 h-3" aria-hidden="true" />
                </div>
              </th>
              <th className="py-2.5 px-3 text-center">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border-rest">
            {projects.map((proj) => (
              <tr key={proj.project_id} className="hover:bg-surface-subtle/50 transition-colors">
                <td className="py-2.5 px-3">
                  <div className="flex items-center gap-1.5 mb-0.5">
                    <span className="font-mono font-bold text-[10px] text-primary-sovereign bg-surface-subtle px-1.5 py-0.2 rounded border border-border-rest">
                      {proj.project_id}
                    </span>
                    <span className="text-[10px] text-text-tertiary">{proj.state}</span>
                  </div>
                  <Link
                    to={`/project/${proj.project_id}`}
                    aria-label={`View details for ${proj.project_name} (${proj.project_id})`}
                    className="font-bold text-text-primary hover:text-primary-sovereign line-clamp-1 transition-colors"
                  >
                    {proj.project_name}
                  </Link>
                </td>

                <td className="py-2.5 px-3">
                  <div className="text-text-primary font-medium line-clamp-1">{proj.sector}</div>
                  <div className="text-[10px] text-text-tertiary line-clamp-1">{proj.ministry}</div>
                </td>

                <td className="py-2.5 px-3 font-mono font-bold text-text-primary">
                  ₹{proj.approved_cost_cr?.toLocaleString('en-IN')}
                </td>

                <td className="py-2.5 px-3">
                  <div className="flex items-center gap-2">
                    <div className="w-16 bg-surface-subtle rounded-full h-1.5 overflow-hidden border border-border-rest">
                      <div
                        className="bg-primary-sovereign h-full rounded-full"
                        style={{ width: `${Math.min(100, Math.max(0, proj.physical_progress_pct))}%` }}
                      />
                    </div>
                    <span className="font-mono font-semibold text-[11px] text-text-primary">
                      {proj.physical_progress_pct}%
                    </span>
                  </div>
                </td>

                <td className="py-2.5 px-3">
                  <span className="inline-flex items-center gap-1.5 font-medium text-[11px] text-text-secondary">
                    <span className={`w-2 h-2 rounded-full ${getStatusDot(proj.status)}`} aria-hidden="true" />
                    <span>{proj.status}</span>
                  </span>
                </td>

                <td className="py-2.5 px-3 text-right">
                  <div className="flex items-center justify-end gap-1.5">
                    <span className="font-mono font-extrabold text-xs text-text-primary">
                      {proj.score || 0}
                    </span>
                    <RiskBadge level={proj.risk_level} />
                  </div>
                </td>

                <td className="py-2.5 px-3 text-center">
                  <div className="flex items-center justify-center gap-1">
                    <Link
                      to={`/project/${proj.project_id}`}
                      aria-label={`View telemetry for ${proj.project_name} (${proj.project_id})`}
                      className="p-1 rounded-md text-text-tertiary hover:text-primary-sovereign hover:bg-surface-subtle transition-colors"
                      title="View Project Telemetry"
                    >
                      <ArrowRight className="w-4 h-4" aria-hidden="true" />
                    </Link>
                    <button
                      type="button"
                      onClick={() => handleDeleteProject(proj.project_id, proj.project_name)}
                      aria-label={`Delete project ${proj.project_name} (${proj.project_id})`}
                      className="p-1 rounded-md text-text-tertiary hover:text-status-critical hover:bg-red-50 transition-colors"
                      title="Delete Project"
                    >
                      <Trash2 className="w-3.5 h-3.5" aria-hidden="true" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ExplorerTable;
