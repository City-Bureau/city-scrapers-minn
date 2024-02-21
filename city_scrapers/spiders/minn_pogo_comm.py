from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnPogoCommSpider(MinnCityMixin):
    name = "minn_pogo_comm"
    agency = "Policy & Government Oversight (POGO) Committee"
    committee_id = 205
    meeting_type = 1
