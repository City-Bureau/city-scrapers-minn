from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnCharCoSpider(MinnCityMixin):
    name = "minn_char_co"
    agency = "Charter Commission"
    committee_id = 42
    meeting_type = 4
