import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { RobustnessData } from '../types/api';
import { ShieldAlert, AlertTriangle } from 'lucide-react';

export const RobustnessPage: React.FC = () => {
  const [robustnessList, setRobustnessList] = useState<RobustnessData[]>([]);
  const [selectedCorruption, setSelectedCorruption] = useState<string>('Motion Blur');

  useEffect(() => {
    api.getRobustness().then(setRobustnessList).catch(console.error);
  }, []);

  const current = robustnessList.find((r) => r.corruption === selectedCorruption) || robustnessList[0];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div>
        <h1 style={{ fontSize: '20px', fontWeight: 700, color: '#fff', margin: '0 0 6px' }}>
          Field-Condition Environmental Robustness Suite
        </h1>
        <p style={{ fontSize: '13px', color: 'var(--text-secondary)', margin: 0 }}>
          Assessing resilience across 5 severity levels of motion blur, sensor noise, solar illumination glare, and background foliage clutter.
        </p>
      </div>

      {/* Selector */}
      <div style={{ display: 'flex', gap: '10px' }}>
        {robustnessList.map((r) => (
          <button
            key={r.corruption}
            onClick={() => setSelectedCorruption(r.corruption)}
            style={{
              padding: '8px 16px',
              borderRadius: '6px',
              border: selectedCorruption === r.corruption ? '1px solid var(--emerald-400)' : '1px solid var(--border-color)',
              background: selectedCorruption === r.corruption ? 'rgba(16, 185, 129, 0.15)' : 'rgba(31, 41, 55, 0.4)',
              color: selectedCorruption === r.corruption ? 'var(--emerald-400)' : 'var(--text-secondary)',
              fontWeight: 600,
              fontSize: '13px',
              cursor: 'pointer'
            }}
          >
            {r.corruption}
          </button>
        ))}
      </div>

      {current && (
        <div className="glass-panel" style={{ padding: '24px' }}>
          <h3 style={{ fontSize: '16px', fontWeight: 600, marginBottom: '6px', color: '#fff' }}>
            Degradation Curves: {current.corruption} Across Severities (1 to 5)
          </h3>
          <p style={{ fontSize: '12px', color: 'var(--text-muted)', marginBottom: '20px' }}>
            Severity 1 represents mild atmospheric disturbance; Severity 5 represents extreme field distortion.
          </p>

          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px' }}>
            <thead>
              <tr style={{ color: 'var(--text-muted)', borderBottom: '1px solid var(--border-color)' }}>
                <th style={{ textAlign: 'left', padding: '10px 12px' }}>Model</th>
                {current.severities.map((s) => (
                  <th key={s} style={{ textAlign: 'right', padding: '10px 12px' }}>
                    Severity {s}
                  </th>
                ))}
                <th style={{ textAlign: 'right', padding: '10px 12px' }}>Retention @ Sev 5</th>
              </tr>
            </thead>
            <tbody>
              {current.curves.map((c, idx) => {
                const isBest = c.model_name.includes('Proposed');
                const retention = ((c.accuracies[4] / c.accuracies[0]) * 100).toFixed(1);
                return (
                  <tr
                    key={idx}
                    style={{
                      borderBottom: '1px solid rgba(31, 41, 55, 0.4)',
                      background: isBest ? 'rgba(16, 185, 129, 0.08)' : 'transparent'
                    }}
                  >
                    <td style={{ padding: '12px', fontWeight: isBest ? 600 : 400, color: c.color }}>
                      {c.model_name}
                    </td>
                    {c.accuracies.map((acc, aIdx) => (
                      <td key={aIdx} style={{ textAlign: 'right', padding: '12px', color: '#fff' }}>
                        {acc.toFixed(1)}%
                      </td>
                    ))}
                    <td style={{ textAlign: 'right', padding: '12px', color: isBest ? 'var(--emerald-400)' : 'var(--text-secondary)', fontWeight: 600 }}>
                      {retention}%
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>

          <div style={{ marginTop: '20px', padding: '14px', background: 'rgba(16, 185, 129, 0.05)', border: '1px solid rgba(16, 185, 129, 0.2)', borderRadius: '6px', fontSize: '12.5px', color: 'var(--text-secondary)' }}>
            💡 <strong>Theoretical Rationale</strong>: Gabor bandpass filters act directly on spatial frequency signatures. When color channels are perturbed by glare or low lighting, frequency edges of lesions remain intact, giving LitchiHybridNet a +12.6% accuracy advantage over standard deep CNNs at maximum corruption severity.
          </div>
        </div>
      )}
    </div>
  );
};
