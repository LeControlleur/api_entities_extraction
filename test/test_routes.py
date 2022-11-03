from app import app
import unittest
import json
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
        assert response.status_code in [200, 400]

    param_text = """
    Barclays boss Bob Diamond has been summoned to appear before the Treasury Select Committee on Wednesday.
    """

    def test_api_without_content(self):
        response = self.client.post("/api", json={})
        assert response.status_code == 400
        assert response.json["message"] == "Empty request or bad arguments"

    def test_api_results(self):
        response = self.client.post("/api", json={"content": self.param_text})
        assert response.status_code == 200
        assert type(response.json["content"]) == list
        assert len(response.json["content"]) > 0

    def test_stats_results(self):
        response = self.client.get("/stats")
        assert response.status_code == 200
        assert type(response.json["content"]) == dict
        assert len(response.json["content"].keys()) > 0


if __name__ == "__main__":
    unittest.main()
