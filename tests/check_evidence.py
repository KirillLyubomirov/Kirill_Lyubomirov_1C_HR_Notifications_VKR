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
assert (s['events'],s['notifications'],s['sent'],len(s['attempts']),len(s['decisions']))==(60,120,120,130,10)
assert all(q['State']=='Принято SMTP-сервером' for q in s['queue'])
t=load('full_batch_workflow.json')['tasks']
assert len(t)==50 and all(x['Выполнена'] for x in t)
assert len({x['БизнесПроцесс'] for x in t})==10
sets=[]
for name,ev,n in [('A',6,12),('B',6,12),('None',0,0)]:
    v=load('display_rls_'+name+'_ok.json')['visible']
    assert len(v['events'])==ev and len(v['notifications'])==n
    assert v['subject_write_denied'] and v['unfiltered_read_denied']
    sets.append({x['Ссылка'] for x in v['events']})
assert not sets[0]&sets[1]
print('OK: archived acceptance metrics, completed tasks and role boundaries agree.')
