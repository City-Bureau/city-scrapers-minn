from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnLbaeSpider(MinnCityMixin):
    name = "minn_lbae"
    agency = "Local Board of Appeal and Equalization"
    committee_id = 173
    meeting_type = 4
