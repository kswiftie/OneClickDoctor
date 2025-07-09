import docker, time, subprocess, sys, pathlib


def run_docker(
    dockerpath: str = '"C:\\Program Files\\Docker\\Docker\\Docker Desktop.exe"',
    timeout: int = 10,
) -> None:
    subprocess.run(["powershell.exe", "Start-Process", dockerpath])
    deadline = timeout + time.time()

    while True:
        try:
            result = subprocess.run(
                ["docker", "info"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=1,
            )
            if result.returncode == 0:
                return
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        if time.time() > deadline:
            sys.exit(1)


class DockerManager:
    def __init__(self):
        run_docker()
        self.client = docker.from_env()
        try:
            self.network = self.client.networks.get("weaviate_net")
        except docker.errors.NotFound:
            self.network = self.client.networks.create("weaviate_net", driver="bridge")

    def create_container(self, **container_params):
        self.client.containers.run(**container_params)
