#!/usr/bin/env python3
"""
Master paper build script for LitchiHybridNet.
Works directly on Windows/Linux/macOS without requiring 'make'.
Runs all data verification, table/figure generation, and PDF rendering.
"""

import sys
import subprocess
from pathlib import Path

def run_step(desc, script_path):
    print(f"\n[RUNNING] {desc}...")
    res = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True)
    if res.returncode == 0:
        print(f"  [SUCCESS] {desc}")
        if res.stdout.strip():
            print("  " + "\n  ".join(res.stdout.strip().split("\n")[:5]))
        return True
    else:
        print(f"  [ERROR] {desc} failed:")
        print(res.stderr)
        return False

def main():
    root = Path(__file__).resolve().parent.parent
    scripts_dir = root / 'scripts'
    paper_dir = root / 'paper'

    steps = [
        ("Step 1: Auto-Numbers Macro Generation", scripts_dir / 'make_auto_numbers.py'),
        ("Step 2: LaTeX Tables Generation", scripts_dir / 'make_paper_tables.py'),
        ("Step 3: 300-DPI Publication Figures Generation", scripts_dir / 'make_paper_figures.py'),
        ("Step 4: BibTeX Reference Verification", scripts_dir / 'verify_references.py'),
        ("Step 5: Number & Cross-Reference Integrity Check", scripts_dir / 'check_paper_numbers.py'),
        ("Step 6: Render Publication PDF", scripts_dir / 'render_paper_pdf.py')
    ]

    all_passed = True
    for desc, script in steps:
        if not run_step(desc, script):
            all_passed = False
            break

    if all_passed:
        print("\n" + "="*70)
        print("ALL PAPER ARTIFACTS AND PDF GENERATED SUCCESSFULLY!")
        print(f"  - Master LaTeX Document : {paper_dir / 'main.tex'}")
        print(f"  - Compiled PDF Document : {paper_dir / 'main.pdf'}")
        print(f"  - Submission Package    : {paper_dir / 'submission'}")
        print(f"  - Figures Directory     : {paper_dir / 'figures'}")
        print(f"  - Tables Directory      : {paper_dir / 'tables'}")
        print("="*70)
    else:
        print("\n[FAILED] Paper build aborted due to errors.")
        sys.exit(1)

if __name__ == '__main__':
    main()
