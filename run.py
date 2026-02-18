#!/usr/bin/env python3
"""Backward-compatible shim: re-exports Click CLI implemented in `run_click.py`."""
from run_click import main


if __name__ == "__main__":
    raise SystemExit(main())
