from test.conftest import get_test_client


class TestRoot:

    def test_root_is_docs(self):
        response = get_test_client().get("/")
        assert response.status_code == 200
        assert 'swagger-ui' in response.text
