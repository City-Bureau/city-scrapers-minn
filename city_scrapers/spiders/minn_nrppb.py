from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnNrppbSpider(MinnCityMixin):
    name = "minn_nrppb"
    agency = "Neighborhood Revitalization Program Policy Board"
    committee_id = 78
    meeting_type = 2
