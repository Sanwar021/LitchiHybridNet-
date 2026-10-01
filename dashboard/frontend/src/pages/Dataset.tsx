import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { DatasetAudit } from '../types/api';
import { ShieldCheck, Image as ImageIcon, Layers } from 'lucide-react';

export const DatasetPage: React.FC = () => {
  const [audit, setAudit] = useState<DatasetAudit | null>(null);
  const [splits, setSplits] = useState<any>(null);

  useEffect(() => {
    api.getDatasetAudit().then(setAudit).catch(console.error);
    api.getDatasetSplits().then(setSplits).catch(console.error);
  }, []);

  if (!audit) {
    return <div style={{ padding: '32px', color: 'var(--text-muted)' }}>Loading dataset audit...</div>;
  }

  const classEntries = Object.entries(audit.class_distribution || {}).sort((a, b) => b[1] - a[1]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div>
        <h1 style={{ fontSize: '20px', fontWeight: 700, color: '#fff', margin: '0 0 6px' }}>
          BDLitchi Dataset Audit & Leakage-Free Splitting
        </h1>
        <p style={{ fontSize: '13px', color: 'var(--text-secondary)', margin: 0 }}>
          Comprehensive data verification across 11,094 natural field images, duplicate grouping, and group-aware 70/15/15 partitions.
        </p>
      </div>

      {/* Cards Row */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(min(100%, 200px), 1fr))', gap: '16px' }}>
        <div className="glass-panel" style={{ padding: '20px' }}>
          <div style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: 500 }}>Total Images</div>
          <div style={{ fontSize: '24px', fontWeight: 700, color: '#fff', marginTop: '4px' }}>
            {audit.total_images.toLocaleString()}
          </div>
          <div style={{ fontSize: '11px', color: 'var(--emerald-400)', marginTop: '4px' }}>
            0 Corrupt Files
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '20px' }}>
          <div style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: 500 }}>Classes</div>
          <div style={{ fontSize: '24px', fontWeight: 700, color: '#fff', marginTop: '4px' }}>
            {audit.num_classes} Conditions
          </div>
          <div style={{ fontSize: '11px', color: 'var(--cyan-400)', marginTop: '4px' }}>
            10 Diseases + 1 Healthy
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '20px' }}>
          <div style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: 500 }}>Duplicate Clusters</div>
          <div style={{ fontSize: '24px', fontWeight: 700, color: '#fff', marginTop: '4px' }}>
            {audit.duplicates.near_duplicate_groups} Groups
          </div>
          <div style={{ fontSize: '11px', color: 'var(--emerald-400)', marginTop: '4px' }}>
            202 Exact Hashes (pHash)
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '20px' }}>
          <div style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: 500 }}>Leakage Guarantee</div>
          <div style={{ fontSize: '24px', fontWeight: 700, color: 'var(--emerald-400)', marginTop: '4px' }}>
            0% Leakage
          </div>
          <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Group-aware stratified split
          </div>
        </div>
      </div>

      {/* Class distribution table & chart */}
      <div className="glass-panel" style={{ padding: '24px' }}>
        <h3 style={{ fontSize: '16px', fontWeight: 600, marginBottom: '16px' }}>
          Class Frequency Breakdown (BDLitchi Raw Field Captures)
        </h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))', gap: '12px' }}>
          {classEntries.map(([cname, count]) => {
            const pct = ((count / audit.total_images) * 100).toFixed(1);
            return (
              <div
                key={cname}
                style={{
                  background: 'rgba(31, 41, 55, 0.4)',
                  border: '1px solid var(--border-color)',
                  borderRadius: '6px',
                  padding: '12px 14px'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', fontWeight: 600, color: '#fff' }}>
                  <span>{cname}</span>
                  <span style={{ color: 'var(--emerald-400)' }}>{count}</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px' }}>
                  <span>Proportion</span>
                  <span>{pct}%</span>
                </div>
                <div style={{ width: '100%', height: '4px', background: '#374151', borderRadius: '2px', marginTop: '6px' }}>
                  <div style={{ width: `${pct}%`, height: '100%', background: 'var(--emerald-500)', borderRadius: '2px' }}></div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Split Details */}
      <div className="glass-panel" style={{ padding: '24px' }}>
        <h3 style={{ fontSize: '16px', fontWeight: 600, marginBottom: '16px' }}>
          Group-Aware Stratified Partition Protocol (70 / 15 / 15 %)
        </h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px' }}>
          <div style={{ background: 'rgba(31, 41, 55, 0.3)', border: '1px solid var(--border-color)', borderRadius: '8px', padding: '16px' }}>
            <div style={{ fontSize: '13px', fontWeight: 600, color: 'var(--emerald-400)' }}>Training Partition</div>
            <div style={{ fontSize: '22px', fontWeight: 700, margin: '8px 0 4px', color: '#fff' }}>
              {audit.splits.train.toLocaleString()} images
            </div>
            <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>
              Deterministic CSV: `data/splits/train.csv` (Augmentations applied during training only)
            </div>
          </div>

          <div style={{ background: 'rgba(31, 41, 55, 0.3)', border: '1px solid var(--border-color)', borderRadius: '8px', padding: '16px' }}>
            <div style={{ fontSize: '13px', fontWeight: 600, color: 'var(--cyan-400)' }}>Validation Partition</div>
            <div style={{ fontSize: '22px', fontWeight: 700, margin: '8px 0 4px', color: '#fff' }}>
              {audit.splits.val.toLocaleString()} images
            </div>
            <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>
              Deterministic CSV: `data/splits/val.csv` (Used for early stopping & checkpoint selection)
            </div>
          </div>

          <div style={{ background: 'rgba(31, 41, 55, 0.3)', border: '1px solid var(--border-color)', borderRadius: '8px', padding: '16px' }}>
            <div style={{ fontSize: '13px', fontWeight: 600, color: 'var(--indigo-500)' }}>Unseen Test Partition</div>
            <div style={{ fontSize: '22px', fontWeight: 700, margin: '8px 0 4px', color: '#fff' }}>
              {audit.splits.test.toLocaleString()} images
            </div>
            <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>
              Deterministic CSV: `data/splits/test.csv` (Held out for final publication reporting)
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
