from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnTecSpider(MinnCityMixin):
    name = "minn_tec"
    agency = "Transgender Equity Council"
    committee_id = 146
    meeting_type = 2
