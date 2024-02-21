from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnVpscSpider(MinnCityMixin):
    name = "minn_vpsc"
    agency = "Violence Prevention Steering Committee"
    committee_id = 182
    meeting_type = 2
