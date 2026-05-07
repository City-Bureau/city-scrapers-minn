from datetime import datetime

from city_scrapers_core.constants import BOARD, COMMITTEE, NOT_CLASSIFIED
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import LegistarSpider


class MinnRamseyCountyMixinMeta(type):
    """
    Metaclass that enforces the implementation of required static
    variables in child classes that inherit from MinnRamseyCountyMixin.
    """

    def __init__(cls, name, bases, dct):
        required_static_vars = ["agency", "name", "dept_id", "guid"]
        missing_vars = [var for var in required_static_vars if var not in dct]

        if missing_vars:
            missing_vars_str = ", ".join(missing_vars)
            raise NotImplementedError(
                f"{name} must define the following static variable(s): {missing_vars_str}."  # noqa
            )

        super().__init__(name, bases, dct)


class MinnRamseyCountyMixin(LegistarSpider, metaclass=MinnRamseyCountyMixinMeta):
    timezone = "America/Chicago"
    # 3 years back per project date range rules
    since_year = datetime.now().year - 3
    # Courthouse address shared by all bodies
    location = {
        "name": "Ramsey County Courthouse",
        "address": "15 W Kellogg Blvd, Saint Paul, MN 55102",
    }

    name = None
    agency = None
    dept_id = None
    guid = None

    @property
    def start_urls(self):
        return [
            "https://ramseycountymn.legistar.com/DepartmentDetail.aspx"
            f"?ID={self.dept_id}&GUID={self.guid}"
        ]

    def parse_legistar(self, events):
        """Parse Meeting items from Legistar event dicts."""
        for item in events:
            meeting = Meeting(
                title=self.agency,
                description="",
                classification=self._parse_classification(),
                start=self._parse_start(item),
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
            except ValueError:
                pass
        if start_date:
            try:
                return datetime.strptime(start_date, "%m/%d/%Y")
            except ValueError:
                pass
        return None

    def _parse_classification(self):
        """Derive classification from agency name."""
        name_lower = self.agency.lower()
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
            return {"name": loc_text, "address": self.location["address"]}
        return self.location

    def _parse_links(self, item):
        """Collect all available document links from a Legistar event dict."""
        links = []
        link_keys = [
            "Meeting Details",
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
