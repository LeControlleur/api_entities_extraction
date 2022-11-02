from app import app
import unittest
import os
import sys
sys.path.append(os.path.join(os.getcwd()))


class RouteTestCase(unittest.TestCase):
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()

    def test_server_connection(self):
        response = self.client.post("/")
        assert response.status_code == 204

    def test_api_connection(self):
        response = self.client.post("/api")
        assert response.status_code == 200

    param_text = """
    Barclays boss Bob Diamond has been summoned to appear before the Treasury Select Committee on Wednesday.
    """

    def test_api_connection(self):
        response = self.client.post("/", data={"content": self.param_text})
        assert response.status_code == 200
        assert response.get_data() == list


if __name__ == "__main__":
    unittest.main()
