import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base
import redis
import mock
import requests_mock

@pytest.fixture
def db_session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

@pytest.fixture
def redis_client():
    return mock.Mock(spec=redis.Redis)

@pytest.fixture
def mock_llm_response():
    return {
        "summary": "Test summary",
        "model": "test-model"
    } 

@pytest.fixture
def mock_scraper():
    return mock.Mock(name="test_scraper")

@pytest.fixture
def mock_nlp_processor():
    processor = mock.Mock()
    processor.filter_irrelevant_content.return_value = True
    processor.extract_keywords.return_value = ["test", "keywords"]
    return processor

@pytest.fixture
def mock_llm_handler():
    handler = mock.Mock()
    handler.generate_summary.return_value = {
        "summary": "Test summary",
        "model": "test-model"
    }
    return handler

@pytest.fixture
def mock_webdriver():
    return mock.Mock()

@pytest.fixture
def requests_mock():
    with requests_mock.Mocker() as m:
        yield m 