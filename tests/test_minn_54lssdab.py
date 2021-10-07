from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.minn_54lssdab import Minn54lssdabSpider

test_response = file_response(
    join(dirname(__file__), "files", "minn_54lssdab.html"),
    url="https://lims.minneapolismn.gov/Calendar/GetCalenderList?fromDate=Dec%2031,%202017&toDate=none&meetingType=2&committeeId=150&pageCount=10000&offsetStart=0&abbreviation=ZBA&keywords=&sortOrder=6",
)
spider = Minn54lssdabSpider()

freezer = freeze_time("2021-08-23")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_title():
    assert parsed_items[4]["title"] == "54th & Lyndale Special Service District Advisory Board"


def test_start():
    assert parsed_items[4]["start"] == datetime(2020, 2, 27, 14, 0)


def test_status():
    assert parsed_items[4]["status"] == "passed"


def test_classification():
    assert parsed_items[4]["classification"] == "Advisory Committee"


# @pytest.mark.parametrize("item", parsed_items)
def test_all_day():
    assert parsed_items[4]["all_day"] is False


def test_location():
    assert parsed_items[4]["location"] == {
        "name": "Washburn Library",
        "address": "5244 Lyndale Ave S"
    }


def test_source():
    assert parsed_items[4]["source"] == "https://lims.minneapolismn.gov/Boards/Meetings/54lyndale"


def test_links():
    assert parsed_items[4]["links"] == [{
        "title": "Report Document",
      "href": "https://lims.minneapolismn.gov/Download/CommitteeReport/1112/54th-&-Lyndale-02272020-regular-meeting-minutes.pdf"
    }]

