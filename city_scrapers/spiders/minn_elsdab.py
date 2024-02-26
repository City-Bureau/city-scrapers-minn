from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnElsdabSpider(MinnCityMixin):
    name = "minn_elsdab"
    agency = "East Lake Special Service District Advisory Board"
    committee_id = 156
    meeting_type = 2
