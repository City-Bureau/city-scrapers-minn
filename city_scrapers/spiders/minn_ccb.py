from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnCcbSpider(MinnCityMixin):
    name = "minn_ccb"
    agency = "City Canvassing Board"
    committee_id = 165
    meeting_type = 4
