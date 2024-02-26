from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnWacSpider(MinnCityMixin):
    name = "minn_wac"
    agency = "Workplace Advisory Committee"
    committee_id = 147
    meeting_type = 2
