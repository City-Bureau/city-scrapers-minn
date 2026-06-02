import re
from collections import defaultdict
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
        required_static_vars = ["name", "agency", "agency_name", "dept_id", "guid"]
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
    agency = None
    agency_name = None
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

    def _parse_legistar_events_page(self, response):
        """Override to skip POST-based pagination incompatible with GET cookie approach.

        The base class _parse_next_page decodes response.request.body which is
        empty on GET requests, causing an error. Since all years are returned on
        the initial GET via the cookie, pagination is not needed.
        """
        legistar_events = self._parse_legistar_events(response)
        yield from self.parse_legistar(legistar_events)

    def _parse_legistar_events(self, response):
        """Override to normalize 'Export to Calendar' header to 'iCalendar'.

        Ramsey County Legistar uses 'Export to Calendar' as the column name
        instead of the empty/ics header the base class expects, so deduplication
        via _scraped_urls would skip every row without this fix.
        """
        events_table = response.css("table.rgMasterTable")[0]

        headers = []
        for th in events_table.css("th[class^='rgHeader']"):
            header_text = (
                " ".join(th.css("*::text").extract()).replace("\xa0", " ").strip()
            )
            header_inputs = th.css("input")
            if header_text:
                headers.append(header_text)
            elif header_inputs:
                headers.append(header_inputs[0].attrib["value"])
            else:
                headers.append(th.css("img")[0].attrib["alt"])

        events = []
        for row in events_table.css("tr.rgRow, tr.rgAltRow"):
            try:
                data = defaultdict(lambda: None)
                for header, field in zip(headers, row.css("td")):
                    field_text = (
                        " ".join(field.css("*::text").extract())
                        .replace("\xa0", " ")
                        .strip()
                    )
                    url = None
                    if field.css("a"):
                        link_el = field.css("a")[0]
                        if "onclick" in link_el.attrib and link_el.attrib[
                            "onclick"
                        ].startswith(("radopen('", "window.open", "OpenTelerikWindow")):
                            url = response.urljoin(
                                link_el.attrib["onclick"].split("'")[1]
                            )
                        elif "href" in link_el.attrib:
                            url = response.urljoin(link_el.attrib["href"])
                    if url and "View.ashx?M=IC" in url:
                        data["iCalendar"] = {"url": url}
                    elif url:
                        data[header] = {"label": field_text, "url": url}
                    else:
                        data[header] = field_text

                ical_url = (data.get("iCalendar") or {}).get("url")
                if ical_url is None or ical_url in self._scraped_urls:
                    continue
                self._scraped_urls.add(ical_url)
                events.append(dict(data))
            except Exception as e:
                self.logger.warning(f"Error while parsing Legistar event row: {e}")
        return events

    def parse_legistar(self, events):
        """Parse Meeting items from Legistar event dicts."""
        for item in events:
            start = self._parse_start(item)
            if start and start.year < self.since_year:
                continue
            meeting = Meeting(
                title=self._parse_dept_title(),
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

    def _parse_dept_title(self):
        """Return the short title by stripping the 'Ramsey County ' prefix."""
        prefix = "Ramsey County "
        if self.agency.startswith(prefix):
            return self.agency[len(prefix) :]
        return self.agency

    def _parse_classification(self):
        """Derive classification from the short department title."""
        name_lower = self._parse_dept_title().lower()
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
