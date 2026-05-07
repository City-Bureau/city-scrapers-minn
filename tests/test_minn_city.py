import json
from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import BOARD, COMMISSION
from freezegun import freeze_time

from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnPlannCoTestSpider(MinnCityMixin):
    name = "minn_plann_co"
    agency = "Planning Commission"
    committee_id = 81
    meeting_type = 4


class MinnCharCoTestSpider(MinnCityMixin):
    name = "minn_char_co"
    agency = "Charter Commission"
    committee_id = 42
    meeting_type = 4
    marked_agenda_path = "MarkedAgenda"


class MinnEpbTestSpider(MinnCityMixin):
    name = "minn_epb"
    agency = "Ethical Practices Board"
    committee_id = 53
    meeting_type = 4


@pytest.fixture
def planning_spider():
    spider = MinnPlannCoTestSpider()
    spider._links_by_date = {}
    return spider


@pytest.fixture
def charter_spider():
    spider = MinnCharCoTestSpider()
    spider._links_by_date = {}
    return spider


@pytest.fixture
def epb_spider():
    spider = MinnEpbTestSpider()
    spider._links_by_date = {}
    return spider


@pytest.fixture(scope="module")
def attachment_json():
    with open(join(dirname(__file__), "files", "minn_city_attachments.json")) as f:
        return json.load(f)


@pytest.fixture(scope="module")
def calendar_json():
    with open(join(dirname(__file__), "files", "minn_city_calendar.json")) as f:
        return json.load(f)


def get_calendar_item(calendar_json, committee_id):
    for item in calendar_json:
        if item["CommitteeId"] == committee_id:
            return item

    raise AssertionError(f"No calendar item found for CommitteeId {committee_id}")


@freeze_time("2026-05-06")
class TestMeetingFields:
    def test_planning_commission_fields(self, planning_spider, calendar_json):
        item = get_calendar_item(calendar_json, planning_spider.committee_id)

        assert planning_spider.name == "minn_plann_co"
        assert planning_spider.agency == "Planning Commission"
        assert planning_spider.committee_id == 81
        assert planning_spider.meeting_type == 4

        assert item["CommitteeName"] == "Planning Commission"
        assert item["CommitteeId"] == planning_spider.committee_id
        assert item["Cancelled"] is True

        assert planning_spider._parse_start(item) == datetime(2025, 9, 25, 16, 30)

        assert planning_spider._parse_location(item) == {
            "address": "250 S. 4th St., Minneapolis, MN 55415",
            "name": "Room 350, Public Service Center",
        }

    def test_charter_commission_fields(self, charter_spider, calendar_json):
        item = get_calendar_item(calendar_json, charter_spider.committee_id)

        assert charter_spider.name == "minn_char_co"
        assert charter_spider.agency == "Charter Commission"
        assert charter_spider.committee_id == 42
        assert charter_spider.meeting_type == 4

        assert item["CommitteeName"] == "Charter Commission"
        assert item["CommitteeId"] == charter_spider.committee_id
        assert item["Cancelled"] is False

        assert charter_spider._parse_start(item) == datetime(2026, 1, 21, 16, 0)

        assert charter_spider._parse_location(item) == {
            "address": "250 S 4th St, Minneapolis, MN 55415",
            "name": "Room 350, Public Service Center",
        }

    def test_ethical_practices_board_fields(self, epb_spider, calendar_json):
        item = get_calendar_item(calendar_json, epb_spider.committee_id)

        assert epb_spider.name == "minn_epb"
        assert epb_spider.agency == "Ethical Practices Board"
        assert epb_spider.committee_id == 53
        assert epb_spider.meeting_type == 4

        assert item["CommitteeName"] == "Ethical Practices Board"
        assert item["CommitteeId"] == epb_spider.committee_id
        assert item["Cancelled"] is False

        assert epb_spider._parse_start(item) == datetime(2026, 5, 19, 15, 0)

        assert epb_spider._parse_location(item) == {
            "address": "250 S 4th St, Minneapolis, MN 55415",
            "name": "Room 350, Public Service Center",
        }


def test_parse_classification_from_calendar_json(
    planning_spider, charter_spider, epb_spider, calendar_json
):
    planning_item = get_calendar_item(calendar_json, planning_spider.committee_id)
    charter_item = get_calendar_item(calendar_json, charter_spider.committee_id)
    epb_item = get_calendar_item(calendar_json, epb_spider.committee_id)

    assert planning_spider._parse_classification(planning_item) == COMMISSION
    assert charter_spider._parse_classification(charter_item) == COMMISSION
    assert epb_spider._parse_classification(epb_item) == BOARD


def test_charter_attachment_links(charter_spider, attachment_json):
    item = attachment_json[0]

    result = charter_spider._parse_attachment_links(
        item,
        marked_agenda_path=charter_spider.marked_agenda_path,
    )

    assert {
        "title": "Video",
        "href": "https://youtube.com/watch?v=qMkEuaJOks0",
    } in result

    assert {
        "title": "Report/Proceedings",
        "href": (
            "https://lims.minneapolismn.gov/Download/CommitteeReport/"
            "4670/Charter_01212026_Committee_Report.pdf"
        ),
    } in result

    assert {
        "title": "Agenda",
        "href": "https://lims.minneapolismn.gov/MarkedAgenda/Charter/5795",
    } in result

    assert len(result) == 3


def test_charter_attachment_links_are_saved_by_meeting_date(
    charter_spider, attachment_json
):
    item = attachment_json[0]
    meeting_date = item["meetingDate"][:10]

    links = charter_spider._parse_attachment_links(
        item,
        marked_agenda_path=charter_spider.marked_agenda_path,
    )

    charter_spider._links_by_date.setdefault(meeting_date, [])
    charter_spider._links_by_date[meeting_date].extend(links)

    assert meeting_date == "2026-01-21"
    assert "2026-01-21" in charter_spider._links_by_date
    assert len(charter_spider._links_by_date["2026-01-21"]) == 3

    titles = [link["title"] for link in charter_spider._links_by_date["2026-01-21"]]

    assert "Video" in titles
    assert "Report/Proceedings" in titles
    assert "Agenda" in titles


def test_charter_calendar_item_receives_matching_attachment_links(
    charter_spider, attachment_json, calendar_json
):
    attachment_item = attachment_json[0]
    charter_calendar_item = get_calendar_item(
        calendar_json,
        charter_spider.committee_id,
    )

    meeting_date = attachment_item["meetingDate"][:10]

    charter_spider._links_by_date[meeting_date] = (
        charter_spider._parse_attachment_links(
            attachment_item,
            marked_agenda_path=charter_spider.marked_agenda_path,
        )
    )

    result = charter_spider._parse_links(charter_calendar_item)

    assert charter_calendar_item["MeetingTime"][:10] == "2026-01-21"
    assert len(result) == 3
    assert any(link["title"] == "Video" for link in result)
    assert any(link["title"] == "Report/Proceedings" for link in result)
    assert any(link["title"] == "Agenda" for link in result)


def test_planning_calendar_item_without_matching_attachment_date_gets_no_links(
    planning_spider, attachment_json, calendar_json
):
    attachment_item = attachment_json[0]
    planning_item = get_calendar_item(calendar_json, planning_spider.committee_id)

    meeting_date = attachment_item["meetingDate"][:10]

    planning_spider._links_by_date[meeting_date] = (
        planning_spider._parse_attachment_links(
            attachment_item,
            marked_agenda_path="MarkedAgenda",
        )
    )

    result = planning_spider._parse_links(planning_item)

    assert planning_item["MeetingTime"][:10] == "2025-09-25"
    assert result == []


def test_epb_calendar_item_without_matching_attachment_date_gets_no_links(
    epb_spider, attachment_json, calendar_json
):
    attachment_item = attachment_json[0]
    epb_item = get_calendar_item(calendar_json, epb_spider.committee_id)

    meeting_date = attachment_item["meetingDate"][:10]

    epb_spider._links_by_date[meeting_date] = epb_spider._parse_attachment_links(
        attachment_item,
        marked_agenda_path="MarkedAgenda",
    )

    result = epb_spider._parse_links(epb_item)

    assert epb_item["MeetingTime"][:10] == "2026-05-19"
    assert result == []


def test_charter_request_attachment_endpoint_uses_marked_agenda_path_override(
    charter_spider,
):
    request = charter_spider._request_attachment_endpoint(0)

    assert request.meta["marked_agenda_path"] == "MarkedAgenda"


def test_planning_request_attachment_endpoint_uses_endpoint_default(
    planning_spider,
):
    request = planning_spider._request_attachment_endpoint(2)

    assert request.meta["marked_agenda_path"] == "Board/MarkedAgenda"


def test_source_url_is_shared_by_all_spiders(
    planning_spider, charter_spider, epb_spider
):
    expected_source = "https://lims.minneapolismn.gov/Calendar/all/monthly"

    assert planning_spider.source_url == expected_source
    assert charter_spider.source_url == expected_source
    assert epb_spider.source_url == expected_source
