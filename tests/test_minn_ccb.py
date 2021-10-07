from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.minn_ccb import MinnCcbSpider

test_response = file_response(
    join(dirname(__file__), "files", "minn_ccb.html"),
    url="https://lims.minneapolismn.gov/Calendar/GetCalenderList?fromDate=Dec%2031,%202017&toDate=none&meetingType=4&committeeId=165&pageCount=10000&offsetStart=0&abbreviation=ZBA&keywords=&sortOrder=6",
)
spider = MinnCcbSpider()

freezer = freeze_time("2021-08-23")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


"""
Uncomment below
"""

def test_title():
    assert parsed_items[0]["title"] == "City Canvassing Board"


def test_start():
    assert parsed_items[0]["start"] == datetime(2018, 11, 16, 9, 15)


def test_status():
    assert parsed_items[0]["status"] == "passed"


def test_classification():
    assert parsed_items[0]["classification"] == "Board"


# @pytest.mark.parametrize("item", parsed_items)
def test_all_day():
    assert parsed_items[0]["all_day"] is False


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Room 317, City Hall",
        "address": "350 S. 5th St., Minneapolis, MN 55415"
    }


def test_source():
    assert parsed_items[0]["source"] == "https://lims.minneapolismn.gov/IndependentBodies/IndependentBodiesMeetings/Canvass"


def test_links():
    assert parsed_items[0]["links"] == [{
        "title": "Report Document",
        "href": "https://lims.minneapolismn.gov/Download/CommitteeReport/1370/Canvassing-Board-Proceedings-11.16.2018.pdf"
    }]

