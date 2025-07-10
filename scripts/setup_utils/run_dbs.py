import docker, time, subprocess, sys, pathlib, platform


def run_docker_windows(
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


def run_docker_linux(timeout: int = 10) -> None:
    status = subprocess.run(
        ["systemctl", "is-active", "docker"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    )
    if status.stdout.strip() != "active":
        try:
            subprocess.run(
                ["sudo", "systemctl", "start", "docker"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
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
        if platform.system() == "Windows":
            run_docker_windows()
        else:
            run_docker_linux()
        self.client = docker.from_env()
        try:
            self.network = self.client.networks.get("weaviate_net")
        except docker.errors.NotFound:
            self.network = self.client.networks.create("weaviate_net", driver="bridge")

    def create_container(self, **container_params):
        self.client.containers.run(**container_params)
