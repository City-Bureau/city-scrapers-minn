from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.minn_bud_comm import MinnBudCommSpider

test_response = file_response(
    join(dirname(__file__), "files", "minn_board.html"),
    url="https://lims.minneapolismn.gov/Calendar/GetCalenderList?fromDate=Nov%2028,%202021&toDate=Jan%201,%202022&meetingType=0&committeeId=null&pageCount=1000&offsetStart=0&abbreviation=undefined&keywords=",
)
spider = MinnBudCommSpider()

freezer = freeze_time("2021-08-31")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_title():
    assert parsed_items[0]["title"] == "Redistricting Group"


def test_start():
    assert parsed_items[0]["start"] == datetime(2021, 11, 29, 16, 0)


def test_status():
    assert parsed_items[0]["status"] == "tentative"


def test_classification():
    assert parsed_items[0]["classification"] == "Committee"


# @pytest.mark.parametrize("item", parsed_items)
def test_all_day():
    assert parsed_items[0]["all_day"] is False


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Online Meeting",
        "address": "Remote"
    }


def test_source():
    assert parsed_items[0]["source"] == "https://lims.minneapolismn.gov/Calendar/citycouncil/upcoming/RG"


def test_links():
    assert parsed_items[0]["links"] == []

