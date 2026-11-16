import React, { useEffect, useState } from 'react';
import PlotlyChart from '../components/PlotlyChart';
import api from '../services/api';

export default function SeasonalAnalysisPage() {
  const [quarterly, setQuarterly] = useState(null);
  const [breakdown, setBreakdown] = useState(null);
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    api.getQuarterlyTrends().then(setQuarterly).catch(console.error);
    api.getSeasonalBreakdown().then(setBreakdown).catch(console.error);
    api.getSeasonalSummary().then(setSummary).catch(console.error);
  }, []);

  // 19-Year Quarterly Trend Chart Data grouped by Season
  const rawQtr = quarterly?.data || [];
  const seasons = ['Winter', 'Summer', 'Monsoon', 'Post-Monsoon'];
  const colorMap = {
    'Winter': '#10b981',
    'Summer': '#f43f5e',
    'Monsoon': '#38bdf8',
    'Post-Monsoon': '#fbbf24',
  };

  const lineChartData = seasons.map((s) => {
    const subset = rawQtr.filter((d) => d.Season === s);
    return {
      x: subset.map((d) => d.Year),
      y: subset.map((d) => d.Arrival_Share_Pct),
      mode: 'lines+markers',
      name: s,
      line: { color: colorMap[s], width: 2.5 },
      marker: { size: 6 },
    };
  });

  // Seasonal Donut Chart Data
  const breakdownData = breakdown?.seasonal_averages || [];
  const donutChartData = [
    {
      values: breakdownData.map((b) => b.share_pct),
      labels: breakdownData.map((b) => b.season),
      type: 'pie',
      hole: 0.45,
      marker: { colors: breakdownData.map((b) => b.color) },
    },
  ];

  return (
    <div>
      <div className="hero-container">
        <h1 className="hero-title">
          Seasonal Demand <span className="hero-gradient-text">Analysis</span>
        </h1>
        <p className="hero-subtitle">19 Years of Quarterly Visitor Influx & Peak Periods</p>
      </div>

      {/* 19-Year Quarterly Trend Chart */}
      <div className="glass-card" style={{ marginBottom: '24px' }}>
        <h3 style={{ fontFamily: 'var(--font-heading)', color: '#ffffff', marginBottom: '8px' }}>
          Quarterly Seasonal Demand Share Over 19 Years (2001–2019)
        </h3>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem', marginBottom: '16px' }}>
          Historical quarter-wise percentage share showing winter/post-monsoon peaks and summer slump:
        </p>

        <PlotlyChart
          data={lineChartData}
          layout={{
            title: { text: '<b>19-Year Seasonal Demand Distribution (% Share by Season)</b>' },
            xaxis: { title: { text: 'Year' } },
            yaxis: { title: { text: 'Percentage Share (%)' } },
          }}
        />
      </div>

      {/* Breakdown Donut & Findings */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(380px, 1fr))', gap: '24px' }}>
        <div className="glass-card">
          <h3 style={{ fontFamily: 'var(--font-heading)', color: '#ffffff', marginBottom: '12px' }}>
            Seasonal Arrival Breakdown
          </h3>
          <PlotlyChart
            data={donutChartData}
            layout={{
              title: { text: '<b>National Average Arrival Share by Season</b>' },
            }}
          />
        </div>

        <div className="glass-card">
          <h3 style={{ fontFamily: 'var(--font-heading)', color: '#ffffff', marginBottom: '16px' }}>
            Peak vs Trough Findings
          </h3>
          <div style={{ fontSize: '0.92rem', color: '#cbd5e1', lineHeight: '1.8' }}>
            <p style={{ marginBottom: '10px' }}>
              • <b>Peak Demand Period:</b> <b style={{ color: '#fbbf24' }}>{summary?.peak_period_description || 'Post-Monsoon (Q4: Oct–Dec)'}</b> captures <b style={{ color: '#ffffff' }}>{summary?.peak_share_pct || 30.5}%</b> of annual tourist volume.
            </p>
            <p style={{ marginBottom: '10px' }}>
              • <b>Secondary Winter Peak:</b> <b style={{ color: '#10b981' }}>{summary?.secondary_peak_season || 'Winter (Q1: Jan–Mar)'}</b> accounts for <b style={{ color: '#ffffff' }}>{summary?.secondary_peak_share_pct || 28.8}%</b> of annual volume.
            </p>
            <p style={{ marginBottom: '10px' }}>
              • <b>Summer Trough:</b> <b style={{ color: '#f43f5e' }}>{summary?.trough_season || 'Summer (Q2: Apr–Jun)'}</b> records the lowest visitor influx at <b style={{ color: '#ffffff' }}>{summary?.trough_share_pct || 19.1}%</b>.
            </p>
            <p style={{ marginBottom: '14px' }}>
              • <b>Seasonality Ratio:</b> Peak demand is <b style={{ color: 'var(--accent-cyan)' }}>{summary?.seasonality_ratio || 1.6}x</b> higher than the summer slump, highlighting the need for off-season incentives.
            </p>
          </div>

          <hr style={{ border: 'none', borderTop: '1px solid var(--border-subtle)', margin: '16px 0' }} />

          <h4 style={{ color: '#ffffff', marginBottom: '10px', fontSize: '0.9rem' }}>
            Historical Quarterly Share Matrix (Recent Years)
          </h4>
          <div className="table-container">
            <table className="custom-table">
              <thead>
                <tr>
                  <th>Year</th>
                  <th>Q1 (Winter)</th>
                  <th>Q2 (Summer)</th>
                  <th>Q3 (Monsoon)</th>
                  <th>Q4 (Post-Monsoon)</th>
                </tr>
              </thead>
              <tbody>
                {(summary?.last_5_years_matrix || []).map((row, idx) => (
                  <tr key={idx}>
                    <td style={{ fontWeight: 600, color: '#38bdf8' }}>{row.Year}</td>
                    <td>{row.Q1 ? `${row.Q1.toFixed(1)}%` : 'N/A'}</td>
                    <td>{row.Q2 ? `${row.Q2.toFixed(1)}%` : 'N/A'}</td>
                    <td>{row.Q3 ? `${row.Q3.toFixed(1)}%` : 'N/A'}</td>
                    <td>{row.Q4 ? `${row.Q4.toFixed(1)}%` : 'N/A'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
