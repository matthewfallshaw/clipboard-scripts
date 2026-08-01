"""Clipboard access and user notification for the pb-* scripts.

Scripts in the repo root reach this module with::

    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
    from pbclip import transform

``Path(__file__).resolve()`` is what makes symlink installation work: ``bin/pb-foo``
is a symlink back to the repo root, and resolving it finds the real ``lib/``.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Callable, Optional, Sequence

LIB_DIR: Path = Path(__file__).resolve().parent
REPO_DIR: Path = LIB_DIR.parent
NOTIFY_SCRIPT: Path = LIB_DIR / "notify"

# Quicksilver and Alfred launch scripts with a bare PATH, so anything not in
# /usr/bin or /bin has to be hunted for.
SEARCH_PATHS: "tuple[str, ...]" = (
    os.path.expanduser("~/.nix-profile/bin"),
    "/etc/profiles/per-user/%s/bin" % os.environ.get("USER", ""),
    "/run/current-system/sw/bin",
    "/opt/homebrew/bin",
    "/usr/local/bin",
    "/opt/local/bin",
)


def paste() -> str:
    """Return the clipboard's text content."""
    return subprocess.run(
        ["/usr/bin/pbpaste"], capture_output=True, text=True, check=True
    ).stdout


def copy(text: str) -> None:
    """Replace the clipboard's text content."""
    subprocess.run(["/usr/bin/pbcopy"], input=text, text=True, check=True)


def notify(message: str, sticky: bool = False) -> None:
    """Show `message` to the user via lib/notify."""
    command = [str(NOTIFY_SCRIPT)]
    if sticky:
        command.append("--sticky")
    command.append(message)
    subprocess.run(command, check=False)


def transform(
    fn: Callable[[str], str], sticky: bool = False, notify_result: bool = True
) -> str:
    """Apply `fn` to the clipboard, put the result back, and show it.

    The shape almost every pb-* script wants. Returns the new content.
    """
    result = fn(paste())
    copy(result)
    if notify_result:
        notify(result, sticky)
    return result


def osascript(script: str, args: Optional[Sequence[str]] = None) -> str:
    """Run an AppleScript and return its output.

    `args` are passed as argv items, so they need no AppleScript escaping; the
    script must wrap itself in ``on run argv`` / ``end run`` to read them.
    """
    command = ["/usr/bin/osascript", "-"]
    if args:
        command.extend(args)
    return subprocess.run(
        command, input=script, capture_output=True, text=True, check=True
    ).stdout.rstrip("\n")


def find_binary(name: str) -> Optional[str]:
    """Locate an external binary, searching beyond a launcher's bare PATH."""
    found = shutil.which(name)
    if found:
        return found
    for directory in SEARCH_PATHS:
        candidate = Path(directory) / name
        if candidate.is_file() and os.access(str(candidate), os.X_OK):
            return str(candidate)
    return None


def require_binary(name: str) -> str:
    """Locate an external binary, or tell the user it's missing and stop."""
    found = find_binary(name)
    if found is None:
        die("%s isn't installed (or I can't find it)." % name)
    return found  # type: ignore[return-value]


def die(message: str, sticky: bool = False) -> "None":
    """Tell the user why we're not doing what they asked, and stop."""
    notify(message, sticky)
    sys.exit(1)
