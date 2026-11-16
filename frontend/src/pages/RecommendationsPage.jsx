import React, { useEffect, useState } from 'react';
import api from '../services/api';

export default function RecommendationsPage({ filterOptions = {} }) {
  const [activeTab, setActiveTab] = useState('strategies');
  const [strategies, setStrategies] = useState([]);
  const [decongestion, setDecongestion] = useState([]);
  const [weatherRecs, setWeatherRecs] = useState([]);
  const [seasonalRecs, setSeasonalRecs] = useState([]);

  // Recommender Form State
  const [prefState, setPrefState] = useState('All');
  const [prefType, setPrefType] = useState('All');
  const [prefCrowd, setPrefCrowd] = useState('Any');
  const [prefWeather, setPrefWeather] = useState('Any');
  const [matchedDests, setMatchedDests] = useState([]);
  const [loadingMatches, setLoadingMatches] = useState(false);

  useEffect(() => {
    api.getClusterStrategies().then((res) => setStrategies(res.strategies || [])).catch(console.error);
    api.getDecongestionRecommendations().then((res) => setDecongestion(res.recommendations || [])).catch(console.error);
    api.getWeatherRecommendations().then((res) => setWeatherRecs(res.recommendations || [])).catch(console.error);
    api.getSeasonalRecommendations().then((res) => setSeasonalRecs(res.recommendations || [])).catch(console.error);
  }, []);

  // Fetch recommended destinations whenever filter preferences change
  useEffect(() => {
    setLoadingMatches(true);
    api.filterRecommendations({
      state: prefState,
      destination_type: prefType,
      crowd_preference: prefCrowd,
      weather_preference: prefWeather,
      top_k: 6,
    })
      .then((res) => {
        setMatchedDests(res.destinations || []);
        setLoadingMatches(false);
      })
      .catch((err) => {
        console.error(err);
        setLoadingMatches(false);
      });
  }, [prefState, prefType, prefCrowd, prefWeather]);

  return (
    <div>
      <div className="hero-container">
        <h1 className="hero-title">
          Insights & <span className="hero-gradient-text">Recommendations</span>
        </h1>
        <p className="hero-subtitle">Empirical Recommendations Calculated Directly from Analytical Findings</p>
      </div>

      {/* Tabs Header */}
      <div className="tab-list">
        <button
          className={`tab-btn ${activeTab === 'strategies' ? 'active' : ''}`}
          onClick={() => setActiveTab('strategies')}
        >
          🏛️ Strategic Interventions
        </button>
        <button
          className={`tab-btn ${activeTab === 'decongestion' ? 'active' : ''}`}
          onClick={() => setActiveTab('decongestion')}
        >
          🚦 Decongestion & Weather
        </button>
        <button
          className={`tab-btn ${activeTab === 'recommender' ? 'active' : ''}`}
          onClick={() => setActiveTab('recommender')}
        >
          🧭 Destination Recommender
        </button>
      </div>

      {/* Tab 1: Strategic Interventions */}
      {activeTab === 'strategies' && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(380px, 1fr))', gap: '20px' }}>
          {strategies.map((strat, idx) => (
            <div key={idx} className="glass-card" style={{ borderLeft: '4px solid var(--accent-cyan)' }}>
              <h4 style={{ color: '#ffffff', fontSize: '1.1rem', margin: '0 0 6px 0' }}>
                📌 {strat.archetype}
              </h4>
              <div style={{ fontSize: '0.82rem', color: 'var(--accent-cyan)', fontWeight: 700, marginBottom: '14px', textTransform: 'uppercase' }}>
                Focus: {strat.focus}
              </div>
              <ul style={{ color: '#cbd5e1', fontSize: '0.88rem', lineHeight: '1.7', paddingLeft: '18px' }}>
                {(strat.strategies || []).map((s, sIdx) => (
                  <li key={sIdx} style={{ marginBottom: '8px' }}>{s}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}

      {/* Tab 2: Decongestion & Weather */}
      {activeTab === 'decongestion' && (
        <div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '24px', marginBottom: '24px' }}>
            <div className="glass-card">
              <h3 style={{ fontFamily: 'var(--font-heading)', color: '#38bdf8', marginBottom: '14px' }}>
                Circuit Decongestion Strategy
              </h3>
              <ul style={{ color: '#cbd5e1', fontSize: '0.9rem', lineHeight: '1.8', paddingLeft: '18px' }}>
                {decongestion.map((item, idx) => (
                  <li key={idx} style={{ marginBottom: '10px' }}>{item}</li>
                ))}
              </ul>
            </div>

            <div className="glass-card">
              <h3 style={{ fontFamily: 'var(--font-heading)', color: '#10b981', marginBottom: '14px' }}>
                Climate & Weather Adaptation
              </h3>
              <ul style={{ color: '#cbd5e1', fontSize: '0.9rem', lineHeight: '1.8', paddingLeft: '18px' }}>
                {weatherRecs.map((item, idx) => (
                  <li key={idx} style={{ marginBottom: '10px' }}>{item}</li>
                ))}
              </ul>
            </div>
          </div>

          <div className="glass-card">
            <h3 style={{ fontFamily: 'var(--font-heading)', color: '#fbbf24', marginBottom: '12px' }}>
              Seasonal Scheduling Advice
            </h3>
            <ul style={{ color: '#cbd5e1', fontSize: '0.9rem', lineHeight: '1.8', paddingLeft: '18px' }}>
              {seasonalRecs.map((item, idx) => (
                <li key={idx} style={{ marginBottom: '8px' }}>{item}</li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {/* Tab 3: Destination Recommender */}
      {activeTab === 'recommender' && (
        <div className="glass-card">
          <h3 style={{ fontFamily: 'var(--font-heading)', color: '#ffffff', marginBottom: '8px' }}>
            🧭 Interactive Destination Recommender
          </h3>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem', marginBottom: '20px' }}>
            Find curated Indian destinations matching your specific travel preferences:
          </p>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', marginBottom: '24px' }}>
            <div className="form-group" style={{ margin: 0 }}>
              <label className="form-label">State</label>
              <select className="form-select" value={prefState} onChange={(e) => setPrefState(e.target.value)}>
                {(filterOptions.states || ['All States']).map((st) => (
                  <option key={st} value={st === 'All States' ? 'All' : st}>{st}</option>
                ))}
              </select>
            </div>

            <div className="form-group" style={{ margin: 0 }}>
              <label className="form-label">Typology</label>
              <select className="form-select" value={prefType} onChange={(e) => setPrefType(e.target.value)}>
                {(filterOptions.typologies || ['All Typologies']).map((typ) => (
                  <option key={typ} value={typ === 'All Typologies' ? 'All' : typ}>{typ}</option>
                ))}
              </select>
            </div>

            <div className="form-group" style={{ margin: 0 }}>
              <label className="form-label">Crowd Level</label>
              <select className="form-select" value={prefCrowd} onChange={(e) => setPrefCrowd(e.target.value)}>
                <option value="Any">Any Crowd Level</option>
                <option value="Low Crowds (<100k)">Low Crowds (&lt;100k)</option>
                <option value="Moderate (100k-500k)">Moderate (100k-500k)</option>
                <option value="High / Iconic (>500k)">High / Iconic (&gt;500k)</option>
              </select>
            </div>

            <div className="form-group" style={{ margin: 0 }}>
              <label className="form-label">Climate Comfort</label>
              <select className="form-select" value={prefWeather} onChange={(e) => setPrefWeather(e.target.value)}>
                <option value="Any">Any Climate</option>
                <option value="Cool (<20°C)">Cool (&lt;20°C)</option>
                <option value="Moderate (20-26°C)">Moderate (20-26°C)</option>
                <option value="Warm (>26°C)">Warm (&gt;26°C)</option>
              </select>
            </div>
          </div>

          <hr style={{ border: 'none', borderTop: '1px solid var(--border-subtle)', margin: '20px 0' }} />

          {loadingMatches ? (
            <div style={{ padding: '30px', textAlign: 'center', color: '#94a3b8' }}>
              Finding matching destinations...
            </div>
          ) : matchedDests.length > 0 ? (
            <div>
              <div style={{ color: '#cbd5e1', fontSize: '0.9rem', marginBottom: '16px' }}>
                Found <b style={{ color: 'var(--accent-cyan)' }}>{matchedDests.length}</b> recommended destinations:
              </div>

              <div className="showcase-grid">
                {matchedDests.map((dest, idx) => (
                  <div key={idx} className="showcase-card">
                    <img src={dest.image_url} alt={dest.name} className="showcase-img" style={{ height: '170px' }} />
                    <div className="showcase-content">
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                        <h4 style={{ margin: 0, fontSize: '1.05rem', color: '#ffffff' }}>{dest.name}</h4>
                        {dest.is_unesco ? (
                          <span className="badge-unesco">★ UNESCO</span>
                        ) : (
                          <span className="badge-protected">Protected</span>
                        )}
                      </div>
                      <p style={{ margin: '2px 0 8px 0', fontSize: '0.8rem', color: '#94a3b8' }}>
                        📍 {dest.circle} Circle, <b>{dest.state}</b>
                      </p>
                      <div style={{ fontSize: '0.82rem', color: '#cbd5e1', lineHeight: '1.6' }}>
                        <div>👥 <b>Visits:</b> {dest.total_visits?.toLocaleString()}</div>
                        <div>🌡️ <b>Temp:</b> {dest.annual_avg_temp_c}°C | 🌧️ {dest.annual_rainfall_mm} mm</div>
                        <div>🏛️ <b>Type:</b> {dest.destination_type}</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div style={{ padding: '30px', textAlign: 'center', color: '#f59e0b', background: 'rgba(245, 158, 11, 0.08)', borderRadius: '12px', border: '1px solid rgba(245, 158, 11, 0.2)' }}>
              No destinations matched these specific criteria. Try selecting 'Any' for some filters.
            </div>
          )}
        </div>
      )}
    </div>
  );
}
