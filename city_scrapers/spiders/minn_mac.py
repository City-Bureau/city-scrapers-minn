from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnMacSpider(MinnCityMixin):
    name = "minn_mac"
    agency = "Minneapolis Arts Commission"
    committee_id = 68
    meeting_type = 2
