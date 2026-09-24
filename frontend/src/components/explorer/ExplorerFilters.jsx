import React from 'react';
import { Search, RotateCcw } from 'lucide-react';

export const ExplorerFilters = ({
  search, setSearch,
  ministry, setMinistry,
  sector, setSector,
  status, setStatus,
  riskLevel, setRiskLevel,
  filterOptions,
  handleResetFilters
}) => {
  return (
    <div className="bg-surface-elevated p-4 rounded-xl border border-border-rest shadow-xs space-y-3">
      <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
        {/* Search Field */}
        <div className="md:col-span-2 relative">
          <Search className="w-4 h-4 text-text-tertiary absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search by project name, ID (e.g. PRJ-00042)..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-9 pr-3 py-2 text-xs bg-surface-subtle border border-border-rest rounded-lg text-text-primary placeholder-text-tertiary focus:outline-hidden focus:ring-1 focus:ring-primary-sovereign"
          />
        </div>

        {/* Ministry Filter */}
        <div>
          <select
            value={ministry}
            onChange={(e) => setMinistry(e.target.value)}
            className="w-full text-xs py-2 px-2.5 bg-surface-subtle border border-border-rest rounded-lg text-text-primary focus:outline-hidden focus:ring-1 focus:ring-primary-sovereign"
          >
            <option value="All">All Ministries</option>
            {filterOptions.ministries?.map((m) => (
              <option key={m} value={m}>{m}</option>
            ))}
          </select>
        </div>

        {/* Sector Filter */}
        <div>
          <select
            value={sector}
            onChange={(e) => setSector(e.target.value)}
            className="w-full text-xs py-2 px-2.5 bg-surface-subtle border border-border-rest rounded-lg text-text-primary focus:outline-hidden focus:ring-1 focus:ring-primary-sovereign"
          >
            <option value="All">All Sectors</option>
            {filterOptions.sectors?.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
        </div>

        {/* Risk Level Filter */}
        <div>
          <select
            value={riskLevel}
            onChange={(e) => setRiskLevel(e.target.value)}
            className="w-full text-xs py-2 px-2.5 bg-surface-subtle border border-border-rest rounded-lg text-text-primary focus:outline-hidden focus:ring-1 focus:ring-primary-sovereign"
          >
            <option value="All">All Risk Levels</option>
            <option value="Critical">Critical Risk (70-100)</option>
            <option value="High">High Risk (50-69)</option>
            <option value="Medium">Medium Risk (30-49)</option>
            <option value="Low">Low Risk (0-29)</option>
          </select>
        </div>
      </div>

      <div className="flex items-center justify-between pt-1 text-xs text-text-tertiary">
        <div className="flex items-center gap-2">
          <span>Status:</span>
          {['All', 'On Track', 'Delayed', 'Stalled', 'Completed'].map((st) => (
            <button
              key={st}
              type="button"
              onClick={() => setStatus(st)}
              className={`px-2 py-0.5 rounded-md text-[11px] font-semibold transition-colors ${
                status === st
                  ? 'bg-primary-sovereign text-white'
                  : 'bg-surface-subtle hover:bg-surface-elevated text-text-secondary border border-border-rest'
              }`}
            >
              {st}
            </button>
          ))}
        </div>

        <button
          type="button"
          onClick={handleResetFilters}
          className="flex items-center gap-1 hover:text-text-primary transition-colors text-xs font-medium"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          <span>Reset Filters</span>
        </button>
      </div>
    </div>
  );
};

export default ExplorerFilters;
