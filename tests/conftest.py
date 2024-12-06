import logging
from unittest import mock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def mock_session():
    from hispanie.db import Base

    # TODO put db params in a ini file
    engine = create_engine("postgresql://postgres:postgres@127.0.0.1:5432/hispanie_test")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)

    with mock.patch("hispanie.db.session") as mocked_session:
        session = Session()
        mocked_session.add.side_effect = session.add
        mocked_session.commit.side_effect = session.flush
        mocked_session.delete.side_effect = session.delete
        mocked_session.query.side_effect = session.query
        yield mocked_session


@pytest.fixture
@mock.patch("hispanie.db.initialize")
def client(func_initialize):
    def mock_initialize(value):
        return value

    func_initialize.side_effect = mock_initialize

    from hispanie.api.api import app

    return TestClient(app)
