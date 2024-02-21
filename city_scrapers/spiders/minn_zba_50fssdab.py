from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnZba50fssdabSpider(MinnCityMixin):
    name = "minn_zba_50fssdab"
    agency = "50th & France Special Service District Advisory Board"
    committee_id = 149
    meeting_type = 2
