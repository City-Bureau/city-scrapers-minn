from datetime import datetime
from os.path import dirname, join

import pytest  # noqa
from city_scrapers_core.constants import COMMITTEE
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.minn_ramsey_county import (
    MinnRamseyCountyBudgetCommitteeSpider,
)

test_response = file_response(
    join(dirname(__file__), "files", "minn_ramsey_bcw.html"),
    url="https://ramseycountymn.legistar.com/DepartmentDetail.aspx?ID=42189&GUID=98D0D44A-168E-4676-B714-BFED6022EF17",  # noqa
)
spider = MinnRamseyCountyBudgetCommitteeSpider()

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
    assert parsed_items[0]["title"] == "Budget Committee of the Whole"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2025, 9, 22, 9, 0)


def test_end():
    assert parsed_items[0]["end"] is None


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_classification():
    assert parsed_items[0]["classification"] == COMMITTEE


def test_all_day():
    assert parsed_items[0]["all_day"] is False


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Council Chambers - Courthouse Room 300",
        "address": "15 W Kellogg Blvd, Saint Paul, MN 55102",
    }


def test_source():
    assert (
        parsed_items[0]["source"]
        == "https://ramseycountymn.legistar.com/MeetingDetail.aspx?ID=1335150&GUID=0FD008AA-D3CA-4906-B11C-1F363DC4C8A9&Options=&Search="  # noqa
    )


def test_links_with_documents():
    assert parsed_items[0]["links"] == [
        {
            "href": "https://ramseycountymn.legistar.com/MeetingDetail.aspx?ID=1335150&GUID=0FD008AA-D3CA-4906-B11C-1F363DC4C8A9&Options=&Search=",  # noqa
            "title": "Meeting Details",
        },
        {
            "href": "https://ramseycountymn.legistar.com/View.ashx?M=A&ID=1335150&GUID=0FD008AA-D3CA-4906-B11C-1F363DC4C8A9",  # noqa
            "title": "Agenda",
        },
        {
            "href": "https://ramseycountymn.legistar.com/View.ashx?M=AADA&ID=1335150&GUID=0FD008AA-D3CA-4906-B11C-1F363DC4C8A9",  # noqa
            "title": "Accessible Agenda",
        },
        {
            "href": "https://ramseycountymn.legistar.com/View.ashx?M=PA&ID=1335150&GUID=0FD008AA-D3CA-4906-B11C-1F363DC4C8A9",  # noqa
            "title": "Agenda Packet",
        },
        {
            "href": "https://ramseycountymn.legistar.com/View.ashx?M=M&ID=1335150&GUID=0FD008AA-D3CA-4906-B11C-1F363DC4C8A9",  # noqa
            "title": "Minutes",
        },
        {
            "href": "https://ramseycountymn.legistar.com/View.ashx?M=MADA&ID=1335150&GUID=0FD008AA-D3CA-4906-B11C-1F363DC4C8A9",  # noqa
            "title": "Accessible Minutes",
        },
        {
            "href": "https://ramseycountymn.legistar.com/Video.aspx?Mode=Granicus&ID1=1348&Mode2=Video",  # noqa
            "title": "Video",
        },
    ]


def test_status():
    assert parsed_items[0]["status"] == "passed"


def test_id():
    assert (
        parsed_items[0]["id"]
        == "minn_ramsey_bcw/202509220900/x/budget_committee_of_the_whole"
    )
