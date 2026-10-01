import os
import time
import asyncio
from pathlib import Path
from typing import AsyncGenerator


async def stream_log_file(log_path: str) -> AsyncGenerator[str, None]:
    """Asynchronously tail a log file and yield lines for SSE."""
    p = Path(log_path)
    if not p.exists():
        yield f"data: Log file not created yet...\n\n"
        return

    with open(p, "r", encoding="utf-8", errors="ignore") as f:
        # First send existing content
        lines = f.readlines()
        for line in lines[-100:]:
            yield f"data: {line.rstrip()}\n\n"

        # Tail file
        while True:
            line = f.readline()
            if line:
                yield f"data: {line.rstrip()}\n\n"
            else:
                await asyncio.sleep(0.5)
