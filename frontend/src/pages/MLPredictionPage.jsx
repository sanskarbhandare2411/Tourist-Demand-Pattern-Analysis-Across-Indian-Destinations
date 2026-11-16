import React, { useEffect, useState } from 'react';
import PlotlyChart from '../components/PlotlyChart';
import api from '../services/api';

export default function MLPredictionPage() {
  const [metricsData, setMetricsData] = useState(null);
  const [form, setForm] = useState({
    is_unesco_site: 1,
    destination_type: 'Fort & Palace',
    foreign_tourist_share: 8.5,
    annual_avg_temp_c: 24.5,
    annual_total_rainfall_mm: 1100,
  });
  const [prediction, setPrediction] = useState(null);
  const [loadingPred, setLoadingPred] = useState(false);

  useEffect(() => {
    api.getMLMetrics().then(setMetricsData).catch(console.error);
  }, []);

  const handlePredict = async (e) => {
    e.preventDefault();
    setLoadingPred(true);
    try {
      const res = await api.predictDemand({
        is_unesco_site: parseInt(form.is_unesco_site),
        destination_type: form.destination_type,
        foreign_tourist_share: parseFloat(form.foreign_tourist_share),
        annual_avg_temp_c: parseFloat(form.annual_avg_temp_c),
        annual_total_rainfall_mm: parseFloat(form.annual_total_rainfall_mm),
      });
      setPrediction(res);
    } catch (err) {
      console.error('Error predicting demand:', err);
    } finally {
      setLoadingPred(false);
    }
  };

  const metrics = metricsData?.metrics || {};
  const coefficients = metricsData?.coefficients || [];

  // Feature Impact Horizontal Bar Chart
  const coefChartData = [
    {
      y: coefficients.map((c) => c.Feature),
      x: coefficients.map((c) => c.Standardized_Coefficient),
      type: 'bar',
      orientation: 'h',
      marker: {
        color: coefficients.map((c) => (c.Standardized_Coefficient >= 0 ? '#10b981' : '#f43f5e')),
      },
    },
  ];

  return (
    <div>
      <div className="hero-container">
        <h1 className="hero-title">
          ML Demand <span className="hero-gradient-text">Prediction</span>
        </h1>
        <p className="hero-subtitle">Multiple Linear Regression Model with Interactive Demand Simulator</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(420px, 1fr))', gap: '24px' }}>
        {/* Left Column: Benchmarks & Coefficients */}
        <div className="glass-card">
          <h3 style={{ fontFamily: 'var(--font-heading)', color: '#ffffff', marginBottom: '16px' }}>
            Model Evaluation Benchmarks
          </h3>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '12px', marginBottom: '16px' }}>
            <div style={{ background: 'rgba(255,255,255,0.03)', padding: '12px', borderRadius: '10px', border: '1px solid var(--border-subtle)', textAlign: 'center' }}>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Log MAE</div>
              <div style={{ fontSize: '1.3rem', fontWeight: 800, color: '#38bdf8', marginTop: '2px' }}>
                {metrics.mae_log?.toFixed(3) || '1.343'}
              </div>
            </div>
            <div style={{ background: 'rgba(255,255,255,0.03)', padding: '12px', borderRadius: '10px', border: '1px solid var(--border-subtle)', textAlign: 'center' }}>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Log RMSE</div>
              <div style={{ fontSize: '1.3rem', fontWeight: 800, color: '#818cf8', marginTop: '2px' }}>
                {metrics.rmse_log?.toFixed(3) || '1.637'}
              </div>
            </div>
            <div style={{ background: 'rgba(255,255,255,0.03)', padding: '12px', borderRadius: '10px', border: '1px solid var(--border-subtle)', textAlign: 'center' }}>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Log R² Score</div>
              <div style={{ fontSize: '1.3rem', fontWeight: 800, color: '#10b981', marginTop: '2px' }}>
                {metrics.r2_log?.toFixed(3) || '0.106'}
              </div>
            </div>
          </div>

          <div style={{ fontSize: '0.88rem', color: '#cbd5e1', lineHeight: '1.7', marginBottom: '20px' }}>
            <div>• <b>5-Fold Cross Validation R²:</b> <code>{metrics.cv_r2_mean?.toFixed(3) || '0.090'} ± {metrics.cv_r2_std?.toFixed(3) || '0.045'}</code></div>
            <div>• <b>5-Fold Cross Validation MAE:</b> <code>{metrics.cv_mae_mean?.toFixed(3) || '1.352'}</code></div>
            <div>• <b>Holdout Test Set Size:</b> <code>{metrics.n_test || 29} destinations (20%)</code></div>
            <div>• <b>Actual Scale Test MAE:</b> <code>{metrics.mae_actual?.toLocaleString() || '425,000'} visits</code></div>
          </div>

          <hr style={{ border: 'none', borderTop: '1px solid var(--border-subtle)', margin: '18px 0' }} />

          <h4 style={{ color: '#ffffff', marginBottom: '10px' }}>Standardized Feature Coefficients</h4>
          <PlotlyChart
            data={coefChartData}
            layout={{
              title: { text: '<b>Impact of Attributes on Tourist Demand</b>' },
              xaxis: { title: { text: 'Standardized Coefficient (Beta)' } },
              yaxis: { autorange: 'reversed' },
            }}
          />
        </div>

        {/* Right Column: Interactive Demand Simulator */}
        <div className="glass-card">
          <h3 style={{ fontFamily: 'var(--font-heading)', color: '#ffffff', marginBottom: '8px' }}>
            Interactive Demand Simulator
          </h3>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '20px' }}>
            Adjust destination parameters to simulate estimated annual visitor footfall:
          </p>

          <form onSubmit={handlePredict}>
            <div className="form-group">
              <label className="form-label">UNESCO World Heritage Status</label>
              <select
                className="form-select"
                value={form.is_unesco_site}
                onChange={(e) => setForm({ ...form, is_unesco_site: e.target.value })}
              >
                <option value={1}>Yes (UNESCO World Heritage Site)</option>
                <option value={0}>No (Standard Centrally Protected Monument)</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Typology</label>
              <select
                className="form-select"
                value={form.destination_type}
                onChange={(e) => setForm({ ...form, destination_type: e.target.value })}
              >
                <option value="Fort & Palace">Fort & Palace</option>
                <option value="Temple & Religious">Temple & Religious</option>
                <option value="Mausoleum & Tomb">Mausoleum & Tomb</option>
                <option value="Caves & Rock-Cut">Caves & Rock-Cut</option>
                <option value="Archaeological Ruins">Archaeological Ruins</option>
                <option value="Heritage & Memorial">Heritage & Memorial</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">
                Expected Foreign Tourist Share: <b>{form.foreign_tourist_share}%</b>
              </label>
              <input
                type="range"
                min="0"
                max="50"
                step="0.5"
                value={form.foreign_tourist_share}
                onChange={(e) => setForm({ ...form, foreign_tourist_share: e.target.value })}
                className="form-range"
              />
            </div>

            <div className="form-group">
              <label className="form-label">
                Annual Average Temperature: <b>{form.annual_avg_temp_c}°C</b>
              </label>
              <input
                type="range"
                min="10"
                max="32"
                step="0.5"
                value={form.annual_avg_temp_c}
                onChange={(e) => setForm({ ...form, annual_avg_temp_c: e.target.value })}
                className="form-range"
              />
            </div>

            <div className="form-group">
              <label className="form-label">
                Annual Total Rainfall: <b>{form.annual_total_rainfall_mm} mm</b>
              </label>
              <input
                type="range"
                min="300"
                max="4000"
                step="50"
                value={form.annual_total_rainfall_mm}
                onChange={(e) => setForm({ ...form, annual_total_rainfall_mm: e.target.value })}
                className="form-range"
              />
            </div>

            <button type="submit" className="btn-primary" style={{ width: '100%', marginTop: '10px' }}>
              {loadingPred ? 'Computing Forecast...' : 'Predict Tourist Demand 🚀'}
            </button>
          </form>

          {prediction && (
            <div style={{ marginTop: '24px', padding: '20px', background: 'rgba(56, 189, 248, 0.08)', borderRadius: '14px', border: '1px solid rgba(56, 189, 248, 0.3)' }}>
              <h4 style={{ color: '#10b981', margin: '0 0 12px 0', fontSize: '1.05rem' }}>
                ✓ Demand Forecast Calculated!
              </h4>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '12px' }}>
                <div style={{ background: 'rgba(15, 23, 42, 0.8)', padding: '12px', borderRadius: '10px', textAlign: 'center' }}>
                  <div style={{ fontSize: '0.72rem', color: '#94a3b8' }}>Predicted Annual Visits</div>
                  <div style={{ fontSize: '1.25rem', fontWeight: 800, color: '#38bdf8', marginTop: '4px' }}>
                    {prediction.predicted_total_visits?.toLocaleString()}
                  </div>
                </div>
                <div style={{ background: 'rgba(15, 23, 42, 0.8)', padding: '12px', borderRadius: '10px', textAlign: 'center' }}>
                  <div style={{ fontSize: '0.72rem', color: '#94a3b8' }}>Lower (-1 RMSE)</div>
                  <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#cbd5e1', marginTop: '4px' }}>
                    {prediction.prediction_interval_lower?.toLocaleString()}
                  </div>
                </div>
                <div style={{ background: 'rgba(15, 23, 42, 0.8)', padding: '12px', borderRadius: '10px', textAlign: 'center' }}>
                  <div style={{ fontSize: '0.72rem', color: '#94a3b8' }}>Upper (+1 RMSE)</div>
                  <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#cbd5e1', marginTop: '4px' }}>
                    {prediction.prediction_interval_upper?.toLocaleString()}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
