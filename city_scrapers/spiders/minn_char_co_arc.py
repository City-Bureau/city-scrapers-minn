from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnCharCoArcSpider(MinnCityMixin):
    name = "minn_char_co_arc"
    agency = "Charter Commission Amendment Review Committee"
    committee_id = 221
    meeting_type = 4
