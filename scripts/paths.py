import os, pathlib

ROOT = pathlib.Path(__file__).parent.parent
# TESTS = ROOT / "tests"
SETUP_DATASET_SCRIPTS = ROOT / "setup_scripts" / "fill_dbs" / "load_datasets"
RUN_DBS_SCRIPT = ROOT / "setup_scripts" / "init_dbs.py"
FILL_DBS_SCRIPT = ROOT / "setup_scripts" / "fill_dbs" / "init_collections.py"
LLM_SERVER_PATH = ROOT / "llm_server"


def configure_python_path():
    python_path = os.getenv("PYTHONPATH")

    if python_path is None:
        os.environ["PYTHONPATH"] = str(ROOT)
    else:
        os.environ["PYTHONPATH"] += ";" + str(ROOT)
    print("Configure python path: ", os.getenv("PYTHONPATH"))
