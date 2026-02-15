"""
Launch the AKN Profiler language server when invoked with:

    python -m akn_profiler
"""

from akn_profiler.server import start_server

if __name__ == "__main__":
    start_server()
