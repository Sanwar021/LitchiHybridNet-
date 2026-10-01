import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { Eye, Layers, Compass } from 'lucide-react';

export const ExplainabilityPage: React.FC = () => {
  const [gateData, setGateData] = useState<any>(null);
  const [gaborKernels, setGaborKernels] = useState<any>(null);

  useEffect(() => {
    api.getGateAnalysis().then(setGateData).catch(console.error);
    fetch('http://localhost:8000/api/explain/gabor-kernels').then((r) => r.json()).then(setGaborKernels).catch(console.error);
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div>
        <h1 style={{ fontSize: '20px', fontWeight: 700, color: '#fff', margin: '0 0 6px' }}>
          Explainability: Frequency Kernels & Dynamic Gating Weights
        </h1>
        <p style={{ fontSize: '13px', color: 'var(--text-secondary)', margin: 0 }}>
          Visualizing the 24 learnable spatial-frequency Gabor kernels and per-class channel gating distributions between CNN semantics and texture signatures.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
        {/* Gabor Filter Bank Specifications */}
        <div className="glass-panel" style={{ padding: '24px' }}>
          <h3 style={{ fontSize: '15px', fontWeight: 600, marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Compass size={16} color="var(--emerald-400)" /> 24-Filter Directional Gabor Bank
          </h3>

          {gaborKernels ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                <div style={{ background: 'rgba(31, 41, 55, 0.4)', padding: '12px', borderRadius: '6px' }}>
                  <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Orientations (θ)</div>
                  <div style={{ fontSize: '16px', fontWeight: 600, color: '#fff', marginTop: '2px' }}>
                    6 Angles [0°, 30°, 60°, 90°, 120°, 150°]
                  </div>
                </div>

                <div style={{ background: 'rgba(31, 41, 55, 0.4)', padding: '12px', borderRadius: '6px' }}>
                  <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Scales (λ Wavelengths)</div>
                  <div style={{ fontSize: '16px', fontWeight: 600, color: '#fff', marginTop: '2px' }}>
                    4 Radial Bands [3.2 to 14.1 px]
                  </div>
                </div>
              </div>

              <div style={{ background: 'rgba(31, 41, 55, 0.4)', padding: '12px', borderRadius: '6px' }}>
                <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Trainable Gabor Parameters</div>
                <div style={{ fontSize: '14px', color: 'var(--emerald-400)', fontWeight: 600, marginTop: '2px' }}>
                  Only 120 total trainable parameters (θ, λ, σ, γ, ψ × 24)
                </div>
                <div style={{ fontSize: '11.5px', color: 'var(--text-secondary)', marginTop: '4px' }}>
                  Differentiable parameter formulation enables direct backpropagation into filter geometry.
                </div>
              </div>

              <div style={{ marginTop: '8px' }}>
                <img
                  src="http://localhost:8000/static/figures/class_distribution.png"
                  alt="Gabor Filter Representation"
                  style={{ width: '100%', borderRadius: '6px', border: '1px solid var(--border-color)', maxHeight: '180px', objectFit: 'cover' }}
                />
              </div>
            </div>
          ) : (
            <div style={{ color: 'var(--text-muted)', fontSize: '12px' }}>Loading filter specifications...</div>
          )}
        </div>

        {/* Gate Values Analysis */}
        <div className="glass-panel" style={{ padding: '24px' }}>
          <h3 style={{ fontSize: '15px', fontWeight: 600, marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Layers size={16} color="var(--cyan-400)" /> SE-Gate Channel Gating Weights by Disease
          </h3>

          {gateData && gateData.per_class_gate_weights ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', maxHeight: '380px', overflowY: 'auto' }}>
              {Object.entries(gateData.per_class_gate_weights).map(([cname, weights]: [string, any]) => {
                const gaborPct = Math.round(weights.gabor_texture * 100);
                const cnnPct = Math.round(weights.cnn * 100);
                return (
                  <div key={cname} style={{ background: 'rgba(31, 41, 55, 0.3)', padding: '8px 12px', borderRadius: '6px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', fontWeight: 600, color: '#fff', marginBottom: '4px' }}>
                      <span>{cname}</span>
                      <span style={{ color: 'var(--text-muted)', fontSize: '11px' }}>
                        CNN {cnnPct}% | Texture {gaborPct}%
                      </span>
                    </div>
                    <div style={{ display: 'flex', height: '6px', borderRadius: '3px', overflow: 'hidden' }}>
                      <div style={{ width: `${cnnPct}%`, background: 'var(--blue-500)' }} title="CNN semantic representation"></div>
                      <div style={{ width: `${gaborPct}%`, background: 'var(--emerald-500)' }} title="Gabor spatial-frequency signature"></div>
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <div style={{ color: 'var(--text-muted)', fontSize: '12px' }}>Loading gate analysis...</div>
          )}
        </div>
      </div>
    </div>
  );
};
