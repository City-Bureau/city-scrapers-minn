from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnBoardSpider(MinnCityMixin):
    name = "minn_board"
    agency = "Minneapolis City Council - Board"
    committee_id = 16
    meeting_type = 1
