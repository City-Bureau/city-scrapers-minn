from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnClssdabSpider(MinnCityMixin):
    name = "minn_clssdab"
    agency = "Chicago-Lake Special Service District Advisory Board"
    committee_id = 154
    meeting_type = 2
