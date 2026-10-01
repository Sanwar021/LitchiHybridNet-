import React from 'react';
import { Cpu, HardDrive, RefreshCw } from 'lucide-react';
import { SystemStatus } from '../types/api';

interface HeaderProps {
  system: SystemStatus | null;
  onRefresh: () => void;
  selectedModel: string;
  onSelectModel: (m: string) => void;
}

export const Header: React.FC<HeaderProps> = ({
  system,
  onRefresh,
  selectedModel,
  onSelectModel,
}) => {
  return (
    <header style={{
      height: '64px',
      background: 'rgba(17, 24, 39, 0.95)',
      backdropFilter: 'blur(10px)',
      borderBottom: '1px solid var(--border-color)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 28px',
      position: 'sticky',
      top: 0,
      zIndex: 30
    }}>
      {/* Title / Subtitle */}
      <div>
        <h2 style={{ fontSize: '16px', fontWeight: 600, color: 'var(--text-primary)', margin: 0 }}>
          LitchiHybridNet Scientific Control Dashboard
        </h2>
        <p style={{ fontSize: '12px', color: 'var(--text-muted)', margin: 0 }}>
          Real-time field leaf disease diagnosis, live training, explainability & paper artifacts
        </p>
      </div>

      {/* Stats pills & Controls */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
        {/* Model Selector */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: 500 }}>Model:</span>
          <select
            value={selectedModel}
            onChange={(e) => onSelectModel(e.target.value)}
            style={{
              background: 'var(--bg-primary)',
              border: '1px solid var(--border-color)',
              color: 'var(--emerald-400)',
              fontSize: '12px',
              padding: '6px 12px',
              borderRadius: '6px',
              fontWeight: 600,
              cursor: 'pointer'
            }}
          >
            <option value="hybrid_seed42">LitchiHybridNet (Seed 42)</option>
            <option value="mobilenetv3_large">MobileNetV3 Baseline</option>
            <option value="efficientnet_b0">EfficientNet-B0</option>
            <option value="resnet50">ResNet-50</option>
          </select>
        </div>

        {/* System telemetry */}
        {system && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              background: 'rgba(31, 41, 55, 0.6)',
              padding: '5px 10px',
              borderRadius: '6px',
              border: '1px solid var(--border-color)',
              fontSize: '12px'
            }}>
              <Cpu size={14} color="#10b981" />
              <span>CPU: {system.cpu_percent.toFixed(0)}%</span>
            </div>

            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              background: 'rgba(31, 41, 55, 0.6)',
              padding: '5px 10px',
              borderRadius: '6px',
              border: '1px solid var(--border-color)',
              fontSize: '12px'
            }}>
              <HardDrive size={14} color="#3b82f6" />
              <span>RAM: {system.ram_used_gb} / {system.ram_total_gb} GB</span>
            </div>
          </div>
        )}

        {/* Refresh button */}
        <button
          onClick={onRefresh}
          title="Refresh Data"
          style={{
            background: 'transparent',
            border: '1px solid var(--border-color)',
            color: 'var(--text-secondary)',
            borderRadius: '6px',
            width: '32px',
            height: '32px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer'
          }}
        >
          <RefreshCw size={14} />
        </button>
      </div>
    </header>
  );
};
