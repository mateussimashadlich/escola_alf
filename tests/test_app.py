import pytest

from ./ import app

appl = app.create_app()


@pytest.fixture
def app():
    yield appl

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def client():
    db_fd, appl.config['DATABASE'] = tempfile.mkstemp()
    appl.config['TESTING'] = True

    with appl.test_client() as client:
        with appl.app_context():
            flaskr.init_db()
        yield client

    os.close(db_fd)
    os.unlink(flaskr.app.config['DATABASE'])

