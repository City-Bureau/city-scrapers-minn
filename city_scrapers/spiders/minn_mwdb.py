from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnMwdbSpider(MinnCityMixin):
    name = "minn_mwdb"
    agency = "Minneapolis Workforce Development Board"
    committee_id = 72
    meeting_type = 2
