from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnHpcSpider(MinnCityMixin):
    name = "minn_hpc"
    agency = "Heritage Preservation Commission"
    committee_id = 56
    meeting_type = 4
