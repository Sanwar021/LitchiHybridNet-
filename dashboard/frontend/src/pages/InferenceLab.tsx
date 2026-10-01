import React, { useState } from 'react';
import { api } from '../services/api';
import { PredictResponse } from '../types/api';
import { UploadCloud, CheckCircle2, Zap, Microscope } from 'lucide-react';

export const InferenceLab: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [modelId, setModelId] = useState('hybrid_seed42');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<PredictResponse | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setResult(null);
    }
  };

  const handleRunInference = async () => {
    if (!selectedFile) return;
    setIsLoading(true);
    try {
      const fd = new FormData();
      fd.append('file', selectedFile);
      fd.append('model_id', modelId);
      fd.append('include_cam', 'true');
      fd.append('include_gabor', 'true');

      const res = await api.predict(fd);
      setResult(res);
    } catch (err: any) {
      alert(`Inference failed: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div>
        <h1 style={{ fontSize: '20px', fontWeight: 700, color: '#fff', margin: '0 0 6px' }}>
          Interactive Diagnostic Inference & Grad-CAM Studio
        </h1>
        <p style={{ fontSize: '13px', color: 'var(--text-secondary)', margin: 0 }}>
          Upload natural field litchi leaf images to observe dual-branch prediction, confidence distribution, and Grad-CAM saliency overlays.
        </p>
      </div>

      <div className="two-panel-grid">
        {/* Upload panel */}
        <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <h3 style={{ fontSize: '15px', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '8px' }}>
            <UploadCloud size={16} color="var(--emerald-400)" /> Image Input
          </h3>

          <div
            style={{
              border: '2px dashed var(--border-color)',
              borderRadius: '8px',
              padding: '24px 16px',
              textAlign: 'center',
              cursor: 'pointer',
              background: 'rgba(31, 41, 55, 0.2)'
            }}
            onClick={() => document.getElementById('leafInput')?.click()}
          >
            <input
              type="file"
              id="leafInput"
              accept="image/*"
              style={{ display: 'none' }}
              onChange={handleFileChange}
            />
            {previewUrl ? (
              <img
                src={previewUrl}
                alt="Selected leaf"
                style={{ maxHeight: '200px', maxWidth: '100%', borderRadius: '6px', margin: '0 auto' }}
              />
            ) : (
              <div>
                <Microscope size={36} color="var(--text-muted)" style={{ margin: '0 auto 8px' }} />
                <div style={{ fontSize: '13px', color: '#fff', fontWeight: 500 }}>Click to select leaf image</div>
                <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px' }}>
                  Supports JPEG, PNG (Field natural background)
                </div>
              </div>
            )}
          </div>

          <div>
            <label style={{ fontSize: '12px', color: 'var(--text-muted)', display: 'block', marginBottom: '6px' }}>
              Inference Model
            </label>
            <select
              value={modelId}
              onChange={(e) => setModelId(e.target.value)}
              style={{ width: '100%', background: 'var(--bg-primary)', border: '1px solid var(--border-color)', color: '#fff', padding: '8px 12px', borderRadius: '6px', fontSize: '13px' }}
            >
              <option value="hybrid_seed42">LitchiHybridNet (Dual-Branch Gabor)</option>
              <option value="mobilenetv3_large">MobileNetV3-Large Baseline</option>
            </select>
          </div>

          <button
            onClick={handleRunInference}
            disabled={!selectedFile || isLoading}
            style={{
              background: 'var(--emerald-500)',
              color: '#fff',
              border: 'none',
              padding: '12px',
              borderRadius: '6px',
              fontWeight: 600,
              fontSize: '13.5px',
              cursor: selectedFile ? 'pointer' : 'not-allowed',
              opacity: selectedFile ? 1 : 0.6,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px'
            }}
          >
            <Zap size={16} /> {isLoading ? 'Analyzing...' : 'Run Leaf Diagnosis'}
          </button>
        </div>

        {/* Results display */}
        <div className="glass-panel" style={{ padding: '24px' }}>
          {result ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid var(--border-color)', paddingBottom: '16px' }}>
                <div>
                  <span style={{ fontSize: '11px', color: 'var(--emerald-400)', fontWeight: 600, textTransform: 'uppercase' }}>
                    Diagnostic Prediction
                  </span>
                  <h2 style={{ fontSize: '22px', fontWeight: 700, color: '#fff', margin: '4px 0' }}>
                    {result.predicted_class}
                  </h2>
                  <span style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>
                    Latency: {result.inference_time_ms} ms (CPU) | Backend: {result.backend.toUpperCase()}
                  </span>
                </div>

                <div style={{ textAlign: 'right' }}>
                  <div style={{ fontSize: '28px', fontWeight: 800, color: 'var(--emerald-400)' }}>
                    {(result.confidence * 100).toFixed(1)}%
                  </div>
                  <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Confidence Score</div>
                </div>
              </div>

              {/* Overlays */}
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(min(100%, 240px), 1fr))', gap: '16px' }}>
                <div>
                  <h4 style={{ fontSize: '13px', fontWeight: 600, color: '#fff', marginBottom: '8px' }}>
                    Grad-CAM Lesion Heatmap Overlay
                  </h4>
                  {result.gradcam_base64 && (
                    <img
                      src={result.gradcam_base64}
                      alt="Grad-CAM"
                      style={{ width: '100%', borderRadius: '6px', border: '1px solid var(--border-color)', maxHeight: '200px', objectFit: 'contain' }}
                    />
                  )}
                </div>

                <div>
                  <h4 style={{ fontSize: '13px', fontWeight: 600, color: '#fff', marginBottom: '8px' }}>
                    Top Disease Probabilities
                  </h4>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', maxHeight: '200px', overflowY: 'auto' }}>
                    {Object.entries(result.probabilities)
                      .sort((a, b) => b[1] - a[1])
                      .slice(0, 5)
                      .map(([cname, prob]) => (
                        <div key={cname}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', color: 'var(--text-secondary)' }}>
                            <span>{cname}</span>
                            <span style={{ fontWeight: 600, color: '#fff' }}>{(prob * 100).toFixed(1)}%</span>
                          </div>
                          <div style={{ width: '100%', height: '4px', background: '#374151', borderRadius: '2px', marginTop: '3px' }}>
                            <div style={{ width: `${prob * 100}%`, height: '100%', background: 'var(--emerald-500)', borderRadius: '2px' }}></div>
                          </div>
                        </div>
                      ))}
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '320px', color: 'var(--text-muted)' }}>
              <Microscope size={48} style={{ opacity: 0.3, marginBottom: '12px' }} />
              <div style={{ fontSize: '14px', fontWeight: 500 }}>No inference executed yet</div>
              <div style={{ fontSize: '12px', marginTop: '4px' }}>
                Select an image on the left and click "Run Leaf Diagnosis".
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
