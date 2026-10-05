import React from 'react';
import {
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Legend, CartesianGrid, PieChart, Pie, Cell
} from 'recharts';
import Card from '../Card';

const TIER_COLORS = ['#0F2B5B', '#1E3A8A', '#059669', '#D97706'];

export const OverviewCharts = ({ data }) => {
  const sectorData = (data.sector_distribution || []).slice(0, 6).map(s => ({
    name: s.sector.length > 18 ? `${s.sector.substring(0, 16)}...` : s.sector,
    'Projects': s.count,
    'Avg Risk': s.avg_risk_score !== undefined ? s.avg_risk_score : (s.avg_score || 0)
  }));

  const rawBrackets = data.cost_tier_distribution || data.cost_brackets || [];
  const costDistributionData = rawBrackets.map((b, i) => {
    const tierName = b.tier || b.range || 'Tier';
    const count = b.count || 0;
    return {
      name: tierName,
      value: count,
      color: TIER_COLORS[i % TIER_COLORS.length],
      'aria-label': `${tierName}: ${count} projects`
    };
  });

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
      {/* Sector Exposure Bar Chart */}
      <div className="lg:col-span-7">
        <Card
          title="Sector Risk & Project Volume Distribution"
          subtitle="Top infrastructure sectors ranked by capital allocation and vulnerability"
        >
          <div className="h-64 mt-2" role="region" aria-label="Sector Risk & Project Volume Distribution Chart">
            <ResponsiveContainer width="100%" height="100%" debounce={50} minWidth={100} minHeight={200}>
              <BarChart data={sectorData} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="name" tick={{ fontSize: 10, fill: '#334155' }} interval={0} angle={-15} textAnchor="end" />
                <YAxis tick={{ fontSize: 11, fill: '#334155' }} />
                <Tooltip contentStyle={{ backgroundColor: '#ffffff', borderRadius: '8px', border: '1px solid #e2e8f0', fontSize: '12px' }} />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
                <Bar dataKey="Projects" fill="#0F2B5B" radius={[4, 4, 0, 0]} />
                <Bar dataKey="Avg Risk" fill="#f59e0b" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>

      {/* Cost Bracket Allocation Donut */}
      <div className="lg:col-span-5">
        <Card
          title="Portfolio Capital Outlay Scale"
          subtitle="Distribution of projects by sanctioned financial outlay"
        >
          <div className="h-64 mt-2" role="region" aria-label="Portfolio Capital Outlay Scale Donut Chart">
            <ResponsiveContainer width="100%" height="100%" debounce={50} minWidth={100} minHeight={200}>
              <PieChart>
                <Pie
                  data={costDistributionData}
                  cx="50%"
                  cy="50%"
                  innerRadius={50}
                  outerRadius={80}
                  paddingAngle={4}
                  dataKey="value"
                  aria-label="Portfolio Capital Outlay Scale"
                >
                  {costDistributionData.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={entry.color}
                      aria-label={`${entry.name}: ${entry.value} projects`}
                    />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: '#ffffff', borderRadius: '8px', border: '1px solid #e2e8f0', fontSize: '12px' }} />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default OverviewCharts;
