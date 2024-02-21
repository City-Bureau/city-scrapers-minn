from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnLhssdabSpider(MinnCityMixin):
    name = "minn_lhssdab"
    agency = "Linden Hills Special Service District Advisory Board"
    committee_id = 159
    meeting_type = 2
