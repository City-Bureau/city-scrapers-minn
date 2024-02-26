from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnTpwCommSpider(MinnCityMixin):
    name = "minn_tpw_comm"
    agency = "Transportation & Public Works (TPW) Committee"
    committee_id = 13
    meeting_type = 1
