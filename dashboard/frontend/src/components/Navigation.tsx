import React from 'react';
import {
  LayoutDashboard,
  Database,
  PlayCircle,
  Layers,
  BarChart3,
  Sliders,
  ShieldCheck,
  Eye,
  Microscope,
  Zap,
  FileText,
  Terminal,
  Settings,
} from 'lucide-react';

export type PageId =
  | 'overview'
  | 'dataset'
  | 'training'
  | 'runs'
  | 'results'
  | 'ablations'
  | 'robustness'
  | 'explainability'
  | 'inference'
  | 'efficiency'
  | 'paper'
  | 'jobs'
  | 'settings';

interface NavigationProps {
  currentPage: PageId;
  onSelectPage: (page: PageId) => void;
  activeJobCount: number;
}

const navItems: { id: PageId; label: string; icon: React.ReactNode; badge?: string }[] = [
  { id: 'overview', label: 'Overview', icon: <LayoutDashboard size={18} /> },
  { id: 'dataset', label: 'Dataset & Audit', icon: <Database size={18} /> },
  { id: 'training', label: 'Training Studio', icon: <PlayCircle size={18} /> },
  { id: 'runs', label: 'Runs & Compare', icon: <Layers size={18} /> },
  { id: 'results', label: 'Results & Baselines', icon: <BarChart3 size={18} /> },
  { id: 'ablations', label: 'Ablations', icon: <Sliders size={18} /> },
  { id: 'robustness', label: 'Robustness Suite', icon: <ShieldCheck size={18} /> },
  { id: 'explainability', label: 'Explainability', icon: <Eye size={18} /> },
  { id: 'inference', label: 'Inference Lab', icon: <Microscope size={18} /> },
  { id: 'efficiency', label: 'Efficiency & Edge', icon: <Zap size={18} /> },
  { id: 'paper', label: 'Paper Assets', icon: <FileText size={18} /> },
  { id: 'jobs', label: 'Jobs & Logs', icon: <Terminal size={18} /> },
  { id: 'settings', label: 'System & Config', icon: <Settings size={18} /> },
];

export const Sidebar: React.FC<NavigationProps> = ({ currentPage, onSelectPage, activeJobCount }) => {
  return (
    <aside style={{
      width: '260px',
      background: 'var(--bg-secondary)',
      borderRight: '1px solid var(--border-color)',
      display: 'flex',
      flexDirection: 'column',
      height: '100vh',
      position: 'fixed',
      left: 0,
      top: 0,
      zIndex: 40
    }}>
      {/* Brand */}
      <div style={{
        padding: '20px 16px',
        borderBottom: '1px solid var(--border-color)',
        display: 'flex',
        alignItems: 'center',
        gap: '12px'
      }}>
        <div style={{
          width: '38px',
          height: '38px',
          borderRadius: '8px',
          background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '20px',
          boxShadow: '0 2px 8px rgba(16, 185, 129, 0.3)'
        }}>
          🌿
        </div>
        <div>
          <div style={{ fontWeight: 700, fontSize: '15px', color: 'var(--text-primary)', letterSpacing: '-0.3px' }}>
            LitchiHybridNet
          </div>
          <div style={{ fontSize: '11px', color: 'var(--emerald-400)', fontWeight: 500 }}>
            Research Control Center
          </div>
        </div>
      </div>

      {/* Nav List */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '12px 8px' }}>
        <div style={{ fontSize: '10px', textTransform: 'uppercase', color: 'var(--text-muted)', fontWeight: 700, padding: '8px 12px', letterSpacing: '0.8px' }}>
          Navigation
        </div>
        {navItems.map((item) => {
          const isActive = currentPage === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onSelectPage(item.id)}
              style={{
                width: '100%',
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                padding: '10px 14px',
                borderRadius: '6px',
                border: 'none',
                background: isActive ? 'rgba(16, 185, 129, 0.15)' : 'transparent',
                color: isActive ? 'var(--emerald-400)' : 'var(--text-secondary)',
                fontWeight: isActive ? 600 : 500,
                fontSize: '13.5px',
                cursor: 'pointer',
                textAlign: 'left',
                transition: 'all 0.15s ease',
                marginBottom: '2px',
                borderLeft: isActive ? '3px solid var(--emerald-400)' : '3px solid transparent'
              }}
            >
              <span style={{ color: isActive ? 'var(--emerald-400)' : 'var(--text-muted)' }}>
                {item.icon}
              </span>
              <span style={{ flex: 1 }}>{item.label}</span>
              {item.id === 'jobs' && activeJobCount > 0 && (
                <span style={{
                  background: 'var(--emerald-500)',
                  color: '#fff',
                  fontSize: '10px',
                  padding: '2px 6px',
                  borderRadius: '10px',
                  fontWeight: 700
                }}>
                  {activeJobCount}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* Footer Status */}
      <div style={{
        padding: '14px 16px',
        borderTop: '1px solid var(--border-color)',
        fontSize: '12px',
        color: 'var(--text-muted)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#10b981', display: 'inline-block' }}></span>
          <span>FastAPI Connected</span>
        </div>
        <span style={{ fontSize: '11px', color: 'var(--emerald-400)' }}>v1.0.0</span>
      </div>
    </aside>
  );
};
