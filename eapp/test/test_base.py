import pytest
from flask import Flask

from eapp import db


def create_app():
    app = app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["PAGE_SIZE"] = 2
    app.config['TESTING'] = True
    app.secret_key = '34y394yjsbdkjsdjksdh'
    db.init_app(app)

    from eapp.index import register_routes
    register_routes(app)
    return app


@pytest.fixture
def test_app():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def test_client(test_app):
 return test_app.test_client()

@pytest.fixture
def test_session(test_app):
    yield db.session
    db.session.rollback()


