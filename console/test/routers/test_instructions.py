from src.console.services.kafka_service import KafkaService
from test.conftest import get_test_client, override_kafka_service_dep


class DummyKafkaService(KafkaService):
    def __init__(self):
        self.published = []

    async def publish(self, instructions):
        self.published = instructions


class TestInstructionRouter:
    base_url = "/instructions/"
    client = get_test_client()

    def test_when_invalid_json__then_validation_error(self):
        response = self.client.post(self.base_url, json=[{"name": "test"}])
        assert response.status_code == 422

    def test_when_valid_json__then_publish(self):
        ks = DummyKafkaService()
        override_kafka_service_dep(ks)
        response = self.client.post(self.base_url, json=[{"name": "EXIT", "params": []}])
        assert response.status_code == 200
        assert len(ks.published) == 1
