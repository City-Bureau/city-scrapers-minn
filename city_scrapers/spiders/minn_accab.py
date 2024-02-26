from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnAccabSpider(MinnCityMixin):
    name = "minn_accab"
    agency = "Animal Care and Control Advisory Board"
    committee_id = 35
    meeting_type = 2
