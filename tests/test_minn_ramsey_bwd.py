from datetime import datetime
from os.path import dirname, join

import pytest  # noqa
from city_scrapers_core.constants import BOARD
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.minn_ramsey_county import MinnRamseyCountyBoardWorkshopSpider

test_response = file_response(
    join(dirname(__file__), "files", "minn_ramsey_bwd.html"),
    url="https://ramseycountymn.legistar.com/DepartmentDetail.aspx?ID=44588&GUID=87E5EA0B-060D-423E-B656-A0557147DB5A",  # noqa
)
spider = MinnRamseyCountyBoardWorkshopSpider()

freezer = freeze_time("2026-05-08")
freezer.start()

parsed_items = [
    item
    for item in spider._parse_legistar_events_page(test_response)
    if hasattr(item, "keys")
]

freezer.stop()


def test_count():
    assert len(parsed_items) == 35


def test_title():
    assert parsed_items[0]["title"] == "Board Workshop / Discussion"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2026, 6, 23, 13, 30)


def test_end():
    assert parsed_items[0]["end"] is None


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_classification():
    assert parsed_items[0]["classification"] == BOARD


def test_all_day():
    assert parsed_items[0]["all_day"] is False


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Courthouse Room 220",
        "address": "15 W Kellogg Blvd, Saint Paul, MN 55102",
    }


def test_source():
    assert (
        parsed_items[0]["source"]
        == "https://ramseycountymn.legistar.com/DepartmentDetail.aspx?ID=44588&GUID=87E5EA0B-060D-423E-B656-A0557147DB5A"  # noqa
    )


def test_links_empty():
    assert parsed_items[0]["links"] == []


def test_links_with_documents():
    assert parsed_items[11]["links"] == [
        {
            "href": "https://ramseycountymn.legistar.com/MeetingDetail.aspx?ID=1403756&GUID=AA88122D-B46B-46C2-A755-D69A3AE67AF2&Options=&Search=",  # noqa
            "title": "Meeting Details",
        },
        {
            "href": "https://ramseycountymn.legistar.com/View.ashx?M=A&ID=1403756&GUID=AA88122D-B46B-46C2-A755-D69A3AE67AF2",  # noqa
            "title": "Agenda",
        },
        {
            "href": "https://ramseycountymn.legistar.com/View.ashx?M=AADA&ID=1403756&GUID=AA88122D-B46B-46C2-A755-D69A3AE67AF2",  # noqa
            "title": "Accessible Agenda",
        },
        {
            "href": "https://ramseycountymn.legistar.com/View.ashx?M=PA&ID=1403756&GUID=AA88122D-B46B-46C2-A755-D69A3AE67AF2",  # noqa
            "title": "Agenda Packet",
        },
        {
            "href": "https://ramseycountymn.legistar.com/Video.aspx?Mode=Granicus&ID1=1451&Mode2=Video",  # noqa
            "title": "Video",
        },
    ]


def test_status():
    assert parsed_items[0]["status"] == "tentative"


def test_status_passed():
    assert parsed_items[11]["status"] == "passed"


def test_id():
    assert (
        parsed_items[0]["id"]
        == "minn_ramsey_bwd/202606231330/x/board_workshop_discussion"
    )
