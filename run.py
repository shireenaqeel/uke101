import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from koa.app import main

if __name__ in {"__main__", "__mp_main__"}:
    main()
