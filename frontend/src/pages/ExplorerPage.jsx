import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Compass, Upload, Download, Trash2 } from 'lucide-react';
import { getProjects, getFilterOptions, deleteProject, clearAllProjects, getRiskReportExportUrl } from '../api/client';
import ImportModal from '../components/ImportModal';
import LoadingSkeleton from '../components/LoadingSkeleton';
import EmptyState from '../components/EmptyState';
import { ExplorerFilters } from '../components/explorer/ExplorerFilters';
import { ExplorerTable } from '../components/explorer/ExplorerTable';
import { ExplorerPagination } from '../components/explorer/ExplorerPagination';

export const ExplorerPage = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [isImportOpen, setIsImportOpen] = useState(false);

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
    } catch (err) {
      alert(`Failed to delete project: ${err?.response?.data?.detail || err?.message}`);
    }
  };

  const handleDeleteAllProjects = async () => {
    if (!window.confirm("⚠️ WARNING: Permanently delete ALL projects?")) return;
    const confirmInput = window.prompt("Type 'DELETE' to confirm:")?.trim().toUpperCase();
    if (confirmInput !== 'DELETE' && confirmInput !== 'DELETE ALL') return;
    try {
      await clearAllProjects();
      setProjects([]);
      setTotal(0);
      alert("All projects purged successfully.");
    } catch (err) {
      alert(`Failed to purge projects: ${err?.response?.data?.detail || err?.response?.data?.message || err?.message}`);
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
          <button onClick={() => setIsImportOpen(true)} aria-label="Import Flash Report or Telemetry" className="btn-secondary text-xs flex items-center gap-1.5">
            <Upload className="w-3.5 h-3.5 text-primary-sovereign" aria-hidden="true" />
            <span>Import Report</span>
          </button>
          <button onClick={() => window.open(getRiskReportExportUrl(), '_blank')} aria-label="Export Project Risk Report CSV" className="btn-secondary text-xs flex items-center gap-1.5">
            <Download className="w-3.5 h-3.5" aria-hidden="true" />
            <span>Export CSV</span>
          </button>
          <button onClick={handleDeleteAllProjects} aria-label="Purge all project records" className="px-2.5 py-1.5 rounded-lg text-xs font-semibold text-status-critical bg-red-50 hover:bg-status-critical hover:text-white border border-red-200 transition-colors flex items-center gap-1.5">
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

      <ImportModal isOpen={isImportOpen} onClose={() => setIsImportOpen(false)} onImportSuccess={() => window.location.reload()} />
    </div>
  );
};

export default ExplorerPage;
