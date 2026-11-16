import React from 'react';

export default function KPICard({ title, value, subtitle, icon: Icon, accentColor = '#38bdf8' }) {
  return (
    <div className="kpi-card" style={{ borderColor: 'rgba(255, 255, 255, 0.08)' }}>
      <div className="kpi-title">
        <span>{title}</span>
        {Icon && <Icon size={16} color={accentColor} />}
      </div>
      <div className="kpi-value">{value}</div>
      {subtitle && <div className="kpi-subtitle">{subtitle}</div>}
    </div>
  );
}
