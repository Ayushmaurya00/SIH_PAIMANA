import React from 'react';
import { UserCheck, UserX, Shield, Briefcase } from 'lucide-react';

export const PersonnelRosterTable = ({
  users = [],
  loading = false,
  togglingId = null,
  onToggleStatus,
  currentAdminEmail = '',
}) => {
  const getBadgeStyle = (role) => {
    switch (role) {
      case 'admin':
        return {
          label: 'MoSPI Registry Official',
          classes: 'bg-indigo-50 text-indigo-700 border-indigo-200',
          icon: Shield,
        };
      case 'employee':
      default:
        return {
          label: 'Operations Employee',
          classes: 'bg-emerald-50 text-emerald-700 border-emerald-200',
          icon: Briefcase,
        };
    }
  };

  return (
    <div className="overflow-x-auto bg-white rounded-xl border border-slate-200 shadow-2xs">
      <table className="w-full text-left border-collapse text-xs">
        <thead>
          <tr className="bg-slate-50 border-b border-slate-200 text-slate-600 font-semibold uppercase tracking-wider text-[11px]">
            <th className="py-3 px-4">Official Name</th>
            <th className="py-3 px-4">Official Email</th>
            <th className="py-3 px-4">Ministry / Department</th>
            <th className="py-3 px-4">Designation Badge</th>
            <th className="py-3 px-4 text-center">Status</th>
            <th className="py-3 px-4 text-right">Statutory Action</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100 text-slate-800">
          {loading ? (
            <tr>
              <td colSpan="6" className="py-8 text-center text-slate-500 font-medium">
                Loading official registry roster...
              </td>
            </tr>
          ) : users.length === 0 ? (
            <tr>
              <td colSpan="6" className="py-8 text-center text-slate-500">
                No personnel found matching the criteria.
              </td>
            </tr>
          ) : (
            users.map((user) => {
              const badge = getBadgeStyle(user.role);
              const BadgeIcon = badge.icon;
              const isSelf =
                currentAdminEmail &&
                user.email.toLowerCase() === currentAdminEmail.toLowerCase();
              const isBusy = togglingId === user.id;

              return (
                <tr
                  key={user.id}
                  className="hover:bg-slate-50/80 transition-colors"
                >
                  <td className="py-3 px-4 font-bold text-slate-900 whitespace-nowrap">
                    <div className="flex items-center gap-2">
                      <div className="w-6 h-6 rounded-full bg-slate-200 text-slate-700 text-[10px] font-bold flex items-center justify-center shrink-0">
                        {user.full_name
                          .split(' ')
                          .slice(0, 2)
                          .map((n) => n[0])
                          .join('')
                          .toUpperCase() || 'OF'}
                      </div>
                      <span>{user.full_name}</span>
                    </div>
                  </td>
                  <td className="py-3 px-4 font-mono text-[11px] text-slate-600">
                    {user.email}
                  </td>
                  <td className="py-3 px-4 text-slate-700 max-w-[220px] truncate" title={user.department}>
                    {user.department}
                  </td>
                  <td className="py-3 px-4 whitespace-nowrap">
                    <span
                      className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-bold border ${badge.classes}`}
                    >
                      <BadgeIcon className="w-3 h-3 shrink-0" aria-hidden="true" />
                      <span>{badge.label}</span>
                    </span>
                  </td>
                  <td className="py-3 px-4 text-center whitespace-nowrap">
                    <span
                      className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-md text-[10px] font-bold uppercase ${
                        user.is_active
                          ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                          : 'bg-red-50 text-red-700 border border-red-200'
                      }`}
                    >
                      <span
                        className={`w-1.5 h-1.5 rounded-full ${
                          user.is_active ? 'bg-emerald-500' : 'bg-red-500'
                        }`}
                      />
                      <span>{user.is_active ? 'Active' : 'Suspended'}</span>
                    </span>
                  </td>
                  <td className="py-3 px-4 text-right whitespace-nowrap">
                    <button
                      type="button"
                      disabled={isBusy || (isSelf && user.is_active)}
                      onClick={() => onToggleStatus(user)}
                      title={
                        isSelf && user.is_active
                          ? 'Self-suspension disabled'
                          : user.is_active
                          ? 'Suspend official credentials'
                          : 'Activate official credentials'
                      }
                      className={`inline-flex items-center gap-1 px-3 py-1 rounded-md text-xs font-semibold transition-all cursor-pointer border ${
                        user.is_active
                          ? 'bg-white hover:bg-red-50 text-red-600 border-red-200 hover:border-red-300 disabled:opacity-40'
                          : 'bg-emerald-600 hover:bg-emerald-700 text-white border-emerald-600 disabled:opacity-40'
                      }`}
                    >
                      {user.is_active ? (
                        <>
                          <UserX className="w-3.5 h-3.5" aria-hidden="true" />
                          <span>{isBusy ? 'Updating...' : 'Suspend'}</span>
                        </>
                      ) : (
                        <>
                          <UserCheck className="w-3.5 h-3.5" aria-hidden="true" />
                          <span>{isBusy ? 'Updating...' : 'Activate'}</span>
                        </>
                      )}
                    </button>
                  </td>
                </tr>
              );
            })
          )}
        </tbody>
      </table>
    </div>
  );
};

export default PersonnelRosterTable;
