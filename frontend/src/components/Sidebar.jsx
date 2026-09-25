import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Compass,
  AlertTriangle,
  FileCheck2,
  ChevronLeft,
  ChevronRight
} from 'lucide-react';

const NAV_ITEMS = [
  {
    to: '/',
    label: 'Portfolio Overview',
    icon: LayoutDashboard,
    badge: null
  },
  {
    to: '/explorer',
    label: 'Central Directory',
    icon: Compass,
    badge: null
  },
  {
    to: '/alerts',
    label: 'Early Warning Alerts',
    icon: AlertTriangle,
    badge: 'Urgent'
  },
  {
    to: '/models',
    label: 'Methodology Audit',
    icon: FileCheck2,
    badge: '95.0%'
  }
];

export const Sidebar = () => {
  const [isCollapsed, setIsCollapsed] = useState(() => {
    try {
      return localStorage.getItem('paimana_sidebar_collapsed') === 'true';
    } catch {
      return false;
    }
  });

  const toggleCollapse = () => {
    setIsCollapsed((prev) => {
      const next = !prev;
      try {
        localStorage.setItem('paimana_sidebar_collapsed', String(next));
      } catch { }
      return next;
    });
  };

  return (
    <aside
      className={`border-r border-border-rest bg-surface-elevated flex flex-col justify-between shrink-0 min-h-[calc(100vh-56px)] z-30 transition-all duration-300 ease-in-out ${isCollapsed ? 'w-16 p-2' : 'w-60 p-4'
        }`}
    >
      <div className="space-y-4">
        {/* Header with Sideways Collapse Toggle */}
        {isCollapsed ? (
          <div className="flex justify-center mb-2">
            <button
              type="button"
              onClick={toggleCollapse}
              className="p-1.5 rounded-lg text-slate-600 hover:text-slate-900 hover:bg-surface-subtle border border-border-rest transition-colors cursor-pointer"
              title="Expand sidebar"
              aria-label="Expand sidebar"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        ) : (
          <div className="flex items-center justify-between px-2 mb-2">
            <span className="text-[10px] font-bold uppercase tracking-wider text-slate-700">
              Administrative Modules
            </span>
            <button
              type="button"
              onClick={toggleCollapse}
              className="p-1 rounded-md text-slate-500 hover:text-slate-900 hover:bg-surface-subtle transition-colors cursor-pointer"
              title="Collapse sidebar"
              aria-label="Collapse sidebar"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
          </div>
        )}

        {/* Navigation Items */}
        <nav className="space-y-1">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                title={isCollapsed ? item.label : undefined}
                className={({ isActive }) =>
                  isCollapsed
                    ? `flex items-center justify-center p-2.5 rounded-lg text-xs font-semibold transition-colors relative ${isActive
                      ? 'bg-surface-subtle text-text-primary border-l-2 border-primary-sovereign rounded-l-none'
                      : 'text-text-secondary hover:text-text-primary hover:bg-surface-subtle'
                    }`
                    : `flex items-center justify-between px-3 py-2 rounded-lg text-xs font-semibold transition-colors ${isActive
                      ? 'bg-surface-subtle text-text-primary border-l-2 border-primary-sovereign rounded-l-none'
                      : 'text-text-secondary hover:text-text-primary hover:bg-surface-subtle'
                    }`
                }
              >
                <div className={`flex items-center ${isCollapsed ? 'justify-center' : 'gap-2.5'}`}>
                  <Icon className="w-4 h-4 text-text-tertiary shrink-0" aria-hidden="true" />
                  {!isCollapsed && <span>{item.label}</span>}
                </div>

                {!isCollapsed && item.badge && (
                  <span
                    className={`text-[10px] font-mono font-medium px-1.5 py-0.2 rounded ${item.badge === 'Urgent'
                        ? 'bg-surface-elevated text-status-critical border border-status-critical/30'
                        : 'bg-surface-subtle text-text-secondary border border-border-rest'
                      }`}
                  >
                    {item.badge}
                  </span>
                )}

                {isCollapsed && item.badge === 'Urgent' && (
                  <span
                    className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-status-critical"
                    title="Urgent alerts"
                  />
                )}
              </NavLink>
            );
          })}
        </nav>
      </div>
    </aside>
  );
};

export default Sidebar;
