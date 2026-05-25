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

items_by_id = {item["id"]: item for item in parsed_items}

# Stable ID known from the fixture; also the item that has full documents
MEETING_ID = "minn_ramsey_bcw/202509220900/x/budget_committee_of_the_whole"


def test_count():
    assert len(parsed_items) >= 1


def test_title():
    assert items_by_id[MEETING_ID]["title"] == "Budget Committee of the Whole"


def test_description():
    assert items_by_id[MEETING_ID]["description"] == ""


def test_start():
    assert items_by_id[MEETING_ID]["start"] == datetime(2025, 9, 22, 9, 0)


def test_end():
    assert items_by_id[MEETING_ID]["end"] is None


def test_time_notes():
    assert items_by_id[MEETING_ID]["time_notes"] == ""


def test_classification():
    assert items_by_id[MEETING_ID]["classification"] == COMMITTEE


def test_all_day():
    assert items_by_id[MEETING_ID]["all_day"] is False


def test_location():
    assert items_by_id[MEETING_ID]["location"] == {
        "name": "Council Chambers - Courthouse Room 300",
        "address": "15 W Kellogg Blvd, Saint Paul, MN 55102",
    }


def test_source():
    assert (
        items_by_id[MEETING_ID]["source"]
        == "https://ramseycountymn.legistar.com/MeetingDetail.aspx?ID=1335150&GUID=0FD008AA-D3CA-4906-B11C-1F363DC4C8A9&Options=&Search="  # noqa
    )


def test_links_with_documents():
    assert items_by_id[MEETING_ID]["links"] == [
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
    assert items_by_id[MEETING_ID]["status"] == "passed"


def test_id():
    assert MEETING_ID in items_by_id
