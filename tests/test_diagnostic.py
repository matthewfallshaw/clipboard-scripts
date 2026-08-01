"""Diagnostic tests to understand the test environment."""

import subprocess
import os
import shutil
from pathlib import Path


def test_script_execution():
    """Test what happens when we actually run the script."""

    info = []
    info.append("=== SCRIPT EXECUTION DIAGNOSTICS ===")

    # Setup
    script_path = Path(__file__).parent.parent / "bin" / "pb-sentence-case"
    test_text = "i love apple products"

    # Put text in clipboard
    subprocess.run(['/usr/bin/pbcopy'], input=test_text, text=True, check=True)

    # Run script
    result = subprocess.run(
        [str(script_path)],
        capture_output=True,
        text=True,
        timeout=15
    )

    info.append(f"\nInput text: {test_text}")
    info.append(f"\nScript exit code: {result.returncode}")
    info.append(f"\nScript stdout:\n{result.stdout}")
    info.append(f"\nScript stderr:\n{result.stderr}")

    # Get result from clipboard
    output = subprocess.run(
        ['/usr/bin/pbpaste'],
        capture_output=True,
        text=True,
        check=True
    ).stdout

    info.append(f"\nClipboard output: {output}")
    info.append(f"\nExpected: I love Apple products")
    info.append(f"\nGot proper noun capitalization: {'Apple' in output}")

    message = "\n".join(info)
    print(message)

    assert False, f"\n{message}\n\nDIAGNOSTIC TEST - INTENTIONAL FAILURE"


def test_environment_inspection():
    """Inspect the test environment and fail to show output."""

    info = []
    info.append("=== ENVIRONMENT DIAGNOSTICS ===")

    # Check PATH
    path = os.environ.get('PATH', '')
    info.append(f"\nPATH:\n{path}")

    # Check for claude
    claude_path = shutil.which('claude')
    info.append(f"\nshutil.which('claude'): {claude_path}")

    # Try to find claude manually
    if not claude_path:
        common_locations = [
            '/etc/profiles/per-user/matt/bin/claude',
            '/usr/local/bin/claude',
            '/opt/homebrew/bin/claude',
        ]
        info.append("\nChecking common locations:")
        for loc in common_locations:
            exists = Path(loc).exists()
            info.append(f"  {loc}: {'EXISTS' if exists else 'not found'}")

    # Check what happens when script runs
    script_path = Path(__file__).parent.parent / "bin" / "pb-sentence-case"
    info.append(f"\nScript path: {script_path}")
    info.append(f"Script exists: {script_path.exists()}")

    if script_path.exists():
        # Try running with some debug
        result = subprocess.run(
            ["python3", "-c",
             "import shutil, os; print('PATH:', os.environ.get('PATH', '')); print('claude:', shutil.which('claude'))"],
            capture_output=True,
            text=True
        )
        info.append(f"\nFrom subprocess (python3 -c):")
        info.append(f"stdout: {result.stdout}")
        info.append(f"stderr: {result.stderr}")

    # Print everything
    message = "\n".join(info)
    print(message)

    # Unconditionally fail to show output
    assert False, f"\n{message}\n\nDIAGNOSTIC TEST - INTENTIONAL FAILURE"
