from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnSgzcSpider(MinnCityMixin):
    name = "minn_sgzc"
    agency = "Southside Green Zone Council"
    committee_id = 188
    meeting_type = 2
