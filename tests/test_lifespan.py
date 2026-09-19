import logging

from fastapi.testclient import TestClient

from my_fastapi_project.core import db
from my_fastapi_project.main import app


def test_lifespan_starts_and_cleans_up(caplog, monkeypatch):
    disposed = []

    async def spy_dispose(self):
        disposed.append(True)

    monkeypatch.setattr(db.AsyncEngine, "dispose", spy_dispose)

    with caplog.at_level(logging.INFO):
        with TestClient(app):
            pass

    messages = [r.getMessage() for r in caplog.records]

    assert any("应用启动" in m for m in messages)
    assert any("应用已关闭" in m for m in messages)
    assert disposed == [True]
