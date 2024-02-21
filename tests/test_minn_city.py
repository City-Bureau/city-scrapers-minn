import unittest
from datetime import datetime

from city_scrapers_core.constants import BOARD, CITY_COUNCIL, COMMITTEE, NOT_CLASSIFIED

from city_scrapers.mixins.minn_city import MinnCityMixin


class TestMinnCityMixin(unittest.TestCase):

    def setUp(self):
        self.spider = MinnCityMixin(name="Test Spider")

    def test_parse_classification(self):
        item = {"CommitteeName": "Sample Board Meeting"}
        self.assertEqual(self.spider._parse_classification(item), BOARD)

        item = {"CommitteeName": "Sample Committee Session"}
        self.assertEqual(self.spider._parse_classification(item), COMMITTEE)

        item = {"CommitteeName": "City Council Discussion"}
        self.assertEqual(self.spider._parse_classification(item), CITY_COUNCIL)

        item = {"CommitteeName": "Other Meeting"}
        self.assertEqual(self.spider._parse_classification(item), NOT_CLASSIFIED)

    def test_parse_start(self):
        item = {"MeetingTime": "2023-04-04T10:37:59"}
        expected = datetime(2023, 4, 4, 10, 37, 59)
        self.assertEqual(self.spider._parse_start(item), expected)

    def test_parse_location(self):
        item = {"Location": "City Hall", "Address": "123 Main St"}
        expected = {"address": "123 Main St", "name": "City Hall"}
        self.assertEqual(self.spider._parse_location(item), expected)

        item = {"Location": "Online Meeting", "Address": "Online Meeting"}
        expected = {"address": "Remote", "name": "Online Meeting"}
        self.assertEqual(self.spider._parse_location(item), expected)

    def test_parse_links(self):
        # Assuming your spider has a 'links' attribute with default links
        item = {
            "CommitteeReportDocument": "Some Document",
            "CommitteeReportDocumentId": 123,
            "Abbreviation": "SampleMeeting",
        }
        result = self.spider._parse_links(item)
        # Check if the default links are included
        self.assertTrue(
            any(link["title"] == "Meeting materials (council)" for link in result)
        )
        # Check if the new link is added correctly
        self.assertTrue(
            any(link["href"].endswith("123/Some-Document") for link in result)
        )


if __name__ == "__main__":
    unittest.main()
