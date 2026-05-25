import re
from datetime import datetime

import scrapy
from city_scrapers_core.constants import BOARD, COMMITTEE, NOT_CLASSIFIED
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import LegistarSpider

# Cookie that sets the date filter to All Years on Ramsey County Legistar pages
_YEAR_COOKIE = (
    "Setting-785-Calendar Year=All Years; "
    "Setting-785-ASP.departmentdetail_aspx.Time.SelectedValue=All"
)


class MinnRamseyCountyMixinMeta(type):
    """
    Metaclass that enforces the implementation of required static
    variables in child classes that inherit from MinnRamseyCountyMixin.
    """

    def __init__(cls, name, bases, dct):
        required_static_vars = ["name", "dept_name", "dept_id", "guid"]
        missing_vars = [var for var in required_static_vars if var not in dct]

        if missing_vars:
            missing_vars_str = ", ".join(missing_vars)
            raise NotImplementedError(
                f"{name} must define the following static variable(s): {missing_vars_str}."  # noqa
            )

        super().__init__(name, bases, dct)


class MinnRamseyCountyMixin(LegistarSpider, metaclass=MinnRamseyCountyMixinMeta):
    timezone = "America/Chicago"
    # Courthouse address shared by all bodies
    location = {
        "name": "Ramsey County Courthouse",
        "address": "15 W Kellogg Blvd, Saint Paul, MN 55102",
    }

    name = None
    dept_name = None
    dept_id = None
    guid = None

    def __init__(self, *args, **kwargs):
        self.start_urls = [
            "https://ramseycountymn.legistar.com/DepartmentDetail.aspx"
            f"?ID={self.dept_id}&GUID={self.guid}"
        ]
        super().__init__(*args, **kwargs)
        # Override after super().__init__() which resets since_year to year - 1
        self.since_year = datetime.now().year - 3

    def start_requests(self):
        """Send All Years cookie to bypass the default This Month date filter."""
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                headers={"Cookie": _YEAR_COOKIE},
                callback=self.parse,
            )

    def parse(self, response):
        """Parse all events directly from the GET response.

        DepartmentDetail.aspx returns all-years data on the initial GET when
        the All Years cookie is set, so no year-iteration POSTs are needed.
        """
        yield from self._parse_legistar_events_page(response)

    def parse_legistar(self, events):
        """Parse Meeting items from Legistar event dicts."""
        for item in events:
            start = self._parse_start(item)
            if start and start.year < self.since_year:
                continue
            meeting = Meeting(
                title=self.dept_name,
                description="",
                classification=self._parse_classification(),
                start=start,
                end=None,
                all_day=False,
                time_notes="",
                location=self._parse_location(item),
                links=self._parse_links(item),
                source=self.legistar_source(item),
            )
            meeting["status"] = self._get_status(meeting)
            meeting["id"] = self._get_id(meeting)
            yield meeting

    def _parse_start(self, item):
        """Parse start datetime from Legistar 'Date' and 'Time' columns."""
        start_date = item.get("Date")
        start_time = item.get("Time")
        if start_date and start_time:
            try:
                return datetime.strptime(
                    f"{start_date} {start_time}", "%m/%d/%Y %I:%M %p"
                )
            except ValueError as e:
                self.logger.warning(f"Error while parsing start time for: {item} - {e}")
        if start_date:
            try:
                return datetime.strptime(start_date, "%m/%d/%Y")
            except ValueError as e:
                self.logger.warning(f"Error while parsing start time for: {item} - {e}")
        self.logger.warning(f"Unable to parse start datetime from item: {item}")
        return None

    def _parse_classification(self):
        """Derive classification from dept_name value."""
        name_lower = self.dept_name.lower()
        if "board" in name_lower or "authority" in name_lower:
            return BOARD
        if "committee" in name_lower:
            return COMMITTEE
        return NOT_CLASSIFIED

    def _parse_location(self, item):
        """Parse location from Legistar row; fall back to courthouse default."""
        loc_text = item.get("Location", "") or ""
        if isinstance(loc_text, dict):
            loc_text = loc_text.get("label", "")
        loc_text = " ".join(loc_text.split())
        if loc_text:
            if any(
                term in loc_text.lower()
                for term in ["remote", "zoom", "video", "virtual"]
            ):
                return {"name": loc_text, "address": ""}
            match = re.match(r"^(.+?) - (\d+.+)$", loc_text)
            if match:
                return {
                    "name": match.group(1).strip(),
                    "address": match.group(2).strip(),
                }
            return {"name": loc_text, "address": self.location["address"]}
        return self.location

    def _parse_links(self, item):
        """Collect all available document links from a Legistar event dict."""
        links = []
        link_keys = [
            "Agenda",
            "Accessible Agenda",
            "Agenda Packet",
            "Minutes",
            "Accessible Minutes",
            "Video",
        ]
        for key in link_keys:
            val = item.get(key)
            if isinstance(val, dict) and val.get("url"):
                url = val["url"]
                if url and url != "#":
                    links.append({"href": url, "title": key})
        return links
