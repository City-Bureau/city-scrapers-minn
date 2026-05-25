from datetime import datetime
from os.path import dirname, join

import pytest  # noqa
from city_scrapers_core.constants import BOARD
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.minn_ramsey_county import (
    MinnRamseyCountyRegionalRailroadSpider,
)

test_response = file_response(
    join(dirname(__file__), "files", "minn_ramsey_rra.html"),
    url="https://ramseycountymn.legistar.com/DepartmentDetail.aspx?ID=42187&GUID=7029D254-4F33-4FE0-B34A-C8AB0ABC3D54",  # noqa
)
spider = MinnRamseyCountyRegionalRailroadSpider()

freezer = freeze_time("2026-05-08")
freezer.start()

parsed_items = [
    item
    for item in spider._parse_legistar_events_page(test_response)
    if hasattr(item, "keys")
]

freezer.stop()

items_by_id = {item["id"]: item for item in parsed_items}

# Stable ID for a future meeting with no documents yet
FUTURE_ID = "minn_ramsey_rra/202605191000/x/regional_railroad_authority"
# Past meeting identified by its unique Legistar meeting ID in the link hrefs
meeting_with_docs = next(
    i for i in parsed_items if any("ID=1396765" in lnk["href"] for lnk in i["links"])
)


def test_count():
    assert len(parsed_items) >= 1


def test_title():
    assert items_by_id[FUTURE_ID]["title"] == "Regional Railroad Authority"


def test_description():
    assert items_by_id[FUTURE_ID]["description"] == ""


def test_start():
    assert items_by_id[FUTURE_ID]["start"] == datetime(2026, 5, 19, 10, 0)


def test_end():
    assert items_by_id[FUTURE_ID]["end"] is None


def test_time_notes():
    assert items_by_id[FUTURE_ID]["time_notes"] == ""


def test_classification():
    assert items_by_id[FUTURE_ID]["classification"] == BOARD


def test_all_day():
    assert items_by_id[FUTURE_ID]["all_day"] is False


def test_location():
    assert items_by_id[FUTURE_ID]["location"] == {
        "name": "Council Chambers - Courthouse Room 300",
        "address": "15 W Kellogg Blvd, Saint Paul, MN 55102",
    }


def test_source():
    assert (
        items_by_id[FUTURE_ID]["source"]
        == "https://ramseycountymn.legistar.com/DepartmentDetail.aspx?ID=42187&GUID=7029D254-4F33-4FE0-B34A-C8AB0ABC3D54"  # noqa
    )


def test_links_empty():
    assert items_by_id[FUTURE_ID]["links"] == []


def test_links_with_documents():
    assert meeting_with_docs["links"] == [
        {
            "href": "https://ramseycountymn.legistar.com/View.ashx?M=A&ID=1396765&GUID=9E2E76EA-82D2-4ADD-817B-565F9A3540BE",  # noqa
            "title": "Agenda",
        },
        {
            "href": "https://ramseycountymn.legistar.com/View.ashx?M=AADA&ID=1396765&GUID=9E2E76EA-82D2-4ADD-817B-565F9A3540BE",  # noqa
            "title": "Accessible Agenda",
        },
        {
            "href": "https://ramseycountymn.legistar.com/View.ashx?M=PA&ID=1396765&GUID=9E2E76EA-82D2-4ADD-817B-565F9A3540BE",  # noqa
            "title": "Agenda Packet",
        },
        {
            "href": "https://ramseycountymn.legistar.com/Video.aspx?Mode=Granicus&ID1=1420&Mode2=Video",  # noqa
            "title": "Video",
        },
    ]


def test_status_tentative():
    assert items_by_id[FUTURE_ID]["status"] == "tentative"


def test_status_passed():
    assert meeting_with_docs["status"] == "passed"


def test_id():
    assert FUTURE_ID in items_by_id
