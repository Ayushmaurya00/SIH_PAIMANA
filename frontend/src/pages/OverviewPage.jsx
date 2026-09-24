import React, { useEffect, useState } from 'react';
import { Layers, DollarSign, AlertTriangle, ShieldCheck } from 'lucide-react';
import { getDashboardSummary } from '../api/client';
import { useAuth } from '../context/AuthContext';
import KPICard from '../components/KPICard';
import HealthIndicator from '../components/HealthIndicator';
import LoadingSkeleton from '../components/LoadingSkeleton';
import EmptyState from '../components/EmptyState';
import { OverviewHeader } from '../components/overview/OverviewHeader';
import { ImmediateAttentionSection } from '../components/overview/ImmediateAttentionSection';
import { OverviewCharts } from '../components/overview/OverviewCharts';
import V3DemoSegment from '../components/overview/V3DemoSegment';
import { formatCurrency } from '../utils/cn';

export const OverviewPage = () => {
  const { isDemoMode } = useAuth();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let mounted = true;
    (async () => {
      try {
        setLoading(true);
        const res = await getDashboardSummary();
        if (mounted) { setData(res); setError(null); }
      } catch {
        if (mounted) setError('Failed to load dashboard telemetry.');
      } finally {
        if (mounted) setLoading(false);
      }
    })();
    return () => { mounted = false; };
  }, []);

  if (loading) {
    return (
      <div className="p-6 space-y-6 max-w-7xl mx-auto">
        <div className="h-8 w-72 bg-surface-subtle rounded-lg shimmer border border-border-rest" />
        <LoadingSkeleton type="kpi" />
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <div className="lg:col-span-7 h-80 bg-surface-subtle rounded-xl shimmer border border-border-rest" />
          <div className="lg:col-span-5 h-80 bg-surface-subtle rounded-xl shimmer border border-border-rest" />
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="p-6 max-w-7xl mx-auto">
        <EmptyState title="Failed to Load Portfolio Overview" description={error || 'Unable to fetch dashboard telemetry.'} icon="alert" action={<button onClick={() => window.location.reload()} className="btn-primary">Retry Connection</button>} />
      </div>
    );
  }

  const topAtRisk = data.top_at_risk_projects || [];
  const highRiskCount = data.high_risk_count || 0;
  const mediumRiskCount = data.medium_risk_count || 0;
  const lowRiskCount = data.low_risk_count || 0;
  const totalProjects = data.total_projects !== undefined ? data.total_projects : 1;

  return (
    <div className="p-6 space-y-6 max-w-7xl mx-auto animate-fade-in">
      <OverviewHeader />

      {/* V.3 Demo Segment: Exclusively rendered when logged in with v.3 demo email */}
      {isDemoMode && <V3DemoSegment />}

      <section aria-label="Portfolio Health Overview">
        <HealthIndicator highCount={highRiskCount} mediumCount={mediumRiskCount} lowCount={lowRiskCount} totalProjects={totalProjects} />
      </section>

      <section aria-label="Key Performance Indicators" className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard title="Monitored Projects" value={totalProjects.toLocaleString()} subtitle="All Central Sector Initiatives" icon={Layers} />
        <KPICard title="Total Sanctioned Outlay" value={formatCurrency(data.total_approved_cost_cr || 0)} subtitle={`Expenditure: ${formatCurrency(data.total_expenditure_cr || 0)}`} icon={DollarSign} />
        <KPICard title="Critical Delay Projects" value={highRiskCount.toLocaleString()} subtitle={`${((highRiskCount / totalProjects) * 100).toFixed(1)}% of Portfolio At-Risk`} icon={AlertTriangle} />
        <KPICard title="On-Track" value={lowRiskCount.toLocaleString()} subtitle="Progress within planned schedule" icon={ShieldCheck} />
      </section>

      <ImmediateAttentionSection topAtRisk={topAtRisk} />
      <OverviewCharts data={data} />
    </div>
  );
};

export default OverviewPage;
