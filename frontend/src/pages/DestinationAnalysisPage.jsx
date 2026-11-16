import React, { useEffect, useState } from 'react';
import MapComponent from '../components/MapComponent';
import PlotlyChart from '../components/PlotlyChart';
import api from '../services/api';

export default function DestinationAnalysisPage({ globalFilters = {} }) {
  const [activeTab, setActiveTab] = useState('spotlight');
  const [destinations, setDestinations] = useState([]);
  const [selectedSpotlight, setSelectedSpotlight] = useState('Taj Mahal');
  const [spotlightData, setSpotlightData] = useState(null);
  const [rankingsTopN, setRankingsTopN] = useState(15);
  const [rankings, setRankings] = useState([]);
  const [mapMarkers, setMapMarkers] = useState([]);
  const [typologyImpact, setTypologyImpact] = useState(null);

  // Fetch initial destinations list for dropdown
  useEffect(() => {
    api.getDestinations({ limit: 200 })
      .then((res) => {
        setDestinations(res.destinations || []);
        if (res.destinations && res.destinations.length > 0) {
          const hasTaj = res.destinations.some((d) => d.Monument_Name.toLowerCase().includes('taj mahal'));
          setSelectedSpotlight(hasTaj ? 'Taj Mahal' : res.destinations[0].Monument_Name);
        }
      })
      .catch(console.error);

    api.getTypologyImpact().then(setTypologyImpact).catch(console.error);
  }, []);

  // Fetch spotlight destination details when selection changes
  useEffect(() => {
    if (selectedSpotlight) {
      api.getDestinationSpotlight(selectedSpotlight)
        .then(setSpotlightData)
        .catch(console.error);
    }
  }, [selectedSpotlight]);

  // Fetch rankings
  useEffect(() => {
    api.getRankings(rankingsTopN)
      .then((res) => setRankings(res.rankings || []))
      .catch(console.error);
  }, [rankingsTopN]);

  // Fetch map markers with global filters applied
  useEffect(() => {
    const params = {};
    if (globalFilters.state && globalFilters.state !== 'All States') params.state = globalFilters.state;
    if (globalFilters.typology && globalFilters.typology !== 'All Typologies') params.typology = globalFilters.typology;
    if (globalFilters.unesco === 'unesco') params.unesco_only = true;
    else if (globalFilters.unesco === 'non-unesco') params.unesco_only = false;

    api.getMapMarkers(params)
      .then((res) => setMapMarkers(res.markers || []))
      .catch(console.error);
  }, [globalFilters]);

  // Rankings Plotly Bar Chart Data
  const rankingsChartData = [
    {
      y: rankings.map((r) => r.Monument_Name),
      x: rankings.map((r) => r.Total_Tourist_Visits),
      type: 'bar',
      orientation: 'h',
      marker: {
        color: rankings.map((r) => r.Foreign_Tourist_Share || 0),
        colorscale: 'Turbo',
        colorbar: { title: 'Foreign Share (%)' },
      },
    },
  ];

  // UNESCO Comparison Bar Chart Data
  const unescoList = typologyImpact?.unesco_comparison || [];
  const unescoChartData = [
    {
      x: unescoList.map((u) => u.Status),
      y: unescoList.map((u) => u.Mean_Footfall),
      type: 'bar',
      marker: { color: ['#818cf8', '#10b981'] },
      text: unescoList.map((u) => `${(u.Mean_Footfall / 1e3).toFixed(0)}k`),
      textposition: 'auto',
    },
  ];

  // Typology Distribution Chart Data
  const typologyList = typologyImpact?.typology_summary || [];
  const typologyChartData = [
    {
      x: typologyList.map((t) => t.Destination_Type),
      y: typologyList.map((t) => t.Mean_Footfall),
      type: 'bar',
      marker: { color: '#38bdf8' },
    },
  ];

  return (
    <div>
      <div className="hero-container">
        <h1 className="hero-title">
          Destination <span className="hero-gradient-text">Analysis</span>
        </h1>
        <p className="hero-subtitle">Monuments Footfall, Heritage Visual Spotlight, and Geospatial Mapping</p>
      </div>

      {/* Tabs Header */}
      <div className="tab-list">
        <button
          className={`tab-btn ${activeTab === 'spotlight' ? 'active' : ''}`}
          onClick={() => setActiveTab('spotlight')}
        >
          📸 Destination Visual Spotlight
        </button>
        <button
          className={`tab-btn ${activeTab === 'rankings' ? 'active' : ''}`}
          onClick={() => setActiveTab('rankings')}
        >
          🏆 Top Footfall Rankings
        </button>
        <button
          className={`tab-btn ${activeTab === 'map' ? 'active' : ''}`}
          onClick={() => setActiveTab('map')}
        >
          🗺️ Geospatial Map
        </button>
        <button
          className={`tab-btn ${activeTab === 'typology' ? 'active' : ''}`}
          onClick={() => setActiveTab('typology')}
        >
          🏛️ Typology & UNESCO Impact
        </button>
      </div>

      {/* Tab 1: Visual Spotlight */}
      {activeTab === 'spotlight' && (
        <div className="glass-card">
          <div style={{ marginBottom: '20px', maxWidth: '400px' }}>
            <label className="form-label">Select Destination to Inspect</label>
            <select
              className="form-select"
              value={selectedSpotlight}
              onChange={(e) => setSelectedSpotlight(e.target.value)}
            >
              {destinations.map((d) => (
                <option key={d.Monument_Name} value={d.Monument_Name}>
                  {d.Monument_Name} ({d.State})
                </option>
              ))}
            </select>
          </div>

          {spotlightData && (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '28px', alignItems: 'center' }}>
              {/* Photo Showcase Card */}
              <div className="showcase-card">
                <img
                  src={spotlightData.Image_URL}
                  alt={spotlightData.Monument_Name}
                  style={{ width: '100%', height: '320px', objectFit: 'cover' }}
                />
                <div style={{ padding: '16px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <h3 style={{ margin: 0, color: '#ffffff', fontSize: '1.25rem' }}>{spotlightData.Monument_Name}</h3>
                    {spotlightData.Is_UNESCO_Site === 1 ? (
                      <span className="badge-unesco">★ UNESCO Site</span>
                    ) : (
                      <span className="badge-protected">Protected</span>
                    )}
                  </div>
                  <p style={{ color: '#94a3b8', margin: '6px 0 0 0', fontSize: '0.88rem' }}>
                    📍 {spotlightData.Circle} Circle | State: <b>{spotlightData.State}</b>
                  </p>
                </div>
              </div>

              {/* Metrics Grid */}
              <div>
                <h3 style={{ fontFamily: 'var(--font-heading)', color: '#ffffff', marginBottom: '16px' }}>
                  Destination Performance Metrics
                </h3>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px', marginBottom: '20px' }}>
                  <div style={{ background: 'rgba(255,255,255,0.03)', padding: '14px', borderRadius: '12px', border: '1px solid var(--border-subtle)' }}>
                    <div style={{ fontSize: '0.78rem', color: '#94a3b8' }}>Annual Footfall</div>
                    <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#ffffff' }}>
                      {spotlightData.Total_Tourist_Visits?.toLocaleString()}
                    </div>
                  </div>
                  <div style={{ background: 'rgba(255,255,255,0.03)', padding: '14px', borderRadius: '12px', border: '1px solid var(--border-subtle)' }}>
                    <div style={{ fontSize: '0.78rem', color: '#94a3b8' }}>Domestic Share</div>
                    <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#10b981' }}>
                      {spotlightData.Domestic_Tourist_Share?.toFixed(1)}%
                    </div>
                  </div>
                  <div style={{ background: 'rgba(255,255,255,0.03)', padding: '14px', borderRadius: '12px', border: '1px solid var(--border-subtle)' }}>
                    <div style={{ fontSize: '0.78rem', color: '#94a3b8' }}>Foreign Share</div>
                    <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#f59e0b' }}>
                      {spotlightData.Foreign_Tourist_Share?.toFixed(1)}%
                    </div>
                  </div>
                  <div style={{ background: 'rgba(255,255,255,0.03)', padding: '14px', borderRadius: '12px', border: '1px solid var(--border-subtle)' }}>
                    <div style={{ fontSize: '0.78rem', color: '#94a3b8' }}>Annual Avg Temp</div>
                    <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#38bdf8' }}>
                      {spotlightData.Annual_Avg_Temp_C?.toFixed(1)}°C
                    </div>
                  </div>
                </div>

                <hr style={{ border: 'none', borderTop: '1px solid var(--border-subtle)', margin: '16px 0' }} />

                <div style={{ fontSize: '0.9rem', color: '#cbd5e1', lineHeight: '1.8' }}>
                  <div>• <b>Architectural Typology:</b> <code>{spotlightData.Destination_Type}</code></div>
                  <div>• <b>Footfall Tier:</b> <code>{spotlightData.Footfall_Tier || 'Tier-3'}</code></div>
                  <div>• <b>Annual Precipitation:</b> <code>{spotlightData.Annual_Total_Rainfall_mm?.toFixed(0)} mm</code></div>
                  <div>• <b>Assigned Demand Cluster:</b> <code>{spotlightData.Cluster_Name || 'Cluster'}</code></div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Tab 2: Top Footfall Rankings */}
      {activeTab === 'rankings' && (
        <div className="glass-card">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
            <h3 style={{ fontFamily: 'var(--font-heading)', color: '#ffffff' }}>Top Visited Monuments across India</h3>
            <div style={{ width: '220px' }}>
              <label className="form-label" style={{ fontSize: '0.78rem' }}>Select Top N: {rankingsTopN}</label>
              <input
                type="range"
                min="5"
                max="30"
                value={rankingsTopN}
                onChange={(e) => setRankingsTopN(parseInt(e.target.value))}
                className="form-range"
              />
            </div>
          </div>

          <PlotlyChart
            data={rankingsChartData}
            layout={{
              title: { text: `<b>Top ${rankingsTopN} Indian Heritage Destinations by Footfall</b>` },
              xaxis: { title: { text: 'Annual Footfall' } },
              yaxis: { autorange: 'reversed' },
            }}
          />

          <div style={{ marginTop: '24px' }}>
            <div className="table-container">
              <table className="custom-table">
                <thead>
                  <tr>
                    <th>Monument</th>
                    <th>Circle</th>
                    <th>State</th>
                    <th>Typology</th>
                    <th>Annual Footfall</th>
                    <th>Domestic Share</th>
                    <th>Foreign Share</th>
                    <th>UNESCO</th>
                  </tr>
                </thead>
                <tbody>
                  {rankings.map((r, idx) => (
                    <tr key={idx}>
                      <td style={{ fontWeight: 600, color: '#ffffff' }}>{r.Monument_Name}</td>
                      <td>{r.Circle}</td>
                      <td>{r.State}</td>
                      <td>{r.Destination_Type}</td>
                      <td style={{ color: '#38bdf8', fontWeight: 600 }}>{r.Total_Tourist_Visits?.toLocaleString()}</td>
                      <td>{r.Domestic_Tourist_Share?.toFixed(1)}%</td>
                      <td>{r.Foreign_Tourist_Share?.toFixed(1)}%</td>
                      <td>
                        {r.Is_UNESCO_Site === 1 ? (
                          <span className="badge-unesco">★ UNESCO</span>
                        ) : (
                          <span style={{ color: '#64748b' }}>No</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* Tab 3: Geospatial Map */}
      {activeTab === 'map' && (
        <div className="glass-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
            <div>
              <h3 style={{ fontFamily: 'var(--font-heading)', color: '#ffffff', margin: 0 }}>
                Geospatial Map of Monitored Cultural Destinations
              </h3>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', margin: '4px 0 0 0' }}>
                Interactive map color-coded by Volume Tier. Click any marker for statistics and photo:
              </p>
            </div>
            <div style={{ display: 'flex', gap: '10px', fontSize: '0.78rem' }}>
              <span style={{ color: '#ef4444' }}>● Tier-1 (&gt;340k)</span>
              <span style={{ color: '#f59e0b' }}>● Tier-2 (125k-340k)</span>
              <span style={{ color: '#3b82f6' }}>● Tier-3 (40k-125k)</span>
              <span style={{ color: '#10b981' }}>● Tier-4 (&lt;40k)</span>
            </div>
          </div>

          <MapComponent markers={mapMarkers} />
        </div>
      )}

      {/* Tab 4: Typology & UNESCO Impact */}
      {activeTab === 'typology' && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '24px' }}>
          <div className="glass-card">
            <h3 style={{ fontFamily: 'var(--font-heading)', color: '#ffffff', marginBottom: '12px' }}>
              Average Footfall: UNESCO vs Non-UNESCO
            </h3>
            <PlotlyChart
              data={unescoChartData}
              layout={{
                title: { text: '<b>UNESCO Recognition Visitor Influx Multiple</b>' },
                yaxis: { title: { text: 'Mean Annual Footfall' } },
              }}
            />
          </div>

          <div className="glass-card">
            <h3 style={{ fontFamily: 'var(--font-heading)', color: '#ffffff', marginBottom: '12px' }}>
              Footfall by Architectural Typology
            </h3>
            <PlotlyChart
              data={typologyChartData}
              layout={{
                title: { text: '<b>Mean Annual Footfall by Typology</b>' },
                yaxis: { title: { text: 'Mean Annual Footfall' } },
              }}
            />
          </div>
        </div>
      )}
    </div>
  );
}
