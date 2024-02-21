from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnSvssdabSpider(MinnCityMixin):
    name = "minn_svssdab"
    agency = "Stadium Village Special Service District Advisory Board"
    committee_id = 163
    meeting_type = 2
