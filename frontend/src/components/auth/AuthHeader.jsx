import React from 'react';
import { Link } from 'react-router-dom';

export const AuthHeader = () => {
  return (
    <header className="w-full bg-white border-b border-slate-200 py-3.5 px-6">
      <div className="max-w-6xl mx-auto flex items-center justify-between">
        <Link to="/login" className="text-lg font-bold text-slate-900 tracking-tight">
          PAIMANA <span className="text-blue-600">AI</span>
        </Link>
        <span className="text-xs font-medium text-slate-500 hidden sm:inline">
          National Infrastructure Project Monitoring • Government of India
        </span>
      </div>
    </header>
  );
};

export default AuthHeader;
