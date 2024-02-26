from city_scrapers.mixins.minn_city import MinnCityMixin


class MinnAuditCoSpider(MinnCityMixin):
    name = "minn_audit_co"
    agency = "Audit Committee"
    committee_id = 1
    meeting_type = 4
