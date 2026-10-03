import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import {
  X, LayoutDashboard, Compass, AlertTriangle, FileCheck2,
  Shield, Building, UserCheck, KeyRound, LogOut, Upload, Printer, Sparkles
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const MobileNavDrawer = ({
  isOpen,
  onClose,
  onOpenAssistant,
  onOpenImport
}) => {
  const navigate = useNavigate();
  const { user, isAuthenticated, logout } = useAuth();
  const isAdmin = user && user.role === 'admin';

  if (!isOpen) return null;

  const handleNavClick = () => {
    onClose();
  };

  const handleLogout = () => {
    logout();
    onClose();
    navigate('/login');
  };

  const navLinks = [
    { to: '/', label: 'Portfolio Overview', icon: LayoutDashboard },
    { to: '/explorer', label: 'Central Directory', icon: Compass },
    { to: '/alerts', label: 'Early Warning Alerts', icon: AlertTriangle, badge: 'Urgent' },
    { to: '/models', label: 'Methodology Audit', icon: FileCheck2 },
    ...(isAdmin ? [{ to: '/admin', label: 'Registry Console', icon: Shield, badge: 'Admin' }] : []),
  ];

  return (
    <div className="fixed inset-0 z-50 md:hidden flex" role="dialog" aria-modal="true">
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-slate-950/50 backdrop-blur-xs transition-opacity animate-fade-in"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Drawer */}
      <div className="relative w-80 max-w-[85vw] bg-white h-full shadow-2xl flex flex-col justify-between z-10 animate-slide-in-left overflow-y-auto">
        <div className="p-4 space-y-4">
          {/* Header */}
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-lg bg-primary-sovereign text-white flex items-center justify-center shadow-xs">
                <Shield className="w-4 h-4 text-amber-400" aria-hidden="true" />
              </div>
              <div>
                <span className="font-extrabold text-sm tracking-tight text-slate-900 block">
                  PAIMANA <span className="text-amber-700">AI</span>
                </span>
                <span className="text-[10px] text-slate-500 font-mono font-semibold">MoSPI / IPMD</span>
              </div>
            </div>
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-slate-500 hover:text-slate-900 hover:bg-slate-100 cursor-pointer"
              aria-label="Close navigation"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* User Profile Card */}
          {isAuthenticated && user && (
            <div className="p-3 rounded-xl bg-slate-50 border border-slate-200/80 space-y-2">
              <div className="flex items-center gap-2.5">
                <div className="w-9 h-9 rounded-full bg-gradient-to-br from-primary-sovereign to-indigo-950 text-amber-300 text-xs font-bold flex items-center justify-center shrink-0 shadow-xs">
                  {user.avatar || 'GO'}
                </div>
                <div className="min-w-0 flex-1">
                  <p className="text-xs font-bold text-slate-900 truncate">
                    {(user?.name || user?.email || 'Officer').split(',')[0]}
                  </p>
                  <p className="text-[11px] text-slate-600 truncate">{user.designation || 'Operations'}</p>
                </div>
              </div>
              <div className="pt-2 border-t border-slate-200/60 flex items-center justify-between text-[11px]">
                <span className="font-semibold text-emerald-700 flex items-center gap-1">
                  <UserCheck className="w-3.5 h-3.5" />
                  {isAdmin ? 'MoSPI Official' : 'Operations Employee'}
                </span>
              </div>
            </div>
          )}

          {/* Navigation Links */}
          <nav className="space-y-1">
            <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500 px-2 block mb-1">
              Modules
            </span>
            {navLinks.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.to}
                  to={item.to}
                  onClick={handleNavClick}
                  className={({ isActive }) =>
                    `flex items-center justify-between px-3 py-2.5 rounded-lg text-xs font-semibold transition-colors ${
                      isActive
                        ? 'bg-blue-50 text-primary-sovereign border-l-3 border-primary-sovereign font-bold'
                        : 'text-slate-700 hover:bg-slate-100'
                    }`
                  }
                >
                  <div className="flex items-center gap-2.5">
                    <Icon className="w-4 h-4 text-slate-600" />
                    <span>{item.label}</span>
                  </div>
                  {item.badge && (
                    <span className="text-[9px] px-1.5 py-0.5 rounded-full font-bold bg-slate-200 text-slate-700">
                      {item.badge}
                    </span>
                  )}
                </NavLink>
              );
            })}
          </nav>

          {/* Quick Actions */}
          <div className="space-y-1 pt-2 border-t border-slate-100">
            <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500 px-2 block mb-1">
              Operations
            </span>
            <button
              onClick={() => { onOpenAssistant(); onClose(); }}
              className="w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-semibold text-primary-sovereign bg-blue-50/70 hover:bg-blue-100/80 cursor-pointer"
            >
              <Sparkles className="w-4 h-4 text-primary-sovereign" />
              <span>Decision Assistant</span>
            </button>
            <button
              onClick={() => { onOpenImport(); onClose(); }}
              className="w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-semibold text-slate-700 hover:bg-slate-100 cursor-pointer"
            >
              <Upload className="w-4 h-4 text-slate-600" />
              <span>Import Flash Report</span>
            </button>
            <button
              onClick={() => { window.print(); onClose(); }}
              className="w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-semibold text-slate-700 hover:bg-slate-100 cursor-pointer"
            >
              <Printer className="w-4 h-4 text-slate-600" />
              <span>Cabinet Briefing</span>
            </button>
          </div>
        </div>

        {/* Footer Actions */}
        <div className="p-4 border-t border-slate-100 bg-slate-50/60 space-y-1">
          <button
            onClick={() => { onClose(); navigate('/login'); }}
            className="w-full flex items-center gap-2 px-2.5 py-2 text-xs text-slate-700 hover:bg-slate-200/60 rounded-lg cursor-pointer font-medium"
          >
            <KeyRound className="w-4 h-4 text-slate-500" />
            <span>Switch Officer Account</span>
          </button>
          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-2 px-2.5 py-2 text-xs text-red-600 hover:bg-red-50 rounded-lg cursor-pointer font-semibold"
          >
            <LogOut className="w-4 h-4 text-red-500" />
            <span>Sign Out</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default MobileNavDrawer;
