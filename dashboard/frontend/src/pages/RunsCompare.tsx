import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { RunSummary } from '../types/api';
import { Layers, CheckCircle } from 'lucide-react';

export const RunsComparePage: React.FC = () => {
  const [runs, setRuns] = useState<RunSummary[]>([]);

  useEffect(() => {
    api.getRuns().then(setRuns).catch(console.error);
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div>
        <h1 style={{ fontSize: '20px', fontWeight: 700, color: '#fff', margin: '0 0 6px' }}>
          Experiment Runs & Multi-Seed Comparison
        </h1>
        <p style={{ fontSize: '13px', color: 'var(--text-secondary)', margin: 0 }}>
          Index of all executed training runs, checkpoints, validation metrics, and duration across seeds.
        </p>
      </div>

      <div className="glass-panel" style={{ padding: '20px' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px', textAlign: 'left' }}>
          <thead>
            <tr style={{ color: 'var(--text-muted)', borderBottom: '1px solid var(--border-color)' }}>
              <th style={{ padding: '10px 12px' }}>Run ID / Name</th>
              <th style={{ padding: '10px 12px' }}>Architecture</th>
              <th style={{ padding: '10px 12px' }}>Seed</th>
              <th style={{ padding: '10px 12px' }}>Status</th>
              <th style={{ padding: '10px 12px' }}>Best Epoch</th>
              <th style={{ padding: '10px 12px' }}>Best Val F1</th>
              <th style={{ padding: '10px 12px' }}>Best Val Acc</th>
              <th style={{ padding: '10px 12px' }}>Duration (s)</th>
            </tr>
          </thead>
          <tbody>
            {runs.length > 0 ? (
              runs.map((r) => (
                <tr key={r.id} style={{ borderBottom: '1px solid rgba(31, 41, 55, 0.4)' }}>
                  <td style={{ padding: '12px', fontWeight: 600, color: '#fff' }}>{r.name}</td>
                  <td style={{ padding: '12px', color: 'var(--text-secondary)' }}>{r.model_type}</td>
                  <td style={{ padding: '12px' }}>{r.seed}</td>
                  <td style={{ padding: '12px' }}>
                    <span style={{
                      background: r.status === 'completed' ? 'rgba(16, 185, 129, 0.15)' : 'rgba(59, 130, 246, 0.15)',
                      color: r.status === 'completed' ? 'var(--emerald-400)' : 'var(--blue-500)',
                      fontSize: '11px',
                      padding: '3px 8px',
                      borderRadius: '4px',
                      fontWeight: 600
                    }}>
                      {r.status.toUpperCase()}
                    </span>
                  </td>
                  <td style={{ padding: '12px' }}>{r.best_epoch || 1}</td>
                  <td style={{ padding: '12px', color: 'var(--emerald-400)', fontWeight: 600 }}>
                    {r.best_val_f1 ? r.best_val_f1.toFixed(4) : '-'}
                  </td>
                  <td style={{ padding: '12px', color: 'var(--cyan-400)' }}>
                    {r.best_val_acc ? `${(r.best_val_acc * 100).toFixed(1)}%` : '-'}
                  </td>
                  <td style={{ padding: '12px' }}>{r.total_time_s ? `${r.total_time_s.toFixed(1)}s` : '-'}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={8} style={{ padding: '24px', textAlign: 'center', color: 'var(--text-muted)' }}>
                  No runs registered yet. Launch a run in the Training Studio.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
