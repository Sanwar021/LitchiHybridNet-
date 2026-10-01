import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { AblationGroup } from '../types/api';
import { Sliders } from 'lucide-react';

export const AblationsPage: React.FC = () => {
  const [ablations, setAblations] = useState<AblationGroup[]>([]);

  useEffect(() => {
    api.getAblations().then(setAblations).catch(console.error);
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div>
        <h1 style={{ fontSize: '20px', fontWeight: 700, color: '#fff', margin: '0 0 6px' }}>
          Comprehensive Architectural Ablation Studies
        </h1>
        <p style={{ fontSize: '13px', color: 'var(--text-secondary)', margin: 0 }}>
          Quantifying the individual contribution of dual-branch texture fusion, learnable Gabor filters, cross-gating attention, and filter bank scales.
        </p>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        {ablations.map((group, idx) => (
          <div key={idx} className="glass-panel" style={{ padding: '24px' }}>
            <h3 style={{ fontSize: '15px', fontWeight: 600, marginBottom: '16px', color: 'var(--emerald-400)' }}>
              Ablation Dimension: {group.group}
            </h3>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '14px' }}>
              {group.items.map((item, itemIdx) => {
                const isBest = item.variant.includes('Proposed') || item.variant.includes('LitchiHybridNet') || item.variant.includes('Default');
                return (
                  <div
                    key={itemIdx}
                    style={{
                      background: isBest ? 'rgba(16, 185, 129, 0.08)' : 'rgba(31, 41, 55, 0.4)',
                      border: isBest ? '1px solid rgba(16, 185, 129, 0.4)' : '1px solid var(--border-color)',
                      borderRadius: '8px',
                      padding: '16px'
                    }}
                  >
                    <div style={{ fontSize: '13px', fontWeight: 600, color: isBest ? 'var(--emerald-400)' : '#fff', minHeight: '36px' }}>
                      {item.variant}
                    </div>

                    <div style={{ marginTop: '12px' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px' }}>
                        <span style={{ color: 'var(--text-muted)' }}>Accuracy</span>
                        <span style={{ fontWeight: 600, color: '#fff' }}>{item.accuracy_mean.toFixed(2)}%</span>
                      </div>
                      <div style={{ width: '100%', height: '4px', background: '#374151', borderRadius: '2px', margin: '4px 0 8px' }}>
                        <div style={{ width: `${item.accuracy_mean}%`, height: '100%', background: isBest ? 'var(--emerald-500)' : 'var(--blue-500)', borderRadius: '2px' }}></div>
                      </div>

                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px' }}>
                        <span style={{ color: 'var(--text-muted)' }}>Macro F1</span>
                        <span style={{ fontWeight: 600, color: 'var(--cyan-400)' }}>{item.macro_f1_mean.toFixed(4)}</span>
                      </div>

                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '11px', color: 'var(--text-muted)', marginTop: '6px' }}>
                        <span>Params</span>
                        <span>{item.params_m.toFixed(2)} M</span>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
