from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnHmfcSpider(MinnCityMixin):
    name = "minn_hmfc"
    agency = "Homegrown Minneapolis Food Council"
    committee_id = 58
    meeting_type = 2
