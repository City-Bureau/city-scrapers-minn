from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnEpbSpider(MinnCityMixin):
    name = "minn_epb"
    agency = "Ethical Practices Board"
    committee_id = 53
    meeting_type = 4
