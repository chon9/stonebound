"""Isolated full-campaign save for visual QA; never touches the player's save."""
import os
import sys
import threading
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
os.environ['STONEBOUND_DATA_DIR']=str(ROOT/'.runtime/campaign-fixture')
from stonebound.app import Stonebound
from stonebound.catalog import OPPONENTS
from server import ThreadingHTTPServer, make_handler

app=Stonebound(ROOT/'.runtime/campaign-fixture/save.json')
if not app.progress.data['defeated']:
    for r in OPPONENTS: app.progress.reward(r['id'],True,'B+0.5')
app.settings({'language':'zh-CN'})
server=ThreadingHTTPServer(('127.0.0.1',8767),make_handler(app))
threading.Thread(target=app.initialize,daemon=True).start()
print('Isolated completed-campaign visual fixture: http://127.0.0.1:8767',flush=True)
try: server.serve_forever()
except KeyboardInterrupt: pass
finally: app.bridge.close();server.server_close()
