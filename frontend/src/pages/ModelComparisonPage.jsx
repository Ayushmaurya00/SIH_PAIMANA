import React, { useState, useEffect } from 'react';
import { getModelMetrics } from '../api/client';
import LoadingSkeleton from '../components/LoadingSkeleton';
import { ModelHeader } from '../components/models/ModelHeader';
import { ArchitectureComparisonCards } from '../components/models/ArchitectureComparisonCards';
import { AblationCharts } from '../components/models/AblationCharts';
import { ModelMetricsTable } from '../components/models/ModelMetricsTable';

export const ModelComparisonPage = () => {
  const [metrics, setMetrics] = useState([]);
  const [featureSetFilter, setFeatureSetFilter] = useState('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;
    const fetchMetrics = async () => {
      try {
        setLoading(true);
        const res = await getModelMetrics();
        if (isMounted) {
          setMetrics(res || []);
        }
      } catch (err) {
        console.error("Failed to load model metrics:", err);
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };
    fetchMetrics();
    return () => { isMounted = false; };
  }, []);

  const cufXgbCls = metrics.find(m => m.feature_set === 'cuf_only' && m.model_name === 'xgboost_classifier');
  const extraXgbCls = metrics.find(m => m.feature_set === 'cuf_plus_extra' && m.model_name === 'xgboost_classifier');
  const cufXgbReg = metrics.find(m => m.feature_set === 'cuf_only' && m.model_name === 'xgboost_regressor');
  const extraXgbReg = metrics.find(m => m.feature_set === 'cuf_plus_extra' && m.model_name === 'xgboost_regressor');
  const cufLogReg = metrics.find(m => m.feature_set === 'cuf_only' && m.model_name === 'logistic_regression');
  const extraLogReg = metrics.find(m => m.feature_set === 'cuf_plus_extra' && m.model_name === 'logistic_regression');
  const cufRidge = metrics.find(m => m.feature_set === 'cuf_only' && m.model_name === 'ridge_regression');
  const extraRidge = metrics.find(m => m.feature_set === 'cuf_plus_extra' && m.model_name === 'ridge_regression');

  const classificationChartData = [
    {
      model: 'Logistic Regression (Linear Baseline)',
      'CUF Only (10 Features)': cufLogReg?.accuracy != null ? Number((cufLogReg.accuracy * 100).toFixed(1)) : 0,
      'CUF + Extra Variables (25 Features)': extraLogReg?.accuracy != null ? Number((extraLogReg.accuracy * 100).toFixed(1)) : 0,
    },
    {
      model: 'XGBoost Classifier (Non-Linear ML)',
      'CUF Only (10 Features)': cufXgbCls?.accuracy != null ? Number((cufXgbCls.accuracy * 100).toFixed(1)) : 0,
      'CUF + Extra Variables (25 Features)': extraXgbCls?.accuracy != null ? Number((extraXgbCls.accuracy * 100).toFixed(1)) : 0,
    }
  ];

  const regressionChartData = [
    {
      target: 'Cost Escalation % (XGB Regressor)',
      'CUF Only (10 Features)': cufXgbReg?.rmse != null ? Number(cufXgbReg.rmse.toFixed(2)) : 0,
      'CUF + Extra Variables (25 Features)': extraXgbReg?.rmse != null ? Number(extraXgbReg.rmse.toFixed(2)) : 0,
    },
    {
      target: 'Cost Escalation % (Ridge Baseline)',
      'CUF Only (10 Features)': cufRidge?.rmse != null ? Number(cufRidge.rmse.toFixed(2)) : 0,
      'CUF + Extra Variables (25 Features)': extraRidge?.rmse != null ? Number(extraRidge.rmse.toFixed(2)) : 0,
    }
  ];

  const r2ChartData = [
    {
      name: 'Variance Explained (R²)',
      'CUF Only (10 Features)': cufXgbReg?.r2 != null ? Number((cufXgbReg.r2 * 100).toFixed(1)) : 0,
      'CUF + Extra Variables (25 Features)': extraXgbReg?.r2 != null ? Number((extraXgbReg.r2 * 100).toFixed(1)) : 0,
    }
  ];

  if (loading) {
    return (
      <div className="p-6 space-y-6 max-w-7xl mx-auto">
        <LoadingSkeleton type="kpi" />
        <LoadingSkeleton type="table" count={6} />
      </div>
    );
  }

  if (!loading && metrics.length === 0) {
    return (
      <div className="p-3 sm:p-6 space-y-4 sm:space-y-6 max-w-7xl mx-auto animate-fade-in">
        <ModelHeader />
        <div className="bg-surface-elevated border border-border-rest rounded-xl p-8 text-center text-text-secondary">
          <p className="text-sm font-semibold">No benchmark evaluation metrics currently recorded in the registry.</p>
          <p className="text-xs text-text-tertiary mt-1">Execute the training orchestrator (`python -m src.models.train_and_evaluate`) to evaluate baseline vs augmented ML architectures.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-3 sm:p-6 space-y-4 sm:space-y-6 max-w-7xl mx-auto animate-fade-in">
      <ModelHeader />
      <ArchitectureComparisonCards
        cufXgbCls={cufXgbCls}
        extraXgbCls={extraXgbCls}
        cufXgbReg={cufXgbReg}
        extraXgbReg={extraXgbReg}
      />
      <AblationCharts
        classificationChartData={classificationChartData}
        regressionChartData={regressionChartData}
        r2ChartData={r2ChartData}
      />
      <ModelMetricsTable
        metrics={metrics}
        featureSetFilter={featureSetFilter}
        setFeatureSetFilter={setFeatureSetFilter}
      />
    </div>
  );
};

export default ModelComparisonPage;
