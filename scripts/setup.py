import subprocess, paths, sys


def fill_dbs():
    subprocess.check_call([sys.executable, paths.FILL_WEAVIATE])


def setup_dbs():
    subprocess.check_call([sys.executable, f"{paths.RUN_DBS_SCRIPT}"])
    subprocess.check_call([sys.executable, f"{paths.FILL_DBS_SCRIPT}"])


def setup_llm():
    subprocess.check_call(["docker", "build", "-t", "llm-api", paths.LLM_SERVER_PATH])
    subprocess.check_call(
        ["docker", "run", "--rm", "-it", "-p", "8000:8000", "llm-api"]
    )


def main_setup():
    paths.configure_python_path()
    setup_dbs()
    fill_dbs()
    setup_llm()


if __name__ == "__main__":
    main_setup()
