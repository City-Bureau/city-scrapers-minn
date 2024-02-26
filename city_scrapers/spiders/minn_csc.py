from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnCscSpider(MinnCityMixin):
    name = "minn_csc"
    agency = "Civil Service Commission"
    committee_id = 46
    meeting_type = 4
