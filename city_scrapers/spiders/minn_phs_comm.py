from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnPhsCommSpider(MinnCityMixin):
    name = "minn_phs_comm"
    agency = "Public Health & Safety (PHS) Committee"
    committee_id = 219
    meeting_type = 1
