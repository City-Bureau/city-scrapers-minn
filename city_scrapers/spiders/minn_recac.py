from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnRecacSpider(MinnCityMixin):
    name = "minn_recac"
    agency = "Racial Equity Community Advisory Committee"
    committee_id = 175
    meeting_type = 2
