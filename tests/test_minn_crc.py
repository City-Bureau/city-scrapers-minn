from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.minn_crc import MinnCrcSpider

test_response = file_response(
    join(dirname(__file__), "files", "minn_crc.html"),
    url="https://lims.minneapolismn.gov/Calendar/GetCalenderList?fromDate=Dec%2031,%202017&toDate=none&meetingType=4&committeeId=45&pageCount=10000&offsetStart=0&abbreviation=ZBA&keywords=&sortOrder=6",
)
spider = MinnCrcSpider()

freezer = freeze_time("2021-08-23")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


"""
Uncomment below
"""

def test_title():
    assert parsed_items[46]["title"] == "Civil Rights Commission"

def test_location():
    assert parsed_items[46]["location"] == {
        "name": "Online Meeting",
        "address": None
    }

def test_source():
    assert parsed_items[46]["source"] == "https://lims.minneapolismn.gov/IndependentBodies/IndependentBodiesMeetings/MCCR"

def test_links():
    print(parsed_items[46])
    assert parsed_items[46]["links"] == [{
        "title": "Report Document",
      "href": "https://lims.minneapolismn.gov/Download/CommitteeReport/2089/Civil-Rights-Commission-Minutes-8-16-21.pdf"
    }]

