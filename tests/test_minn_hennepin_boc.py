from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import BOARD, COMMITTEE
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.minn_hennepin_boc import MinnHennepinBocSpider


@pytest.fixture(scope="module")
def boc_items():
    spider = MinnHennepinBocSpider()
    response = file_response(
        join(dirname(__file__), "files", "minn_hennepin_boc.html"),
        url="https://hennepinmn.legistar.com/Calendar.aspx",
    )
    with freeze_time("2026-05-18"):
        return list(spider._parse_legistar_events_page(response))


@pytest.fixture(scope="module")
def admin_items():
    spider = MinnHennepinBocSpider()
    response = file_response(
        join(dirname(__file__), "files", "minn_hennepin_admin_op_bud_committee.html"),
        url="https://hennepinmn.legistar.com/Calendar.aspx",
    )
    with freeze_time("2026-05-18"):
        return list(spider._parse_legistar_events_page(response))


# --- Board of Hennepin County Commissioners ---


def test_boc_title(boc_items):
    assert boc_items[0]["title"] == "Board of Hennepin County Commissioners"


def test_boc_description(boc_items):
    assert boc_items[0]["description"] == ""


def test_boc_classification(boc_items):
    assert boc_items[0]["classification"] == BOARD


def test_boc_start(boc_items):
    assert boc_items[0]["start"] == datetime(2026, 5, 19, 13, 30)


def test_boc_end(boc_items):
    assert boc_items[0]["end"] is None


def test_boc_time_notes(boc_items):
    assert boc_items[0]["time_notes"] == ""


def test_boc_location(boc_items):
    assert boc_items[0]["location"] == {
        "name": "Government Center - County Board Chambers",
        "address": "300 South 6th Street Minneapolis, MN 55487",
    }


def test_boc_links(boc_items):
    assert boc_items[0]["links"] == []


def test_boc_source(boc_items):
    assert boc_items[0]["source"] == (
        "https://hennepinmn.legistar.com/DepartmentDetail.aspx"
        "?ID=49857&GUID=F467C72F-EA78-44C3-828B-564462B9A54F"
    )


def test_boc_status(boc_items):
    assert boc_items[0]["status"] == "tentative"


def test_boc_all_day(boc_items):
    assert boc_items[0]["all_day"] is False


# --- Administration, Operations and Budget Committee ---


def test_admin_title(admin_items):
    assert admin_items[0]["title"] == "Administration, Operations and Budget Committee"


def test_admin_description(admin_items):
    assert admin_items[0]["description"] == ""


def test_admin_classification(admin_items):
    assert admin_items[0]["classification"] == COMMITTEE


def test_admin_start(admin_items):
    assert admin_items[0]["start"] == datetime(2025, 11, 10, 12, 0)


def test_admin_end(admin_items):
    assert admin_items[0]["end"] is None


def test_admin_time_notes(admin_items):
    assert admin_items[0]["time_notes"] == ""


def test_admin_location(admin_items):
    assert admin_items[0]["location"] == {
        "name": "Government Center - County Board Chambers Budget Working Session",
        "address": "300 South 6th Street Minneapolis, MN 55487",
    }


def test_admin_links(admin_items):
    assert admin_items[0]["links"] == [
        {
            "href": "https://hennepinmn.legistar.com/View.ashx?M=A&ID=1352206&GUID=57C165D3-CF2D-45A8-8AFD-6360450D93FC",  # noqa
            "title": "Agenda",
        },
        {
            "href": "https://hennepinmn.legistar.com/View.ashx?M=M&ID=1352206&GUID=57C165D3-CF2D-45A8-8AFD-6360450D93FC",  # noqa
            "title": "Minutes",
        },
        {
            "href": "https://hennepinmn.legistar.com/Video.aspx?Mode=Granicus&ID1=5595&Mode2=Video",  # noqa
            "title": "Video",
        },
        {
            "href": "https://hennepinmn.legistar.com/View.ashx?M=PA&ID=1352206&GUID=57C165D3-CF2D-45A8-8AFD-6360450D93FC",  # noqa
            "title": "Agenda Packet",
        },
    ]


def test_admin_source(admin_items):
    assert admin_items[0]["source"] == (
        "https://hennepinmn.legistar.com/MeetingDetail.aspx"
        "?ID=1352206&GUID=57C165D3-CF2D-45A8-8AFD-6360450D93FC&Options=info|&Search="
    )


def test_admin_status(admin_items):
    assert admin_items[0]["status"] == "passed"


def test_admin_all_day(admin_items):
    assert admin_items[0]["all_day"] is False
