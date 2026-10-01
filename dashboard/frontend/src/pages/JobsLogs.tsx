import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { Job } from '../types/api';
import { Terminal, RefreshCw, XCircle } from 'lucide-react';

export const JobsLogsPage: React.FC = () => {
  const [jobs, setJobs] = useState<Job[]>([]);

  const fetchJobs = () => {
    api.getJobs().then(setJobs).catch(console.error);
  };

  useEffect(() => {
    fetchJobs();
    const interval = setInterval(fetchJobs, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1 style={{ fontSize: '20px', fontWeight: 700, color: '#fff', margin: '0 0 6px' }}>
            Job Execution Queue & Subprocess Logs
          </h1>
          <p style={{ fontSize: '13px', color: 'var(--text-secondary)', margin: 0 }}>
            Live status of background training, evaluation, benchmark, and paper compilation tasks.
          </p>
        </div>

        <button
          onClick={fetchJobs}
          style={{
            background: 'rgba(31, 41, 55, 0.6)',
            border: '1px solid var(--border-color)',
            color: 'var(--text-secondary)',
            padding: '8px 14px',
            borderRadius: '6px',
            fontSize: '12px',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '6px'
          }}
        >
          <RefreshCw size={14} /> Refresh Jobs
        </button>
      </div>

      <div className="glass-panel" style={{ padding: '20px' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px', textAlign: 'left' }}>
          <thead>
            <tr style={{ color: 'var(--text-muted)', borderBottom: '1px solid var(--border-color)' }}>
              <th style={{ padding: '10px 12px' }}>Job ID</th>
              <th style={{ padding: '10px 12px' }}>Type</th>
              <th style={{ padding: '10px 12px' }}>Status</th>
              <th style={{ padding: '10px 12px' }}>Command</th>
              <th style={{ padding: '10px 12px' }}>PID</th>
              <th style={{ padding: '10px 12px' }}>Created</th>
              <th style={{ padding: '10px 12px' }}>Action</th>
            </tr>
          </thead>
          <tbody>
            {jobs.length > 0 ? (
              jobs.map((j) => (
                <tr key={j.id} style={{ borderBottom: '1px solid rgba(31, 41, 55, 0.4)' }}>
                  <td style={{ padding: '12px', fontFamily: 'monospace', color: '#fff' }}>{j.id}</td>
                  <td style={{ padding: '12px', textTransform: 'capitalize', color: 'var(--cyan-400)' }}>{j.job_type}</td>
                  <td style={{ padding: '12px' }}>
                    <span style={{
                      background: j.status === 'running' ? 'rgba(16, 185, 129, 0.15)' : j.status === 'failed' ? 'rgba(239, 68, 68, 0.15)' : 'rgba(107, 114, 128, 0.15)',
                      color: j.status === 'running' ? 'var(--emerald-400)' : j.status === 'failed' ? 'var(--rose-500)' : 'var(--text-muted)',
                      fontSize: '11px',
                      padding: '3px 8px',
                      borderRadius: '4px',
                      fontWeight: 600
                    }}>
                      {j.status.toUpperCase()}
                    </span>
                  </td>
                  <td style={{ padding: '12px', fontFamily: 'monospace', fontSize: '11px', color: 'var(--text-secondary)', maxWidth: '300px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {j.command}
                  </td>
                  <td style={{ padding: '12px' }}>{j.pid || '-'}</td>
                  <td style={{ padding: '12px', fontSize: '11px', color: 'var(--text-muted)' }}>
                    {new Date(j.created_at).toLocaleTimeString()}
                  </td>
                  <td style={{ padding: '12px' }}>
                    {j.status === 'running' && (
                      <button
                        onClick={async () => {
                          await api.cancelJob(j.id);
                          fetchJobs();
                        }}
                        style={{
                          background: 'rgba(239, 68, 68, 0.2)',
                          border: '1px solid rgba(239, 68, 68, 0.4)',
                          color: '#f87171',
                          padding: '4px 8px',
                          borderRadius: '4px',
                          fontSize: '11px',
                          cursor: 'pointer'
                        }}
                      >
                        Cancel
                      </button>
                    )}
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={7} style={{ padding: '24px', textAlign: 'center', color: 'var(--text-muted)' }}>
                  No active or historical jobs in the SQLite registry.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
