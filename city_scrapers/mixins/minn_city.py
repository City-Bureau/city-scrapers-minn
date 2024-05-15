import json
from datetime import datetime, timedelta

import scrapy
from city_scrapers_core.constants import BOARD, CITY_COUNCIL, COMMITTEE, NOT_CLASSIFIED
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
    # scrape all meetings from one month ago
    from_date = datetime.now() - timedelta(days=30)
    base_url = "https://lims.minneapolismn.gov/Calendar/GetCalenderList"
    to_date = ""
    links = [
        {
            "title": "Meeting materials (council)",
            "href": "https://lims.minneapolismn.gov/Boards/Meetings/Council",
        },
        {
            "title": "Meeting materials (independent bodies)",
            "href": "https://lims.minneapolismn.gov/IndependentBodies/Meetings",
        },
        {
            "title": "Meeting materials (boards)",
            "href": "https://lims.minneapolismn.gov/Boards/Meetings",
        },
    ]
    name = None
    agency = None
    committee_id = None
    meeting_type = None

    def start_requests(self):
        """
        Create a GET request to the city's Calendar endpoint with
        the appropriate query parameters. We use a headless browser
        (scrapy-playwright) to handle our request because the city uses
        Cloudflare to detect and block requests from obvious bots.
        """
        full_url = f"{self.base_url}?fromDate={self.from_date}&toDate={self.to_date}&meetingType={self.meeting_type}&committeeId={self.committee_id}&pageCount=1000&offsetStart=0&abbreviation=&keywords=&sortOrder=1"  # noqa
        yield scrapy.Request(
            url=full_url,
            meta={"playwright": True},
            callback=self.parse,
        )

    def parse(self, response):
        """
        Extract JSON from the HTML response and parse it into a list of Meeting items.
        """
        json_data = response.css("pre::text").get()
        data = json.loads(json_data)
        for item in data:
            meeting = Meeting(
                title=str(item["CommitteeName"]),
                description=str(item["Description"]),
                classification=self._parse_classification(item),
                start=self._parse_start(item),
                end=None,
                all_day=False,
                time_notes="",
                location=self._parse_location(item),
                links=self._parse_links(item),
                source=self._parse_source(item),
            )
            if item["Cancelled"]:
                meeting["status"] = self._get_status(
                    meeting, text="Meeting is cancelled"
                )
            else:
                meeting["status"] = self._get_status(meeting)
            meeting["id"] = self._get_id(meeting)
            yield meeting

    def _parse_title(self, item):
        """Parse or generate meeting title."""
        return ""

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        return ""

    def _parse_classification(self, item):
        """Parse or generate classification from title."""
        if not item["CommitteeName"]:
            return NOT_CLASSIFIED
        committee_name = item["CommitteeName"].lower()
        if "board" in committee_name:
            return BOARD
        elif "committee" in committee_name:
            return COMMITTEE
        elif "council" in committee_name:
            return CITY_COUNCIL
        else:
            return NOT_CLASSIFIED

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        return datetime.strptime(item["MeetingTime"], "%Y-%m-%dT%H:%M:%S")

    def _parse_end(self, item):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        return None

    def _parse_time_notes(self, item):
        """Parse any additional notes on the timing of the meeting"""
        return ""

    def _parse_all_day(self, item):
        """Parse or generate all-day status. Defaults to False."""
        return False

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

    def _parse_source(self, item):
        return "https://lims.minneapolismn.gov/Boards/Meetings/" + item["Abbreviation"]

    def _parse_links(self, item):
        """Parse or generate links."""
        new_links = self.links.copy()  # Copy the default links
        if "CommitteeReportDocument" in item and item["CommitteeReportDocument"]:
            new_links.append(
                {
                    "title": "Report Document",
                    "href": "https://lims.minneapolismn.gov/Download/CommitteeReport/"
                    + str(item["CommitteeReportDocumentId"])
                    + "/"
                    + str(item["CommitteeReportDocument"]).replace(" ", "-"),
                }
            )
        return new_links
