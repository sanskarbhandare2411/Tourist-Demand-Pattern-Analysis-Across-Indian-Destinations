import React from 'react';
import { Menu, Terminal, ExternalLink, Activity } from 'lucide-react';

export default function Navbar({ onMenuToggle, currentPageTitle, isOnline = true }) {
  return (
    <header
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '16px 20px',
        marginBottom: '24px',
        background: 'rgba(15, 23, 42, 0.65)',
        backdropFilter: 'blur(14px)',
        border: '1px solid var(--border-subtle)',
        borderRadius: '16px',
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
        <button
          onClick={onMenuToggle}
          style={{
            background: 'rgba(255, 255, 255, 0.05)',
            border: '1px solid var(--border-subtle)',
            borderRadius: '8px',
            color: '#ffffff',
            padding: '6px 10px',
            cursor: 'pointer',
          }}
          className="mobile-toggle-btn"
        >
          <Menu size={18} />
        </button>
        <div>
          <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Platform / </span>
          <span style={{ fontSize: '0.92rem', fontWeight: 700, color: '#ffffff' }}>{currentPageTitle}</span>
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.8rem', color: isOnline ? '#10b981' : '#f43f5e' }}>
          <Activity size={14} />
          <span>{isOnline ? 'FastAPI Backend Online' : 'Connecting to API...'}</span>
        </div>

        <a
          href="/api/docs"
          target="_blank"
          rel="noreferrer"
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '6px',
            fontSize: '0.8rem',
            color: 'var(--accent-cyan)',
            textDecoration: 'none',
            background: 'rgba(56, 189, 248, 0.1)',
            border: '1px solid rgba(56, 189, 248, 0.25)',
            padding: '4px 10px',
            borderRadius: '8px',
            fontWeight: 600,
          }}
        >
          <Terminal size={13} />
          <span>API Docs</span>
          <ExternalLink size={12} />
        </a>
      </div>
    </header>
  );
}
