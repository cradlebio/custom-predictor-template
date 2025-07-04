import subprocess
from pathlib import Path

from custom_predictor import METADATA


def top_level_path() -> Path:
    out = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], stdout=subprocess.PIPE, cwd=str(Path(__file__).parent), check=True
    )
    return Path(out.stdout.decode("utf-8").strip())


def build_args() -> list[str]:
    return ["docker", "build", str(top_level_path()), "-t", METADATA.name]


def build_docker_image():
    args = build_args()
    print(" ".join(args))

    return subprocess.run(args).returncode


def import_to_cradle():
    cwd = str(top_level_path())

    # Make sure git is clean
    out = subprocess.run(["git", "status", "--porcelain"], stdout=subprocess.PIPE, cwd=cwd, check=True)
    if len(out.stdout) > 0:
        raise ValueError("Repository has uncommitted changes, please commit before importing the predictor")

    out = subprocess.run(["uv", "run", "pytest"], cwd=cwd)
    if out.returncode != 0:
        raise ValueError("Not all tests are passing")

    # 1. Build container for linux/amd64 platform
    # 2. `docker save` the result to a tarball
    # 3. Make API calls to create new predictor (version)
    #    - here we might need cr.be.platform_api_v2_sdk, or build it all ourselves including auth?
    # 4. Upload container image
    # 5. (optional?) Wait until provisioned
    # 6. git tag

    raise NotImplementedError("The `import` command is not yet implemented")
