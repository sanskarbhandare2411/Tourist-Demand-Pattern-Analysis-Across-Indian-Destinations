import React, { useEffect, useState } from 'react';
import PlotlyChart from '../components/PlotlyChart';
import api from '../services/api';

export default function WeatherTourismPage() {
  const [activeTab, setActiveTab] = useState('temp');
  const [tempData, setTempData] = useState(null);
  const [rainData, setRainData] = useState(null);
  const [corrData, setCorrData] = useState(null);

  useEffect(() => {
    api.getTemperatureAnalysis().then(setTempData).catch(console.error);
    api.getRainfallAnalysis().then(setRainData).catch(console.error);
    api.getCorrelationMatrix().then(setCorrData).catch(console.error);
  }, []);

  // Temperature Scatter Chart
  const tempPoints = tempData?.scatter_points || [];
  const tempChartData = [
    {
      x: tempPoints.map((p) => p.avg_temp_c),
      y: tempPoints.map((p) => p.total_visits),
      text: tempPoints.map((p) => `${p.name} (${p.state}): ${p.avg_temp_c}°C`),
      mode: 'markers',
      type: 'scatter',
      marker: {
        size: 9,
        color: tempPoints.map((p) => p.foreign_share_pct),
        colorscale: 'Plasma',
        colorbar: { title: 'Foreign Share (%)' },
      },
    },
  ];

  // Rainfall Scatter Chart
  const rainPoints = rainData?.scatter_points || [];
  const rainChartData = [
    {
      x: rainPoints.map((p) => p.annual_rainfall_mm),
      y: rainPoints.map((p) => p.total_visits),
      text: rainPoints.map((p) => `${p.name} (${p.state}): ${p.annual_rainfall_mm}mm`),
      mode: 'markers',
      type: 'scatter',
      marker: {
        size: 9,
        color: rainPoints.map((p) => p.monsoon_rainfall_mm),
        colorscale: 'Tealgrn',
        colorbar: { title: 'Monsoon Rain (mm)' },
      },
    },
  ];

  // Correlation Heatmap Chart
  const corrVars = corrData?.variables || [];
  const corrMatrix = (corrData?.matrix || []).map((m) => m.correlations);
  const heatmapData = [
    {
      z: corrMatrix,
      x: corrVars,
      y: corrVars,
      type: 'heatmap',
      colorscale: 'RdBu',
      reversescale: true,
      zmin: -1,
      zmax: 1,
    },
  ];

  return (
    <div>
      <div className="hero-container">
        <h1 className="hero-title">
          Weather & Tourism <span className="hero-gradient-text">Demand</span>
        </h1>
        <p className="hero-subtitle">Empirical Relationships Between Climate Variables & Visitor Footfalls</p>
      </div>

      {/* Tabs */}
      <div className="tab-list">
        <button
          className={`tab-btn ${activeTab === 'temp' ? 'active' : ''}`}
          onClick={() => setActiveTab('temp')}
        >
          🌡️ Temperature vs Demand
        </button>
        <button
          className={`tab-btn ${activeTab === 'rain' ? 'active' : ''}`}
          onClick={() => setActiveTab('rain')}
        >
          🌧️ Rainfall Impact
        </button>
        <button
          className={`tab-btn ${activeTab === 'corr' ? 'active' : ''}`}
          onClick={() => setActiveTab('corr')}
        >
          📊 Correlation Matrix
        </button>
      </div>

      {/* Tab 1: Temperature */}
      {activeTab === 'temp' && (
        <div className="glass-card">
          <h3 style={{ fontFamily: 'var(--font-heading)', color: '#ffffff', marginBottom: '8px' }}>
            Destination Average Temperature vs Tourist Footfall
          </h3>
          <PlotlyChart
            data={tempChartData}
            layout={{
              title: { text: '<b>Destination Average Temperature vs Tourist Footfall (Log Scale)</b>' },
              xaxis: { title: { text: 'Annual Average Temperature (°C)' } },
              yaxis: { title: { text: 'Tourist Footfall (Log Scale)' }, type: 'log' },
              shapes: [
                {
                  type: 'line',
                  x0: 22.0,
                  x1: 22.0,
                  y0: 1000,
                  y1: 10000000,
                  line: { color: '#10b981', width: 2, dash: 'dash' },
                },
              ],
            }}
          />

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '20px', marginTop: '20px' }}>
            <div style={{ background: 'rgba(255,255,255,0.02)', padding: '18px', borderRadius: '12px', border: '1px solid var(--border-subtle)' }}>
              <h4 style={{ color: 'var(--accent-cyan)', marginBottom: '8px' }}>Thermal Comfort Insights:</h4>
              <ul style={{ color: '#cbd5e1', fontSize: '0.88rem', lineHeight: '1.7', paddingLeft: '18px' }}>
                {(tempData?.key_takeaways || []).map((t, idx) => (
                  <li key={idx} style={{ marginBottom: '6px' }}>{t}</li>
                ))}
              </ul>
            </div>

            <div style={{ background: 'rgba(255,255,255,0.02)', padding: '18px', borderRadius: '12px', border: '1px solid var(--border-subtle)' }}>
              <h4 style={{ color: '#ffffff', marginBottom: '10px' }}>Destinations by Thermal Comfort Tier:</h4>
              <div className="table-container">
                <table className="custom-table">
                  <thead>
                    <tr>
                      <th>Thermal Comfort Tier</th>
                      <th>Destinations Count</th>
                    </tr>
                  </thead>
                  <tbody>
                    {(tempData?.comfort_tiers || []).map((tier, idx) => (
                      <tr key={idx}>
                        <td style={{ fontWeight: 600, color: '#ffffff' }}>{tier.tier}</td>
                        <td style={{ color: '#38bdf8', fontWeight: 600 }}>{tier.count}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab 2: Rainfall */}
      {activeTab === 'rain' && (
        <div className="glass-card">
          <h3 style={{ fontFamily: 'var(--font-heading)', color: '#ffffff', marginBottom: '8px' }}>
            Annual Precipitation vs Destination Tourist Footfall
          </h3>
          <PlotlyChart
            data={rainChartData}
            layout={{
              title: { text: '<b>Precipitation vs Footfall (Log Scale)</b>' },
              xaxis: { title: { text: 'Annual Total Rainfall (mm)' } },
              yaxis: { title: { text: 'Tourist Footfall (Log Scale)' }, type: 'log' },
            }}
          />

          <div style={{ marginTop: '20px', padding: '18px', background: 'rgba(56, 189, 248, 0.08)', borderRadius: '12px', border: '1px solid rgba(56, 189, 248, 0.25)' }}>
            <h4 style={{ color: 'var(--accent-cyan)', marginBottom: '8px' }}>Precipitation & Monsoon Exposure Insights:</h4>
            <ul style={{ color: '#cbd5e1', fontSize: '0.88rem', lineHeight: '1.7', paddingLeft: '18px' }}>
              {(rainData?.key_takeaways || []).map((t, idx) => (
                <li key={idx} style={{ marginBottom: '6px' }}>{t}</li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {/* Tab 3: Correlation */}
      {activeTab === 'corr' && (
        <div className="glass-card">
          <h3 style={{ fontFamily: 'var(--font-heading)', color: '#ffffff', marginBottom: '8px' }}>
            Statistical Correlation Matrix: Tourism & Meteorological Variables
          </h3>
          <PlotlyChart
            data={heatmapData}
            layout={{
              title: { text: '<b>Pearson Correlation Heatmap</b>' },
              margin: { l: 140, r: 40, t: 60, b: 140 },
            }}
          />

          <div style={{ marginTop: '20px', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px' }}>
            {(corrData?.key_correlations || []).map((c, idx) => (
              <div key={idx} style={{ background: 'rgba(255,255,255,0.03)', padding: '16px', borderRadius: '12px', border: '1px solid var(--border-subtle)' }}>
                <div style={{ fontSize: '0.8rem', color: '#94a3b8' }}>{c.pair}</div>
                <div style={{ fontSize: '1.4rem', fontWeight: 800, color: c.r > 0 ? '#10b981' : '#f43f5e', margin: '4px 0' }}>
                  r = {c.r > 0 ? `+${c.r}` : c.r}
                </div>
                <div style={{ fontSize: '0.82rem', color: '#cbd5e1' }}>{c.interpretation}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
