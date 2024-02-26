from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnPhacSpider(MinnCityMixin):
    name = "minn_phac"
    agency = "Public Health Advisory Committee"
    committee_id = 72
    meeting_type = 2
