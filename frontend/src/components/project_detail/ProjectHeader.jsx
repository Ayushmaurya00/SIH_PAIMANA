import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, Trash2, Calendar, MapPin, Clock, Sparkles } from 'lucide-react';
import RiskBadge from '../RiskBadge';
import { useAuth } from '../../context/AuthContext';

export const ProjectHeader = ({ project, costDelta, costDeltaPct, handleDelete, onOpenAssistantWithContext }) => {
  const { user } = useAuth();
  const isAuditor = user && user.role === 'auditor';
  return (
    <div className="space-y-4">
      {/* Top Breadcrumb & Actions Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-200 pb-4">
        <div className="flex items-center gap-2">
          <Link
            to="/explorer"
            aria-label="Return to Project Explorer"
            className="text-xs text-slate-600 hover:text-slate-900 flex items-center gap-1 font-medium transition-colors"
          >
            <ArrowLeft aria-hidden="true" className="w-4 h-4" />
            <span>Back to Explorer</span>
          </Link>
          <span className="text-slate-300">/</span>
          <span className="text-xs font-mono font-bold text-blue-700 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
            {project.project_id}
          </span>
        </div>

        <div className="flex items-center gap-2">
          {onOpenAssistantWithContext && (
            <button
              onClick={() => onOpenAssistantWithContext(project.project_id)}
              aria-label="Ask AI Copilot about this project"
              className="btn-primary text-xs flex items-center gap-1.5 py-1.5 px-3 bg-blue-700 hover:bg-blue-800 text-white rounded-lg shadow-xs"
            >
              <Sparkles aria-hidden="true" className="w-3.5 h-3.5" />
              <span>Ask AI Copilot</span>
            </button>
          )}
          <button
            onClick={() => !isAuditor && handleDelete()}
            disabled={isAuditor}
            title={isAuditor ? "Requires Nodal Desk Officer Clearance" : "Delete Project from monitoring directory"}
            aria-label="Delete Project from monitoring directory"
            className={`text-xs flex items-center gap-1.5 py-1.5 px-3 rounded-lg transition-colors border ${
              isAuditor
                ? 'bg-slate-100 text-slate-400 border-slate-200 cursor-not-allowed'
                : 'border-red-200 text-red-600 hover:bg-red-50 cursor-pointer'
            }`}
          >
            <Trash2 aria-hidden="true" className="w-3.5 h-3.5" />
            <span>Delete Project</span>
          </button>
        </div>
      </div>

      {/* Project Title & Metadata Bar */}
      <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs flex flex-col md:flex-row md:items-start justify-between gap-4">
        <div>
          <div className="flex items-center gap-2.5 flex-wrap mb-2">
            <span className="text-xs font-bold px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700 border border-slate-300">
              {project.sector}
            </span>
            <span className="text-xs font-semibold text-slate-600">
              {project.ministry}
            </span>
            <span className="text-xs font-bold px-2 py-0.5 rounded bg-blue-50 text-blue-700 border border-blue-200">
              {project.implementing_agency}
            </span>
          </div>

          <h1 className="text-xl font-extrabold text-slate-900 tracking-tight">
            {project.project_name}
          </h1>

          <div className="flex items-center gap-4 text-xs text-slate-600 mt-2 flex-wrap">
            <div className="flex items-center gap-1">
              <MapPin aria-hidden="true" className="w-3.5 h-3.5 text-slate-500" />
              <span>{project.state}</span>
            </div>
            <div className="flex items-center gap-1">
              <Calendar aria-hidden="true" className="w-3.5 h-3.5 text-slate-500" />
              <span>Approved: {project.approval_date}</span>
            </div>
            <div className="flex items-center gap-1">
              <Clock aria-hidden="true" className="w-3.5 h-3.5 text-slate-500" />
              <span>Target COD: {project.revised_completion || project.scheduled_completion}</span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-4 self-start md:self-auto bg-slate-50 p-3 rounded-lg border border-slate-200">
          <div className="text-right">
            <div className="text-[10px] uppercase font-mono text-slate-500 font-bold">Composite Risk</div>
            <div className="text-xl font-black text-slate-900">{project.risk_score || project.score || 0}/100</div>
          </div>
          <RiskBadge level={project.risk_level} />
        </div>
      </div>
    </div>
  );
};

export default ProjectHeader;
