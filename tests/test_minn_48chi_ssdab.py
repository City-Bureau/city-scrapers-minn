from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.minn_48chi_ssdab import Minn48chiSsdabSpider

test_response = file_response(
    join(dirname(__file__), "files", "minn_48chi_ssdab.html"),
    url="https://lims.minneapolismn.gov/Calendar/GetCalenderList?fromDate=Dec%2031,%202017&toDate=none&meetingType=2&committeeId=153&pageCount=10000&offsetStart=0&abbreviation=ZBA&keywords=&sortOrder=6",
)
spider = Minn48chiSsdabSpider()

freezer = freeze_time("2021-08-23")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


"""
Uncomment below
"""


def test_title():
    assert parsed_items[1]["title"] == "48th & Chicago Special Service District Advisory Board"


def test_start():
    assert parsed_items[1]["start"] == datetime(2019, 7, 18, 15, 0)



def test_status():
    assert parsed_items[1]["status"] == "passed"



def test_classification():
    assert parsed_items[1]["classification"] == "Advisory Committee"


# @pytest.mark.parametrize("item", parsed_items)
def test_all_day():
    assert parsed_items[0]["all_day"] is False



def test_location():
    assert parsed_items[1]["location"] == {
        "name": "Pizza Biga",
        "address": "4762 Chicago Ave., Minneapolis, MN 55407"
    }

def test_source():
    assert parsed_items[1]["source"] == "https://lims.minneapolismn.gov/Boards/Meetings/48Chicago"

def test_links():
    print(parsed_items[1])
    assert parsed_items[1]["links"] == [{
        "title": "Report Document",
      "href": "https://lims.minneapolismn.gov/Download/CommitteeReport/1129/48th-&-Chicago-07182019-regular-meeting-minutes.pdf"
    }]

