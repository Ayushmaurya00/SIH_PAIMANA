import React, { useState, useEffect } from 'react';
import { ShieldAlert, CheckCircle2 } from 'lucide-react';
import { getAlerts, getAlertCount, reviewAlert } from '../api/client';
import LoadingSkeleton from '../components/LoadingSkeleton';
import EmptyState from '../components/EmptyState';
import { AlertsFilterBar } from '../components/alerts/AlertsFilterBar';
import { AlertCardItem } from '../components/alerts/AlertCardItem';
import { AlertsPagination } from '../components/alerts/AlertsPagination';

const CHUNK_SIZE = 30;

export const AlertsPage = () => {
  const [alerts, setAlerts] = useState([]);
  const [severityFilter, setSeverityFilter] = useState('All');
  const [statusFilter, setStatusFilter] = useState('All');
  const [page, setPage] = useState(0);
  const [totalCount, setTotalCount] = useState(0);
  const [highCount, setHighCount] = useState(0);
  const [medCount, setMedCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [actionSuccess, setActionSuccess] = useState(null);

  // Fetch overall critical and watchlist totals
  useEffect(() => {
    let mounted = true;
    (async () => {
      try {
        const [highRes, medRes] = await Promise.all([
          getAlertCount({ severity: 'High' }),
          getAlertCount({ severity: 'Medium' })
        ]);
        if (mounted) {
          setHighCount(highRes?.count || 0);
          setMedCount(medRes?.count || 0);
        }
      } catch (err) {
        console.error('Error fetching alert totals:', err);
      }
    })();
    return () => { mounted = false; };
  }, []);

  // Reset to first chunk whenever filter changes
  useEffect(() => {
    setPage(0);
  }, [severityFilter, statusFilter]);

  // Fetch chunked alerts for current filter and page
  useEffect(() => {
    let mounted = true;
    const fetchChunk = async () => {
      try {
        setLoading(true);
        const filterParams = {
          severity: severityFilter !== 'All' ? severityFilter : undefined,
          status: statusFilter !== 'All' ? statusFilter : undefined
        };

        const [alertsRes, countRes] = await Promise.all([
          getAlerts({
            ...filterParams,
            limit: CHUNK_SIZE,
            offset: page * CHUNK_SIZE
          }),
          getAlertCount(filterParams)
        ]);

        if (mounted) {
          setAlerts(alertsRes || []);
          setTotalCount(countRes?.count || 0);
        }
      } catch (err) {
        console.error('Error fetching alerts chunk:', err);
      } finally {
        if (mounted) setLoading(false);
      }
    };

    fetchChunk();
    return () => { mounted = false; };
  }, [severityFilter, statusFilter, page]);

  const handleReview = async (alertId) => {
    try {
      await reviewAlert(alertId);
      setAlerts((prev) => prev.map((a) => (a.alert_id === alertId ? { ...a, status: 'Reviewed' } : a)));
      setActionSuccess(`Escalation Alert #${alertId} acknowledged and logged.`);
      setTimeout(() => setActionSuccess(null), 3500);
    } catch (err) {
      console.error('Error reviewing alert:', err);
    }
  };

  return (
    <div className="p-3 sm:p-6 space-y-4 sm:space-y-6 max-w-7xl mx-auto animate-fade-in">
      {/* Header section with portfolio summary */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 sm:gap-4 border-b border-border-rest pb-3">
        <div>
          <h1 className="text-lg sm:text-xl font-extrabold text-text-primary tracking-tight flex items-center gap-2">
            <ShieldAlert className="w-5 h-5 text-status-critical shrink-0" aria-hidden="true" />
            <span>Early Warning & Escalation Triage</span>
          </h1>
        </div>
        <div className="flex items-center gap-2 text-xs flex-wrap">
          <span className="px-2.5 py-1 rounded-md bg-surface-elevated border border-red-200 text-status-critical font-mono font-semibold">
            {highCount} Critical Escalations
          </span>
          <span className="px-2.5 py-1 rounded-md bg-surface-elevated border border-amber-200 text-status-warning font-mono font-semibold">
            {medCount} Watchlist Warnings
          </span>
        </div>
      </div>

      {actionSuccess && (
        <div className="p-3 rounded-lg bg-surface-elevated border border-emerald-300 text-emerald-800 text-xs font-semibold flex items-center gap-2 shadow-xs">
          <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" aria-hidden="true" />
          <span>{actionSuccess}</span>
        </div>
      )}

      {/* Severity & Status Filters */}
      <AlertsFilterBar
        severityFilter={severityFilter}
        setSeverityFilter={setSeverityFilter}
        statusFilter={statusFilter}
        setStatusFilter={setStatusFilter}
      />

      {/* Main Content: Skeleton, Empty, or Chunked List */}
      {loading ? (
        <div className="space-y-4">
          <LoadingSkeleton type="kpi" />
          <LoadingSkeleton type="table" count={5} />
        </div>
      ) : alerts.length === 0 ? (
        <EmptyState
          title="No Active Escalation Alerts"
          description="There are currently no early-warning threshold triggers for the selected filter combination."
          icon="check"
          action={
            <button
              onClick={() => { setSeverityFilter('All'); setStatusFilter('All'); }}
              className="btn-primary text-xs"
            >
              Reset Alert Filters
            </button>
          }
        />
      ) : (
        <div className="space-y-4">
          <div className="space-y-3">
            {alerts.map((a) => (
              <AlertCardItem key={a.alert_id} alert={a} onReview={handleReview} />
            ))}
          </div>

          {/* Chunked Pagination (30 items at once) */}
          <AlertsPagination
            page={page}
            totalCount={totalCount}
            chunkSize={CHUNK_SIZE}
            setPage={setPage}
          />
        </div>
      )}
    </div>
  );
};

export default AlertsPage;
