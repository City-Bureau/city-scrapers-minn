from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnUssdabSpider(MinnCityMixin):
    name = "minn_ussdab"
    agency = "Uptown Special Service District Advisory Board"
    committee_id = 164
    meeting_type = 2
