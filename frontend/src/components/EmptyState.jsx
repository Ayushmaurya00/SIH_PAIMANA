import React from 'react';
import { Inbox, Search, Filter, AlertCircle, RefreshCw } from 'lucide-react';

const ICON_MAP = {
  inbox: Inbox,
  search: Search,
  filter: Filter,
  alert: AlertCircle,
  refresh: RefreshCw
};

export const EmptyState = ({ 
  title = 'No records found',
  description = 'Try adjusting your search criteria or review filters.',
  icon = 'inbox',
  action = null,
  className = ''
}) => {
  const Icon = ICON_MAP[icon] || Inbox;
  
  return (
    <div className={`flex flex-col items-center justify-center py-16 px-4 text-center rounded-xl bg-white border border-slate-200 shadow-xs ${className}`}>
      <div className="w-14 h-14 rounded-full bg-slate-100 border border-slate-200 flex items-center justify-center mb-3.5 shadow-xs">
        <Icon className="w-7 h-7 text-slate-600" aria-hidden="true" />
      </div>
      <h3 className="text-sm font-bold text-gov-navy mb-1">{title}</h3>
      <p className="text-xs text-slate-600 max-w-sm leading-relaxed">{description}</p>
      {action && <div className="mt-4">{action}</div>}
    </div>
  );
};

export default EmptyState;
