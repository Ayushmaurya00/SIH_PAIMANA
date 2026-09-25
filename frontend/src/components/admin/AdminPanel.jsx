import React, { useState, useEffect } from 'react';
import { Shield, UserPlus, Search, RefreshCw, CheckCircle2 } from 'lucide-react';
import { getAdminUsers, toggleUserStatus } from '../../api/client';
import { useAuth } from '../../context/AuthContext';
import AdminStats from './AdminStats';
import PersonnelRosterTable from './PersonnelRosterTable';
import ProvisionOfficerModal from './ProvisionOfficerModal';

export const AdminPanel = () => {
  const { user: currentOfficer } = useAuth();
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [roleFilter, setRoleFilter] = useState('all');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [togglingId, setTogglingId] = useState(null);
  const [notification, setNotification] = useState(null);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const data = await getAdminUsers();
      setUsers(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error('Failed to load personnel roster:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleToggleStatus = async (targetUser) => {
    try {
      setTogglingId(targetUser.id);
      const res = await toggleUserStatus(targetUser.id);
      if (res && res.status === 'success') {
        setUsers((prev) =>
          prev.map((u) => (u.id === targetUser.id ? { ...u, is_active: res.is_active } : u))
        );
        showNotification(res.message);
      }
    } catch (err) {
      const msg = err?.response?.data?.message || 'Failed to update user status.';
      alert(msg);
    } finally {
      setTogglingId(null);
    }
  };

  const showNotification = (msg) => {
    setNotification(msg);
    setTimeout(() => setNotification(null), 5000);
  };

  const filteredUsers = users.filter((u) => {
    const matchesSearch =
      (u.full_name || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
      (u.email || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
      (u.department || '').toLowerCase().includes(searchTerm.toLowerCase());
    const matchesRole = roleFilter === 'all' || u.role === roleFilter;
    return matchesSearch && matchesRole;
  });

  return (
    <div className="p-6 space-y-6 max-w-7xl mx-auto animate-fade-in text-slate-800">
      {/* Header Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 pb-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-indigo-50 text-indigo-700 border border-indigo-200">
              MoSPI / Central Registry
            </span>
            <span className="text-xs text-slate-500 font-medium">RBAC Security Tier</span>
          </div>
          <h1 className="text-xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
            <Shield className="w-5 h-5 text-indigo-700" aria-hidden="true" />
            <span>MoSPI Central Registry | Sovereign Administration Console</span>
          </h1>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={fetchUsers}
            disabled={loading}
            className="p-2 rounded-lg border border-slate-300 hover:bg-slate-50 text-slate-700 text-xs font-semibold flex items-center gap-1.5 transition-colors"
            title="Refresh Roster"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            <span className="hidden sm:inline">Refresh</span>
          </button>
          <button
            onClick={() => setIsModalOpen(true)}
            className="px-3.5 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold flex items-center gap-1.5 shadow-xs transition-colors"
          >
            <UserPlus className="w-3.5 h-3.5" aria-hidden="true" />
            <span>Provision Officer Credentials</span>
          </button>
        </div>
      </div>

      {notification && (
        <div className="p-3 rounded-lg bg-emerald-50 border border-emerald-300 text-emerald-800 text-xs font-semibold flex items-center gap-2 shadow-2xs">
          <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" aria-hidden="true" />
          <span>{notification}</span>
        </div>
      )}

      {/* Overview Stat Cards */}
      <AdminStats users={users} />

      {/* Roster Controls & Filters */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pt-2">
        <div className="relative max-w-sm w-full">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Search by name, email, or department..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 text-xs rounded-lg border border-slate-300 bg-white focus:ring-2 focus:ring-indigo-600 focus:outline-none"
          />
        </div>

        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold text-slate-500">Filter Role:</span>
          <select
            value={roleFilter}
            onChange={(e) => setRoleFilter(e.target.value)}
            className="text-xs py-1.5 px-3 rounded-lg border border-slate-300 bg-white focus:ring-2 focus:ring-indigo-600 focus:outline-none"
          >
            <option value="all">All Statutory Clearances</option>
            <option value="admin">MoSPI Registry Official</option>
            <option value="nodal_officer">Nodal Desk Officer</option>
            <option value="auditor">Read-Only Auditor</option>
          </select>
        </div>
      </div>

      {/* Personnel Roster Table */}
      <PersonnelRosterTable
        users={filteredUsers}
        loading={loading}
        togglingId={togglingId}
        onToggleStatus={handleToggleStatus}
        currentAdminEmail={currentOfficer?.email || ''}
      />

      {/* Provision Officer Modal */}
      <ProvisionOfficerModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSuccess={(msg) => {
          showNotification(msg);
          fetchUsers();
        }}
      />
    </div>
  );
};

export default AdminPanel;
