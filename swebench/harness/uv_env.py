import hashlib
import subprocess
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "swebench" / "envs"


def _hash_scripts(scripts: list[str]) -> str:
    m = hashlib.sha256()
    m.update("\n".join(scripts).encode())
    return m.hexdigest()[:22]


def get_env_path(env_key: str) -> Path:
    return CACHE_DIR / env_key


def create_env(scripts: list[str], env_key: str | None = None) -> Path:
    """Create a uv-managed environment and run install scripts."""
    if env_key is None:
        env_key = _hash_scripts(scripts)
    env_path = get_env_path(env_key)
    if not env_path.exists():
        env_path.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["uv", "venv", str(env_path)], check=True)
        for cmd in scripts:
            subprocess.run(
                f"source {env_path}/bin/activate && {cmd}",
                shell=True,
                check=True,
                executable="/bin/bash",
            )
    return env_path
    