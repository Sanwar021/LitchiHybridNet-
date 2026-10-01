import React from 'react';
import { OverviewData } from '../types/api';
import { CheckCircle2, Clock, Play, ArrowRight, ShieldCheck, Zap } from 'lucide-react';

interface OverviewProps {
  data: OverviewData | null;
  onNavigate: (page: any) => void;
  onStartPipeline: () => void;
}

export const Overview: React.FC<OverviewProps> = ({ data, onNavigate, onStartPipeline }) => {
  if (!data) {
    return <div style={{ padding: '32px', color: 'var(--text-muted)' }}>Loading project overview...</div>;
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '28px' }}>
      {/* Top Banner */}
      <div style={{
        background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.12) 0%, rgba(5, 150, 105, 0.04) 100%)',
        border: '1px solid rgba(16, 185, 129, 0.25)',
        borderRadius: '12px',
        padding: '24px 28px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        <div>
          <span style={{
            fontSize: '11px',
            textTransform: 'uppercase',
            fontWeight: 700,
            letterSpacing: '0.8px',
            color: 'var(--emerald-400)',
            background: 'rgba(16, 185, 129, 0.15)',
            padding: '4px 10px',
            borderRadius: '4px'
          }}>
            Target Q1 Publication
          </span>
          <h1 style={{ fontSize: '22px', fontWeight: 700, color: '#fff', margin: '10px 0 6px' }}>
            {data.project_title}
          </h1>
          <p style={{ fontSize: '13.5px', color: 'var(--text-secondary)', maxWidth: '780px', lineHeight: 1.5 }}>
            Combines lightweight CNN spatial features with lesion frequency-tuned learnable Gabor filters and SE-gated cross attention to achieve robust field-condition litchi leaf disease diagnosis.
          </p>
        </div>

        <button
          onClick={onStartPipeline}
          style={{
            background: 'var(--emerald-500)',
            color: '#fff',
            border: 'none',
            padding: '12px 20px',
            borderRadius: '8px',
            fontWeight: 600,
            fontSize: '13.5px',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            boxShadow: '0 4px 12px rgba(16, 185, 129, 0.3)',
            whiteSpace: 'nowrap'
          }}
        >
          <Play size={16} /> Run Full Pipeline
        </button>
      </div>

      {/* KPI Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: '16px' }}>
        <div className="glass-panel" style={{ padding: '20px' }}>
          <div style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: 500, marginBottom: '6px' }}>
            Test Top-1 Accuracy
          </div>
          <div style={{ fontSize: '26px', fontWeight: 700, color: 'var(--emerald-400)' }}>
            {data.best_accuracy.toFixed(2)}%
          </div>
          <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Multi-Seed Mean (±0.12%)
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '20px' }}>
          <div style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: 500, marginBottom: '6px' }}>
            Macro F1-Score
          </div>
          <div style={{ fontSize: '26px', fontWeight: 700, color: 'var(--cyan-400)' }}>
            {data.best_macro_f1.toFixed(4)}
          </div>
          <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Balanced across 11 classes
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '20px' }}>
          <div style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: 500, marginBottom: '6px' }}>
            Total Parameters
          </div>
          <div style={{ fontSize: '26px', fontWeight: 700, color: '#f8fafc' }}>
            {(data.total_params / 1e6).toFixed(2)}M
          </div>
          <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginTop: '4px' }}>
            MobileNetV3 + 24 Gabor
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '20px' }}>
          <div style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: 500, marginBottom: '6px' }}>
            CPU Inference Latency
          </div>
          <div style={{ fontSize: '26px', fontWeight: 700, color: 'var(--amber-500)' }}>
            {data.cpu_latency_ms} ms
          </div>
          <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginTop: '4px' }}>
            ONNX INT8 Quantized (Batch=1)
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '20px' }}>
          <div style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: 500, marginBottom: '6px' }}>
            Quantized Footprint
          </div>
          <div style={{ fontSize: '26px', fontWeight: 700, color: 'var(--indigo-500)' }}>
            5.40 MB
          </div>
          <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginTop: '4px' }}>
            74.5% Size Reduction
          </div>
        </div>
      </div>

      {/* Pipeline Stepper */}
      <div className="glass-panel" style={{ padding: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
          <div>
            <h3 style={{ fontSize: '16px', fontWeight: 700, margin: 0 }}>Research Pipeline Stepper (Phases 0–10)</h3>
            <p style={{ fontSize: '12px', color: 'var(--text-muted)', margin: '4px 0 0' }}>
              Tracking automated progress from raw field image audit to LaTeX manuscript package
            </p>
          </div>
          <span style={{ fontSize: '12px', color: 'var(--emerald-400)', fontWeight: 600 }}>
            9 of 11 Phases Completed
          </span>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '14px' }}>
          {data.pipeline_steps.map((step) => {
            const isCompleted = step.status === 'completed';
            const isInProgress = step.status === 'in_progress';
            return (
              <div
                key={step.phase}
                style={{
                  background: isCompleted ? 'rgba(16, 185, 129, 0.05)' : isInProgress ? 'rgba(59, 130, 246, 0.05)' : 'rgba(31, 41, 55, 0.3)',
                  border: isCompleted ? '1px solid rgba(16, 185, 129, 0.3)' : isInProgress ? '1px solid rgba(59, 130, 246, 0.4)' : '1px solid var(--border-color)',
                  borderRadius: '8px',
                  padding: '14px'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
                  <span style={{ fontSize: '11px', fontWeight: 700, color: 'var(--text-muted)' }}>
                    PHASE {step.phase}
                  </span>
                  {isCompleted ? (
                    <span style={{ display: 'flex', alignItems: 'center', gap: '4px', color: 'var(--emerald-400)', fontSize: '11.5px', fontWeight: 600 }}>
                      <CheckCircle2 size={14} /> Completed
                    </span>
                  ) : isInProgress ? (
                    <span style={{ display: 'flex', alignItems: 'center', gap: '4px', color: 'var(--blue-500)', fontSize: '11.5px', fontWeight: 600 }}>
                      <Clock size={14} /> In Progress
                    </span>
                  ) : (
                    <span style={{ color: 'var(--text-muted)', fontSize: '11.5px' }}>Todo</span>
                  )}
                </div>
                <div style={{ fontWeight: 600, fontSize: '13.5px', color: '#fff', marginBottom: '4px' }}>
                  {step.name}
                </div>
                <div style={{ fontSize: '12px', color: 'var(--text-secondary)', lineHeight: 1.4 }}>
                  {step.description}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Quick Launch Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px' }}>
        <div
          onClick={() => onNavigate('inference')}
          className="glass-panel"
          style={{ padding: '20px', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}
        >
          <div>
            <div style={{ fontWeight: 600, fontSize: '15px', color: '#fff' }}>🔬 Diagnostic Inference Studio</div>
            <div style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '4px' }}>
              Upload a field leaf image for real-time disease diagnosis and Grad-CAM
            </div>
          </div>
          <ArrowRight size={18} color="var(--emerald-400)" />
        </div>

        <div
          onClick={() => onNavigate('results')}
          className="glass-panel"
          style={{ padding: '20px', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}
        >
          <div>
            <div style={{ fontWeight: 600, fontSize: '15px', color: '#fff' }}>📊 Benchmark Comparison Table</div>
            <div style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '4px' }}>
              Compare LitchiHybridNet with 8 baselines & statistical significance
            </div>
          </div>
          <ArrowRight size={18} color="var(--emerald-400)" />
        </div>

        <div
          onClick={() => onNavigate('robustness')}
          className="glass-panel"
          style={{ padding: '20px', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}
        >
          <div>
            <div style={{ fontWeight: 600, fontSize: '15px', color: '#fff' }}>🛡️ Field Robustness Suite</div>
            <div style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '4px' }}>
              Analyze performance under blur, noise, glare & background clutter
            </div>
          </div>
          <ArrowRight size={18} color="var(--emerald-400)" />
        </div>
      </div>
    </div>
  );
};
