from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnZbaSpider(MinnCityMixin):
    name = "minn_zba"
    agency = "Zoning Board of Adjustment"
    committee_id = 94
    meeting_type = 4
