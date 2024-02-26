from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnPlannCoSpider(MinnCityMixin):
    name = "minn_plann_co"
    agency = "Planning Commission"
    committee_id = 81
    meeting_type = 4
