from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnFlecSpider(MinnCityMixin):
    name = "minn_flec"
    agency = "Futuro Latino Empowerment Commission"
    committee_id = 193
    meeting_type = 2
