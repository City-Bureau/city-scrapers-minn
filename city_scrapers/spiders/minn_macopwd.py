from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnMacopwdSpider(MinnCityMixin):
    name = "minn_macopwd"
    agency = "Minneapolis Advisory Committee On People With Disabilities"
    committee_id = 67
    meeting_type = 2
