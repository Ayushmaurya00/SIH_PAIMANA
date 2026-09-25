import React, { useState, useRef, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  Shield, Sparkles, ChevronDown, UserCheck,
  Upload, Printer, LogOut, LogIn, Building, KeyRound
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const Header = ({ onOpenAssistant, onOpenImport, alertCount = 0 }) => {
  const navigate = useNavigate();
  const { user, isAuthenticated, logout } = useAuth();
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const dropdownRef = useRef(null);

  // Close dropdown on outside click
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsProfileOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleLogout = () => {
    logout();
    setIsProfileOpen(false);
    navigate('/login');
  };

  return (
    <header className="sticky top-0 z-40 bg-surface-elevated border-b border-border-rest h-14">
      <div className="max-w-7xl mx-auto px-6 h-full flex items-center justify-between gap-4">
        {/* Identity & Department Badge */}
        <Link to="/" aria-label="PAIMANA AI Home" className="flex items-center gap-3 group">
          <div className="w-8 h-8 rounded-lg bg-primary-sovereign text-white flex items-center justify-center shrink-0 shadow-sm group-hover:bg-blue-900 transition-colors">
            <Shield className="w-4 h-4 text-amber-400" aria-hidden="true" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold text-sm tracking-tight text-text-primary">
                PAIMANA <span className="text-amber-800 font-bold">AI</span>
              </span>
              <span className="text-[10px] font-bold px-1.5 py-0.2 rounded bg-surface-subtle text-text-secondary font-mono border border-border-rest">
                MoSPI / IPMD
              </span>
            </div>
          </div>
        </Link>

        {/* Right Actions & Official Role Selector */}
        <div className="flex items-center gap-2.5">
          {/* Official Officer Profile Dropdown */}
          {isAuthenticated && user ? (
            <div className="relative" ref={dropdownRef}>
              <button
                type="button"
                onClick={() => setIsProfileOpen(!isProfileOpen)}
                className={`hidden sm:flex items-center gap-2.5 pl-1.5 pr-3 py-1 rounded-full border transition-all duration-200 cursor-pointer group select-none ${isProfileOpen
                  ? 'bg-blue-50/80 border-blue-300 shadow-xs ring-2 ring-blue-500/20'
                  : 'bg-white hover:bg-slate-50 border-slate-200/90 shadow-2xs hover:shadow-xs hover:border-slate-300'
                  }`}
                aria-label="Official Session Profile"
                aria-expanded={isProfileOpen}
              >
                <div className="relative shrink-0">
                  <div className="w-7 h-7 rounded-full bg-gradient-to-br from-primary-sovereign via-blue-900 to-indigo-950 text-amber-300 text-[11px] font-bold flex items-center justify-center shadow-xs ring-1.5 ring-white">
                    {user.avatar || 'GO'}
                  </div>
                  {/* <span className="absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 rounded-full bg-emerald-500 ring-2 ring-white" title="Active session" /> */}
                </div>
                <div className="text-left leading-tight max-w-[130px]">
                  <span className="text-[12px] font-semibold text-slate-800 group-hover:text-primary-sovereign block truncate transition-colors">
                    {user.name.split(',')[0]}
                  </span>
                  <span className="text-[10px] text-slate-500 block truncate font-medium">
                    {user.role === 'admin' ? 'MoSPI Registry Official' : (user.role === 'auditor' ? 'Read-Only Auditor' : (user.role === 'nodal_officer' ? 'Nodal Desk Officer' : user.role || 'Officer'))}
                  </span>
                </div>
                <ChevronDown
                  className={`w-3.5 h-3.5 text-slate-400 group-hover:text-slate-600 transition-transform duration-200 shrink-0 ${isProfileOpen ? 'rotate-180 text-blue-600' : ''}`}
                  aria-hidden="true"
                />
              </button>

              {/* Profile Dropdown Menu */}
              {isProfileOpen && (
                <div className="absolute right-0 mt-2 w-72 rounded-xl bg-white border border-slate-200 shadow-xl p-3 z-50 animate-fade-in text-slate-800">
                  <div className="border-b border-slate-100 pb-3 mb-2">
                    <div className="flex items-center gap-2.5">
                      <div className="w-9 h-9 rounded-lg bg-primary-sovereign text-amber-400 font-black text-xs flex items-center justify-center shrink-0" aria-hidden="true">
                        {user.avatar || 'GO'}
                      </div>
                      <div className="min-w-0">
                        <p className="text-xs font-bold text-slate-900 truncate">{user.name}</p>
                        <p className="text-[11px] text-slate-600 truncate">{user.designation}</p>
                      </div>
                    </div>

                    <div className="mt-2.5 pt-2 border-t border-slate-100/80 space-y-1 text-[11px] text-slate-600">
                      <p className="flex items-center gap-1.5 truncate">
                        <Building className="w-3.5 h-3.5 text-slate-400 shrink-0" aria-hidden="true" />
                        <span className="truncate">{user.ministry}</span>
                      </p>
                      <p className="flex items-center gap-1.5">
                        <UserCheck className="w-3.5 h-3.5 text-emerald-600 shrink-0" aria-hidden="true" />
                        <span className="font-semibold text-emerald-700">
                          {user.role === 'admin' ? 'MoSPI Registry Official' : (user.role === 'auditor' ? 'Read-Only Auditor' : (user.role === 'nodal_officer' ? 'Nodal Desk Officer' : user.role))}
                        </span>
                      </p>
                    </div>
                  </div>

                  <div className="space-y-1">
                    {user.role === 'admin' && (
                      <Link
                        to="/admin"
                        onClick={() => setIsProfileOpen(false)}
                        className="w-full text-left px-2.5 py-1.5 text-xs text-indigo-700 bg-indigo-50/70 hover:bg-indigo-100 rounded-lg flex items-center gap-2 transition-colors font-semibold"
                      >
                        <Shield className="w-3.5 h-3.5 text-indigo-600" aria-hidden="true" />
                        <span>Registry Console</span>
                      </Link>
                    )}

                    <Link
                      to="/login"
                      onClick={() => setIsProfileOpen(false)}
                      className="w-full text-left px-2.5 py-1.5 text-xs text-slate-700 hover:bg-slate-100 rounded-lg flex items-center gap-2 transition-colors"
                    >
                      <KeyRound className="w-3.5 h-3.5 text-slate-500" aria-hidden="true" />
                      <span>Switch Officer Account</span>
                    </Link>

                    <button
                      onClick={handleLogout}
                      className="w-full text-left px-2.5 py-1.5 text-xs text-red-600 hover:bg-red-50 rounded-lg flex items-center gap-2 transition-colors font-medium"
                    >
                      <LogOut className="w-3.5 h-3.5 text-red-500" aria-hidden="true" />
                      <span>Sign Out</span>
                    </button>
                  </div>
                </div>
              )}
            </div>
          ) : (
            <Link
              to="/login"
              className="hidden sm:flex items-center gap-2 pl-1.5 pr-3 py-1 rounded-full bg-white hover:bg-slate-50 border border-slate-200/90 shadow-2xs hover:shadow-xs hover:border-slate-300 text-xs text-slate-700 font-semibold transition-all duration-200 group"
            >
              <div className="w-6 h-6 rounded-full bg-slate-100 group-hover:bg-blue-50 text-slate-600 group-hover:text-primary-sovereign flex items-center justify-center transition-colors">
                <LogIn className="w-3.5 h-3.5" aria-hidden="true" />
              </div>
              <span>Officer Sign In</span>
            </Link>
          )}

          {/* Action Buttons */}
          <button onClick={() => window.print()} className="btn-secondary text-xs flex items-center gap-1.5" aria-label="Print or Export Cabinet Briefing PDF">
            <Printer className="w-3.5 h-3.5 text-primary-sovereign" aria-hidden="true" />
            <span className="hidden sm:inline">Cabinet Briefing</span>
          </button>

          <button onClick={onOpenImport} className="btn-secondary text-xs flex items-center gap-1.5" aria-label="Import Flash Report PDF or CUF CSV dataset">
            <Upload className="w-3.5 h-3.5 text-primary-sovereign" aria-hidden="true" />
            <span className="hidden sm:inline">Import Report</span>
          </button>

          <button onClick={onOpenAssistant} className="btn-primary text-xs" aria-label="Open Decision Intelligence Assistant">
            <Sparkles className="w-3.5 h-3.5" aria-hidden="true" />
            <span className="hidden sm:inline">Decision Assistant</span>
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;
