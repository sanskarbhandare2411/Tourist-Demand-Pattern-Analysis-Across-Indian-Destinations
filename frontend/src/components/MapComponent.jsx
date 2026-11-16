import React from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup, Tooltip } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const colorMap = {
  'Tier-1 (>340k)': '#ef4444',
  'Tier-2 (125k-340k)': '#f59e0b',
  'Tier-3 (40k-125k)': '#3b82f6',
  'Tier-4 (<40k)': '#10b981',
};

export default function MapComponent({ markers = [] }) {
  const center = [22.0, 79.0];

  return (
    <div style={{ position: 'relative', width: '100%', borderRadius: '16px', overflow: 'hidden' }}>
      <MapContainer
        center={center}
        zoom={5}
        scrollWheelZoom={false}
        style={{ height: '520px', width: '100%' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {markers.map((m, idx) => {
          const markerColor = colorMap[m.footfall_tier] || '#3b82f6';
          const radius = m.is_unesco ? 9 : 6;

          return (
            <CircleMarker
              key={`${m.name}-${idx}`}
              center={[m.lat, m.lon]}
              radius={radius}
              pathOptions={{
                color: markerColor,
                fillColor: markerColor,
                fillOpacity: 0.8,
                weight: 2,
              }}
            >
              <Tooltip>
                <b>{m.name}</b> ({m.total_visits?.toLocaleString()} visits)
              </Tooltip>
              <Popup>
                <div style={{ minWidth: '200px', color: '#0f172a', fontFamily: 'sans-serif' }}>
                  {m.image_url && (
                    <img
                      src={m.image_url}
                      alt={m.name}
                      style={{ width: '100%', height: '110px', objectFit: 'cover', borderRadius: '8px', marginBottom: '8px' }}
                    />
                  )}
                  <h4 style={{ margin: '0 0 4px 0', fontSize: '1rem', color: '#0f172a' }}>{m.name}</h4>
                  <div style={{ fontSize: '0.8rem', color: '#475569', marginBottom: '6px' }}>
                    📍 {m.circle} Circle, <b>{m.state}</b>
                  </div>
                  <hr style={{ margin: '6px 0', border: 'none', borderTop: '1px solid #cbd5e1' }} />
                  <div style={{ fontSize: '0.82rem', lineHeight: '1.5' }}>
                    <div><b>Status:</b> {m.is_unesco ? '★ UNESCO World Heritage' : 'Protected Monument'}</div>
                    <div><b>Annual Visits:</b> {m.total_visits?.toLocaleString()}</div>
                    <div><b>Foreign Share:</b> {m.foreign_share_pct}%</div>
                    <div><b>Climate:</b> {m.avg_temp_c}°C, {m.annual_rainfall_mm} mm rain</div>
                    <div><b>Tier:</b> {m.footfall_tier}</div>
                  </div>
                </div>
              </Popup>
            </CircleMarker>
          );
        })}
      </MapContainer>
    </div>
  );
}
