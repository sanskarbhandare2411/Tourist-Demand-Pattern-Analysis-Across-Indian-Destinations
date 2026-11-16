import React from 'react';
import {
  Compass,
  TrendingUp,
  MapPin,
  Calendar,
  CloudRain,
  Cpu,
  Network,
  Lightbulb,
  X,
  SlidersHorizontal,
} from 'lucide-react';

export const PAGES = [
  { id: 'overview', title: '1. Overview', icon: Compass },
  { id: 'demand', title: '2. Tourism Demand Analysis', icon: TrendingUp },
  { id: 'destination', title: '3. Destination Analysis', icon: MapPin },
  { id: 'seasonal', title: '4. Seasonal Analysis', icon: Calendar },
  { id: 'weather', title: '5. Weather & Tourism', icon: CloudRain },
  { id: 'ml', title: '6. ML Demand Prediction', icon: Cpu },
  { id: 'clustering', title: '7. Destination Clustering', icon: Network },
  { id: 'recommendations', title: '8. Insights & Recommendations', icon: Lightbulb },
];

export default function Sidebar({
  activePage,
  setActivePage,
  filterOptions = {},
  filters = {},
  setFilters,
  isOpen = false,
  setIsOpen,
  activeCount = 144,
  totalCount = 144,
}) {
  const handleFilterChange = (key, value) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  };

  return (
    <aside className={`sidebar ${isOpen ? 'open' : ''}`}>
      {/* Platform Branding */}
      <div style={{ padding: '24px 20px 16px 20px', borderBottom: '1px solid var(--border-subtle)' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span className="pulse-dot"></span>
            <span style={{ fontSize: '0.72rem', color: 'var(--accent-cyan)', fontWeight: 800, letterSpacing: '0.8px' }}>
              LIVE PLATFORM
            </span>
          </div>
          {setIsOpen && (
            <button
              onClick={() => setIsOpen(false)}
              style={{ background: 'none', border: 'none', color: '#94a3b8', cursor: 'pointer', display: 'none' }}
              className="mobile-close-btn"
            >
              <X size={20} />
            </button>
          )}
        </div>
        <h2 style={{ fontFamily: 'var(--font-heading)', fontSize: '1.35rem', fontWeight: 800, color: '#ffffff', margin: 0 }}>
          Tourist Demand
        </h2>
        <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', margin: '2px 0 0 0', fontWeight: 500 }}>
          Pattern Analysis & Intelligence
        </p>
      </div>

      {/* Navigation Menu */}
      <div style={{ padding: '14px 0', borderBottom: '1px solid var(--border-subtle)' }}>
        <div style={{ padding: '0 18px 8px 18px', fontSize: '0.72rem', fontWeight: 700, color: 'var(--text-dim)', textTransform: 'uppercase', letterSpacing: '0.8px' }}>
          Navigation Menu
        </div>
        {PAGES.map((page) => {
          const Icon = page.icon;
          const isActive = activePage === page.id;
          return (
            <div
              key={page.id}
              className={`nav-item ${isActive ? 'active' : ''}`}
              onClick={() => {
                setActivePage(page.id);
                if (setIsOpen) setIsOpen(false);
              }}
            >
              <Icon size={18} color={isActive ? '#38bdf8' : '#94a3b8'} />
              <span>{page.title}</span>
            </div>
          );
        })}
      </div>

      {/* Global Destination Filters */}
      <div style={{ padding: '18px 20px', flex: 1 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px' }}>
          <SlidersHorizontal size={15} color="var(--accent-cyan)" />
          <span style={{ fontSize: '0.78rem', fontWeight: 700, color: '#e2e8f0', textTransform: 'uppercase', letterSpacing: '0.6px' }}>
            Destination Filters
          </span>
        </div>

        {/* State Filter */}
        <div className="form-group">
          <label className="form-label" style={{ fontSize: '0.78rem' }}>Filter by State</label>
          <select
            className="form-select"
            value={filters.state || 'All States'}
            onChange={(e) => handleFilterChange('state', e.target.value)}
          >
            {(filterOptions.states || ['All States']).map((st) => (
              <option key={st} value={st}>{st}</option>
            ))}
          </select>
        </div>

        {/* Visitor Type */}
        <div className="form-group">
          <label className="form-label" style={{ fontSize: '0.78rem' }}>Visitor Type</label>
          <select
            className="form-select"
            value={filters.visitorType || 'All Tourists (Total)'}
            onChange={(e) => handleFilterChange('visitorType', e.target.value)}
          >
            {(filterOptions.tourist_types || ['All Tourists (Total)', 'Domestic Only', 'Foreign Only']).map((vt) => (
              <option key={vt} value={vt}>{vt}</option>
            ))}
          </select>
        </div>

        {/* Heritage Typology */}
        <div className="form-group">
          <label className="form-label" style={{ fontSize: '0.78rem' }}>Heritage Typology</label>
          <select
            className="form-select"
            value={filters.typology || 'All Typologies'}
            onChange={(e) => handleFilterChange('typology', e.target.value)}
          >
            {(filterOptions.typologies || ['All Typologies']).map((typ) => (
              <option key={typ} value={typ}>{typ}</option>
            ))}
          </select>
        </div>

        {/* UNESCO Classification */}
        <div className="form-group">
          <label className="form-label" style={{ fontSize: '0.78rem' }}>Heritage Classification</label>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', fontSize: '0.82rem', color: '#cbd5e1' }}>
            {[
              { id: 'all', label: 'All Sites' },
              { id: 'unesco', label: 'UNESCO Sites Only' },
              { id: 'non-unesco', label: 'Non-UNESCO Only' },
            ].map((option) => (
              <label key={option.id} style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
                <input
                  type="radio"
                  name="unesco_filter"
                  checked={(filters.unesco || 'all') === option.id}
                  onChange={() => handleFilterChange('unesco', option.id)}
                  style={{ accentColor: 'var(--accent-cyan)' }}
                />
                <span>{option.label}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Filter Stats */}
        <div style={{ marginTop: '16px', padding: '10px 14px', background: 'rgba(255, 255, 255, 0.03)', borderRadius: '10px', border: '1px solid var(--border-subtle)', fontSize: '0.78rem', color: '#94a3b8' }}>
          Active Filter: <b style={{ color: 'var(--accent-cyan)' }}>{activeCount}</b> / {totalCount} destinations
        </div>
      </div>
    </aside>
  );
}
