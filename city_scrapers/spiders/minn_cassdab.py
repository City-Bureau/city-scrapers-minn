from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnCassdabSpider(MinnCityMixin):
    name = "minn_cassdab"
    agency = "Central Avenue Special Service District Advisory Board"
    committee_id = 152
    meeting_type = 2
