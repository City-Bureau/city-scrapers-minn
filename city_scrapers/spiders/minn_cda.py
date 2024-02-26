from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnCdaSpider(MinnCityMixin):
    name = "minn_cda"
    agency = "Minneapolis Community Development Agency"
    committee_id = 148
    meeting_type = 4
