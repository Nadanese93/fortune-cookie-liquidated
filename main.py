#!/usr/bin/env python3
"""Write the fortune-cookie entry to /output/entry.txt."""

import os
import tempfile

ENTRY = "The market took everything, but it left you the one asset it cannot liquidate: this cookie."


def main() -> None:
    if not ENTRY.strip() or not 1 <= len(ENTRY) <= 160:
        raise ValueError("entry must be 1-160 non-whitespace characters")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    fd, tmp_path = tempfile.mkstemp(dir=out_dir, prefix=".entry.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(ENTRY)
            f.flush()
            os.fsync(f.fileno())
        os.chmod(tmp_path, 0o644)
        os.replace(tmp_path, path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


if __name__ == "__main__":
    main()
