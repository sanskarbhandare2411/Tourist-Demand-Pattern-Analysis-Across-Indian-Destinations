import React, { useEffect, useState } from 'react';
import PlotlyChart from '../components/PlotlyChart';
import api from '../services/api';

export default function ClusteringPage() {
  const [activeTab, setActiveTab] = useState('pca');
  const [overview, setOverview] = useState(null);
  const [evaluation, setEvaluation] = useState(null);
  const [profiles, setProfiles] = useState(null);
  const [selectedCluster, setSelectedCluster] = useState('Cluster 0: Global Heritage Icons');
  const [members, setMembers] = useState([]);

  useEffect(() => {
    api.getClusteringOverview().then(setOverview).catch(console.error);
    api.getClusteringEvaluation().then(setEvaluation).catch(console.error);
    api.getClusterProfiles().then(setProfiles).catch(console.error);
  }, []);

  useEffect(() => {
    if (selectedCluster) {
      api.getClusterMembers(selectedCluster)
        .then((res) => setMembers(res.members || []))
        .catch(console.error);
    }
  }, [selectedCluster]);

  // PCA Scatter Plot Data
  const pcaPoints = overview?.pca_points || [];
  const clusterNames = [...new Set(pcaPoints.map((p) => p.cluster_name))];
  const clusterColors = ['#ef4444', '#f59e0b', '#3b82f6', '#10b981'];

  const pcaChartData = clusterNames.map((name, idx) => {
    const subset = pcaPoints.filter((p) => p.cluster_name === name);
    return {
      x: subset.map((p) => p.pca_dim1),
      y: subset.map((p) => p.pca_dim2),
      text: subset.map((p) => `${p.name} (${p.state})<br>Visits: ${p.total_visits?.toLocaleString()}<br>Foreign: ${p.foreign_share_pct}%`),
      mode: 'markers',
      name: name,
      marker: {
        size: 8,
        color: clusterColors[idx % clusterColors.length],
      },
    };
  });

  // Validation Curves Data
  const evalData = evaluation?.evaluation_data || [];
  const elbowChartData = [
    {
      x: evalData.map((d) => d.k),
      y: evalData.map((d) => d.Inertia),
      mode: 'lines+markers',
      name: 'Inertia',
      line: { color: '#38bdf8', width: 2.5 },
      marker: { size: 6 },
    },
  ];

  const silhouetteChartData = [
    {
      x: evalData.map((d) => d.k),
      y: evalData.map((d) => d.Silhouette_Score),
      mode: 'lines+markers',
      name: 'Silhouette Score',
      line: { color: '#10b981', width: 2.5 },
      marker: { size: 6 },
    },
  ];

  return (
    <div>
      <div className="hero-container">
        <h1 className="hero-title">
          Destination <span className="hero-gradient-text">Clustering</span>
        </h1>
        <p className="hero-subtitle">K-Means Segmentation of Indian Destinations Based on Demand Behaviors</p>
      </div>

      {/* Tabs Header */}
      <div className="tab-list">
        <button
          className={`tab-btn ${activeTab === 'pca' ? 'active' : ''}`}
          onClick={() => setActiveTab('pca')}
        >
          🎯 Cluster Map & PCA
        </button>
        <button
          className={`tab-btn ${activeTab === 'curves' ? 'active' : ''}`}
          onClick={() => setActiveTab('curves')}
        >
          📈 Validation Curves
        </button>
        <button
          className={`tab-btn ${activeTab === 'profiles' ? 'active' : ''}`}
          onClick={() => setActiveTab('profiles')}
        >
          📋 Cluster Profiles
        </button>
      </div>

      {/* Tab 1: PCA Map */}
      {activeTab === 'pca' && (
        <div className="glass-card">
          <h3 style={{ fontFamily: 'var(--font-heading)', color: '#ffffff', marginBottom: '8px' }}>
            Destination Clusters in 2D PCA Latent Space (k=4)
          </h3>
          <PlotlyChart
            data={pcaChartData}
            layout={{
              title: { text: '<b>2D PCA Projection of Destination Demand Clusters</b>' },
              xaxis: { title: { text: 'Principal Component 1 (Volume & Prominence)' } },
              yaxis: { title: { text: 'Principal Component 2 (Climate & Rainfall)' } },
            }}
          />

          <div style={{ marginTop: '24px', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '16px' }}>
            {(overview?.archetypes || []).map((arch) => (
              <div
                key={arch.id}
                style={{
                  background: 'rgba(255, 255, 255, 0.03)',
                  padding: '16px',
                  borderRadius: '12px',
                  border: '1px solid var(--border-subtle)',
                  borderTop: `3px solid ${clusterColors[arch.id % clusterColors.length]}`,
                }}
              >
                <h4 style={{ color: '#ffffff', margin: '0 0 6px 0', fontSize: '1rem' }}>{arch.name}</h4>
                <p style={{ color: '#cbd5e1', fontSize: '0.85rem', lineHeight: '1.6', margin: 0 }}>
                  {arch.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 2: Validation Curves */}
      {activeTab === 'curves' && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '24px' }}>
          <div className="glass-card">
            <h3 style={{ fontFamily: 'var(--font-heading)', color: '#ffffff', marginBottom: '8px' }}>
              Elbow Method (Inertia vs k)
            </h3>
            <PlotlyChart
              data={elbowChartData}
              layout={{
                title: { text: '<b>Inertia Reduction across k</b>' },
                xaxis: { title: { text: 'Number of Clusters (k)' } },
                yaxis: { title: { text: 'Inertia' } },
                shapes: [
                  {
                    type: 'line',
                    x0: 4,
                    x1: 4,
                    y0: 0,
                    y1: 1500,
                    line: { color: '#f43f5e', width: 2, dash: 'dash' },
                  },
                ],
              }}
            />
          </div>

          <div className="glass-card">
            <h3 style={{ fontFamily: 'var(--font-heading)', color: '#ffffff', marginBottom: '8px' }}>
              Silhouette Analysis vs k
            </h3>
            <PlotlyChart
              data={silhouetteChartData}
              layout={{
                title: { text: '<b>Silhouette Coefficient Optimization</b>' },
                xaxis: { title: { text: 'Number of Clusters (k)' } },
                yaxis: { title: { text: 'Silhouette Score' } },
                shapes: [
                  {
                    type: 'line',
                    x0: 4,
                    x1: 4,
                    y0: 0,
                    y1: 0.6,
                    line: { color: '#f43f5e', width: 2, dash: 'dash' },
                  },
                ],
              }}
            />
          </div>
        </div>
      )}

      {/* Tab 3: Cluster Profiles */}
      {activeTab === 'profiles' && (
        <div className="glass-card">
          <h3 style={{ fontFamily: 'var(--font-heading)', color: '#ffffff', marginBottom: '14px' }}>
            Cluster Profiles Summary Table
          </h3>
          <div className="table-container" style={{ marginBottom: '28px' }}>
            <table className="custom-table">
              <thead>
                <tr>
                  <th>Archetype</th>
                  <th>Count</th>
                  <th>Avg Visits</th>
                  <th>Median Visits</th>
                  <th>Foreign Share</th>
                  <th>Domestic Share</th>
                  <th>Avg Temp</th>
                  <th>Avg Rain</th>
                  <th>UNESCO Sites</th>
                </tr>
              </thead>
              <tbody>
                {(profiles?.profiles || []).map((prof, idx) => (
                  <tr key={idx}>
                    <td style={{ fontWeight: 700, color: '#38bdf8' }}>{prof.Cluster_Name}</td>
                    <td>{prof.Destination_Count}</td>
                    <td>{prof.Avg_Total_Visits?.toLocaleString()}</td>
                    <td>{prof.Median_Total_Visits?.toLocaleString()}</td>
                    <td>{prof.Avg_Foreign_Share?.toFixed(1)}%</td>
                    <td>{prof.Avg_Domestic_Share?.toFixed(1)}%</td>
                    <td>{prof.Avg_Annual_Temp?.toFixed(1)}°C</td>
                    <td>{prof.Avg_Annual_Rainfall?.toFixed(0)} mm</td>
                    <td style={{ color: '#f59e0b', fontWeight: 600 }}>{prof.UNESCO_Sites_Count}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <h3 style={{ fontFamily: 'var(--font-heading)', color: '#ffffff', marginBottom: '12px' }}>
            Inspect Destinations by Cluster Archetype
          </h3>
          <div style={{ maxWidth: '420px', marginBottom: '16px' }}>
            <select
              className="form-select"
              value={selectedCluster}
              onChange={(e) => setSelectedCluster(e.target.value)}
            >
              {(profiles?.profiles || []).map((p) => (
                <option key={p.Cluster_Name} value={p.Cluster_Name}>
                  {p.Cluster_Name} ({p.Destination_Count} sites)
                </option>
              ))}
            </select>
          </div>

          <div className="table-container">
            <table className="custom-table">
              <thead>
                <tr>
                  <th>Monument</th>
                  <th>Circle</th>
                  <th>State</th>
                  <th>Typology</th>
                  <th>Annual Visits</th>
                  <th>Foreign Share</th>
                  <th>Avg Temp</th>
                  <th>Rainfall</th>
                  <th>UNESCO</th>
                </tr>
              </thead>
              <tbody>
                {members.map((m, idx) => (
                  <tr key={idx}>
                    <td style={{ fontWeight: 600, color: '#ffffff' }}>{m.Monument_Name}</td>
                    <td>{m.Circle}</td>
                    <td>{m.State}</td>
                    <td>{m.Destination_Type}</td>
                    <td style={{ color: '#38bdf8' }}>{m.Total_Tourist_Visits?.toLocaleString()}</td>
                    <td>{m.Foreign_Tourist_Share?.toFixed(1)}%</td>
                    <td>{m.Annual_Avg_Temp_C?.toFixed(1)}°C</td>
                    <td>{m.Annual_Total_Rainfall_mm?.toFixed(0)} mm</td>
                    <td>{m.Is_UNESCO_Site === 1 ? '★ Yes' : 'No'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
