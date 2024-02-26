from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnDssdabSpider(MinnCityMixin):
    name = "minn_dssdab"
    agency = "Dinkytown Special Service District Advisory Board"
    committee_id = 155
    meeting_type = 2
