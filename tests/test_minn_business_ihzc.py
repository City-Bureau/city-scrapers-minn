from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.minn_business_ihzc import MinnBusinessIhzcSpider

test_response = file_response(
    join(dirname(__file__), "files", "minn_business_ihzc.html"),
    url="https://lims.minneapolismn.gov/Calendar/GetCalenderList?fromDate=Dec%2031,%202017&toDate=null&meetingType=1&committeeId=220&pageCount=1000&offsetStart=0&abbreviation=undefined&keywords=",
)
spider = MinnBusinessIhzcSpider()

freezer = freeze_time("2021-09-01")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()



"""
Uncomment below
"""
def test_title():
    assert parsed_items[0]["title"] == "Business, Inspections, Housing & Zoning Committee"


def test_start():
    assert parsed_items[0]["start"] == datetime(2020, 9, 8, 13, 30)


def test_status():
    assert parsed_items[0]["status"] == "passed"


def test_classification():
    assert parsed_items[0]["classification"] == "Committee"


# @pytest.mark.parametrize("item", parsed_items)
def test_all_day():
    assert parsed_items[0]["all_day"] is False


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Online Meeting",
        "address": None
    }


def test_source():
    assert parsed_items[0]["source"] == "https://lims.minneapolismn.gov/Calendar/citycouncil/upcoming/BIHZ"


def test_links():
    assert parsed_items[0]["links"] == []

