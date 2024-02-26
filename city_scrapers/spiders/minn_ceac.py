from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnCeacSpider(MinnCityMixin):
    name = "minn_ceac"
    agency = "Community Environmental Advisory Commission"
    committee_id = 48
    meeting_type = 2
