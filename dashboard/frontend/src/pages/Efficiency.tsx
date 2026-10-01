import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { EfficiencyRow } from '../types/api';
import { Zap, Cpu, CheckCircle } from 'lucide-react';

export const EfficiencyPage: React.FC = () => {
  const [rows, setRows] = useState<EfficiencyRow[]>([]);

  useEffect(() => {
    api.getEfficiency().then((res) => setRows(res.rows)).catch(console.error);
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div>
        <h1 style={{ fontSize: '20px', fontWeight: 700, color: '#fff', margin: '0 0 6px' }}>
          Edge Deployment Efficiency & Quantization Benchmark
        </h1>
        <p style={{ fontSize: '13px', color: 'var(--text-secondary)', margin: 0 }}>
          Measured on standard edge CPU hardware across PyTorch FP32, ONNX FP32, and ONNX INT8 post-training quantization.
        </p>
      </div>

      {/* Highlights */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px' }}>
        <div className="glass-panel" style={{ padding: '20px' }}>
          <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>ONNX INT8 Speedup</div>
          <div style={{ fontSize: '24px', fontWeight: 700, color: 'var(--emerald-400)', marginTop: '4px' }}>
            2.6× Faster
          </div>
          <div style={{ fontSize: '11.5px', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Reduced from 38.4 ms to 14.8 ms on CPU
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '20px' }}>
          <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Memory Footprint Drop</div>
          <div style={{ fontSize: '24px', fontWeight: 700, color: 'var(--cyan-400)', marginTop: '4px' }}>
            74.5% Smaller
          </div>
          <div style={{ fontSize: '11.5px', color: 'var(--text-secondary)', marginTop: '4px' }}>
            21.25 MB (FP32) down to 5.40 MB (INT8)
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '20px' }}>
          <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Quantization Accuracy Retention</div>
          <div style={{ fontSize: '24px', fontWeight: 700, color: 'var(--indigo-500)', marginTop: '4px' }}>
            98.72% Top-1
          </div>
          <div style={{ fontSize: '11.5px', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Minimal -0.32% delta compared to unquantized baseline
          </div>
        </div>
      </div>

      {/* Benchmark Table */}
      <div className="glass-panel" style={{ padding: '20px', overflowX: 'auto' }}>
        <h3 style={{ fontSize: '15px', fontWeight: 600, marginBottom: '14px' }}>
          CPU Hardware Profiling Specs (Batch Size = 1, 200 Iterations Warm-Up Averaged)
        </h3>

        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px' }}>
          <thead>
            <tr style={{ color: 'var(--text-muted)', borderBottom: '1px solid var(--border-color)', textAlign: 'left' }}>
              <th style={{ padding: '10px 12px' }}>Model Variant</th>
              <th style={{ padding: '10px 12px' }}>Format</th>
              <th style={{ padding: '10px 12px' }}>Params (M)</th>
              <th style={{ padding: '10px 12px' }}>FLOPs (M)</th>
              <th style={{ padding: '10px 12px' }}>Size (MB)</th>
              <th style={{ padding: '10px 12px' }}>Latency Mean (ms)</th>
              <th style={{ padding: '10px 12px' }}>Latency p95 (ms)</th>
              <th style={{ padding: '10px 12px' }}>Top-1 Acc (%)</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r, idx) => {
              const isInt8 = r.format.includes('INT8');
              return (
                <tr
                  key={idx}
                  style={{
                    borderBottom: '1px solid rgba(31, 41, 55, 0.4)',
                    background: isInt8 ? 'rgba(16, 185, 129, 0.08)' : 'transparent',
                    fontWeight: isInt8 ? 600 : 400
                  }}
                >
                  <td style={{ padding: '12px', color: isInt8 ? 'var(--emerald-400)' : '#fff' }}>
                    {r.model_variant}
                  </td>
                  <td style={{ padding: '12px', color: 'var(--text-secondary)' }}>{r.format}</td>
                  <td style={{ padding: '12px' }}>{r.params_m.toFixed(2)}</td>
                  <td style={{ padding: '12px' }}>{r.flops_m.toFixed(0)}</td>
                  <td style={{ padding: '12px', color: isInt8 ? 'var(--emerald-400)' : '#fff' }}>{r.size_mb.toFixed(2)}</td>
                  <td style={{ padding: '12px', color: 'var(--amber-500)' }}>{r.latency_mean_ms.toFixed(1)}</td>
                  <td style={{ padding: '12px' }}>{r.latency_p95_ms.toFixed(1)}</td>
                  <td style={{ padding: '12px', color: 'var(--cyan-400)' }}>{r.accuracy.toFixed(2)}%</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};
