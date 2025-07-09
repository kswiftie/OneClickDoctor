import json, pathlib
from run_dbs import DockerManager

dm = DockerManager()

JSON_ROOT = pathlib.Path(__file__).parent / "setup_data"
files = {"text2vec.json", "weaviate.json"}

for file_name in files:
    cur_path = JSON_ROOT / file_name
    with open(cur_path, encoding="utf-8") as f:
        data = json.load(f)
        dm.create_container(**data)
