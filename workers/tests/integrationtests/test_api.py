"""
Testing FastAPI Applications:
https://fastapi.tiangolo.com/tutorial/testing/
"""

import json
import unittest

import geojson
from fastapi.testclient import TestClient

from ohsome_quality_analyst.api.api import app

from .api_response_schema import get_general_schema, get_result_schema


class TestApi(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.general_schema = get_general_schema()
        self.result_schema = get_result_schema()

    def test_get_available_regions(self):
        url = "/regions?asGeoJSON=true"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_content = json.loads(response.content)
        self.assertTrue(self.general_schema.is_valid(response_content))
        result = geojson.loads(json.dumps(response_content))
        self.assertTrue(result.is_valid)
        url = "/regions?asGeoJSON=false"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_content = json.loads(response.content)
        self.assertTrue(self.general_schema.is_valid(response_content))
        url = "/regions"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_content = json.loads(response.content)
        self.assertTrue(self.general_schema.is_valid(response_content))

    def test_list_indicators(self):
        url = "/indicatorNames"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response_content = json.loads(response.content)
        self.assertTrue(self.general_schema.is_valid(response_content))
        self.assertTrue(self.result_schema.is_valid(response_content))

    def test_list_layers(self):
        url = "/layerNames"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response_content = json.loads(response.content)
        self.assertTrue(self.general_schema.is_valid(response_content))
        self.assertTrue(self.result_schema.is_valid(response_content))

    def test_list_datasets(self):
        url = "/datasetNames"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response_content = json.loads(response.content)
        self.assertTrue(self.general_schema.is_valid(response_content))
        self.assertTrue(self.result_schema.is_valid(response_content))

    def test_list_fid_field(self):
        url = "/FidFields"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response_content = json.loads(response.content)
        self.assertTrue(self.general_schema.is_valid(response_content))
        self.assertTrue(self.result_schema.is_valid(response_content))

    def test_list_reports(self):
        url = "/reportNames"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response_content = json.loads(response.content)
        self.assertTrue(self.general_schema.is_valid(response_content))
        self.assertTrue(self.result_schema.is_valid(response_content))


if __name__ == "__main__":
    unittest.main()
