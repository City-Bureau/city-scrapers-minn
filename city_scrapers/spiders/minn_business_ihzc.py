from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnBusinessIhzcSpider(MinnCityMixin):
    name = "minn_business_ihzc"
    agency = "Business, Inspections, Housing & Zoning (BIHZ) Committee"
    committee_id = 220
    meeting_type = 1
