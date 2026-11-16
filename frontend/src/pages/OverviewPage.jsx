import React, { useEffect, useState } from 'react';
import { Compass, Landmark, Users, Award, CloudSun, CheckCircle2 } from 'lucide-react';
import KPICard from '../components/KPICard';
import api from '../services/api';

export default function OverviewPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getOverview()
      .then((res) => {
        setData(res);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Error fetching overview data:', err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div style={{ padding: '40px', textAlign: 'center', color: '#94a3b8' }}>
        Loading Overview Intelligence...
      </div>
    );
  }

  const kpis = data?.kpis || {};
  const showcase = data?.showcase || [];
  const scope = data?.analytical_scope || {};
  const sources = data?.data_sources || {};

  return (
    <div>
      {/* Hero Banner */}
      <div className="hero-container">
        <div className="hero-badge">
          <span className="pulse-dot"></span> NATIONAL TOURISM INTELLIGENCE PLATFORM
        </div>
        <h1 className="hero-title">
          TOURIST DEMAND<br />
          <span className="hero-gradient-text">PATTERN ANALYSIS</span>
        </h1>
        <p className="hero-subtitle">Across Indian Destinations</p>
      </div>

      {/* KPI Cards Grid */}
      <div className="kpi-grid">
        <KPICard
          title="Monuments Footfall"
          value={`${kpis.total_monuments_footfall_m || 46.4}M`}
          subtitle={`${kpis.total_destinations_monitored || 144} Centrally-Protected Sites`}
          icon={Landmark}
          accentColor="#38bdf8"
        />
        <KPICard
          title="Top Heritage Hub"
          value={kpis.top_destination?.name?.substring(0, 14) || 'Taj Mahal'}
          subtitle={`${kpis.top_destination?.annual_visits_m || 5.07}M Annual Visitors`}
          icon={Compass}
          accentColor="#818cf8"
        />
        <KPICard
          title="Domestic Share"
          value={`${kpis.average_domestic_share_pct || 91.5}%`}
          subtitle="Predominant Visitor Base"
          icon={Users}
          accentColor="#10b981"
        />
        <KPICard
          title="UNESCO Heritage"
          value={kpis.unesco_sites_count || 24}
          subtitle="World Heritage Sites"
          icon={Award}
          accentColor="#f59e0b"
        />
        <KPICard
          title="Average Climate"
          value={`${kpis.average_annual_temperature_c || 25.1}°C`}
          subtitle="Mean Destination Temp"
          icon={CloudSun}
          accentColor="#38bdf8"
        />
      </div>

      {/* Real-World Destination Showcase Gallery */}
      <div style={{ marginBottom: '32px' }}>
        <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '1.4rem', color: '#ffffff', marginBottom: '6px' }}>
          🌟 Featured Destinations Showcase
        </h3>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem', marginBottom: '20px' }}>
          Visual highlights of prominent heritage hubs analyzed in the platform:
        </p>

        <div className="showcase-grid">
          {showcase.map((item, idx) => (
            <div key={idx} className="showcase-card">
              <img src={item.image} alt={item.name} className="showcase-img" />
              <div className="showcase-content">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                  <h4 style={{ margin: 0, fontSize: '1.15rem', color: '#ffffff' }}>{item.name}</h4>
                  {item.is_unesco && <span className="badge-unesco">UNESCO</span>}
                </div>
                <p style={{ margin: '2px 0 10px 0', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                  📍 {item.location}
                </p>
                <div style={{ display: 'inline-block', background: 'rgba(56, 189, 248, 0.12)', border: '1px solid rgba(56, 189, 248, 0.25)', padding: '4px 10px', borderRadius: '8px', fontSize: '0.8rem', color: '#38bdf8', fontWeight: 600 }}>
                  👥 {item.volume_str}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Analytical Scope & Methodology Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '24px' }}>
        <div className="glass-card">
          <h3 style={{ marginTop: 0, color: 'var(--accent-cyan)', fontFamily: 'var(--font-heading)', fontSize: '1.25rem', marginBottom: '12px' }}>
            {scope.title || 'Problem Definition & Analytical Scope'}
          </h3>
          <p style={{ color: '#cbd5e1', lineHeight: '1.6', fontSize: '0.92rem', marginBottom: '14px' }}>
            {scope.description}
          </p>
          <ul style={{ color: '#cbd5e1', lineHeight: '1.7', fontSize: '0.88rem', paddingLeft: '20px' }}>
            {(scope.key_pillars || []).map((pillar, idx) => (
              <li key={idx} style={{ marginBottom: '8px' }}>{pillar}</li>
            ))}
          </ul>
        </div>

        <div className="glass-card">
          <h3 style={{ marginTop: 0, color: 'var(--accent-cyan)', fontFamily: 'var(--font-heading)', fontSize: '1.25rem', marginBottom: '12px' }}>
            {sources.title || 'Data Sources & Quality Verification'}
          </h3>
          <ul style={{ color: '#cbd5e1', lineHeight: '1.7', fontSize: '0.88rem', paddingLeft: '20px' }}>
            {(sources.points || []).map((point, idx) => (
              <li key={idx} style={{ marginBottom: '10px' }}>{point}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
