from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnPcrpSpider(MinnCityMixin):
    name = "minn_pcrp"
    agency = "Police Conduct Review Panel"
    committee_id = 83
    meeting_type = 2
