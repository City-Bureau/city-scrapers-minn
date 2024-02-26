from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnClricSpider(MinnCityMixin):
    name = "minn_clric"
    agency = "Capital Long-Range Improvements Committee"
    committee_id = 40
    meeting_type = 2
