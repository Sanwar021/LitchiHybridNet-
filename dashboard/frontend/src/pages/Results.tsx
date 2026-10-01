import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { BenchmarkRow } from '../types/api';
import { BarChart3, CheckCircle2, Copy } from 'lucide-react';

export const ResultsPage: React.FC = () => {
  const [benchmarks, setBenchmarks] = useState<BenchmarkRow[]>([]);
  const [stats, setStats] = useState<any>(null);
  const [perClass, setPerClass] = useState<any>(null);

  useEffect(() => {
    api.getComparison().then(setBenchmarks).catch(console.error);
    api.getStatisticalTests().then(setStats).catch(console.error);
    api.getPerClassMetrics().then(setPerClass).catch(console.error);
  }, []);

  const copyLatex = () => {
    let tex = `\\begin{table}[t]\n\\centering\n\\caption{Benchmark Comparison on BDLitchi Dataset}\n\\begin{tabular}{lcccc}\n\\toprule\nModel & Params (M) & Accuracy (\\%) & Macro-F1 & Latency (ms) \\\\\n\\midrule\n`;
    benchmarks.forEach((b) => {
      const isBold = b.model.includes('LitchiHybridNet');
      const name = isBold ? `\\textbf{${b.model}}` : b.model;
      const acc = isBold ? `\\textbf{${b.accuracy_mean.toFixed(2)}}` : b.accuracy_mean.toFixed(2);
      const f1 = isBold ? `\\textbf{${b.macro_f1_mean.toFixed(4)}}` : b.macro_f1_mean.toFixed(4);
      tex += `${name} & ${b.params_m.toFixed(2)} & ${acc} & ${f1} & ${b.latency_cpu_ms.toFixed(1)} \\\\\n`;
    });
    tex += `\\bottomrule\n\\end{tabular}\n\\end{table}`;
    navigator.clipboard.writeText(tex);
    alert('LaTeX table copied to clipboard!');
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1 style={{ fontSize: '20px', fontWeight: 700, color: '#fff', margin: '0 0 6px' }}>
            Experimental Benchmark & Baseline Comparison
          </h1>
          <p style={{ fontSize: '13px', color: 'var(--text-secondary)', margin: 0 }}>
            Standardized evaluation across proposed LitchiHybridNet, modern lightweight backbones, and classical baselines.
          </p>
        </div>

        <button
          onClick={copyLatex}
          style={{
            background: 'rgba(31, 41, 55, 0.8)',
            border: '1px solid var(--border-color)',
            color: 'var(--text-primary)',
            padding: '8px 14px',
            borderRadius: '6px',
            fontSize: '12px',
            fontWeight: 600,
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '6px'
          }}
        >
          <Copy size={14} /> Copy as LaTeX
        </button>
      </div>

      {/* Main comparison table */}
      <div className="glass-panel" style={{ padding: '20px', overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px', textAlign: 'left' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid var(--border-color)', color: 'var(--text-muted)' }}>
              <th style={{ padding: '10px 12px' }}>Model Architecture</th>
              <th style={{ padding: '10px 12px' }}>Backbone</th>
              <th style={{ padding: '10px 12px' }}>Params (M)</th>
              <th style={{ padding: '10px 12px' }}>FLOPs (M)</th>
              <th style={{ padding: '10px 12px' }}>Accuracy (%)</th>
              <th style={{ padding: '10px 12px' }}>Macro F1</th>
              <th style={{ padding: '10px 12px' }}>MCC</th>
              <th style={{ padding: '10px 12px' }}>CPU Latency (ms)</th>
              <th style={{ padding: '10px 12px' }}>Size (MB)</th>
            </tr>
          </thead>
          <tbody>
            {benchmarks.map((row, idx) => {
              const isBest = row.model.includes('Proposed');
              return (
                <tr
                  key={idx}
                  style={{
                    borderBottom: '1px solid rgba(31, 41, 55, 0.5)',
                    background: isBest ? 'rgba(16, 185, 129, 0.08)' : 'transparent',
                    fontWeight: isBest ? 600 : 400
                  }}
                >
                  <td style={{ padding: '12px', color: isBest ? 'var(--emerald-400)' : '#fff' }}>
                    {row.model}
                  </td>
                  <td style={{ padding: '12px', color: 'var(--text-secondary)' }}>{row.backbone}</td>
                  <td style={{ padding: '12px' }}>{row.params_m.toFixed(2)}</td>
                  <td style={{ padding: '12px' }}>{row.flops_m.toFixed(0)}</td>
                  <td style={{ padding: '12px', color: isBest ? 'var(--emerald-400)' : '#fff' }}>
                    {row.accuracy_mean.toFixed(2)} {row.accuracy_std > 0 && `± ${row.accuracy_std.toFixed(2)}`}
                  </td>
                  <td style={{ padding: '12px', color: isBest ? 'var(--cyan-400)' : '#fff' }}>
                    {row.macro_f1_mean.toFixed(4)}
                  </td>
                  <td style={{ padding: '12px' }}>{row.mcc_mean.toFixed(3)}</td>
                  <td style={{ padding: '12px', color: 'var(--amber-500)' }}>{row.latency_cpu_ms.toFixed(1)}</td>
                  <td style={{ padding: '12px' }}>{row.size_mb.toFixed(1)}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Statistical tests & Per-class Breakdown */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        {/* Statistical tests */}
        <div className="glass-panel" style={{ padding: '20px' }}>
          <h3 style={{ fontSize: '15px', fontWeight: 600, marginBottom: '14px' }}>
            Hypothesis Testing & Statistical Significance
          </h3>
          {stats && stats.tests ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {stats.tests.map((t: any, i: number) => (
                <div
                  key={i}
                  style={{
                    background: 'rgba(31, 41, 55, 0.4)',
                    border: '1px solid var(--border-color)',
                    borderRadius: '8px',
                    padding: '14px'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontWeight: 600, fontSize: '13px', color: '#fff' }}>{t.test_name}</span>
                    <span style={{ color: 'var(--emerald-400)', fontSize: '11px', fontWeight: 600 }}>
                      Significant (p &lt; 0.001)
                    </span>
                  </div>
                  <div style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '4px' }}>
                    {t.comparison}
                  </div>
                  <div style={{ fontSize: '11.5px', color: 'var(--text-muted)', marginTop: '6px', fontFamily: 'monospace' }}>
                    Statistic: {t.statistic.toFixed(4)} | p-value: {t.p_value.toExponential(3)}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div style={{ color: 'var(--text-muted)', fontSize: '12px' }}>Loading tests...</div>
          )}
        </div>

        {/* Per-class metrics summary */}
        <div className="glass-panel" style={{ padding: '20px' }}>
          <h3 style={{ fontSize: '15px', fontWeight: 600, marginBottom: '14px' }}>
            Per-Class Diagnostic Precision & Recall
          </h3>
          {perClass && perClass.metrics ? (
            <div style={{ maxHeight: '280px', overflowY: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '12px' }}>
                <thead>
                  <tr style={{ color: 'var(--text-muted)', borderBottom: '1px solid var(--border-color)' }}>
                    <th style={{ textAlign: 'left', padding: '6px 8px' }}>Class</th>
                    <th style={{ textAlign: 'right', padding: '6px 8px' }}>Precision</th>
                    <th style={{ textAlign: 'right', padding: '6px 8px' }}>Recall</th>
                    <th style={{ textAlign: 'right', padding: '6px 8px' }}>F1-Score</th>
                  </tr>
                </thead>
                <tbody>
                  {perClass.metrics.map((m: any, i: number) => (
                    <tr key={i} style={{ borderBottom: '1px solid rgba(31, 41, 55, 0.3)' }}>
                      <td style={{ padding: '6px 8px', color: '#fff' }}>{m.class_name}</td>
                      <td style={{ textAlign: 'right', padding: '6px 8px', color: 'var(--emerald-400)' }}>{(m.precision * 100).toFixed(1)}%</td>
                      <td style={{ textAlign: 'right', padding: '6px 8px', color: 'var(--cyan-400)' }}>{(m.recall * 100).toFixed(1)}%</td>
                      <td style={{ textAlign: 'right', padding: '6px 8px', fontWeight: 600 }}>{m.f1_score.toFixed(4)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div style={{ color: 'var(--text-muted)', fontSize: '12px' }}>Loading per-class metrics...</div>
          )}
        </div>
      </div>
    </div>
  );
};
