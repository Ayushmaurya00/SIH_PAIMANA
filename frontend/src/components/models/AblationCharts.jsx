import React from 'react';
import {
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Legend, CartesianGrid
} from 'recharts';
import Card from '../Card';

export const AblationCharts = ({ classificationChartData, regressionChartData, r2ChartData }) => {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Classification Accuracy Chart */}
      <Card
        title="Predictive Lift: Overrun Classification Accuracy (%)"
        subtitle="Chronological out-of-time evaluation across ML algorithms"
      >
        <div className="h-64 mt-2" role="region" aria-label="Overrun Classification Accuracy Chart">
          <ResponsiveContainer width="100%" height="100%" debounce={50} minWidth={100} minHeight={200}>
            <BarChart data={classificationChartData} margin={{ top: 15, right: 20, left: -10, bottom: 25 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" opacity={0.6} />
              <XAxis dataKey="model" tick={{ fontSize: 10, fill: '#334155' }} interval={0} angle={-8} textAnchor="end" />
              <YAxis domain={[50, 100]} tick={{ fontSize: 11, fill: '#334155' }} unit="%" />
              <Tooltip formatter={(val) => [`${val.toFixed(1)}%`, '']} contentStyle={{ backgroundColor: '#ffffff', borderRadius: '8px', border: '1px solid #e2e8f0', fontSize: '12px' }} />
              <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
              <Bar dataKey="CUF Only (10 Features)" fill="#94a3b8" radius={[4, 4, 0, 0]} />
              <Bar dataKey="CUF + Extra Variables (25 Features)" fill="#2563eb" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </Card>

      {/* Regression RMSE & Variance Explained Chart */}
      <Card
        title="Cost Escalation Prediction Precision (RMSE Error %)"
        subtitle="Lower RMSE indicates narrower forecast uncertainty bands"
      >
        <div className="h-64 mt-2" role="region" aria-label="Cost Escalation Prediction Precision Chart">
          <ResponsiveContainer width="100%" height="100%" debounce={50} minWidth={100} minHeight={200}>
            <BarChart data={regressionChartData} margin={{ top: 15, right: 20, left: -10, bottom: 25 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" opacity={0.6} />
              <XAxis dataKey="target" tick={{ fontSize: 10, fill: '#334155' }} interval={0} angle={-8} textAnchor="end" />
              <YAxis domain={[0, 20]} tick={{ fontSize: 11, fill: '#334155' }} unit="%" />
              <Tooltip formatter={(val) => [`±${val}%`, '']} contentStyle={{ backgroundColor: '#ffffff', borderRadius: '8px', border: '1px solid #e2e8f0', fontSize: '12px' }} />
              <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
              <Bar dataKey="CUF Only (10 Features)" fill="#f87171" radius={[4, 4, 0, 0]} />
              <Bar dataKey="CUF + Extra Variables (25 Features)" fill="#10b981" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </Card>
    </div>
  );
};

export default AblationCharts;
