from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnBetSpider(MinnCityMixin):
    name = "minn_bet"
    agency = "Board of Estimate and Taxation"
    committee_id = 177
    meeting_type = 4
