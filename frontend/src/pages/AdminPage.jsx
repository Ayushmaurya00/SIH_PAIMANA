import React from 'react';
import { Navigate, Link } from 'react-router-dom';
import { ShieldAlert, ArrowLeft } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import AdminPanel from '../components/admin/AdminPanel';

export const AdminPage = () => {
  const { user, isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // RBAC Guard: Strictly MoSPI Registry Official ('admin')
  const isAdmin = user && user.role === 'admin';

  if (!isAdmin) {
    return (
      <div className="p-8 max-w-2xl mx-auto my-12 bg-white rounded-2xl border border-red-200 shadow-sm text-center space-y-4">
        <div className="w-12 h-12 mx-auto rounded-full bg-red-100 text-red-600 flex items-center justify-center">
          <ShieldAlert className="w-6 h-6" aria-hidden="true" />
        </div>
        <h1 className="text-xl font-bold text-slate-900">
          Statutory Clearance Error (403 Forbidden)
        </h1>
        <p className="text-xs text-slate-600 max-w-md mx-auto leading-relaxed">
          Access to the MoSPI Central Registry Console is restricted to authenticated
          <strong> MoSPI Registry Officials</strong> with Level-5 Cabinet Secretariat statutory clearance.
          Your current account role is <span className="font-mono font-bold text-slate-800">{user?.role || 'Guest'}</span>.
        </p>
        <div className="pt-2">
          <Link
            to="/explorer"
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Return to Central Directory</span>
          </Link>
        </div>
      </div>
    );
  }

  return <AdminPanel />;
};

export default AdminPage;
