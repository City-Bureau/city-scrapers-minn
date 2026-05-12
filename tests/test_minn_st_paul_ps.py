from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import BOARD
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.minn_st_paul_ps import MinnStPaulPsSpider


@pytest.fixture(scope="module")
def parsed_items():
    spider = MinnStPaulPsSpider()

    # parse materials archive
    materials_response = file_response(
        join(dirname(__file__), "files", "minn_st_paul_ps_materials.html"),
        url="https://www.spps.org/about/board-of-education/meeting-materials-archive/2026-meeting-materials",  # noqa
    )
    spider.materials_pending = 2
    list(spider.parse_materials(materials_response))

    # parse boardbook
    boardbook_response = file_response(
        join(dirname(__file__), "files", "minn_st_paul_ps_boardbook.html"),
        url="https://meetings.boardbook.org/Public/Organization/1810",
    )
    spider.materials_pending = 1
    list(spider.parse_boardbook(boardbook_response))

    # parse iCal
    ical_response = file_response(
        join(dirname(__file__), "files", "minn_st_paul_ps_ical.ics"),
        url="https://calendar.google.com/calendar/ical/2pe1lc650lrr2moeok6a7g1em4%40group.calendar.google.com/public/basic.ics",  # noqa
    )

    with freeze_time("2026-05-04"):
        return list(spider.parse(ical_response))


def test_count(parsed_items):
    assert len(parsed_items) > 0


def test_title(parsed_items):
    titles = [item["title"] for item in parsed_items]
    assert "Regular Board of Education Meeting" in titles


def test_description(parsed_items):
    assert parsed_items[0]["description"] == ""


def test_start(parsed_items):
    item = next(
        i
        for i in parsed_items
        if i["title"] == "Regular Board of Education Meeting"
        and i["start"].month == 2
        and i["start"].year == 2026
    )
    assert item["start"] == datetime(2026, 2, 17, 17, 30)


def test_end(parsed_items):
    item = next(
        i
        for i in parsed_items
        if i["title"] == "Regular Board of Education Meeting"
        and i["start"].month == 2
        and i["start"].year == 2026
    )
    assert item["end"] == datetime(2026, 2, 17, 21, 0)


def test_time_notes(parsed_items):
    assert parsed_items[0]["time_notes"] == ""


def test_id(parsed_items):
    item = next(i for i in parsed_items if i["start"] == datetime(2026, 2, 17, 17, 30))
    assert (
        item["id"]
        == "minn_st_paul_ps/202602171730/x/regular_board_of_education_meeting"
    )


def test_status(parsed_items):
    item = next(i for i in parsed_items if i["start"] == datetime(2026, 2, 17, 17, 30))
    assert item["status"] == "passed"


def test_location(parsed_items):
    item = next(i for i in parsed_items if i["start"] == datetime(2026, 2, 17, 17, 30))
    assert item["location"] == {
        "name": "Conference Rooms A and B",
        "address": "360 Colborne St, St Paul, MN 55102",
    }


def test_location_with_name(parsed_items):
    """Test that known SPPS address gets correct name."""
    items_with_spps = [
        i for i in parsed_items if i["location"]["name"] == "Saint Paul Public Schools"
    ]
    if items_with_spps:
        assert "360" in items_with_spps[0]["location"]["address"]


def test_source(parsed_items):
    assert (
        parsed_items[0]["source"]
        == "https://www.spps.org/about/board-of-education/calendar"
    )


def test_links(parsed_items):
    item = next(i for i in parsed_items if i["start"] == datetime(2026, 2, 17, 17, 30))
    assert len(item["links"]) > 0
    link_titles = [l["title"] for l in item["links"]]
    assert "Agenda" in link_titles


def test_classification(parsed_items):
    item = next(i for i in parsed_items if "Regular Board" in i["title"])
    assert item["classification"] == BOARD


def test_all_day(parsed_items):
    for item in parsed_items:
        assert item["all_day"] is False


def test_no_empty_links(parsed_items):
    for item in parsed_items:
        for link in item["links"]:
            assert link["href"] != "" or link["title"] != ""
