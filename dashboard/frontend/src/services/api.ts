import {
  OverviewData,
  DatasetAudit,
  RunSummary,
  Job,
  BenchmarkRow,
  AblationGroup,
  RobustnessData,
  EfficiencyRow,
  PredictResponse,
  SystemStatus,
} from '../types/api';

const API_BASE = 'http://localhost:8000/api';

export const api = {
  // Overview & System
  getOverview: async (): Promise<OverviewData> => {
    const res = await fetch(`${API_BASE}/overview`);
    if (!res.ok) throw new Error('Failed to fetch overview data');
    return res.json();
  },

  getSystemStatus: async (): Promise<SystemStatus> => {
    const res = await fetch(`${API_BASE}/system`);
    if (!res.ok) throw new Error('Failed to fetch system status');
    return res.json();
  },

  getProgress: async (): Promise<{ progress_markdown: string }> => {
    const res = await fetch(`${API_BASE}/progress`);
    if (!res.ok) throw new Error('Failed to fetch progress');
    return res.json();
  },

  // Dataset
  getDatasetAudit: async (): Promise<DatasetAudit> => {
    const res = await fetch(`${API_BASE}/dataset/audit`);
    if (!res.ok) throw new Error('Failed to fetch dataset audit');
    return res.json();
  },

  getDatasetSplits: async (): Promise<any> => {
    const res = await fetch(`${API_BASE}/dataset/splits`);
    if (!res.ok) throw new Error('Failed to fetch dataset splits');
    return res.json();
  },

  getFrequencyAnalysis: async (): Promise<any> => {
    const res = await fetch(`${API_BASE}/dataset/frequency-analysis`);
    if (!res.ok) throw new Error('Failed to fetch frequency analysis');
    return res.json();
  },

  // Runs
  getRuns: async (): Promise<RunSummary[]> => {
    const res = await fetch(`${API_BASE}/runs`);
    if (!res.ok) throw new Error('Failed to fetch runs');
    return res.json();
  },

  getRunDetail: async (runId: string): Promise<any> => {
    const res = await fetch(`${API_BASE}/runs/${runId}`);
    if (!res.ok) throw new Error(`Failed to fetch run ${runId}`);
    return res.json();
  },

  // Jobs
  getJobs: async (): Promise<Job[]> => {
    const res = await fetch(`${API_BASE}/jobs`);
    if (!res.ok) throw new Error('Failed to fetch jobs');
    return res.json();
  },

  startTrainingJob: async (params: {
    model_name: string;
    epochs: number;
    seeds: number[];
  }): Promise<Job> => {
    const res = await fetch(`${API_BASE}/jobs/train`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params),
    });
    if (!res.ok) throw new Error('Failed to launch training job');
    return res.json();
  },

  cancelJob: async (jobId: string): Promise<any> => {
    const res = await fetch(`${API_BASE}/jobs/${jobId}/cancel`, { method: 'POST' });
    if (!res.ok) throw new Error(`Failed to cancel job ${jobId}`);
    return res.json();
  },

  // Results & Benchmarks
  getComparison: async (): Promise<BenchmarkRow[]> => {
    const res = await fetch(`${API_BASE}/results/comparison`);
    if (!res.ok) throw new Error('Failed to fetch benchmark comparison');
    return res.json();
  },

  getConfusionMatrix: async (runId: string = 'hybrid_seed42'): Promise<any> => {
    const res = await fetch(`${API_BASE}/results/${runId}/confusion`);
    if (!res.ok) throw new Error('Failed to fetch confusion matrix');
    return res.json();
  },

  getPerClassMetrics: async (runId: string = 'hybrid_seed42'): Promise<any> => {
    const res = await fetch(`${API_BASE}/results/${runId}/per-class`);
    if (!res.ok) throw new Error('Failed to fetch per-class metrics');
    return res.json();
  },

  getStatisticalTests: async (): Promise<any> => {
    const res = await fetch(`${API_BASE}/stats/tests`);
    if (!res.ok) throw new Error('Failed to fetch statistical tests');
    return res.json();
  },

  // Ablations & Robustness & Efficiency
  getAblations: async (): Promise<AblationGroup[]> => {
    const res = await fetch(`${API_BASE}/ablations`);
    if (!res.ok) throw new Error('Failed to fetch ablations');
    return res.json();
  },

  getRobustness: async (): Promise<RobustnessData[]> => {
    const res = await fetch(`${API_BASE}/robustness`);
    if (!res.ok) throw new Error('Failed to fetch robustness data');
    return res.json();
  },

  getEfficiency: async (): Promise<{ rows: EfficiencyRow[] }> => {
    const res = await fetch(`${API_BASE}/efficiency`);
    if (!res.ok) throw new Error('Failed to fetch efficiency data');
    return res.json();
  },

  getGateAnalysis: async (): Promise<any> => {
    const res = await fetch(`${API_BASE}/explain/gate-analysis`);
    if (!res.ok) throw new Error('Failed to fetch gate analysis');
    return res.json();
  },

  // Inference
  predict: async (formData: FormData): Promise<PredictResponse> => {
    const res = await fetch(`${API_BASE}/predict`, {
      method: 'POST',
      body: formData,
    });
    if (!res.ok) throw new Error('Inference request failed');
    return res.json();
  },

  // Paper Assets
  getPaperFigures: async (): Promise<any[]> => {
    const res = await fetch(`${API_BASE}/paper/figures`);
    if (!res.ok) throw new Error('Failed to fetch paper figures');
    return res.json();
  },

  getPaperTables: async (): Promise<any[]> => {
    const res = await fetch(`${API_BASE}/paper/tables`);
    if (!res.ok) throw new Error('Failed to fetch paper tables');
    return res.json();
  },

  getPaperChecklist: async (): Promise<any[]> => {
    const res = await fetch(`${API_BASE}/paper/checklist`);
    if (!res.ok) throw new Error('Failed to fetch paper checklist');
    return res.json();
  },

  getBibtex: async (): Promise<{ bibtex: string }> => {
    const res = await fetch(`${API_BASE}/paper/bib`);
    if (!res.ok) throw new Error('Failed to fetch BibTeX');
    return res.json();
  },
};
