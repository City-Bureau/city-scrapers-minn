from city_scrapers.mixins.minn_city import MinnCityMixin


class Minn48chiSsdabSpider(MinnCityMixin):
    name = "minn_48chi_ssdab"
    agency = "48th & Chicago Special Service District Advisory Board"
    committee_id = 153
    meeting_type = 2
