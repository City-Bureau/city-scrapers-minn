from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnPacSpider(MinnCityMixin):
    name = "minn_pac"
    agency = "Pedestrian Advisory Committee"
    committee_id = 80
    meeting_type = 2
