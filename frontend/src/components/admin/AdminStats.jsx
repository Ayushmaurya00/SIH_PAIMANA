import React from 'react';
import { Users, UserCheck, Building2, ShieldCheck } from 'lucide-react';

export const AdminStats = ({ users = [] }) => {
  const totalUsers = users.length;
  const activeUsers = users.filter((u) => u.is_active).length;
  const uniqueDepartments = new Set(
    users.map((u) => u.department).filter(Boolean)
  ).size;

  const stats = [
    {
      label: 'Total Registered Accounts',
      value: totalUsers,
      subtext: 'Central Sovereign Directory',
      icon: Users,
      color: 'text-indigo-600 bg-indigo-50 border-indigo-200',
    },
    {
      label: 'Active Field Officers',
      value: activeUsers,
      subtext: `${totalUsers - activeUsers} Suspended Credentials`,
      icon: UserCheck,
      color: 'text-emerald-600 bg-emerald-50 border-emerald-200',
    },
    {
      label: 'Assigned Ministerial Desks',
      value: uniqueDepartments,
      subtext: 'Cross-Sector Infrastructure Wings',
      icon: Building2,
      color: 'text-blue-600 bg-blue-50 border-blue-200',
    },
    {
      label: 'Registry Governance',
      value: 'Level-5',
      subtext: 'Cabinet Secretariat Clearance',
      icon: ShieldCheck,
      color: 'text-amber-600 bg-amber-50 border-amber-200',
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {stats.map((stat, idx) => {
        const IconComponent = stat.icon;
        return (
          <div
            key={idx}
            className="p-4 rounded-xl bg-white border border-slate-200 shadow-2xs hover:shadow-xs transition-shadow"
          >
            <div className="flex items-center justify-between gap-3">
              <div>
                <p className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">
                  {stat.label}
                </p>
                <p className="text-2xl font-black text-slate-900 mt-1">
                  {stat.value}
                </p>
                <p className="text-[11px] text-slate-500 font-medium mt-0.5">
                  {stat.subtext}
                </p>
              </div>
              <div
                className={`w-10 h-10 rounded-lg flex items-center justify-center shrink-0 border ${stat.color}`}
              >
                <IconComponent className="w-5 h-5" aria-hidden="true" />
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default AdminStats;
