import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { FileText, Download, CheckCircle2, Copy } from 'lucide-react';

export const PaperAssetsPage: React.FC = () => {
  const [figures, setFigures] = useState<any[]>([]);
  const [tables, setTables] = useState<any[]>([]);
  const [checklist, setChecklist] = useState<any[]>([]);
  const [bibtex, setBibtex] = useState<string>('');

  useEffect(() => {
    api.getPaperFigures().then(setFigures).catch(console.error);
    api.getPaperTables().then(setTables).catch(console.error);
    api.getPaperChecklist().then(setChecklist).catch(console.error);
    api.getBibtex().then((r) => setBibtex(r.bibtex)).catch(console.error);
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div>
        <h1 style={{ fontSize: '20px', fontWeight: 700, color: '#fff', margin: '0 0 6px' }}>
          IEEE Manuscript Assets & Submission Package
        </h1>
        <p style={{ fontSize: '13px', color: 'var(--text-secondary)', margin: 0 }}>
          Direct access to high-resolution figures (300+ DPI), formatted LaTeX tables, verified BibTeX citations, and publication QA checklist.
        </p>
      </div>

      {/* QA Checklist */}
      <div className="glass-panel" style={{ padding: '24px' }}>
        <h3 style={{ fontSize: '15px', fontWeight: 600, marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <CheckCircle2 size={16} color="var(--emerald-400)" /> Publication Quality Assurance Checklist
        </h3>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '12px' }}>
          {checklist.map((item, idx) => (
            <div
              key={idx}
              style={{
                background: 'rgba(31, 41, 55, 0.4)',
                border: '1px solid rgba(16, 185, 129, 0.3)',
                borderRadius: '6px',
                padding: '12px 14px',
                display: 'flex',
                alignItems: 'flex-start',
                gap: '10px'
              }}
            >
              <CheckCircle2 size={16} color="var(--emerald-400)" style={{ flexShrink: 0, marginTop: '2px' }} />
              <div>
                <div style={{ fontSize: '13px', fontWeight: 600, color: '#fff' }}>{item.item}</div>
                <div style={{ fontSize: '11.5px', color: 'var(--text-secondary)', marginTop: '2px' }}>
                  {item.evidence}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Figures Gallery */}
      <div className="glass-panel" style={{ padding: '24px' }}>
        <h3 style={{ fontSize: '15px', fontWeight: 600, marginBottom: '16px' }}>
          Publication Vector & High-Res Figures (figures/)
        </h3>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))', gap: '16px' }}>
          {figures.map((fig, idx) => (
            <div
              key={idx}
              style={{
                background: 'rgba(31, 41, 55, 0.3)',
                border: '1px solid var(--border-color)',
                borderRadius: '8px',
                overflow: 'hidden'
              }}
            >
              <div style={{ height: '140px', background: '#0a0f1d', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <img
                  src={`http://localhost:8000${fig.url}`}
                  alt={fig.name}
                  style={{ maxHeight: '100%', maxWidth: '100%', objectFit: 'contain' }}
                  onError={(e: any) => {
                    e.target.style.display = 'none';
                  }}
                />
              </div>
              <div style={{ padding: '12px' }}>
                <div style={{ fontSize: '12px', fontWeight: 600, color: '#fff', wordBreak: 'break-all' }}>{fig.name}</div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '6px' }}>
                  <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>{fig.size_kb} KB ({fig.format})</span>
                  <a
                    href={`http://localhost:8000${fig.url}`}
                    target="_blank"
                    rel="noreferrer"
                    style={{ fontSize: '11px', color: 'var(--emerald-400)', textDecoration: 'none', fontWeight: 600 }}
                  >
                    View High-Res
                  </a>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* BibTeX */}
      <div className="glass-panel" style={{ padding: '24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
          <h3 style={{ fontSize: '15px', fontWeight: 600, margin: 0 }}>Verified References (references.bib)</h3>
          <button
            onClick={() => {
              navigator.clipboard.writeText(bibtex);
              alert('BibTeX copied to clipboard!');
            }}
            style={{
              background: 'transparent',
              border: '1px solid var(--border-color)',
              color: 'var(--text-secondary)',
              padding: '6px 12px',
              borderRadius: '6px',
              fontSize: '12px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px'
            }}
          >
            <Copy size={13} /> Copy BibTeX
          </button>
        </div>

        <pre style={{
          background: '#0a0f1d',
          border: '1px solid #1f2937',
          padding: '14px',
          borderRadius: '6px',
          fontSize: '12px',
          color: '#34d399',
          maxHeight: '180px',
          overflowY: 'auto'
        }}>
          {bibtex}
        </pre>
      </div>
    </div>
  );
};
