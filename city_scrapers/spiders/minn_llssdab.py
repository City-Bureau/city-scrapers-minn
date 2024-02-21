from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnLlssdabSpider(MinnCityMixin):
    name = "minn_llssdab"
    agency = "Lyndale-Lake Special Service District Advisory Board"
    committee_id = 161
    meeting_type = 2
