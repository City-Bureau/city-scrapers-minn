from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.minn_tpw_comm import MinnTpwCommSpider

test_response = file_response(
    join(dirname(__file__), "files", "minn_tpw_comm.html"),
    url="https://lims.minneapolismn.gov/Calendar/GetCalenderList?fromDate=Sep%201,%202021&toDate=null&meetingType=1&committeeId=13&pageCount=null&offsetStart=0&abbreviation=undefined&keywords=",
)
spider = MinnTpwCommSpider()

freezer = freeze_time("2021-09-01")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()



def test_title():
    assert parsed_items[0]["title"] == "Transportation & Public Works Committee"


def test_start():
    assert parsed_items[0]["start"] == datetime(2021, 9, 15, 13, 30)


def test_status():
    assert parsed_items[0]["status"] == "tentative"


def test_classification():
    assert parsed_items[0]["classification"] == "Committee"


# @pytest.mark.parametrize("item", parsed_items)
def test_all_day():
    assert parsed_items[0]["all_day"] is False


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Online Meeting ",
        "address": "Minneapolis, MN"
    }


def test_source():
    assert parsed_items[0]["source"] == "https://lims.minneapolismn.gov/Calendar/citycouncil/upcoming/TPW"


def test_links():
    assert parsed_items[0]["links"] == []

