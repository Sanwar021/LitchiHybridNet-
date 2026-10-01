import sys
import psutil
import torch
from pathlib import Path
from ..core.config import PROJECT_ROOT


class SystemService:
    @staticmethod
    def get_system_stats():
        cpu_pct = psutil.cpu_percent(interval=None)
        cpu_cnt = psutil.cpu_count(logical=True)
        vmem = psutil.virtual_memory()
        disk = psutil.disk_usage(str(PROJECT_ROOT))
        
        gpu_avail = torch.cuda.is_available()
        gpu_name = torch.cuda.get_device_name(0) if gpu_avail else None

        return {
            "cpu_percent": float(cpu_pct),
            "cpu_count": int(cpu_cnt),
            "ram_percent": float(vmem.percent),
            "ram_used_gb": round(vmem.used / (1024**3), 2),
            "ram_total_gb": round(vmem.total / (1024**3), 2),
            "gpu_available": gpu_avail,
            "gpu_name": gpu_name,
            "disk_percent": float(disk.percent),
            "python_version": sys.version.split()[0],
            "torch_version": torch.__version__,
            "git_commit": "HEAD (main)",
            "active_jobs": 0
        }
