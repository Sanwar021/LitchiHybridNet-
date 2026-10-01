import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { SystemStatus } from '../types/api';
import { Settings, Cpu, HardDrive, GitBranch } from 'lucide-react';

export const SettingsPage: React.FC = () => {
  const [system, setSystem] = useState<SystemStatus | null>(null);

  useEffect(() => {
    api.getSystemStatus().then(setSystem).catch(console.error);
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div>
        <h1 style={{ fontSize: '20px', fontWeight: 700, color: '#fff', margin: '0 0 6px' }}>
          System Telemetry & Project Environment
        </h1>
        <p style={{ fontSize: '13px', color: 'var(--text-secondary)', margin: 0 }}>
          Hardware resources, PyTorch execution backend, repository commit, and project configurations.
        </p>
      </div>

      {system && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px' }}>
          <div className="glass-panel" style={{ padding: '20px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--emerald-400)', marginBottom: '10px' }}>
              <Cpu size={18} />
              <span style={{ fontWeight: 600, fontSize: '14px' }}>Processor / Compute</span>
            </div>
            <div style={{ fontSize: '13px', color: 'var(--text-secondary)', display: 'flex', flexDirection: 'column', gap: '6px' }}>
              <div>CPU Utilization: <strong style={{ color: '#fff' }}>{system.cpu_percent.toFixed(1)}%</strong></div>
              <div>Logical Cores: <strong style={{ color: '#fff' }}>{system.cpu_count}</strong></div>
              <div>GPU Accelerator: <strong style={{ color: system.gpu_available ? 'var(--emerald-400)' : 'var(--text-muted)' }}>{system.gpu_available ? system.gpu_name : 'None (CPU Only)'}</strong></div>
            </div>
          </div>

          <div className="glass-panel" style={{ padding: '20px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--cyan-400)', marginBottom: '10px' }}>
              <HardDrive size={18} />
              <span style={{ fontWeight: 600, fontSize: '14px' }}>Memory & Storage</span>
            </div>
            <div style={{ fontSize: '13px', color: 'var(--text-secondary)', display: 'flex', flexDirection: 'column', gap: '6px' }}>
              <div>RAM Used: <strong style={{ color: '#fff' }}>{system.ram_used_gb} GB</strong></div>
              <div>RAM Total: <strong style={{ color: '#fff' }}>{system.ram_total_gb} GB</strong></div>
              <div>Disk Utilization: <strong style={{ color: '#fff' }}>{system.disk_percent.toFixed(1)}%</strong></div>
            </div>
          </div>

          <div className="glass-panel" style={{ padding: '20px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--indigo-500)', marginBottom: '10px' }}>
              <GitBranch size={18} />
              <span style={{ fontWeight: 600, fontSize: '14px' }}>Software & Git</span>
            </div>
            <div style={{ fontSize: '13px', color: 'var(--text-secondary)', display: 'flex', flexDirection: 'column', gap: '6px' }}>
              <div>Python: <strong style={{ color: '#fff' }}>{system.python_version}</strong></div>
              <div>PyTorch: <strong style={{ color: '#fff' }}>{system.torch_version}</strong></div>
              <div>Git Head: <strong style={{ color: '#fff' }}>{system.git_commit}</strong></div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
