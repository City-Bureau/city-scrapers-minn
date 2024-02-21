from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnCrcSpider(MinnCityMixin):
    name = "minn_crc"
    agency = "Civil Rights Commission"
    committee_id = 45
    meeting_type = 4
