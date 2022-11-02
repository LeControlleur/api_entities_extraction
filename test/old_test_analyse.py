import utils.entities_extraction as entities_extraction
import unittest
import os
import sys
from utils.entities_extraction import infosToFetch
sys.path.append(os.path.join(os.getcwd()))


class AnalysisTestCase(unittest.TestCase):

    param_text = """
Barclays boss Bob Diamond has been summoned to appear before the Treasury Select Committee on Wednesday.
    """

    def test_returned_entities(self):
        result = entities_extraction.entities_extraction("")
        assert result is not None

    def test_request_without_text(self):
        result = entities_extraction.entities_extraction("")
        expected_result = {
            "message": "Missing text"
        }
        assert result is not None
        assert result == expected_result

    def test_request_with_wrong_params(self):
        result = entities_extraction.entities_extraction(12)
        expected_result = {
            "message": "Please, provide a text for entities extraction"
        }
        assert result is not None
        assert result == expected_result

    def test_output_type(self):
        result = entities_extraction.entities_extraction(self.param_text)
        assert type(result) == list

    def test_empty_results(self):
        result = entities_extraction.entities_extraction("Potatoes")
        assert type(result) == list
        assert len(result) == 0

    def test_output_format(self):
        result = entities_extraction.entities_extraction(self.param_text)[0]
        assert len(result) > 0
        for i in result.keys():
            assert i in infosToFetch
            assert type(result[i]) == list and len(
                result[i] > 0) or (i != "age" and type(result[i]) == str) or (i == "age" and type(result[i]) == int)

if __name__ == "__main__":
    unittest.main()
