import React, { useState, useRef, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  Shield, Sparkles, ChevronDown, UserCheck, Menu,
  Upload, Printer, LogOut, LogIn, Building, KeyRound
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import MobileNavDrawer from './MobileNavDrawer';

export const Header = ({ onOpenAssistant, onOpenImport }) => {
  const navigate = useNavigate();
  const { user, isAuthenticated, logout } = useAuth();
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const dropdownRef = useRef(null);

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

  const isAdmin = user && user.role === 'admin';

  return (
    <header className="sticky top-0 z-40 bg-surface-elevated border-b border-border-rest h-14">
      <div className="max-w-7xl mx-auto px-3 sm:px-6 h-full flex items-center justify-between gap-2 sm:gap-4">
        {/* Left: Mobile Menu Toggle + Identity */}
        <div className="flex items-center gap-1.5 sm:gap-3">
          <button
            type="button"
            onClick={() => setIsMobileMenuOpen(true)}
            className="md:hidden p-1.5 -ml-1 text-slate-700 hover:text-slate-900 hover:bg-slate-100 rounded-lg cursor-pointer"
            aria-label="Open navigation menu"
          >
            <Menu className="w-5 h-5" />
          </button>

          <Link to="/" aria-label="PAIMANA AI Home" className="flex items-center gap-2 sm:gap-3 group">
            <div className="w-8 h-8 rounded-lg bg-primary-sovereign text-white flex items-center justify-center shrink-0 shadow-sm group-hover:bg-blue-900 transition-colors">
              <Shield className="w-4 h-4 text-amber-400" aria-hidden="true" />
            </div>
            <div>
              <div className="flex items-center gap-1.5 sm:gap-2">
                <span className="font-extrabold text-xs sm:text-sm tracking-tight text-text-primary">
                  PAIMANA <span className="text-amber-800 font-bold">AI</span>
                </span>
                <span className="text-[9px] sm:text-[10px] font-bold px-1.5 py-0.2 rounded bg-surface-subtle text-text-secondary font-mono border border-border-rest hidden xs:inline-block">
                  MoSPI / IPMD
                </span>
              </div>
            </div>
          </Link>
        </div>

        {/* Right Actions & Officer Profile */}
        <div className="flex items-center gap-1.5 sm:gap-2.5">
          {isAuthenticated && user ? (
            <div className="relative" ref={dropdownRef}>
              <button
                type="button"
                onClick={() => setIsProfileOpen(!isProfileOpen)}
                className={`flex items-center gap-1.5 sm:gap-2.5 p-1 sm:pl-1.5 sm:pr-3 sm:py-1 rounded-full border transition-all duration-200 cursor-pointer select-none ${
                  isProfileOpen
                    ? 'bg-blue-50/80 border-blue-300 ring-2 ring-blue-500/20'
                    : 'bg-white hover:bg-slate-50 border-slate-200/90 shadow-2xs'
                }`}
                aria-label="Official Session Profile"
                aria-expanded={isProfileOpen}
              >
                <div className="w-7 h-7 rounded-full bg-gradient-to-br from-primary-sovereign via-blue-900 to-indigo-950 text-amber-300 text-[11px] font-bold flex items-center justify-center shadow-xs">
                  {user.avatar || 'GO'}
                </div>
                <div className="hidden sm:block text-left leading-tight max-w-[130px]">
                  <span className="text-[12px] font-semibold text-slate-800 block truncate">
                    {(user?.name || user?.email || 'Officer').split(',')[0]}
                  </span>
                  <span className="text-[10px] text-slate-500 block truncate font-medium">
                    {isAdmin ? 'MoSPI Official' : 'Operations'}
                  </span>
                </div>
                <ChevronDown
                  className={`hidden sm:block w-3.5 h-3.5 text-slate-400 transition-transform duration-200 shrink-0 ${
                    isProfileOpen ? 'rotate-180 text-blue-600' : ''
                  }`}
                  aria-hidden="true"
                />
              </button>

              {/* Profile Dropdown Menu */}
              {isProfileOpen && (
                <div className="absolute right-0 mt-2 w-72 max-w-[90vw] rounded-xl bg-white border border-slate-200 shadow-xl p-3 z-50 animate-fade-in text-slate-800">
                  <div className="border-b border-slate-100 pb-2.5 mb-2">
                    <div className="flex items-center gap-2.5">
                      <div className="w-8 h-8 rounded-lg bg-primary-sovereign text-amber-400 font-bold text-xs flex items-center justify-center shrink-0">
                        {user.avatar || 'GO'}
                      </div>
                      <div className="min-w-0">
                        <p className="text-xs font-bold text-slate-900 truncate">{user.name}</p>
                        <p className="text-[11px] text-slate-600 truncate">{user.designation}</p>
                      </div>
                    </div>
                    <div className="mt-2 pt-1.5 border-t border-slate-100 space-y-1 text-[11px] text-slate-600">
                      <p className="flex items-center gap-1.5 truncate"><Building className="w-3.5 h-3.5 text-slate-400 shrink-0" /><span className="truncate">{user.ministry}</span></p>
                      <p className="flex items-center gap-1.5 font-semibold text-emerald-700"><UserCheck className="w-3.5 h-3.5 text-emerald-600 shrink-0" /><span>{isAdmin ? 'MoSPI Official' : 'Operations Employee'}</span></p>
                    </div>
                  </div>
                  <div className="space-y-1">
                    {isAdmin && (
                      <Link to="/admin" onClick={() => setIsProfileOpen(false)} className="w-full text-left px-2.5 py-1.5 text-xs text-indigo-700 bg-indigo-50/70 hover:bg-indigo-100 rounded-lg flex items-center gap-2 font-semibold">
                        <Shield className="w-3.5 h-3.5 text-indigo-600" /><span>Registry Console</span>
                      </Link>
                    )}
                    <Link to="/login" onClick={() => setIsProfileOpen(false)} className="w-full text-left px-2.5 py-1.5 text-xs text-slate-700 hover:bg-slate-100 rounded-lg flex items-center gap-2">
                      <KeyRound className="w-3.5 h-3.5 text-slate-500" /><span>Switch Account</span>
                    </Link>
                    <button onClick={handleLogout} className="w-full text-left px-2.5 py-1.5 text-xs text-red-600 hover:bg-red-50 rounded-lg flex items-center gap-2 font-medium cursor-pointer">
                      <LogOut className="w-3.5 h-3.5 text-red-500" /><span>Sign Out</span>
                    </button>
                  </div>
                </div>
              )}
            </div>
          ) : (
            <Link
              to="/login"
              className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-white hover:bg-slate-50 border border-slate-200 text-xs text-slate-700 font-semibold shadow-2xs"
            >
              <LogIn className="w-3.5 h-3.5 text-primary-sovereign" />
              <span className="hidden xs:inline">Sign In</span>
            </Link>
          )}

          {/* Quick Action Buttons (Responsive) */}
          <button
            onClick={() => window.print()}
            className="hidden sm:flex btn-secondary text-xs items-center gap-1.5"
            aria-label="Cabinet Briefing"
          >
            <Printer className="w-3.5 h-3.5 text-primary-sovereign" />
            <span>Briefing</span>
          </button>

          <button
            onClick={onOpenImport}
            className="hidden sm:flex btn-secondary text-xs items-center gap-1.5"
            aria-label="Import Report"
          >
            <Upload className="w-3.5 h-3.5 text-primary-sovereign" />
            <span>Import</span>
          </button>

          <button
            onClick={onOpenAssistant}
            className="btn-primary text-xs flex items-center gap-1.5 px-2 sm:px-3 py-1.5"
            aria-label="Open Decision Intelligence Assistant"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Decision Assistant</span>
          </button>
        </div>
      </div>

      {/* Mobile Navigation Drawer */}
      <MobileNavDrawer
        isOpen={isMobileMenuOpen}
        onClose={() => setIsMobileMenuOpen(false)}
        onOpenAssistant={onOpenAssistant}
        onOpenImport={onOpenImport}
      />
    </header>
  );
};

export default Header;
