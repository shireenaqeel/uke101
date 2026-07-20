import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_package_imports():
    import koa

    assert koa.__version__


def test_app_module_imports():
    from koa import app

    assert hasattr(app, "build_library")
    assert hasattr(app, "main")
