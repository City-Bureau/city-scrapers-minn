from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnCharCoRswSpider(MinnCityMixin):
    name = "minn_char_co_rsw"
    agency = "Charter Commission Rent Stabilization Work Group"
    committee_id = 225
    meeting_type = 2
