from city_scrapers.mixins.minn_city import MinnCityMixin

"""
The `agency_name` field is only used by the Airtable slug sync workflow
for matching the spider with its corresponding Backlog table record.
"""
spider_configs = [
    {
        "class_name": "MinnAuditCoSpider",
        "name": "minn_audit_co",
        "agency": "Minneapolis Audit Committee",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 1,
        "meeting_type": 4,
        "marked_agenda_path": "MarkedAgenda",
    },
    {
        "class_name": "MinnBacSpider",
        "name": "minn_bac",
        "agency": "Minneapolis Bicycle Advisory Committee",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 38,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnBetSpider",
        "name": "minn_bet",
        "agency": "Minneapolis Board of Estimate and Taxation",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 177,
        "meeting_type": 4,
    },
    {
        "class_name": "MinnBlssdabSpider",
        "name": "minn_blssdab",
        "agency": "Minneapolis Bloomington-Lake Special Service District Advisory Board",  # noqa
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 151,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnBoardSpider",
        "name": "minn_board",
        "agency": "Minneapolis City Council - Board",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 16,
        "meeting_type": 1,
    },
    {
        "class_name": "MinnBudCommSpider",
        "name": "minn_bud_comm",
        "agency": "Minneapolis Budget Committee",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 179,
        "meeting_type": 1,
    },
    {
        "class_name": "MinnBusinessIhzcSpider",
        "name": "minn_business_ihzc",
        "agency": "Minneapolis Business, Inspections, Housing & Zoning (BIHZ) Committee",  # noqa
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 220,
        "meeting_type": 1,
    },
    {
        "class_name": "MinnCdaSpider",
        "name": "minn_cda",
        "agency": "Minneapolis Community Development Agency",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 148,
        "meeting_type": 4,
    },
    {
        "class_name": "MinnCeacSpider",
        "name": "minn_ceac",
        "agency": "Minneapolis Community Environmental Advisory Commission",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 48,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnCharCoRswSpider",
        "name": "minn_char_co_rsw",
        "agency": "Minneapolis Charter Commission Rent Stabilization Work Group",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 225,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnCharCoSpider",
        "name": "minn_char_co",
        "agency": "Minneapolis Charter Commission",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 42,
        "meeting_type": 4,
        "marked_agenda_path": "MarkedAgenda",
    },
    {
        "class_name": "MinnClricSpider",
        "name": "minn_clric",
        "agency": "Minneapolis Capital Long-Range Improvements Committee",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 40,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnClssdabSpider",
        "name": "minn_clssdab",
        "agency": "Minneapolis Chicago-Lake Special Service District Advisory Board",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 154,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnCrcSpider",
        "name": "minn_crc",
        "agency": "Minneapolis Civil Rights Commission",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 45,
        "meeting_type": 4,
    },
    {
        "class_name": "MinnCscSpider",
        "name": "minn_csc",
        "agency": "Minneapolis Civil Service Commission",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 46,
        "meeting_type": 4,
    },
    {
        "class_name": "MinnElsdabSpider",
        "name": "minn_elsdab",
        "agency": "Minneapolis East Lake Special Service District Advisory Board",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 156,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnEpbSpider",
        "name": "minn_epb",
        "agency": "Minneapolis Ethical Practices Board",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 53,
        "meeting_type": 4,
    },
    {
        "class_name": "MinnFlecSpider",
        "name": "minn_flec",
        "agency": "Minneapolis Futuro Latino Empowerment Commission",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 193,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnHmfcSpider",
        "name": "minn_hmfc",
        "agency": "Minneapolis Homegrown Minneapolis Food Council",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 58,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnHpcSpider",
        "name": "minn_hpc",
        "agency": "Minneapolis Heritage Preservation Commission",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 56,
        "meeting_type": 4,
    },
    {
        "class_name": "MinnLbaeSpider",
        "name": "minn_lbae",
        "agency": "Minneapolis Local Board of Appeal and Equalization",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 173,
        "meeting_type": 4,
    },
    {
        "class_name": "MinnLhsdabSpider",
        "name": "minn_lhsdab",
        "agency": "Minneapolis Lowry Hill Special Service District Advisory Board",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 160,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnLlssdabSpider",
        "name": "minn_llssdab",
        "agency": "Minneapolis Lyndale-Lake Special Service District Advisory Board",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 161,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnMacSpider",
        "name": "minn_mac",
        "agency": "Minneapolis Arts Commission",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 68,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnMacaSpider",
        "name": "minn_maca",
        "agency": "Minneapolis Advisory Committee on Aging",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 66,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnMachSpider",
        "name": "minn_mach",
        "agency": "Minneapolis Advisory Committee on Housing",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 183,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnMacopwdSpider",
        "name": "minn_macopwd",
        "agency": "Minneapolis Advisory Committee On People With Disabilities",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 67,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnMwdbSpider",
        "name": "minn_mwdb",
        "agency": "Minneapolis Workforce Development Board",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 72,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnNgztfSpider",
        "name": "minn_ngztf",
        "agency": "Minneapolis Northside Green Zone Task Force",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 187,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnNrppbSpider",
        "name": "minn_nrppb",
        "agency": "Minneapolis Neighborhood Revitalization Program Policy Board",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 78,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnPacSpider",
        "name": "minn_pac",
        "agency": "Minneapolis Pedestrian Advisory Committee",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 80,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnPcrpSpider",
        "name": "minn_pcrp",
        "agency": "Minneapolis Police Conduct Review Panel",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 83,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnPhacSpider",
        "name": "minn_phac",
        "agency": "Minneapolis Public Health Advisory Committee",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 84,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnPhsCommSpider",
        "name": "minn_phs_comm",
        "agency": "Minneapolis Public Health & Safety (PHS) Committee",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 219,
        "meeting_type": 1,
    },
    {
        "class_name": "MinnPlannCoSpider",
        "name": "minn_plann_co",
        "agency": "Minneapolis Planning Commission",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 81,
        "meeting_type": 4,
    },
    {
        "class_name": "MinnPogoCommSpider",
        "name": "minn_pogo_comm",
        "agency": "Minneapolis Policy & Government Oversight (POGO) Committee",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 205,
        "meeting_type": 1,
    },
    {
        "class_name": "MinnSgzcSpider",
        "name": "minn_sgzc",
        "agency": "Minneapolis Southside Green Zone Council",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 188,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnTecSpider",
        "name": "minn_tec",
        "agency": "Minneapolis Transgender Equity Council",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 146,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnWacSpider",
        "name": "minn_wac",
        "agency": "Minneapolis Workplace Advisory Committee",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 147,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnZba50fssdabSpider",
        "name": "minn_zba_50fssdab",
        "agency": "Minneapolis 50th & France Special Service District Advisory Board",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 149,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnZbaSpider",
        "name": "minn_zba",
        "agency": "Minneapolis Zoning Board of Adjustment",
        "agency_name": "Minneapolis Planning Commission",
        "committee_id": 94,
        "meeting_type": 4,
    },
]


def create_spiders():
    """
    Dynamically create spider classes using the spider_configs list
    and register them in the global namespace.
    """
    for config in spider_configs:
        class_name = config["class_name"]

        if class_name not in globals():
            # Build attributes dict without class_name to avoid duplication.
            # We make sure that the class_name is not already in the global namespace
            # Because some scrapy CLI commands like `scrapy list` will inadvertently
            # declare the spider class more than once otherwise
            attrs = {k: v for k, v in config.items() if k != "class_name"}

            # Dynamically create the spider class
            spider_class = type(
                class_name,
                (MinnCityMixin,),
                attrs,
            )

            globals()[class_name] = spider_class


# Create all spider classes at module load
create_spiders()
