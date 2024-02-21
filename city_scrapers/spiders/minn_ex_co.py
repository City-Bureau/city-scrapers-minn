from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnExCoSpider(MinnCityMixin):
    name = "minn_ex_co"
    agency = "Executive Committee"
    committee_id = 7
    meeting_type = 4
