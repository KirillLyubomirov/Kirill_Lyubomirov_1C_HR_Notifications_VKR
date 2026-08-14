#!/usr/bin/env python3
"""Verify the saved repository bytes. No 1C runtime is started."""
from pathlib import Path
import hashlib,sys
root=Path(__file__).resolve().parents[1]
expected={}
for line in (root/'CHECKSUMS.sha256').read_text(encoding='utf-8').splitlines():
    digest,name=line.split('  ',1)
