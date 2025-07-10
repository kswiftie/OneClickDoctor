import os, pathlib

ROOT = pathlib.Path(__file__).parent.parent
# TESTS = ROOT / "tests"
SETUP_DATASET_SCRIPTS = ROOT / "scripts" / "fill_dbs" / "load_sber"
RUN_DBS_SCRIPT = ROOT / "scripts" / "setup_utils" / "init_dbs.py"
FILL_DBS_SCRIPT = ROOT / "scripts" / "setup_utils" / "init_collections.py"
FILL_WEAVIATE = ROOT / "scripts" / "setup_utils" / "load_sber.py"
LLM_SERVER_PATH = ROOT / "llm_server"


def configure_python_path():
    python_path = os.getenv("PYTHONPATH")

    if python_path is None:
        os.environ["PYTHONPATH"] = str(ROOT)
    else:
        os.environ["PYTHONPATH"] += ";" + str(ROOT)
    print("Configure python path: ", os.getenv("PYTHONPATH"))
