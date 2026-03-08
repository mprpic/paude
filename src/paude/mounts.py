"""Volume mount builder for paude containers."""

from __future__ import annotations

from pathlib import Path


def resolve_path(path: Path) -> Path | None:
    """Resolve symlinks to physical path.

    Args:
        path: Path to resolve.

    Returns:
        Resolved path, or None if path doesn't exist.
    """
    try:
        if path.exists():
            return path.resolve()
    except OSError:
        pass
    return None


def build_mounts(home: Path) -> list[str]:
    """Build the list of volume mount arguments for podman.

    Note: Workspace is NOT mounted here - it uses a named volume at /pvc/workspace.
    Users sync code via git remote (paude remote add + git push/pull).

    Note: gcloud ADC credentials are injected via Podman secrets, not bind mounts.

    Mounts (in order):
    1. Claude seed directory (ro, if exists)
    2. Plugins at original host path (ro, if exists)
    3. gitconfig (ro, if exists)
    4. claude.json seed (ro, if exists)

    Args:
        home: Path to the user's home directory.

    Returns:
        List of mount argument strings (e.g., ["-v", "/path:/path:rw", ...]).
    """
    mounts: list[str] = []

    # Claude seed directory (ro)
    claude_dir = home / ".claude"
    resolved_claude = resolve_path(claude_dir)
    if resolved_claude and resolved_claude.is_dir():
        mounts.extend(["-v", f"{resolved_claude}:/tmp/claude.seed:ro"])

        # Plugins at original host path (ro)
        plugins_dir = resolved_claude / "plugins"
        if plugins_dir.is_dir():
            mounts.extend(["-v", f"{plugins_dir}:{plugins_dir}:ro"])

    # gitconfig (ro)
    gitconfig = home / ".gitconfig"
    resolved_gitconfig = resolve_path(gitconfig)
    if resolved_gitconfig and resolved_gitconfig.is_file():
        mounts.extend(["-v", f"{resolved_gitconfig}:/home/paude/.gitconfig:ro"])

    # claude.json seed (ro)
    claude_json = home / ".claude.json"
    resolved_claude_json = resolve_path(claude_json)
    if resolved_claude_json and resolved_claude_json.is_file():
        mounts.extend(["-v", f"{resolved_claude_json}:/tmp/claude.json.seed:ro"])

    return mounts
