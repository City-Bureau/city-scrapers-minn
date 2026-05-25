import json
import urllib.parse
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import scrapy
from city_scrapers_core.constants import (
    BOARD,
    CITY_COUNCIL,
    COMMISSION,
    COMMITTEE,
    NOT_CLASSIFIED,
)
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider


class MinnCityMixinMeta(type):
    """
    Metaclass that enforces the implementation of required static
    variables in child classes that inherit from MinnCityMixinMixin.
    """

    def __init__(cls, name, bases, dct):
        required_static_vars = ["agency", "name", "committee_id", "meeting_type"]
        missing_vars = [var for var in required_static_vars if var not in dct]

        if missing_vars:
            missing_vars_str = ", ".join(missing_vars)
            raise NotImplementedError(
                f"{name} must define the following static variable(s): {missing_vars_str}."  # noqa
            )

        super().__init__(name, bases, dct)


class MinnCityMixin(CityScrapersSpider, metaclass=MinnCityMixinMeta):
    timezone = "America/North_Dakota/Beulah"
    today = datetime.now(tz=ZoneInfo(timezone)).date()
    from_date = today - timedelta(days=365 * 4)
    to_date = today + timedelta(days=365)
    source_url = "https://lims.minneapolismn.gov/Calendar/all/monthly"
    lims_base_url = "https://lims.minneapolismn.gov"
    calendar_path = "Calendar/GetCalenderList"
    custom_settings = {
        "FEED_EXPORT_ENCODING": "utf-8",
    }
    attachment_endpoints = [
        {
            "path": "CityCouncil/CityCouncilMeetingsPagedList",
            "marked_agenda_path": "MarkedAgenda",
        },
        {
            "path": "Jobs/PublicBoardMeetingsPagedList",
            "marked_agenda_path": "Board/MarkedAgenda",
        },
        {
            "path": "IndependentBodies/IndependentBodiesMeetingsPagedList",
            "marked_agenda_path": "Board/MarkedAgenda",
        },
    ]

    name = None
    agency = None
    committee_id = None
    meeting_type = None
    abbreviation = None

    attachment_formdata = {
        "draw": "1",
        "columns[0][data]": "CommitteeName",
        "columns[0][name]": "CommitteeName",
        "columns[0][searchable]": "true",
        "columns[0][orderable]": "true",
        "columns[0][search][value]": "",
        "columns[0][search][regex]": "false",
        "columns[1][data]": "MeetingDate",
        "columns[1][name]": "MeetingDate",
        "columns[1][searchable]": "true",
        "columns[1][orderable]": "true",
        "columns[1][search][value]": "",
        "columns[1][search][regex]": "false",
        "columns[2][data]": "MeetingDate",
        "columns[2][name]": "MeetingDate",
        "columns[2][searchable]": "true",
        "columns[2][orderable]": "false",
        "columns[2][search][value]": "",
        "columns[2][search][regex]": "false",
        "columns[3][data]": "Video",
        "columns[3][name]": "Video",
        "columns[3][searchable]": "true",
        "columns[3][orderable]": "false",
        "columns[3][search][value]": "",
        "columns[3][search][regex]": "false",
        "order[0][column]": "1",
        "order[0][dir]": "DESC",
        "start": "0",
        "length": "3000",
        "search[value]": "",
        "search[regex]": "false",
    }

    def start_requests(self):
        self._links_by_date = {}
        yield self._request_attachment_endpoint(0)

    def _request_attachment_endpoint(self, endpoint_index):
        endpoint = self.attachment_endpoints[endpoint_index]
        formdata = self.attachment_formdata.copy()

        if self.abbreviation:
            formdata["abbreviation"] = self.abbreviation

        url = (
            f"{self.lims_base_url}/{endpoint['path']}"
            f"?abbreviation={self.abbreviation or ''}"
        )

        spider_path_override = getattr(self, "marked_agenda_path", None)
        resolved_path = spider_path_override or endpoint["marked_agenda_path"]

        return scrapy.Request(
            url=url,
            method="POST",
            body=urllib.parse.urlencode(formdata),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            meta={
                "playwright": True,
                "endpoint_index": endpoint_index,
                "marked_agenda_path": resolved_path,
            },
            callback=self._parse_attachment_endpoint,
        )

    def _parse_attachment_endpoint(self, response):
        json_data = response.css("pre::text").get() or response.text
        data = json.loads(json_data)

        marked_agenda_path = response.meta["marked_agenda_path"]

        for item in data.get("data", []):
            if item.get("committeeId") != self.committee_id:
                continue

            meeting_date = item.get("meetingDate", "")[:10]
            links = self._parse_attachment_links(item, marked_agenda_path)

            self._links_by_date.setdefault(meeting_date, [])
            self._links_by_date[meeting_date].extend(links)

        next_index = response.meta["endpoint_index"] + 1

        if next_index < len(self.attachment_endpoints):
            yield self._request_attachment_endpoint(next_index)
        else:
            yield self._request_primary_calendar()

    def _parse_attachment_links(self, item, marked_agenda_path):
        links = []

        if item.get("mainVideoURL"):
            links.append(
                {
                    "title": "Video",
                    "href": item["mainVideoURL"],
                }
            )

        if item.get("committeeReportDocument") and item.get(
            "committeeReportDocumentId"
        ):
            links.append(
                {
                    "title": "Report/Proceedings",
                    "href": (
                        f"{self.lims_base_url}/Download/CommitteeReport/"
                        f"{item['committeeReportDocumentId']}/"
                        f"{str(item['committeeReportDocument']).replace(' ', '-')}"
                    ),
                }
            )

        if item.get("agendaPdf"):
            links.append(
                {
                    "title": "Agenda PDF",
                    "href": item["agendaPdf"],
                }
            )

        if (
            item.get("markedAgendaPublished")
            and item.get("agendaId")
            and item.get("abbreviation")
        ):
            links.append(
                {
                    "title": "Agenda",
                    "href": (
                        f"{self.lims_base_url}/{marked_agenda_path}/"
                        f"{item['abbreviation']}/{item['agendaId']}"
                    ),
                }
            )

        return links

    def _request_primary_calendar(self):
        full_url = (
            f"{self.lims_base_url}/{self.calendar_path}"
            f"?fromDate={self.from_date}"
            f"&toDate={self.to_date}"
            f"&meetingType={self.meeting_type}"
            f"&committeeId={self.committee_id}"
            f"&pageCount=1000"
            f"&offsetStart=0"
            f"&abbreviation="
            f"&keywords="
            f"&sortOrder=1"
        )
        return scrapy.Request(
            url=full_url,
            meta={"playwright": True},
            callback=self.parse,
        )

    def _parse_source(self, links):
        agenda = next((l["href"] for l in links if l.get("title") == "Agenda"), None)
        return agenda or self.source_url

    def parse(self, response):
        """
        Extract JSON from the HTML response and parse it into a list of Meeting items.
        """
        json_data = response.css("pre::text").get()
        data = json.loads(json_data)
        for item in data:
            links = self._parse_links(item)
            meeting = Meeting(
                title=str(item["CommitteeName"]),
                description=str(item["Description"]),
                classification=self._parse_classification(item),
                start=self._parse_start(item),
                end=None,
                all_day=False,
                time_notes="",
                location=self._parse_location(item),
                links=links,
                source=self._parse_source(links),
            )
            status_str = "cancel" if item["Cancelled"] else ""
            meeting["status"] = self._get_status(meeting, text=status_str)
            meeting["id"] = self._get_id(meeting)
            yield meeting

    def _parse_classification(self, item):
        """Parse or generate classification from title."""
        if not item["CommitteeName"]:
            return NOT_CLASSIFIED
        committee_name = item["CommitteeName"].lower()
        if "board" in committee_name:
            return BOARD
        elif "commission" in committee_name:
            return COMMISSION
        elif "committee" in committee_name:
            return COMMITTEE
        elif "council" in committee_name:
            return CITY_COUNCIL
        else:
            return NOT_CLASSIFIED

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        return datetime.strptime(item["MeetingTime"], "%Y-%m-%dT%H:%M:%S")

    def _parse_location(self, item):
        """Parse or generate location."""
        if item["Location"] != "Online Meeting":
            address = item["Address"]
        else:
            address = None
            if (
                item["Location"] == "Online Meeting"
                or item["Address"] == "Online Meeting"
            ):
                address = "Remote"

        return {"address": address, "name": item["Location"]}

    def _parse_links(self, item):
        meeting_date = item["MeetingTime"][:10]
        return self._links_by_date.get(meeting_date, [])
