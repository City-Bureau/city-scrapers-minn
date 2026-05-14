import re
from datetime import date, datetime

import pytz
import recurring_ical_events
import scrapy
from city_scrapers_core.constants import BOARD
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil.parser import parse as parse_date
from icalendar import Calendar


class MinnStPaulPsSpider(CityScrapersSpider):
    name = "minn_st_paul_ps"
    agency = "St. Paul School Board"
    timezone = "America/Chicago"
    source_url = "https://www.spps.org/about/board-of-education/calendar"
    ical_url = "https://calendar.google.com/calendar/ical/2pe1lc650lrr2moeok6a7g1em4%40group.calendar.google.com/public/basic.ics"  # noqa
    boardbook_attachment_url = "https://meetings.boardbook.org/Public/Organization/1810"
    archive_attachment_url = "https://www.spps.org/about/board-of-education/meeting-materials-archive/{year}-meeting-materials"  # noqa

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.materials = {}
        self.boardbook_links = {}
        self.materials_pending = 0

    location_regular_board = {
        "name": "Conference Rooms A and B",
        "address": "360 Colborne St, St Paul, MN 55102",
    }
    location_committee = {
        "name": "Conference Room 5A",
        "address": "360 Colborne St, St Paul, MN 55102",
    }

    excluded_link_titles = {
        "map it",
        "streaming meeting url",
    }

    custom_settings = {
        "ROBOTSTXT_OBEY": False,
        "FEED_EXPORT_ENCODING": "utf-8",
    }

    def start_requests(self):
        current_year = datetime.now().year
        years = list(range(current_year - 3, current_year + 2))
        self.materials_pending = len(years) + 1  # +1 for boardbook

        yield scrapy.Request(
            self.boardbook_attachment_url,
            callback=self.parse_boardbook,
            errback=self.materials_errback,
        )

        for year in years:
            url = self.archive_attachment_url.format(year=year)
            yield scrapy.Request(
                url,
                callback=self.parse_materials,
                errback=self.materials_errback,
            )

    def _trigger_ical(self):
        """Decrement counter and trigger iCal fetch when all sources are done."""
        self.materials_pending -= 1
        if self.materials_pending == 0:
            return scrapy.Request(
                self.ical_url,
                callback=self.parse,
            )
        return None

    def materials_errback(self, failure):
        """Handle failed requests and trigger iCal if all sources are done."""
        self.logger.error(f"Request failed: {failure.request.url}")
        request = self._trigger_ical()
        if request:
            yield request

    def parse_boardbook(self, response):
        """Parse meeting links from boardbook."""
        for row in response.css("table#PublicMeetingsTable tbody tr.row-for-board"):
            text = (
                row.css("td:first-child div:first-child")
                .xpath("string()")
                .get("")
                .strip()
            )
            text = re.sub(r"Cancelled", "", text).strip()

            match = re.match(
                r"(\w+ \d+, \d{4})\s+(?:at\s+)?(\d+:\d+\s*[APMapm]+)\s*-\s*(.+)", text
            )
            if not match:
                continue

            date_str, time_str, meeting_type = match.groups()
            meeting_type = meeting_type.strip().lower()

            try:
                meeting_date = parse_date(date_str).date()
                meeting_time = parse_date(f"{date_str} {time_str.strip()}").time()
            except Exception:
                self.logger.error(f"Failed to parse date: {date_str} {time_str}")
                continue

            links = [
                link
                for link in (
                    [
                        self._build_link(a, "https://meetings.boardbook.org")
                        for a in row.css("td:nth-child(3) a")
                    ]
                    + [self._build_link(a) for a in row.css("td:nth-child(2) a")]
                )
                if (
                    link
                    and link.get("title", "").strip().lower()
                    not in self.excluded_link_titles
                )
            ]
            self.boardbook_links[(meeting_date, meeting_time, meeting_type)] = links

        request = self._trigger_ical()
        if request:
            yield request

    def parse_materials(self, response):
        """Parse meeting links from materials archive."""
        for category_section in response.css("section.fsPanelGroup"):
            category = category_section.css("h2.fsElementTitle::text").get("").strip()

            for meeting_section in category_section.css("section.fsPanel"):
                date_text = (
                    meeting_section.css("h2.fsElementTitle a::text").get("").strip()
                )

                subtitle = ""
                if "|" in date_text:
                    date_text, subtitle = date_text.split("|", 1)
                    date_text = date_text.strip()
                    subtitle = subtitle.strip()

                try:
                    # remove (Wed) etc from date text before parsing
                    date_text_clean = re.sub(r"\s*\([^)]*\)", "", date_text).strip()
                    # remove *bold* text from date text before parsing
                    date_text_clean = re.sub(
                        r"\s*\*[^*]*\*", "", date_text_clean
                    ).strip()
                    meeting_date = parse_date(date_text_clean).date()
                except Exception:
                    self.logger.error(f"Failed to parse date: {date_text}")
                    continue

                links = [
                    link
                    for link in (
                        [
                            self._build_link(a, "https://www.spps.org")
                            for a in meeting_section.css("div.fsElementContent a[href]")
                        ]
                    )
                    if link and (link.get("href") or link.get("title"))
                ]
                self.materials[(meeting_date, category)] = links
                if subtitle:
                    self.materials[(meeting_date, subtitle.lower())] = links

        request = self._trigger_ical()
        if request:
            yield request

    def parse(self, response):
        """Parse meetings from iCal feed and merge with materials and boardbook links."""  # noqa

        try:
            cal = Calendar.from_ical(response.text)
        except Exception as e:
            self.logger.error(f"Failed to parse iCal from {response.url}: {e}")
            return

        current_year = datetime.now().year
        events = recurring_ical_events.of(cal).between(
            date(current_year - 3, 1, 1),
            date(current_year + 1, 12, 31),
        )

        for event in events:
            start = self._parse_dt(event.get("dtstart"))
            if not start:
                continue

            title = self._normalize_title(self._parse_title(event), start)
            end = self._parse_dt(event.get("dtend"))
            links = []
            meeting_date = start.date()
            meeting_type = self._get_meeting_type(title)

            links = self._resolve_links(meeting_date, meeting_type, start.time())
            links = [link for link in links if link.get("href") or link.get("title")]

            meeting = Meeting(
                title=title,
                description="",
                classification=BOARD,
                start=start,
                end=end,
                all_day=False,
                time_notes="",
                location=self._parse_location(event),
                links=links,
                source=self.source_url,
            )

            meeting["status"] = self._get_status(meeting)
            meeting["id"] = self._get_id(meeting)

            yield meeting

    def _get_meeting_type(self, title):
        """Map calendar title to meeting type."""
        title_lower = title.lower()
        if "committee" in title_lower:
            return "Committee of the Board"
        if (
            "special" in title_lower
            or "closed" in title_lower
            or "attorney" in title_lower
        ):
            return "Special"
        if (
            "board of education" in title_lower
            or "boe" in title_lower
            or "regular" in title_lower
        ):
            return "Board of Education"
        if "annual" in title_lower:
            return "annual"
        return None

    def _normalize_title(self, title, start):
        """Normalize edge-case meeting titles."""
        if (
            "special regular board of education" in title.lower()
            and start.strftime("%H:%M") == "17:30"
        ):
            return "Regular Board of Education Meeting"
        return title

    def _parse_title(self, event):
        """Parse title from VEVENT summary."""
        return str(event.get("summary", "")).strip()

    def _parse_dt(self, dt_prop):
        """Parse a dtstart/dtend property into a naive datetime in local time."""
        if dt_prop is None:
            return None
        dt = dt_prop.dt
        if isinstance(dt, datetime):
            if dt.tzinfo is not None:
                local_tz = pytz.timezone(self.timezone)
                dt = dt.astimezone(local_tz).replace(tzinfo=None)
            return dt
        return datetime(dt.year, dt.month, dt.day)

    def _resolve_links(self, meeting_date, meeting_type, start_time):
        """Return the best available links: materials first, boardbook as fallback."""
        if meeting_type:
            links = self._get_materials_links(meeting_date, meeting_type)
            if links:
                return links
        return self._get_boardbook_links(meeting_date, meeting_type, start_time)

    def _get_materials_links(self, meeting_date, meeting_type):
        """Find materials links with exact or partial match on meeting type."""
        key = (meeting_date, meeting_type)
        if key in self.materials:
            return self.materials[key]

        date_keys = [k for k in self.materials if k[0] == meeting_date]
        matched_keys = [k for k in date_keys if meeting_type.lower() in k[1].lower()]
        if len(matched_keys) == 1:
            return self.materials[matched_keys[0]]
        return []

    def _get_boardbook_links(self, meeting_date, meeting_type, start_time):
        """Find boardbook links matching on date, time, and meeting type."""
        date_keys = [k for k in self.boardbook_links if k[0] == meeting_date]
        if not date_keys:
            return []

        time_matched = [k for k in date_keys if start_time and k[1] == start_time]
        if time_matched:
            if len(time_matched) == 1:
                return self.boardbook_links[time_matched[0]]
            elif meeting_type:
                for k in time_matched:
                    if meeting_type.lower() in k[2]:
                        return self.boardbook_links[k]

        if meeting_type:
            for k in date_keys:
                if meeting_type.lower() in k[2]:
                    return self.boardbook_links[k]

        return []

    def _build_link(self, a, base_url=""):
        """Build a link dict from an anchor element or None if empty."""
        href = a.attrib.get("href", "")
        title = a.css("::text").get("").strip()
        if base_url and href.startswith("/"):
            href = f"{base_url}{href}"
        if not href and not title:
            return None
        return {"href": href, "title": title}

    def _parse_location(self, event):
        """Parse location from VEVENT."""
        location = str(event.get("location", "")).strip()
        title = self._parse_title(event).lower()

        # use calendar location if present
        if location:
            name = ""
            address = location

            # if location starts with a name (not a street number), split it out
            parts = location.split(",", 1)
            if parts[0] and not parts[0].strip()[0].isdigit():
                name = parts[0].strip()
                address = parts[1].strip() if len(parts) > 1 else location

            # override name for known SPPS address
            if not name and (
                "360 colborne" in address.lower() or "360 s colborne" in address.lower()
            ):
                name = "Saint Paul Public Schools"

            return {"name": name, "address": address}

        # fallback location based on title
        if "committee" in title:
            return self.location_committee
        if "board" in title:
            return self.location_regular_board

        return {"name": "", "address": location}
