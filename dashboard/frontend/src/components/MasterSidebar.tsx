import React from 'react';
import { Settings, Sliders, Microscope } from 'lucide-react';
import { PageId } from './Navigation';

interface MasterSidebarProps {
  currentPage: PageId;
  onSelectPage: (page: PageId) => void;
}

// Our Project Disease Conditions (matching thumbnail list from reference)
const diseaseAtlasItems = [
  {
    id: 'overview' as PageId,
    title: 'LitchiHybridNet',
    subtitle: 'Dual-Branch Gabor',
    coverBg: 'linear-gradient(135deg, #c88a4b 0%, #8c5a2b 100%)',
    coverIcon: '🌿',
  },
  {
    id: 'inference' as PageId,
    title: 'Leaf Blight Disease',
    subtitle: 'Necrotic Margin',
    coverBg: 'linear-gradient(135deg, #f97316 0%, #c2410c 100%)',
    coverIcon: '🍂',
  },
  {
    id: 'results' as PageId,
    title: 'Black Spot Disease',
    subtitle: 'High Frequency',
    coverBg: 'linear-gradient(135deg, #eab308 0%, #a16207 100%)',
    coverIcon: '⚫',
  },
  {
    id: 'robustness' as PageId,
    title: 'Red Rust Disease',
    subtitle: 'Cephaleuros Algal',
    coverBg: 'linear-gradient(135deg, #ef4444 0%, #991b1b 100%)',
    coverIcon: '🍁',
  },
  {
    id: 'dataset' as PageId,
    title: 'Healthy Leaf Lamina',
    subtitle: 'BDLitchi Natural',
    coverBg: 'linear-gradient(135deg, #10b981 0%, #065f46 100%)',
    coverIcon: '🍃',
  },
];

// Active Research Engines & Pipelines (matching circular avatar list from reference)
const activePipelines = [
  { name: 'Seed 42 Primary', role: '98.29% Val F1', avatar: '🎯', color: '#f8d356' },
  { name: 'ONNX INT8 Quant', role: '14.8 ms CPU', avatar: '⚡', color: '#ffa066' },
  { name: 'Grad-CAM Studio', role: 'Lesion Saliency', avatar: '🔬', color: '#cbb0f2' },
  { name: 'Robustness Suite', role: '5 Severities', avatar: '🛡️', color: '#a9e858' },
  { name: 'BDLitchi Dataset', role: '11,094 Images', avatar: '🇧🇩', color: '#8ad8ee' },
  { name: 'Multi-Seed CV', role: '5-Seed Mean', avatar: '📊', color: '#f8d356' },
  { name: 'IEEE Manuscript', role: 'Q1 Submission', avatar: '📄', color: '#c88a4b' },
  { name: 'Gabor Filter Bank', role: '24 Orientations', avatar: '🌀', color: '#34d399' },
];

export const MasterSidebar: React.FC<MasterSidebarProps> = ({
  currentPage,
  onSelectPage,
}) => {
  return (
    <aside style={{
      background: 'var(--sidebar-bg)',
      borderRight: '1px solid rgba(212, 163, 115, 0.16)',
      display: 'flex',
      flexDirection: 'column',
      height: '100%',
      padding: '16px 14px 14px',
      userSelect: 'none',
      fontSize: '12px'
    }}>
      {/* 1. Project Profile Header */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '10px',
        padding: '2px 4px 14px',
        borderBottom: '1px solid rgba(212, 163, 115, 0.14)'
      }}>
        <div style={{
          width: '32px',
          height: '32px',
          borderRadius: '50%',
          background: 'linear-gradient(135deg, #c88a4b 0%, #8c5a2b 100%)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '16px',
          border: '1.5px solid rgba(235, 215, 190, 0.35)',
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.4)',
          flexShrink: 0
        }}>
          🌿
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
          <span style={{ fontSize: '13px', fontWeight: 800, color: '#ffffff', lineHeight: 1.2 }}>
            LitchiHybridNet
          </span>
          <span style={{ fontSize: '10.5px', color: 'var(--accent-gold)', fontWeight: 600 }}>
            Q1 Research Control
          </span>
        </div>
      </div>

      {/* Scrollable List */}
      <div style={{ flex: 1, overflowY: 'auto', paddingTop: '14px', paddingRight: '2px' }}>
        
        {/* =================================================== */}
        {/* SECTION: DISEASE ATLAS (Matching Books Section)     */}
        {/* =================================================== */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          color: 'var(--text-light-muted)',
          fontSize: '10px',
          fontWeight: 800,
          textTransform: 'uppercase',
          letterSpacing: '0.6px',
          padding: '2px 4px 8px'
        }}>
          <span>Disease Atlas</span>
          <div
            onClick={() => onSelectPage('dataset')}
            style={{
              width: '18px',
              height: '18px',
              borderRadius: '4px',
              background: 'rgba(212, 163, 115, 0.15)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer'
            }}
          >
            <Sliders size={11} color="var(--text-light-secondary)" />
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '3px', marginBottom: '18px' }}>
          {diseaseAtlasItems.map((b) => {
            const isActive = currentPage === b.id;
            return (
              <div
                key={b.id}
                onClick={() => onSelectPage(b.id)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '9px',
                  padding: '5px 8px',
                  borderRadius: '7px',
                  cursor: 'pointer',
                  background: isActive ? 'rgba(212, 163, 115, 0.22)' : 'transparent',
                  borderLeft: isActive ? '2.5px solid var(--accent-gold)' : '2.5px solid transparent',
                  transition: 'background 0.15s ease'
                }}
                onMouseEnter={(e) => {
                  if (!isActive) e.currentTarget.style.background = 'rgba(212, 163, 115, 0.1)';
                }}
                onMouseLeave={(e) => {
                  if (!isActive) e.currentTarget.style.background = 'transparent';
                }}
              >
                {/* Mini rectangular disease thumbnail */}
                <div style={{
                  width: '18px',
                  height: '24px',
                  borderRadius: '3px',
                  background: b.coverBg,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '9px',
                  boxShadow: '0 2px 5px rgba(0, 0, 0, 0.5)',
                  flexShrink: 0
                }}>
                  {b.coverIcon}
                </div>

                <span style={{
                  fontSize: '11.5px',
                  fontWeight: isActive ? 700 : 500,
                  color: isActive ? '#ffffff' : 'var(--text-light-secondary)',
                  whiteSpace: 'nowrap',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis'
                }}>
                  {b.title}
                </span>
              </div>
            );
          })}
        </div>

        {/* =================================================== */}
        {/* SECTION: ENGINES & PIPELINES (Matching Friends)    */}
        {/* =================================================== */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          color: 'var(--text-light-muted)',
          fontSize: '10px',
          fontWeight: 800,
          textTransform: 'uppercase',
          letterSpacing: '0.6px',
          padding: '2px 4px 8px'
        }}>
          <span>Active Engines</span>
          <div
            onClick={() => onSelectPage('training')}
            style={{
              width: '18px',
              height: '18px',
              borderRadius: '4px',
              background: 'rgba(212, 163, 115, 0.15)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer'
            }}
          >
            <span style={{ fontSize: '12px', color: 'var(--text-light-secondary)', fontWeight: 700 }}>+</span>
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '3px' }}>
          {activePipelines.map((f, i) => (
            <div
              key={i}
              onClick={() => onSelectPage('inference')}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '9px',
                padding: '4px 8px',
                borderRadius: '6px',
                cursor: 'pointer',
                transition: 'background 0.15s ease'
              }}
              onMouseEnter={(e) => (e.currentTarget.style.background = 'rgba(212, 163, 115, 0.1)')}
              onMouseLeave={(e) => (e.currentTarget.style.background = 'transparent')}
            >
              <div style={{
                width: '20px',
                height: '20px',
                borderRadius: '50%',
                background: f.color,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '10px',
                flexShrink: 0
              }}>
                {f.avatar}
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
                <span style={{
                  fontSize: '11.5px',
                  fontWeight: 600,
                  color: 'var(--text-light-secondary)',
                  whiteSpace: 'nowrap',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis'
                }}>
                  {f.name}
                </span>
              </div>
            </div>
          ))}

          {/* See more link */}
          <div style={{ padding: '6px 8px' }}>
            <span
              onClick={() => onSelectPage('results')}
              style={{
                fontSize: '11px',
                color: 'var(--accent-gold)',
                fontWeight: 700,
                cursor: 'pointer',
                textDecoration: 'underline'
              }}
            >
              See all 13 modules &rarr;
            </span>
          </div>
        </div>

      </div>

      {/* 3. Bottom Settings Button */}
      <div style={{
        paddingTop: '10px',
        borderTop: '1px solid rgba(212, 163, 115, 0.14)'
      }}>
        <div
          onClick={() => onSelectPage('settings')}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            padding: '6px 8px',
            borderRadius: '6px',
            cursor: 'pointer',
            color: 'var(--text-light-muted)',
            transition: 'color 0.15s ease'
          }}
          onMouseEnter={(e) => (e.currentTarget.style.color = '#ffffff')}
          onMouseLeave={(e) => (e.currentTarget.style.color = 'var(--text-light-muted)')}
        >
          <Settings size={14} />
          <span style={{ fontSize: '11.5px', fontWeight: 600 }}>Settings & Hardware</span>
        </div>
      </div>
    </aside>
  );
};
