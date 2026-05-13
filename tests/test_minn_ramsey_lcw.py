from datetime import datetime
from os.path import dirname, join

import pytest  # noqa
from city_scrapers_core.constants import COMMITTEE
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.minn_ramsey_county import (
    MinnRamseyCountyLegislativeCommitteeSpider,
)

test_response = file_response(
    join(dirname(__file__), "files", "minn_ramsey_lcw.html"),
    url="https://ramseycountymn.legistar.com/DepartmentDetail.aspx?ID=42190&GUID=AE0EDFEA-0EE4-4FFD-A92A-BD3857E2B442",  # noqa
)
spider = MinnRamseyCountyLegislativeCommitteeSpider()

freezer = freeze_time("2026-05-08")
freezer.start()

parsed_items = [
    item
    for item in spider._parse_legistar_events_page(test_response)
    if hasattr(item, "keys")
]

freezer.stop()

items_by_id = {item["id"]: item for item in parsed_items}

# Stable ID known from the fixture; also the item that has documents
MEETING_ID = "minn_ramsey_lcw/202511041000/x/legislative_committee_of_the_whole"


def test_count():
    assert len(parsed_items) >= 1


def test_title():
    assert items_by_id[MEETING_ID]["title"] == "Legislative Committee of the Whole"


def test_description():
    assert items_by_id[MEETING_ID]["description"] == ""


def test_start():
    assert items_by_id[MEETING_ID]["start"] == datetime(2025, 11, 4, 10, 0)


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
        == "https://ramseycountymn.legistar.com/MeetingDetail.aspx?ID=1347052&GUID=04F05611-D612-47A1-A332-0D9F4BA1EFE4&Options=&Search="  # noqa
    )


def test_links_with_documents():
    assert items_by_id[MEETING_ID]["links"] == [
        {
            "href": "https://ramseycountymn.legistar.com/View.ashx?M=A&ID=1347052&GUID=04F05611-D612-47A1-A332-0D9F4BA1EFE4",  # noqa
            "title": "Agenda",
        },
        {
            "href": "https://ramseycountymn.legistar.com/View.ashx?M=AADA&ID=1347052&GUID=04F05611-D612-47A1-A332-0D9F4BA1EFE4",  # noqa
            "title": "Accessible Agenda",
        },
        {
            "href": "https://ramseycountymn.legistar.com/View.ashx?M=PA&ID=1347052&GUID=04F05611-D612-47A1-A332-0D9F4BA1EFE4",  # noqa
            "title": "Agenda Packet",
        },
        {
            "href": "https://ramseycountymn.legistar.com/Video.aspx?Mode=Granicus&ID1=1369&Mode2=Video",  # noqa
            "title": "Video",
        },
    ]


def test_status():
    assert items_by_id[MEETING_ID]["status"] == "passed"


def test_id():
    assert MEETING_ID in items_by_id
