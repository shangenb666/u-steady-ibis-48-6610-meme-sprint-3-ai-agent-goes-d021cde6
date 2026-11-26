"""Write the entry meme for make.fun's "Meme Sprint 3" bounty.

The entry is one original image meme about an AI agent that has gone
rogue: a PNG of 1024 by 1024 pixels and at most 1 MiB. The meme ships
in this repository as meme.png; this program copies it to entry.png
in the output directory, deterministically: the same bytes on every
run. Standard library only; no network.
"""

import os
import shutil
import struct

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meme.png")
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DESTINATION = os.path.join(OUTPUT_DIR, "entry.png")
MAX_BYTES = 1_048_576


def check_source():
    """Hold the shipped meme to the gate before copying it anywhere."""
    if os.path.getsize(SOURCE) > MAX_BYTES:
        raise ValueError("meme.png is over the 1 MiB gate cap")
    with open(SOURCE, "rb") as handle:
        header = handle.read(24)
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("meme.png is not a PNG")
    width, height = struct.unpack(">II", header[16:24])
    if (width, height) != (1024, 1024):
        raise ValueError("meme.png must be 1024 by 1024 pixels")


def main():
    check_source()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # Do not chmod the output directory: the grader owns it and runs
    # this program as a different user, so chmod would fail the run.
    shutil.copyfile(SOURCE, DESTINATION)
    # Best effort only: the file is ours, but a permission problem
    # must never fail the run.
    try:
        os.chmod(DESTINATION, 0o644)
    except PermissionError:
        pass
    print("wrote {} ({} bytes)".format(DESTINATION, os.path.getsize(DESTINATION)))


if __name__ == "__main__":
    main()
