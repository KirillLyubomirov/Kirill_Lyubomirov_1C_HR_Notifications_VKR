#!/usr/bin/env python3
"""Check archived acceptance results; this does not rerun the 1C platform."""
from pathlib import Path
import json
root=Path(__file__).resolve().parent/'evidence'
def load(name):
    data=json.loads((root/'cases'/name).read_text(encoding='utf-8-sig'))
    assert data['ok'] is True,name
    assert data['version']=='0.12.1',name
    assert data['at'].startswith('2026-09-10'),name
    return data
s=load('full_batch_send.json')['snapshot']
