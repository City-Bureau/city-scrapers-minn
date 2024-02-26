from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnMacaSpider(MinnCityMixin):
    name = "minn_maca"
    agency = "Minneapolis Advisory Committee on Aging"
    committee_id = 66
    meeting_type = 2
