#!/usr/bin/env python3
"""Verify the saved repository bytes. No 1C runtime is started."""
from pathlib import Path
import hashlib,sys
root=Path(__file__).resolve().parents[1]
expected={}
for line in (root/'CHECKSUMS.sha256').read_text(encoding='utf-8').splitlines():
    digest,name=line.split('  ',1)
    path=(root/name).resolve()
    if not path.is_relative_to(root) or path.is_symlink() or not path.is_file():
        raise SystemExit('Missing or unsafe file: '+name)
    if hashlib.sha256(path.read_bytes()).hexdigest()!=digest:
        raise SystemExit('Checksum mismatch: '+name)
    expected[name]=digest
actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and '.git' not in p.relative_to(root).parts and '__pycache__' not in p.parts and p.name!='CHECKSUMS.sha256'}
if actual!=set(expected):raise SystemExit('File inventory differs: '+str(sorted(actual^set(expected))))
print('OK: '+str(len(expected))+' files; original byte content verified.')
