from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.minn_bud_comm import MinnBudCommSpider

test_response = file_response(
    join(dirname(__file__), "files", "minn_bud_comm.html"),
    url="https://lims.minneapolismn.gov/Calendar/GetCalenderList?fromDate=Dec%2031,%202017&toDate=null&meetingType=1&committeeId=179&pageCount=10000&offsetStart=0&abbreviation=undefined&keywords=",
)
spider = MinnBudCommSpider()

freezer = freeze_time("2021-08-31")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_title():
    assert parsed_items[0]["title"] == "Budget Committee"


def test_start():
    assert parsed_items[0]["start"] == datetime(2018, 8, 27, 13, 30)


def test_status():
    assert parsed_items[0]["status"] == "cancelled"


def test_classification():
    assert parsed_items[0]["classification"] == "Committee"


# @pytest.mark.parametrize("item", parsed_items)
def test_all_day():
    assert parsed_items[0]["all_day"] is False


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Room 317, City Hall",
        "address": "350 S. 5th St., Minneapolis, MN 55415"
    }


def test_source():
    assert parsed_items[0]["source"] == "https://lims.minneapolismn.gov/Calendar/citycouncil/upcoming/Budget"


def test_links():
    assert parsed_items[0]["links"] == []

