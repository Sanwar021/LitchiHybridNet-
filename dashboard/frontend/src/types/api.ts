export interface PipelineStep {
  phase: number;
  name: string;
  status: 'completed' | 'in_progress' | 'todo' | 'failed';
  description: string;
  notes?: string;
}

export interface OverviewData {
  project_title: string;
  total_images: number;
  num_classes: number;
  best_model_name: string;
  best_accuracy: number;
  best_macro_f1: number;
  total_params: number;
  model_size_mb: number;
  cpu_latency_ms: number;
  pipeline_steps: PipelineStep[];
  dataset_summary: Record<string, any>;
}

export interface DatasetAudit {
  total_images: number;
  num_classes: number;
  classes: string[];
  class_distribution: Record<string, number>;
  resolution_stats: Record<string, number>;
  duplicates: {
    exact_hash_duplicates: number;
    near_duplicate_groups: number;
    cross_class_duplicates: number;
  };
  splits: {
    train: number;
    val: number;
    test: number;
    total: number;
    group_aware: boolean;
    leakage_count: number;
  };
}

export interface RunSummary {
  id: string;
  name: string;
  model_type: string;
  seed: number;
  status: string;
  best_epoch?: number;
  best_val_f1?: number;
  best_val_acc?: number;
  total_params?: number;
  total_time_s?: number;
  created_at?: string;
}

export interface Job {
  id: string;
  job_type: string;
  status: string;
  command: string;
  created_at: string;
  started_at?: string;
  finished_at?: string;
  exit_code?: number;
  log_file?: string;
  pid?: number;
}

export interface BenchmarkRow {
  model: string;
  backbone: string;
  params_m: number;
  flops_m: number;
  accuracy_mean: number;
  accuracy_std: number;
  macro_f1_mean: number;
  macro_f1_std: number;
  mcc_mean: number;
  latency_cpu_ms: number;
  size_mb: number;
}

export interface AblationItem {
  variant: string;
  params_m: number;
  accuracy_mean: number;
  accuracy_std: number;
  macro_f1_mean: number;
  macro_f1_std: number;
}

export interface AblationGroup {
  group: string;
  items: AblationItem[];
}

export interface RobustnessCurve {
  model_name: string;
  color: string;
  accuracies: number[];
}

export interface RobustnessData {
  corruption: string;
  severities: number[];
  curves: RobustnessCurve[];
}

export interface EfficiencyRow {
  model_variant: string;
  format: string;
  device: string;
  batch_size: number;
  params_m: number;
  flops_m: number;
  size_mb: number;
  latency_mean_ms: number;
  latency_p95_ms: number;
  accuracy: number;
}

export interface PredictResponse {
  model_id: string;
  backend: string;
  predicted_class: string;
  predicted_index: number;
  confidence: number;
  probabilities: Record<string, number>;
  inference_time_ms: number;
  gradcam_base64?: string;
  gabor_response_base64?: string;
  gate_values?: Record<string, number>;
}

export interface SystemStatus {
  cpu_percent: number;
  cpu_count: number;
  ram_percent: number;
  ram_used_gb: number;
  ram_total_gb: number;
  gpu_available: boolean;
  gpu_name?: string;
  disk_percent: number;
  python_version: string;
  torch_version: string;
  git_commit?: string;
  active_jobs: number;
}
