from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnPcocSpider(MinnCityMixin):
    name = "minn_pcoc"
    agency = "Police Conduct Oversight Commission"
    committee_id = 215
    meeting_type = 4
