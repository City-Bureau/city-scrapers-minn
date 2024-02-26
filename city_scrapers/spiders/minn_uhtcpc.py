from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnUhtcpcSpider(MinnCityMixin):
    name = "minn_uhtcpc"
    agency = "Upper Harbor Terminal Collaborative Planning Committee"
    committee_id = 189
    meeting_type = 2
