import datetime
from collections import defaultdict

from city_scrapers_core.constants import BOARD, COMMITTEE, NOT_CLASSIFIED
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import LegistarSpider


class MinnHennepinBocSpider(LegistarSpider):
    name = "minn_hennepin_boc"
    agency = "Hennepin County"
    timezone = "America/Chicago"
    start_urls = ["https://hennepinmn.legistar.com/Calendar.aspx"]
    custom_settings = {
        "ROBOTSTXT_OBEY": False,
        "FEED_EXPORT_ENCODING": "utf-8",
    }
    link_types = ["Agenda Packet"]
    _non_location_strings = {"special meeting"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.since_year = datetime.datetime.now().year - 3

    def parse_legistar(self, events):
        for item in events:
            meeting = Meeting(
                title=self._parse_title(item),
                description=self._parse_description(item),
                classification=self._parse_classification(item),
                start=self.legistar_start(item),
                end=None,
                all_day=False,
                time_notes="",
                location=self._parse_location(item),
                links=self.legistar_links(item),
                source=self._parse_source(item),
            )

            meeting["status"] = self._get_status(meeting)
            meeting["id"] = self._get_id(meeting)

            yield meeting

    def _parse_legistar_events(self, response):
        events_table = response.css("table.rgMasterTable")
        if not events_table:
            return []
        events_table = events_table[0]

        headers = []
        for header in events_table.css("th[class^='rgHeader']"):
            header_text = (
                " ".join(header.css("*::text").extract()).replace("&nbsp;", " ").strip()
            )
            header_inputs = header.css("input")
            if header_text:
                headers.append(header_text)
            elif len(header_inputs) > 0:
                headers.append(header_inputs[0].attrib["value"])
            else:
                images = header.css("img")
                headers.append(images[0].attrib["alt"] if images else "")

        events = []
        for row in events_table.css("tr.rgRow, tr.rgAltRow"):
            data = defaultdict(lambda: None)
            for header, field in zip(headers, row.css("td")):
                field_text = (
                    " ".join(field.css("*::text").extract())
                    .replace("&nbsp;", " ")
                    .strip()
                )
                url = None
                link_el = field.css("a")
                if link_el:
                    link_el = link_el[0]
                    if "onclick" in link_el.attrib and link_el.attrib[
                        "onclick"
                    ].startswith(("radopen('", "window.open", "OpenTelerikWindow")):
                        url = response.urljoin(link_el.attrib["onclick"].split("'")[1])
                    elif "href" in link_el.attrib:
                        url = response.urljoin(link_el.attrib["href"])
                if url:
                    if header in ["", "ics"] and "View.ashx?M=IC" in url:
                        header = "iCalendar"
                        value = {"url": url}
                    else:
                        value = {"label": field_text, "url": url}
                else:
                    value = field_text
                data[header] = value
            events.append(dict(data))
        return events

    def _parse_title(self, item):
        name = item.get("Name")
        if isinstance(name, dict):
            title = name.get("label", "").strip()
        else:
            title = str(name or "").strip()
        return title or self.agency

    def _parse_description(self, item):
        location = item.get("Meeting Location") or item.get("Location") or ""
        location = location.strip()
        if location.lower() in self._non_location_strings:
            return location
        return ""

    def _parse_classification(self, item):
        title = self._parse_title(item).lower()

        if "board" in title or "authority" in title:
            return BOARD

        if "committee" in title:
            return COMMITTEE

        return NOT_CLASSIFIED

    def _parse_location(self, item):
        location = item.get("Meeting Location") or item.get("Location") or ""
        location = location.strip()

        if location.lower() in self._non_location_strings:
            return {"name": "", "address": ""}

        address = ""
        if "Government Center" in location:
            address = "300 South 6th Street Minneapolis, MN 55487"

        return {
            "name": location,
            "address": address,
        }

    def _parse_source(self, item):
        default_url = self.start_urls[0]
        if isinstance(item.get("Meeting Details"), dict):
            url = item["Meeting Details"].get("url")
            if url:
                return url
        if isinstance(item.get("Name"), dict):
            return item["Name"].get("url", default_url)
        return default_url
