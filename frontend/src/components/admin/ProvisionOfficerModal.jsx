import React, { useState } from 'react';
import { X, KeyRound, ShieldAlert, CheckCircle2, UserPlus } from 'lucide-react';
import { CANONICAL_MINISTRIES } from '../../context/demoProfiles';
import { createAdminUser } from '../../api/client';

export const ProvisionOfficerModal = ({ isOpen, onClose, onSuccess }) => {
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [department, setDepartment] = useState(CANONICAL_MINISTRIES[0]);
  const [role, setRole] = useState('nodal_officer');
  const [tempPassword, setTempPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  if (!isOpen) return null;

  const generatePassword = () => {
    const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789!@#$%&*';
    let pwd = '';
    for (let i = 0; i < 12; i++) {
      pwd += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    setTempPassword(pwd);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    const cleanEmail = email.trim().toLowerCase();
    if (!cleanEmail.endsWith('.gov.in') && !cleanEmail.endsWith('.nic.in') && !cleanEmail.includes('@')) {
      setError('Please provide a valid official government email (e.g. officer@mospi.gov.in).');
      return;
    }
    if (!tempPassword || tempPassword.length < 8) {
      setError('Temporary password must be at least 8 characters long.');
      return;
    }

    try {
      setLoading(true);
      await createAdminUser({
        full_name: fullName.trim(),
        email: cleanEmail,
        department,
        role,
        temporary_password: tempPassword,
      });

      onSuccess(`Credentials provisioned for ${cleanEmail}. Temporary password: ${tempPassword}`);
      onClose();
    } catch (err) {
      const msg = err?.response?.data?.message || err?.response?.data?.detail || 'Failed to provision officer credentials.';
      setError(typeof msg === 'string' ? msg : JSON.stringify(msg));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-xs animate-fade-in">
      <div className="bg-white rounded-2xl border border-slate-200 shadow-2xl max-w-lg w-full overflow-hidden">
        <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <UserPlus className="w-5 h-5 text-indigo-600" aria-hidden="true" />
            <h2 className="text-sm font-bold text-slate-900">Provision Official Credentials</h2>
          </div>
          <button onClick={onClose} className="p-1 rounded-md text-slate-400 hover:text-slate-600 hover:bg-slate-100">
            <X className="w-4 h-4" />
          </button>
        </div>

        {error && (
          <div className="mx-6 mt-4 p-3 rounded-lg bg-red-50 border border-red-200 text-red-700 text-xs font-medium flex items-center gap-2">
            <ShieldAlert className="w-4 h-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="p-6 space-y-4 text-xs">
          <div>
            <label className="block font-semibold text-slate-700 mb-1">Official Full Name & Rank</label>
            <input
              type="text"
              required
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              placeholder="e.g. Smt. Sunita Rao, IRS"
              className="w-full px-3 py-2 border border-slate-300 rounded-lg text-slate-900 focus:ring-2 focus:ring-indigo-600 focus:outline-none"
            />
          </div>

          <div>
            <label className="block font-semibold text-slate-700 mb-1">Official Government Email (@*.gov.in)</label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="officer.name@mospi.gov.in"
              className="w-full px-3 py-2 border border-slate-300 rounded-lg text-slate-900 font-mono focus:ring-2 focus:ring-indigo-600 focus:outline-none"
            />
          </div>

          <div>
            <label className="block font-semibold text-slate-700 mb-1">Assigned Ministry / Sector</label>
            <select
              value={department}
              onChange={(e) => setDepartment(e.target.value)}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg text-slate-900 bg-white focus:ring-2 focus:ring-indigo-600 focus:outline-none"
            >
              {CANONICAL_MINISTRIES.map((m) => (
                <option key={m} value={m}>{m}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block font-semibold text-slate-700 mb-1">Statutory Access Role</label>
            <select
              value={role}
              onChange={(e) => setRole(e.target.value)}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg text-slate-900 bg-white focus:ring-2 focus:ring-indigo-600 focus:outline-none"
            >
              <option value="nodal_officer">Nodal Desk Officer (Operational Oversight & Review)</option>
              <option value="auditor">Read-Only Auditor (Statutory Review & Read-Only Access)</option>
              <option value="admin">MoSPI Registry Official (Full Registry Administration)</option>
            </select>
          </div>

          <div>
            <div className="flex items-center justify-between mb-1">
              <label className="font-semibold text-slate-700">One-Time Temporary Password</label>
              <button
                type="button"
                onClick={generatePassword}
                className="text-[11px] font-bold text-indigo-600 hover:text-indigo-800 flex items-center gap-1"
              >
                <KeyRound className="w-3 h-3" />
                <span>Generate Secure Password</span>
              </button>
            </div>
            <input
              type="text"
              required
              value={tempPassword}
              onChange={(e) => setTempPassword(e.target.value)}
              placeholder="Click Generate or enter temporary password"
              className="w-full px-3 py-2 border border-slate-300 rounded-lg text-slate-900 font-mono tracking-wider focus:ring-2 focus:ring-indigo-600 focus:outline-none"
            />
          </div>

          <div className="pt-2 flex items-center justify-end gap-2 border-t border-slate-100">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-lg border border-slate-300 text-slate-700 hover:bg-slate-50 font-medium"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white font-bold transition-all disabled:opacity-50"
            >
              {loading ? 'Provisioning...' : 'Provision Officer'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ProvisionOfficerModal;
