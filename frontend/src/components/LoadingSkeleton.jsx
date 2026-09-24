import React from 'react';

export const LoadingSkeleton = ({ type = 'card', count = 3 }) => {
  if (type === 'card') {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {[...Array(count)].map((_, i) => (
          <div key={i} className="bg-white rounded-xl p-5 border border-slate-200 shimmer min-h-[140px]" />
        ))}
      </div>
    );
  }
  
  if (type === 'table') {
    return (
      <div className="space-y-3">
        <div className="h-10 bg-slate-100 rounded-lg shimmer" />
        {[...Array(count)].map((_, i) => (
          <div key={i} className="h-14 bg-slate-50 rounded-lg shimmer border border-slate-200" />
        ))}
      </div>
    );
  }
  
  if (type === 'kpi') {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="bg-white rounded-xl p-5 border border-slate-200 shimmer min-h-[110px]" />
        ))}
      </div>
    );
  }

  if (type === 'detail') {
    return (
      <div className="space-y-6 max-w-7xl mx-auto">
        <div className="h-6 w-32 bg-slate-200 rounded" />
        <div className="h-24 bg-white rounded-xl shimmer border border-slate-200" />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="h-24 bg-white rounded-xl shimmer border border-slate-200" />
          ))}
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <div className="lg:col-span-7 h-80 bg-white rounded-xl shimmer border border-slate-200" />
          <div className="lg:col-span-5 h-80 bg-white rounded-xl shimmer border border-slate-200" />
        </div>
      </div>
    );
  }
  
  return <div className="h-8 bg-slate-100 rounded-lg shimmer" />;
};

export default LoadingSkeleton;
