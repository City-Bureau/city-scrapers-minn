from datetime import datetime
from os.path import dirname, join

import pytest  # noqa
from city_scrapers_core.constants import CITY_COUNCIL, TENTATIVE
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.minn_board import MinnBoardSpider

test_response = file_response(
    join(dirname(__file__), "files", "minn_board.html"),
    url="https://lims.minneapolismn.gov/Boards/Meetings/Council",
)
spider = MinnBoardSpider()

freezer = freeze_time("2024-02-22")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_title():
    assert parsed_items[0]["title"] == "City Council"


def test_description():
    assert (
        parsed_items[0]["description"]
        == "The Council is the legislative and primary policy-making body of the City of Minneapolis."  # noqa
    )


def test_start():
    assert parsed_items[0]["start"] == datetime(2024, 3, 7, 9, 30)


def test_end():
    assert parsed_items[0]["end"] is None


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_id():
    assert parsed_items[0]["id"] == "minn_board/202403070930/x/city_council"


def test_status():
    assert parsed_items[0]["status"] == TENTATIVE


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Room 350, Public Service Center (PSC)",
        "address": "250 S 4th St, Minneapolis, MN 55415",
    }


def test_source():
    assert (
        parsed_items[0]["source"]
        == "https://lims.minneapolismn.gov/Boards/Meetings/Council"
    )


def test_links():
    assert parsed_items[0]["links"] == [
        {
            "href": "https://lims.minneapolismn.gov/Boards/Meetings/Council",
            "title": "Meeting materials (council)",
        },
        {
            "href": "https://lims.minneapolismn.gov/IndependentBodies/Meetings",
            "title": "Meeting materials (independent bodies)",
        },
        {
            "href": "https://lims.minneapolismn.gov/Boards/Meetings",
            "title": "Meeting materials (boards)",
        },
    ]


def test_classification():
    assert parsed_items[0]["classification"] == CITY_COUNCIL


def test_all_day():
    assert parsed_items[0]["all_day"] is False
