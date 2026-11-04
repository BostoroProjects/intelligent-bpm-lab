from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1] / 'backend'))
from fastapi.testclient import TestClient
from main import app
client=TestClient(app)
def test_health():
    assert client.get('/api/health').json()['status']=='ok'
def test_providers():
    data=client.get('/api/providers').json()
    assert set(data['providers'])=={'OpenAI','Claude','DeepSeek','Kimi','Qwen'}
def test_reject_invalid_provider():
    r=client.post('/api/run',json={'provider':'Unknown','model':'x','api_key':'test','case_input':'case'})
    assert r.status_code==422
def test_reject_invalid_model():
    r=client.post('/api/run',json={'provider':'OpenAI','model':'bad model with spaces','api_key':'test','case_input':'case'})
    assert r.status_code==422
