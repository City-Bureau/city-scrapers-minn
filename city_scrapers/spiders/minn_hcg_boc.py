import json
from datetime import datetime

from city_scrapers_core.constants import BOARD
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil.relativedelta import relativedelta


class MinnHcgBocSpider(CityScrapersSpider):
    name = "minn_hcg_boc"
    agency = "Hennepin County Government "
    timezone = "America/North_Dakota/Beulah"
    today = datetime.today()
    fromDate = today.strftime("%Y-%m-%d")
    one_month = datetime.today() + relativedelta(months=-1)
    six_months = datetime.today() + relativedelta(months=+6)
    start_urls = [
        "https://prodboarddocsrch-hc-api.azurewebsites.net/api/Values/-1/-1/"
        + str(one_month.strftime("%Y-%m-%d"))
        + "/"
        + str(six_months.strftime("%Y-%m-%d"))
        + "/none/true"
    ]

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        data = json.loads(response.text)

        for item in data["dtMtg"]:
            if "board" in str(item["MeetingType"]).lower():
                meeting = Meeting(
                    title=str(item["MeetingType"]),
                    description="",
                    classification=self._parse_classification(item),
                    start=self._parse_start(item),
                    end=None,
                    all_day=False,
                    time_notes="",
                    location=self._parse_location(item),
                    links=self._parse_links(item),
                    source=self._parse_source(item),
                )

                if "cancelled" in str(item["MeetingType"]).lower():
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
        """Parse or generate classification from allowed options."""
        return BOARD

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        return datetime.strptime(item["MeetingDate"], "%Y-%m-%dT%H:%M:%S")

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
        if item["Location"] != "Virtually via hennepin.us":
            address = item["Location"]
        else:
            address = None
            if (
                item["Location"] == "Virtually via hennepin.us"
                or item["Location"] == "Online Meeting"
            ):
                address = "Virtually via hennepin.us"

        return {"address": address, "name": "Online Meeting"}

    def _parse_source(self, item):
        return (
            "https://www.hennepin.us/your-government/leadership/county-board-meetings"
        )

    def _parse_links(self, item):
        """Parse or generate links."""
        links = []
        if "AgendaPDFExists" in item and item["AgendaPDFExists"]:
            links.append(
                {
                    "title": "Agenda Document",
                    "href": "https://hennepin.novusagenda.com/agendapublic/DisplayAgendaPDF.ashx?MeetingID="  # noqa
                    + str(item["MeetingID"]),
                }
            )
        return links
