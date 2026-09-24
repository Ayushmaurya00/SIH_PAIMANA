import React, { useState, useRef, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  Shield,
  Sparkles,
  ChevronDown,
  UserCheck,
  Upload,
  Printer,
  LogOut,
  User,
  LogIn,
  Building,
  KeyRound
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
                onClick={() => setIsProfileOpen(!isProfileOpen)}
                className="hidden sm:flex items-center gap-2 px-2.5 py-1 rounded-md bg-surface-subtle hover:bg-slate-150 border border-border-rest text-xs text-text-secondary font-medium transition-colors"
                aria-label="Official Session Profile"
                aria-expanded={isProfileOpen}
              >
                <div className="w-5 h-5 rounded-full bg-primary-sovereign text-amber-400 text-[10px] font-bold flex items-center justify-center" aria-hidden="true">
                  {user.avatar || 'GO'}
                </div>
                <div className="text-left leading-tight max-w-[140px] truncate">
                  <span className="font-semibold text-text-primary block truncate">
                    {user.name.split(',')[0]}
                  </span>
                </div>
                <ChevronDown className={`w-3 h-3 text-text-tertiary transition-transform ${isProfileOpen ? 'rotate-180' : ''}`} aria-hidden="true" />
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
                        <span className="font-semibold text-emerald-700">{user.role}</span>
                      </p>
                    </div>
                  </div>

                  <div className="space-y-1">
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
              className="hidden sm:flex items-center gap-1.5 px-3 py-1 rounded-md bg-surface-subtle hover:bg-slate-100 border border-border-rest text-xs text-text-primary font-semibold transition-colors"
            >
              <LogIn className="w-3.5 h-3.5 text-primary-sovereign" aria-hidden="true" />
              <span>Officer Sign In</span>
            </Link>
          )}

          {/* Cabinet Briefing (PDF) Button */}
          <button
            onClick={() => window.print()}
            className="btn-secondary text-xs flex items-center gap-1.5"
            aria-label="Print or Export Cabinet Briefing PDF"
          >
            <Printer className="w-3.5 h-3.5 text-primary-sovereign" aria-hidden="true" />
            <span className="hidden sm:inline">Cabinet Briefing</span>
          </button>

          {/* Import Flash Report / Telemetry Button */}
          <button
            onClick={onOpenImport}
            className="btn-secondary text-xs flex items-center gap-1.5"
            aria-label="Import Flash Report PDF or CUF CSV dataset"
          >
            <Upload className="w-3.5 h-3.5 text-primary-sovereign" aria-hidden="true" />
            <span className="hidden sm:inline">Import Report</span>
          </button>

          {/* AI Decision Copilot Button */}
          <button
            onClick={onOpenAssistant}
            className="btn-primary text-xs"
            aria-label="Open Decision Intelligence Assistant"
          >
            <Sparkles className="w-3.5 h-3.5" aria-hidden="true" />
            <span className="hidden sm:inline">Decision Assistant</span>
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;
