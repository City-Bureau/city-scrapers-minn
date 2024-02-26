from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnBlssdabSpider(MinnCityMixin):
    name = "minn_blssdab"
    agency = "Bloomington-Lake Special Service District Advisory Board"
    committee_id = 151
    meeting_type = 2
