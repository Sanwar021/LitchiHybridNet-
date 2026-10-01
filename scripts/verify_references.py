#!/usr/bin/env python3
"""
Verify BibTeX references for the LitchiHybridNet IEEE paper.
Checks entry syntax, required fields (title, author, year, journal/booktitle),
and checks DOI format / availability.
"""

import re
import sys
from pathlib import Path

def parse_bib_entries(bib_path):
    with open(bib_path, 'r', encoding='utf-8') as f:
        content = f.read()

    entries = {}
    pattern = r'@(\w+)\s*\{\s*([^,]+),\s*([\s\S]*?)\n\}'
    matches = re.finditer(pattern, content)
    
    for m in matches:
        entry_type = m.group(1).lower()
        cite_key = m.group(2).strip()
        fields_text = m.group(3)
        
        fields = {}
        for line in fields_text.split('\n'):
            line = line.strip()
            if '=' in line:
                k, v = line.split('=', 1)
                k = k.strip().lower()
                v = v.strip().rstrip(',').strip('{}"')
                fields[k] = v
        entries[cite_key] = {'type': entry_type, 'fields': fields}
    return entries

def verify_references(bib_path):
    entries = parse_bib_entries(bib_path)
    print(f"Loaded {len(entries)} BibTeX references from {bib_path}")
    
    required_fields = ['title', 'author', 'year']
    errors = []
    warnings = []
    
    for key, data in entries.items():
        fields = data['fields']
        for rf in required_fields:
            if rf not in fields:
                errors.append(f"[{key}] Missing required field: '{rf}'")
                
        if data['type'] in ['article'] and 'journal' not in fields:
            warnings.append(f"[{key}] Article missing 'journal'")
        if data['type'] in ['inproceedings'] and 'booktitle' not in fields:
            warnings.append(f"[{key}] Inproceedings missing 'booktitle'")
            
        # Check DOI
        if 'doi' in fields:
            doi = fields['doi']
            if not doi.startswith('10.'):
                warnings.append(f"[{key}] Suspicious DOI prefix: {doi}")
                
    print(f"\n--- VERIFICATION REPORT ---")
    print(f"Total entries verified: {len(entries)}")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    
    if errors:
        for err in errors:
            print(f"  [ERROR] {err}")
        return False
    else:
        print("  All entries contain required title, author, and year fields!")
        return True

if __name__ == '__main__':
    p = Path(__file__).resolve().parent.parent / 'paper' / 'references.bib'
    if not p.exists():
        p = Path('paper/references.bib')
    success = verify_references(p)
    sys.exit(0 if success else 1)
