import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Compass, Trash2 } from 'lucide-react';
import { getProjects, getFilterOptions, deleteProject, clearAllProjects } from '../api/client';
import LoadingSkeleton from '../components/LoadingSkeleton';
import EmptyState from '../components/EmptyState';
import { ExplorerFilters } from '../components/explorer/ExplorerFilters';
import { ExplorerTable } from '../components/explorer/ExplorerTable';
import { ExplorerPagination } from '../components/explorer/ExplorerPagination';
import PurgeConfirmModal from '../components/explorer/PurgeConfirmModal';
import StatusModal from '../components/StatusModal';

export const ExplorerPage = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [isPurgeOpen, setIsPurgeOpen] = useState(false);
  const [isPurging, setIsPurging] = useState(false);
  const [statusModal, setStatusModal] = useState({ isOpen: false, type: 'success', title: '', message: '' });

  const [search, setSearch] = useState(searchParams.get('search') || '');
  const [ministry, setMinistry] = useState(searchParams.get('ministry') || 'All');
  const [sector, setSector] = useState(searchParams.get('sector') || 'All');
  const [status, setStatus] = useState(searchParams.get('status') || 'All');
  const [riskLevel, setRiskLevel] = useState(searchParams.get('risk_level') || 'All');
  const [sortBy, setSortBy] = useState('score');
  const [sortOrder, setSortOrder] = useState('desc');
  const [page, setPage] = useState(0);
  const pageSize = 30;

  const [filterOptions, setFilterOptions] = useState({ ministries: [], sectors: [] });
  const [projects, setProjects] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getFilterOptions().then(res => setFilterOptions(res || { ministries: [], sectors: [] })).catch(console.error);
  }, []);

  useEffect(() => {
    const fetchFilteredProjects = async () => {
      try {
        setLoading(true);
        const params = {
          search: search || undefined,
          ministry: ministry !== 'All' ? ministry : undefined,
          sector: sector !== 'All' ? sector : undefined,
          status: status !== 'All' ? status : undefined,
          risk_level: riskLevel !== 'All' ? riskLevel : undefined,
          sort_by: sortBy, sort_order: sortOrder, limit: pageSize, offset: page * pageSize
        };
        const res = await getProjects(params);
        setProjects(res.projects || []);
        setTotal(res.total || 0);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchFilteredProjects();
  }, [search, ministry, sector, status, riskLevel, sortBy, sortOrder, page]);

  const handleResetFilters = () => {
    setSearch(''); setMinistry('All'); setSector('All'); setStatus('All');
    setRiskLevel('All'); setSortBy('score'); setSortOrder('desc'); setPage(0);
    setSearchParams({});
  };

  const handleDeleteProject = async (projectId, projectName) => {
    if (!window.confirm(`Are you sure you want to delete "${projectName}" (${projectId})?`)) return;
    try {
      await deleteProject(projectId);
      setProjects(prev => prev.filter(p => p.project_id !== projectId));
      setTotal(prev => Math.max(0, prev - 1));
      setStatusModal({
        isOpen: true,
        type: 'success',
        title: 'Project Deleted',
        message: `Project "${projectName}" has been permanently removed.`
      });
    } catch (err) {
      setStatusModal({
        isOpen: true,
        type: 'error',
        title: 'Delete Failed',
        message: err?.response?.data?.detail || err?.message || 'Failed to delete project.'
      });
    }
  };

  const handleConfirmPurge = async () => {
    try {
      setIsPurging(true);
      await clearAllProjects();
      setProjects([]);
      setTotal(0);
      setIsPurgeOpen(false);
      setStatusModal({
        isOpen: true,
        type: 'success',
        title: 'Database Purged',
        message: 'All projects and telemetry purged successfully.'
      });
    } catch (err) {
      setStatusModal({
        isOpen: true,
        type: 'error',
        title: 'Purge Failed',
        message: err?.response?.data?.detail || err?.response?.data?.message || err?.message || 'Failed to purge projects.'
      });
    } finally {
      setIsPurging(false);
    }
  };

  const totalPages = Math.ceil(total / pageSize);

  return (
    <div className="p-3 sm:p-6 space-y-4 sm:space-y-6 max-w-7xl mx-auto animate-fade-in">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 sm:gap-4 border-b border-border-rest pb-3">
        <div>
          <h1 className="text-lg sm:text-xl font-extrabold text-text-primary tracking-tight flex items-center gap-2">
            <Compass className="w-5 h-5 text-primary-sovereign shrink-0" aria-hidden="true" />
            <span>Central Sector Project Directory</span>
          </h1>
        </div>
        <div className="flex items-center gap-2 flex-wrap">
          <button onClick={() => setIsPurgeOpen(true)} aria-label="Purge all project records" className="px-2.5 py-1.5 rounded-lg text-xs font-semibold text-status-critical bg-red-50 hover:bg-status-critical hover:text-white border border-red-200 transition-colors flex items-center gap-1.5 cursor-pointer">
            <Trash2 className="w-3.5 h-3.5" aria-hidden="true" />
            <span>Purge All</span>
          </button>
        </div>
      </div>

      <ExplorerFilters
        search={search} setSearch={setSearch} ministry={ministry} setMinistry={setMinistry}
        sector={sector} setSector={setSector} status={status} setStatus={setStatus}
        riskLevel={riskLevel} setRiskLevel={setRiskLevel} filterOptions={filterOptions}
        handleResetFilters={handleResetFilters}
      />

      {loading ? (
        <LoadingSkeleton type="table" count={8} />
      ) : projects.length === 0 ? (
        <EmptyState title="No Projects Found" description="Try adjusting search parameters or clear filters." action={<button onClick={handleResetFilters} className="btn-primary text-xs">Reset All Filters</button>} />
      ) : (
        <>
          <ExplorerTable
            projects={projects} sortBy={sortBy} sortOrder={sortOrder}
            setSortBy={setSortBy} setSortOrder={setSortOrder} handleDeleteProject={handleDeleteProject}
          />
          <ExplorerPagination page={page} totalPages={totalPages} total={total} pageSize={pageSize} setPage={setPage} />
        </>
      )}

      <PurgeConfirmModal isOpen={isPurgeOpen} onClose={() => setIsPurgeOpen(false)} onConfirm={handleConfirmPurge} loading={isPurging} />
      <StatusModal
        isOpen={statusModal.isOpen}
        type={statusModal.type}
        title={statusModal.title}
        message={statusModal.message}
        onClose={() => setStatusModal(prev => ({ ...prev, isOpen: false }))}
      />
    </div>
  );
};

export default ExplorerPage;
