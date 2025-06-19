import os
import subprocess

from custom_predictor import CustomPredictorMetadata


def top_level_path() -> str:
    if __package__ is None:
        raise ValueError("top_level_path() must be called from within a package")

    packages = __package__.split(".")
    cur_dir = os.path.dirname(__file__)
    for _ in packages:
        cur_dir = os.path.dirname(cur_dir)
    return cur_dir


def build_args() -> list[str]:
    metadata = CustomPredictorMetadata()
    return ["docker", "build", top_level_path(), "-t", metadata.name]


def build_docker_image():
    args = build_args()
    print(" ".join(args))

    os.execvp(args[0], args)


def import_to_cradle():
    cwd = top_level_path()

    # Make sure git is clean
    out = subprocess.run(["git", "status", "--porcelain"], stdout=subprocess.PIPE, cwd=cwd)
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
