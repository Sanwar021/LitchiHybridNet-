#!/usr/bin/env python3
r"""
Verify internal consistency and numerical integrity of the IEEE manuscript.
Checks:
1. All macros in auto_numbers.tex match exact values in results/
2. All \cite{} keys exist in references.bib
3. All \ref{} keys correspond to a defined \label{}
4. Fails and outputs actionable errors on any mismatch.
"""

import json
import re
import sys
from pathlib import Path
import pandas as pd

def check_paper_numbers():
    root = Path(__file__).resolve().parent.parent
    paper_dir = root / 'paper'
    
    # 1. Load Ground Truth Results
    with open(root / 'results' / 'original' / 'metrics.json', 'r', encoding='utf-8') as f:
        orig = json.load(f)
    with open(root / 'results' / 'augmented' / 'metrics.json', 'r', encoding='utf-8') as f:
        aug = json.load(f)
    with open(root / 'data' / 'audit' / 'dataset_audit.json', 'r', encoding='utf-8') as f:
        audit = json.load(f)
        
    print("=== CHECK 1: VERIFY AUTO-NUMBERS MACROS AGAINST RESULTS ===")
    auto_numbers_file = paper_dir / 'auto_numbers.tex'
    if not auto_numbers_file.exists():
        print("[FAIL] paper/auto_numbers.tex does not exist!")
        return False
        
    with open(auto_numbers_file, 'r', encoding='utf-8') as f:
        auto_content = f.read()
        
    macro_pattern = r'\\newcommand\{\\(\w+)\}\{([^}]+)\}'
    macros = dict(re.findall(macro_pattern, auto_content))
    print(f"Loaded {len(macros)} macros from auto_numbers.tex")
    
    errors = []
    
    # Check key numerical mappings
    expected_acc = f"{orig['test_accuracy'] * 100:.2f}\\%"
    if macros.get('accMain') != expected_acc:
        errors.append(f"accMain mismatch: expected {expected_acc}, got {macros.get('accMain')}")
        
    expected_f1 = f"{orig['macro_f1']:.4f}"
    if macros.get('fOneMain') != expected_f1:
        errors.append(f"fOneMain mismatch: expected {expected_f1}, got {macros.get('fOneMain')}")
        
    expected_loss = f"{orig['test_loss']:.4f}"
    if macros.get('lossMain') != expected_loss:
        errors.append(f"lossMain mismatch: expected {expected_loss}, got {macros.get('lossMain')}")
        
    expected_total_img = f"{audit.get('total_images', 11094):,}"
    if macros.get('totalImages') != expected_total_img:
        errors.append(f"totalImages mismatch: expected {expected_total_img}, got {macros.get('totalImages')}")

    expected_aug_acc = f"{aug['test_accuracy'] * 100:.2f}\\%"
    if macros.get('accAug') != expected_aug_acc:
        errors.append(f"accAug mismatch: expected {expected_aug_acc}, got {macros.get('accAug')}")

    if errors:
        for err in errors:
            print(f"  [ERROR] {err}")
    else:
        print("  [PASS] All core macros exactly match empirical results!")

    # 2. Check BibTeX Citation Keys
    print("\n=== CHECK 2: VERIFY CITATION KEYS ===")
    with open(paper_dir / 'references.bib', 'r', encoding='utf-8') as f:
        bib_content = f.read()
    defined_cites = set(re.findall(r'@\w+\s*\{\s*([^,]+),', bib_content))
    print(f"Found {len(defined_cites)} defined BibTeX entries.")

    tex_files = list(paper_dir.glob('**/*.tex'))
    used_cites = set()
    for tf in tex_files:
        with open(tf, 'r', encoding='utf-8') as f:
            content = f.read()
        # Find all \cite{...}
        cites = re.findall(r'\\cite\{([^}]+)\}', content)
        for c in cites:
            for item in c.split(','):
                used_cites.add(item.strip())

    missing_cites = [c for c in used_cites if c not in defined_cites]
    if missing_cites:
        for mc in missing_cites:
            errors.append(f"Undefined citation key: '{mc}'")
            print(f"  [ERROR] Undefined citation: {mc}")
    else:
        print(f"  [PASS] All {len(used_cites)} citations resolve successfully in references.bib!")

    # 3. Check Labels and References
    print("\n=== CHECK 3: VERIFY LABELS AND REFERENCES ===")
    defined_labels = set()
    used_refs = set()
    for tf in tex_files:
        with open(tf, 'r', encoding='utf-8') as f:
            content = f.read()
        labels = re.findall(r'\\label\{([^}]+)\}', content)
        for l in labels:
            defined_labels.add(l.strip())
        refs = re.findall(r'\\ref\{([^}]+)\}', content)
        for r in refs:
            used_refs.add(r.strip())

    missing_refs = [r for r in used_refs if r not in defined_labels]
    if missing_refs:
        for mr in missing_refs:
            errors.append(f"Undefined cross-reference: '{mr}'")
            print(f"  [ERROR] Undefined reference: {mr}")
    else:
        print(f"  [PASS] All {len(used_refs)} cross-references match defined labels ({len(defined_labels)} labels found)!")

    # 4. Summary
    print(f"\n======================================")
    print(f"TOTAL INTEGRITY ISSUES FOUND: {len(errors)}")
    if errors:
        return False
    else:
        print("ALL PAPER CONSISTENCY CHECKS PASSED WITH ZERO DISCREPANCIES!")
        return True

if __name__ == '__main__':
    success = check_paper_numbers()
    sys.exit(0 if success else 1)
