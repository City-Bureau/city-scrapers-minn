from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnBacSpider(MinnCityMixin):
    name = "minn_bac"
    agency = "Minneapolis Bicycle Advisory Committee"
    committee_id = 38
    meeting_type = 2
