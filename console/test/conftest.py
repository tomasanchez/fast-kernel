from src.console.main import app
from src.console.dependencies import get_kafka_service
from src.console.services.kafka_service import KafkaService


def get_test_client():
    from starlette.testclient import TestClient
    return TestClient(app)


def override_kafka_service_dep(ks: KafkaService):
    app.dependency_overrides[get_kafka_service] = lambda: ks
