from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnEsssdabSpider(MinnCityMixin):
    name = "minn_esssdab"
    agency = "Eat Street Special Service District Advisory Board"
    committee_id = 162
    meeting_type = 2
