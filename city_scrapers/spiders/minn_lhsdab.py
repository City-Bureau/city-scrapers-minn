from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnLhsdabSpider(MinnCityMixin):
    name = "minn_lhsdab"
    agency = "Lowry Hill Special Service District Advisory Board"
    committee_id = 160
    meeting_type = 2
