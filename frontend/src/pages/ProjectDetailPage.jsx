import React, { useEffect, useState, useMemo } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { getProjectDetail, deleteProject } from '../api/client';
import { useAuth } from '../context/AuthContext';
import Card from '../components/Card';
import MilestoneGantt from '../components/MilestoneGantt';
import InterventionCard from '../components/InterventionCard';
import LoadingSkeleton from '../components/LoadingSkeleton';
import EmptyState from '../components/EmptyState';
import { ProjectHeader } from '../components/project_detail/ProjectHeader';
import { PredictiveTelemetry } from '../components/project_detail/PredictiveTelemetry';
import { FinancialSCurve } from '../components/project_detail/FinancialSCurve';
import { PhaseExecutionGantt } from '../components/project_detail/PhaseExecutionGantt';
import { generateSCurveData, generatePhaseData } from '../components/project_detail/simulationHelpers';

export const ProjectDetailPage = ({ onOpenAssistantWithContext }) => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { isDemoMode } = useAuth();
  const [project, setProject] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let mounted = true;
    (async () => {
      try {
        setLoading(true);
        const res = await getProjectDetail(id);
        if (mounted) { setProject(res); setError(null); }
      } catch {
        if (mounted) setError(`Failed to load project details for ${id}.`);
      } finally {
        if (mounted) setLoading(false);
      }
    })();
    return () => { mounted = false; };
  }, [id]);

  const sCurveData = useMemo(() => (isDemoMode && project) ? generateSCurveData(project) : [], [isDemoMode, project]);
  const phaseData = useMemo(() => (isDemoMode && project) ? generatePhaseData(project) : [], [isDemoMode, project]);

  const handleDelete = async () => {
    if (!window.confirm(`Permanently delete "${project.project_name}"? This cannot be undone.`)) return;
    try {
      await deleteProject(project.project_id);
      navigate('/explorer');
    } catch (err) {
      alert(`Failed to delete: ${err?.response?.data?.detail || err?.message}`);
    }
  };

  if (loading) return <div className="p-6 max-w-7xl mx-auto"><LoadingSkeleton type="detail" /></div>;
  if (error || !project) return (
    <div className="p-6 max-w-7xl mx-auto">
      <EmptyState title="Project Not Found" description={error || `No telemetry for ${id}.`} icon="alert"
        action={<Link to="/explorer" className="btn-primary">Back to Project Directory</Link>} />
    </div>
  );

  const approved = Number(project.approved_cost_cr) || 0;
  const revised = Number(project.revised_cost_cr) || 0;
  const expenditure = Number(project.cumulative_expenditure_cr) || 0;
  const costDelta = revised - approved;
  const costDeltaPct = approved > 0 ? (costDelta / approved) * 100 : 0;
  const expPct = approved > 0 ? ((expenditure / approved) * 100).toFixed(1) : '0.0';

  return (
    <div className="p-6 space-y-6 max-w-7xl mx-auto animate-fade-in">
      <ProjectHeader project={project} costDelta={costDelta} costDeltaPct={costDeltaPct} handleDelete={handleDelete} onOpenAssistantWithContext={onOpenAssistantWithContext} />
      <PredictiveTelemetry project={project} costDelta={costDelta} costDeltaPct={costDeltaPct} expPct={expPct} />

      {/* Synthetic Demonstration Visualizations: Rendered strictly when in V.3 Demo Mode */}
      {isDemoMode && (
        <div className="space-y-6 animate-fade-in">
          <div className="px-4 py-2 rounded-lg bg-purple-50 border border-purple-200 text-purple-900 text-xs flex items-center justify-between">
            <span className="font-semibold">V.3 Demo Mode Active: Displaying synthetic S-Curve forecast and simulated phase breakdown.</span>
            <span className="font-mono text-[10px] bg-purple-200 text-purple-900 px-2 py-0.5 rounded font-bold">SIMULATION</span>
          </div>
          <FinancialSCurve sCurveData={sCurveData} />
          <PhaseExecutionGantt phaseData={phaseData} />
        </div>
      )}

      {/* Authentic Statutory Milestones from Database */}
      {project.milestones && project.milestones.length > 0 && <MilestoneGantt milestones={project.milestones} />}

      {/* Actionable Statutory Interventions */}
      {/* {project.prescriptive_actions && project.prescriptive_actions.length > 0 && (
        <Card title="" subtitle="">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-3">
            {project.prescriptive_actions.map((act, i) => (
              <InterventionCard key={i} title={act.title} recommendedAction={act.recommended_action} authority={act.authority} statutoryTimelineDays={act.statutory_timeline_days} />
            ))}
          </div>
        </Card>
      )} */}
    </div>
  );
};

export default ProjectDetailPage;
