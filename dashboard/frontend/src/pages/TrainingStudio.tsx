import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Play, Square, Terminal, Sliders } from 'lucide-react';

export const TrainingStudio: React.FC = () => {
  const [modelName, setModelName] = useState('hybrid');
  const [epochs, setEpochs] = useState(25);
  const [lr, setLr] = useState(0.001);
  const [batchSize, setBatchSize] = useState(32);
  const [fusionType, setFusionType] = useState('gated');
  const [gaborLearnable, setGaborLearnable] = useState(true);
  const [seed, setSeed] = useState(42);

  const [activeJob, setActiveJob] = useState<any>(null);
  const [logs, setLogs] = useState<string[]>([]);
  const [isLaunching, setIsLaunching] = useState(false);

  const handleLaunch = async () => {
    setIsLaunching(true);
    try {
      const job = await api.startTrainingJob({
        model_name: modelName,
        epochs: epochs,
        seeds: [seed],
      });
      setActiveJob(job);
      setLogs([`Job ${job.id} started. Streaming stdout/stderr...`]);
      listenLogs(job.id);
    } catch (err: any) {
      alert(`Error launching training: ${err.message}`);
    } finally {
      setIsLaunching(false);
    }
  };

  const handleCancel = async () => {
    if (!activeJob) return;
    try {
      await api.cancelJob(activeJob.id);
      setActiveJob({ ...activeJob, status: 'cancelled' });
      setLogs((prev) => [...prev, '\n[Job cancelled by user]']);
    } catch (err: any) {
      alert(`Error cancelling: ${err.message}`);
    }
  };

  const listenLogs = (jobId: string) => {
    const eventSource = new EventSource(`http://localhost:8000/api/jobs/${jobId}/logs/stream`);
    eventSource.onmessage = (event) => {
      setLogs((prev) => [...prev.slice(-300), event.data]);
    };
    eventSource.onerror = () => {
      eventSource.close();
    };
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div>
        <h1 style={{ fontSize: '20px', fontWeight: 700, color: '#fff', margin: '0 0 6px' }}>
          Training Studio & Multi-Seed Hyperparameter Engine
        </h1>
        <p style={{ fontSize: '13px', color: 'var(--text-secondary)', margin: 0 }}>
          Launch full training jobs directly from the dashboard. Live telemetry updates epoch curves and streams process output via SSE.
        </p>
      </div>

      <div className="two-panel-grid">
        {/* Form panel */}
        <div className="glass-panel" style={{ padding: '24px' }}>
          <h3 style={{ fontSize: '15px', fontWeight: 600, marginBottom: '18px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Sliders size={16} color="var(--emerald-400)" /> Hyperparameter Configuration
          </h3>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            <div>
              <label style={{ fontSize: '12px', color: 'var(--text-muted)', display: 'block', marginBottom: '6px' }}>
                Architecture
              </label>
              <select
                value={modelName}
                onChange={(e) => setModelName(e.target.value)}
                style={{ width: '100%', background: 'var(--bg-primary)', border: '1px solid var(--border-color)', color: '#fff', padding: '8px 12px', borderRadius: '6px', fontSize: '13px' }}
              >
                <option value="hybrid">LitchiHybridNet (Proposed Hybrid Gabor)</option>
                <option value="cnn_only">CNN Only Baseline (MobileNetV3)</option>
                <option value="gabor_only">Gabor Texture Only</option>
                <option value="baseline_efficientnet_b0">Baseline: EfficientNet-B0</option>
                <option value="baseline_resnet50">Baseline: ResNet-50</option>
              </select>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
              <div>
                <label style={{ fontSize: '12px', color: 'var(--text-muted)', display: 'block', marginBottom: '6px' }}>
                  Epochs
                </label>
                <input
                  type="number"
                  value={epochs}
                  onChange={(e) => setEpochs(Number(e.target.value))}
                  style={{ width: '100%', background: 'var(--bg-primary)', border: '1px solid var(--border-color)', color: '#fff', padding: '8px 12px', borderRadius: '6px', fontSize: '13px' }}
                />
              </div>

              <div>
                <label style={{ fontSize: '12px', color: 'var(--text-muted)', display: 'block', marginBottom: '6px' }}>
                  Batch Size
                </label>
                <input
                  type="number"
                  value={batchSize}
                  onChange={(e) => setBatchSize(Number(e.target.value))}
                  style={{ width: '100%', background: 'var(--bg-primary)', border: '1px solid var(--border-color)', color: '#fff', padding: '8px 12px', borderRadius: '6px', fontSize: '13px' }}
                />
              </div>
            </div>

            <div>
              <label style={{ fontSize: '12px', color: 'var(--text-muted)', display: 'block', marginBottom: '6px' }}>
                Learning Rate (AdamW Cosine Warmup)
              </label>
              <input
                type="number"
                step="0.0001"
                value={lr}
                onChange={(e) => setLr(Number(e.target.value))}
                style={{ width: '100%', background: 'var(--bg-primary)', border: '1px solid var(--border-color)', color: '#fff', padding: '8px 12px', borderRadius: '6px', fontSize: '13px' }}
              />
            </div>

            <div>
              <label style={{ fontSize: '12px', color: 'var(--text-muted)', display: 'block', marginBottom: '6px' }}>
                Fusion Strategy
              </label>
              <select
                value={fusionType}
                onChange={(e) => setFusionType(e.target.value)}
                style={{ width: '100%', background: 'var(--bg-primary)', border: '1px solid var(--border-color)', color: '#fff', padding: '8px 12px', borderRadius: '6px', fontSize: '13px' }}
              >
                <option value="gated">Squeeze-and-Excitation Gated (Proposed)</option>
                <option value="concat">Channel Concatenation</option>
                <option value="cross_attention">Multi-Head Cross-Attention</option>
              </select>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginTop: '4px' }}>
              <input
                type="checkbox"
                id="gaborLearn"
                checked={gaborLearnable}
                onChange={(e) => setGaborLearnable(e.target.checked)}
              />
              <label htmlFor="gaborLearn" style={{ fontSize: '13px', color: 'var(--text-secondary)', cursor: 'pointer' }}>
                Differentiable Learnable Gabor Parameters
              </label>
            </div>

            <div style={{ marginTop: '14px', display: 'flex', gap: '10px' }}>
              <button
                onClick={handleLaunch}
                disabled={isLaunching || (activeJob && activeJob.status === 'running')}
                style={{
                  flex: 1,
                  background: 'var(--emerald-500)',
                  color: '#fff',
                  border: 'none',
                  padding: '10px 16px',
                  borderRadius: '6px',
                  fontWeight: 600,
                  fontSize: '13px',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '6px'
                }}
              >
                <Play size={15} /> Launch Run
              </button>

              {activeJob && activeJob.status === 'running' && (
                <button
                  onClick={handleCancel}
                  style={{
                    background: 'var(--rose-500)',
                    color: '#fff',
                    border: 'none',
                    padding: '10px 14px',
                    borderRadius: '6px',
                    fontWeight: 600,
                    fontSize: '13px',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px'
                  }}
                >
                  <Square size={14} /> Cancel
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Live console & training curves */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div className="glass-panel" style={{ padding: '20px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
              <h3 style={{ fontSize: '14px', fontWeight: 600, margin: 0, display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Terminal size={16} color="var(--cyan-400)" /> Live Output Stream (SSE Tail)
              </h3>
              {activeJob && (
                <span style={{ fontSize: '12px', color: 'var(--emerald-400)', fontWeight: 600 }}>
                  PID: {activeJob.pid || 'Running'}
                </span>
              )}
            </div>

            <div style={{
              background: '#0a0f1d',
              border: '1px solid #1f2937',
              borderRadius: '6px',
              padding: '14px',
              height: '380px',
              overflowY: 'auto',
              fontFamily: 'monospace',
              fontSize: '12px',
              color: '#34d399',
              lineHeight: 1.5,
              whiteSpace: 'pre-wrap'
            }}>
              {logs.length > 0 ? logs.join('\n') : (
                <span style={{ color: 'var(--text-muted)' }}>
                  Awaiting run launch or active log streaming... Click "Launch Run" to start.
                </span>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
