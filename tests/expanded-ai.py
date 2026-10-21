"""Real KaTrain turns at intermediate and dan targets using the QA fixture."""
import json
import time
import urllib.request

BASE='http://127.0.0.1:8767/api/'

def request(route,body=None):
    data=json.dumps(body).encode() if body is not None else None
    req=urllib.request.Request(BASE+route,data=data,headers={'Content-Type':'application/json'})
    return json.load(urllib.request.urlopen(req,timeout=90))

for rival,size in [('kaede',13),('sora',19)]:
    state=request('state')
    if state['match'] and not state['match']['finished']:
        request('match/abandon',{})
    deadline=time.monotonic()+300
    while request('state')['engine']['status']!='ready':
        assert time.monotonic()<deadline
        time.sleep(.5)
    request('match/start',{'opponent':rival,'size':size})
    request('match/play',{'point':[3,3]})
    deadline=time.monotonic()+90
    while True:
        m=request('state')['match']
        if not m['thinking']:break
        assert time.monotonic()<deadline
        time.sleep(.2)
    assert not m['error'],m['error']
    assert m['moveNumber']==2 and m['moves'][1][0]=='W',m
    print(rival,size,m['moves'],flush=True)
    request('match/abandon',{})
print('PASS: new intermediate rival and final 4 dan target both generated real KaTrain moves.')
