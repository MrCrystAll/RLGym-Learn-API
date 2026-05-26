import json

from rlgym_learn_api.main import app

with open("openapi.json", "w") as f:
    _open_api = app.openapi()
    _open_api["servers"] = [{"url": "http://localhost:8000"}]
    json.dump(_open_api, f)
