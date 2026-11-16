import React, { useEffect, useState } from 'react';
import PlotlyChart from '../components/PlotlyChart';
import api from '../services/api';

export default function DemandAnalysisPage() {
  const [activeTab, setActiveTab] = useState('longitudinal');
  const [longitudinal, setLongitudinal] = useState(null);
  const [statewise, setStatewise] = useState(null);
  const [composition, setComposition] = useState(null);
  const [topN, setTopN] = useState(12);
  const [sortBy, setSortBy] = useState('Total Visits');

  useEffect(() => {
    api.getLongitudinalDemand().then(setLongitudinal).catch(console.error);
    api.getVisitorComposition().then(setComposition).catch(console.error);
  }, []);

  useEffect(() => {
    api.getStatewiseDemand(topN, sortBy).then(setStatewise).catch(console.error);
  }, [topN, sortBy]);

  // Longitudinal FTA Chart Data
  const ftaSeries = longitudinal?.time_series || [];
  const ftaChartData = [
    {
      x: ftaSeries.map((d) => d.Year),
      y: ftaSeries.map((d) => d.FTAs_Million),
      type: 'scatter',
      mode: 'lines+markers',
      name: 'Foreign Tourist Arrivals (M)',
      line: { color: '#38bdf8', width: 3 },
      marker: { size: 6, color: '#0284c7' },
      fill: 'tozeroy',
      fillcolor: 'rgba(56, 189, 248, 0.12)',
    },
  ];

  // State-wise Horizontal Stacked Bar Chart
  const stateList = statewise?.states || [];
  const stateChartData = [
    {
      y: stateList.map((s) => s.State),
      x: stateList.map((s) => (s.Domestic_2019 || 0) / 1e6),
      name: 'Domestic (M)',
      type: 'bar',
      orientation: 'h',
      marker: { color: '#3b82f6' },
    },
    {
      y: stateList.map((s) => s.State),
      x: stateList.map((s) => (s.Foreign_2019 || 0) / 1e6),
      name: 'Foreign (M)',
      type: 'bar',
      orientation: 'h',
      marker: { color: '#f59e0b' },
    },
  ];

  // Composition Charts
  const pieData = [
    {
      values: (composition?.overall_pie || []).map((p) => p.value),
      labels: (composition?.overall_pie || []).map((p) => p.name),
      type: 'pie',
      hole: 0.45,
      marker: { colors: ['#38bdf8', '#f59e0b'] },
    },
  ];

  const scatterData = [
    {
      x: (composition?.scatter_points || []).map((p) => p.total_visits),
      y: (composition?.scatter_points || []).map((p) => p.foreign_share_pct),
      text: (composition?.scatter_points || []).map((p) => `${p.name} (${p.state})`),
      mode: 'markers',
      type: 'scatter',
      marker: {
        size: (composition?.scatter_points || []).map((p) => Math.max(6, Math.min(22, Math.sqrt(p.domestic_visits / 15000)))),
        color: (composition?.scatter_points || []).map((p) => p.is_unesco ? '#10b981' : '#38bdf8'),
        opacity: 0.85,
        line: { color: 'rgba(255,255,255,0.2)', width: 1 },
      },
    },
  ];

  return (
    <div>
      <div className="hero-container">
        <h1 className="hero-title">
          Tourism Demand <span className="hero-gradient-text">Analysis</span>
        </h1>
        <p className="hero-subtitle">Longitudinal Growth Trajectories & State-Wise Tourist Footfalls</p>
      </div>

      {/* Tabs Header */}
      <div className="tab-list">
        <button
          className={`tab-btn ${activeTab === 'longitudinal' ? 'active' : ''}`}
          onClick={() => setActiveTab('longitudinal')}
        >
          📈 Longitudinal Growth (40 Years)
        </button>
        <button
          className={`tab-btn ${activeTab === 'statewise' ? 'active' : ''}`}
          onClick={() => setActiveTab('statewise')}
        >
          🗺️ State-Wise Footfall
        </button>
        <button
          className={`tab-btn ${activeTab === 'composition' ? 'active' : ''}`}
          onClick={() => setActiveTab('composition')}
        >
          👥 Domestic vs Foreign Dynamics
        </button>
      </div>

      {/* Tab 1: Longitudinal */}
      {activeTab === 'longitudinal' && (
        <div className="glass-card">
          <h3 style={{ fontFamily: 'var(--font-heading)', color: '#ffffff', marginBottom: '8px' }}>
            Foreign Tourist Arrivals (1981–2020)
          </h3>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem', marginBottom: '18px' }}>
            Historical timeline of international visitation demonstrating growth and COVID-19 disruption:
          </p>

          <PlotlyChart
            data={ftaChartData}
            layout={{
              title: { text: '<b>Longitudinal Foreign Tourist Arrivals in India (1981–2020)</b>' },
              xaxis: { title: { text: 'Year' } },
              yaxis: { title: { text: 'Arrivals (Million Visitors)' } },
            }}
          />

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px', marginTop: '20px' }}>
            <div style={{ background: 'rgba(255, 255, 255, 0.03)', padding: '16px', borderRadius: '12px', border: '1px solid var(--border-subtle)' }}>
              <div style={{ fontSize: '0.78rem', color: '#94a3b8', textTransform: 'uppercase' }}>Pre-Pandemic Peak (2019)</div>
              <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#38bdf8', marginTop: '4px' }}>
                {longitudinal?.metrics?.pre_pandemic_peak_2019_million || 10.93} Million
              </div>
            </div>
            <div style={{ background: 'rgba(255, 255, 255, 0.03)', padding: '16px', borderRadius: '12px', border: '1px solid var(--border-subtle)' }}>
              <div style={{ fontSize: '0.78rem', color: '#94a3b8', textTransform: 'uppercase' }}>Historical CAGR (1991–2019)</div>
              <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#10b981', marginTop: '4px' }}>
                {longitudinal?.metrics?.historical_cagr_1991_2019 || '~6.2% Annual Growth'}
              </div>
            </div>
            <div style={{ background: 'rgba(255, 255, 255, 0.03)', padding: '16px', borderRadius: '12px', border: '1px solid var(--border-subtle)' }}>
              <div style={{ fontSize: '0.78rem', color: '#94a3b8', textTransform: 'uppercase' }}>Pandemic Impact (2020)</div>
              <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#f43f5e', marginTop: '4px' }}>
                {longitudinal?.metrics?.pandemic_impact_2020_pct || -74.9}% YoY
              </div>
            </div>
          </div>

          <div style={{ marginTop: '16px', padding: '14px 18px', background: 'rgba(56, 189, 248, 0.08)', borderRadius: '12px', border: '1px solid rgba(56, 189, 248, 0.2)', fontSize: '0.88rem', color: '#cbd5e1' }}>
            💡 <b>Trend Insight:</b> {longitudinal?.insight}
          </div>
        </div>
      )}

      {/* Tab 2: State-wise Footfall */}
      {activeTab === 'statewise' && (
        <div className="glass-card">
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 3fr', gap: '24px' }}>
            {/* Controls */}
            <div style={{ background: 'rgba(255,255,255,0.02)', padding: '18px', borderRadius: '14px', border: '1px solid var(--border-subtle)', height: 'fit-content' }}>
              <h4 style={{ color: '#ffffff', marginBottom: '14px', fontSize: '0.95rem' }}>Comparison Controls</h4>
              <div className="form-group">
                <label className="form-label">Display Top States: {topN}</label>
                <input
                  type="range"
                  min="5"
                  max="25"
                  value={topN}
                  onChange={(e) => setTopN(parseInt(e.target.value))}
                  className="form-range"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Rank By</label>
                <select className="form-select" value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
                  <option value="Total Visits">Total Visits</option>
                  <option value="Domestic Visits">Domestic Visits</option>
                  <option value="Foreign Visits">Foreign Visits</option>
                </select>
              </div>
            </div>

            {/* Stacked Chart */}
            <div>
              <h3 style={{ fontFamily: 'var(--font-heading)', color: '#ffffff', marginBottom: '8px' }}>
                State-Level Tourism Demand Comparison
              </h3>
              <PlotlyChart
                data={stateChartData}
                layout={{
                  barmode: 'stack',
                  title: { text: `<b>Top ${topN} Indian States by Tourist Volume (2019 Baseline)</b>` },
                  xaxis: { title: { text: 'Tourist Visits (Millions)' } },
                  yaxis: { autorange: 'reversed' },
                }}
              />
            </div>
          </div>

          {/* Table */}
          <div style={{ marginTop: '24px' }}>
            <h4 style={{ color: '#ffffff', marginBottom: '10px' }}>State-Level Statistics Table (Top {topN} States)</h4>
            <div className="table-container">
              <table className="custom-table">
                <thead>
                  <tr>
                    <th>State</th>
                    <th>Region</th>
                    <th>Domestic 2019</th>
                    <th>Foreign 2019</th>
                    <th>Total Visits</th>
                    <th>Domestic Share</th>
                    <th>Foreign Share</th>
                  </tr>
                </thead>
                <tbody>
                  {stateList.map((st, idx) => (
                    <tr key={idx}>
                      <td style={{ fontWeight: 600 }}>{st.State}</td>
                      <td>{st.Region || 'N/A'}</td>
                      <td>{st.Domestic_2019?.toLocaleString()}</td>
                      <td>{st.Foreign_2019?.toLocaleString()}</td>
                      <td style={{ color: '#38bdf8', fontWeight: 600 }}>{st.Total_Visits_2019?.toLocaleString()}</td>
                      <td>{st.Domestic_Share_2019 ? `${st.Domestic_Share_2019.toFixed(1)}%` : 'N/A'}</td>
                      <td>{st.Foreign_Share_2019 ? `${st.Foreign_Share_2019.toFixed(1)}%` : 'N/A'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* Tab 3: Domestic vs Foreign Dynamics */}
      {activeTab === 'composition' && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '24px' }}>
          <div className="glass-card">
            <h3 style={{ fontFamily: 'var(--font-heading)', color: '#ffffff', marginBottom: '12px' }}>
              Overall Monument Visitor Base
            </h3>
            <PlotlyChart
              data={pieData}
              layout={{
                title: { text: '<b>Domestic vs Foreign Breakdown</b>' },
              }}
            />
          </div>

          <div className="glass-card">
            <h3 style={{ fontFamily: 'var(--font-heading)', color: '#ffffff', marginBottom: '12px' }}>
              Volume vs Foreign Visitor Share (%)
            </h3>
            <PlotlyChart
              data={scatterData}
              layout={{
                title: { text: '<b>Visits (Log Scale) vs Foreign Share (%)</b>' },
                xaxis: { title: { text: 'Total Tourist Visits (Log Scale)' }, type: 'log' },
                yaxis: { title: { text: 'Foreign Share (%)' } },
              }}
            />
          </div>
        </div>
      )}
    </div>
  );
}
