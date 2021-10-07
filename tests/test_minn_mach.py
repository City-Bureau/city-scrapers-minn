from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.minn_mach import MinnMachSpider

test_response = file_response(
    join(dirname(__file__), "files", "minn_mach.html"),
    url="https://lims.minneapolismn.gov/Calendar/GetCalenderList?fromDate=Dec%2031,%202017&toDate=none&meetingType=2&committeeId=183&pageCount=10000&offsetStart=0&abbreviation=ZBA&keywords=&sortOrder=6",
)
spider = MinnMachSpider()

freezer = freeze_time("2021-08-23")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_title():
    assert parsed_items[0]["title"] == "Minneapolis Advisory Committee on Housing"


def test_start():
    assert parsed_items[0]["start"] == datetime(2019, 2, 13, 15, 0)


def test_status():
    assert parsed_items[0]["status"] == "passed"


def test_classification():
    assert parsed_items[0]["classification"] == "Advisory Committee"


# @pytest.mark.parametrize("item", parsed_items)
def test_all_day():
    assert parsed_items[0]["all_day"] is False


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Room 333, City Hall",
        "address": "350 S. 5th St., Minneapolis, MN 55415"
    }


def test_source():
    assert parsed_items[0]["source"] == "https://lims.minneapolismn.gov/Boards/Meetings/MACH"


def test_links():
    assert parsed_items[0]["links"] == []

