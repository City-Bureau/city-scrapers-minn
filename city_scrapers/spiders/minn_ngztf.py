from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnNgztfSpider(MinnCityMixin):
    name = "minn_ngztf"
    agency = "Northside Green Zone Task Force"
    committee_id = 187
    meeting_type = 2
