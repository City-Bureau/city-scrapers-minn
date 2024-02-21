from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnBudCommSpider(MinnCityMixin):
    name = "minn_bud_comm"
    agency = "Budget Committee"
    committee_id = 179
    meeting_type = 1
