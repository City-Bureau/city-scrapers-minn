from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.minn_cassdab import MinnCassdabSpider

test_response = file_response(
    join(dirname(__file__), "files", "minn_cassdab.html"),
    url="https://lims.minneapolismn.gov/Calendar/GetCalenderList?fromDate=Dec%2031,%202017&toDate=none&meetingType=2&committeeId=152&pageCount=10000&offsetStart=0&abbreviation=ZBA&keywords=&sortOrder=6",
)
spider = MinnCassdabSpider()

freezer = freeze_time("2021-08-23")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()



"""
Uncomment below
"""

def test_title():
    assert parsed_items[0]["title"] == "Central Avenue Special Service District Advisory Board"


# def test_description():
#     assert parsed_items[0]["description"] == "EXPECTED DESCRIPTION"


def test_start():
    assert parsed_items[0]["start"] == datetime(2019, 3, 28, 11, 30)


# def test_end():
#     assert parsed_items[0]["end"] == datetime(2019, 1, 1, 0, 0)


# def test_time_notes():
#     assert parsed_items[0]["time_notes"] == "EXPECTED TIME NOTES"


# def test_id():
#     assert parsed_items[0]["id"] == "EXPECTED ID"


def test_status():
    assert parsed_items[0]["status"] == "passed"


# def test_location():
#     assert parsed_items[0]["location"] == {
#         "name": "EXPECTED NAME",
#         "address": "EXPECTED ADDRESS"
#     }


# def test_source():
#     assert parsed_items[0]["source"] == "EXPECTED URL"


# def test_links():
#     assert parsed_items[0]["links"] == [{
#       "href": "EXPECTED HREF",
#       "title": "EXPECTED TITLE"
#     }]


def test_classification():
    assert parsed_items[0]["classification"] == "Advisory Committee"


# @pytest.mark.parametrize("item", parsed_items)
def test_all_day():
    assert parsed_items[0]["all_day"] is False
