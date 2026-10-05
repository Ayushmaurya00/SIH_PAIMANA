import React from 'react';

export const OverviewHeader = () => {
  return (
    <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 pb-2 border-b border-border-rest">
      <div>
        <h1 className="text-xl font-extrabold text-text-primary tracking-tight">
          National Infrastructure Portfolio Overview
        </h1>
      </div>
    </div>
  );
};

export default OverviewHeader;
