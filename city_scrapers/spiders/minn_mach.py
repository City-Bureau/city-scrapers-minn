from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnMachSpider(MinnCityMixin):
    name = "minn_mach"
    agency = "Minneapolis Advisory Committee on Housing"
    committee_id = 183
    meeting_type = 2
