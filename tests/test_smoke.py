import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_package_imports():
    import koa

    assert koa.__version__


def test_app_and_pages_import():
    from koa import app
    from koa.pages import library, switching

    assert hasattr(app, "main")
    assert hasattr(library, "build_library")
    assert hasattr(switching, "build_switching")
