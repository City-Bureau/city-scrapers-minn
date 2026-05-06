
from city_scrapers.mixins.minn_city import MinnCityMixin

spider_configs = [
    {
        "class_name": "MinnAuditCoSpider",
        "name": "minn_audit_co",
        "agency": "Minneapolis Audit Committee",
        "category_label": "Audit Committee Meeting",
        "committee_id": 1,
        "meeting_type": 4,
        "marked_agenda_path": "MarkedAgenda",
    },
     {
        "class_name": "MinnBacSpider",
        "name": "minn_bac",
        "agency": "Minneapolis Bicycle Advisory Committee",
        "committee_id": 38,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnBetSpider",
        "name": "minn_bet",
        "agency": "Board of Estimate and Taxation",
        "committee_id": 177,
        "meeting_type": 4,
    },
    {
        "class_name": "MinnBlssdabSpider",
        "name": "minn_blssdab",
        "agency": "Bloomington-Lake Special Service District Advisory Board",
        "committee_id": 151,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnBoardSpider",
        "name": "minn_board",
        "agency": "Minneapolis City Council - Board",
        "committee_id": 16,
        "meeting_type": 1,
    },
    {
        "class_name": "MinnBudCommSpider",
        "name": "minn_bud_comm",
        "agency": "Budget Committee",
        "committee_id": 179,
        "meeting_type": 1,
    },
    {
        "class_name": "MinnBusinessIhzcSpider",
        "name": "minn_business_ihzc",
        "agency": "Business, Inspections, Housing & Zoning (BIHZ) Committee",
        "committee_id": 220,
        "meeting_type": 1,
    },
    {
        "class_name": "MinnCdaSpider",
        "name": "minn_cda",
        "agency": "Minneapolis Community Development Agency",
        "committee_id": 148,
        "meeting_type": 4,
    },
    {
        "class_name": "MinnCeacSpider",
        "name": "minn_ceac",
        "agency": "Community Environmental Advisory Commission",
        "committee_id": 48,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnCharCoRswSpider",
        "name": "minn_char_co_rsw",
        "agency": "Charter Commission Rent Stabilization Work Group",
        "committee_id": 225,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnCharCoSpider",
        "name": "minn_char_co",
        "agency": "Charter Commission",
        "committee_id": 42,
        "meeting_type": 4,
        "marked_agenda_path": "MarkedAgenda",
    },
    {
        "class_name": "MinnClricSpider",
        "name": "minn_clric",
        "agency": "Capital Long-Range Improvements Committee",
        "committee_id": 40,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnClssdabSpider",
        "name": "minn_clssdab",
        "agency": "Chicago-Lake Special Service District Advisory Board",
        "committee_id": 154,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnCrcSpider",
        "name": "minn_crc",
        "agency": "Civil Rights Commission",
        "committee_id": 45,
        "meeting_type": 4,
    },
    {
        "class_name": "MinnCscSpider",
        "name": "minn_csc",
        "agency": "Civil Service Commission",
        "committee_id": 46,
        "meeting_type": 4,
    },
    {
        "class_name": "MinnElsdabSpider",
        "name": "minn_elsdab",
        "agency": "East Lake Special Service District Advisory Board",
        "committee_id": 156,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnEpbSpider",
        "name": "minn_epb",
        "agency": "Ethical Practices Board",
        "committee_id": 53,
        "meeting_type": 4,
    },
    {
        "class_name": "MinnFlecSpider",
        "name": "minn_flec",
        "agency": "Futuro Latino Empowerment Commission",
        "committee_id": 193,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnHmfcSpider",
        "name": "minn_hmfc",
        "agency": "Homegrown Minneapolis Food Council",
        "committee_id": 58,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnHpcSpider",
        "name": "minn_hpc",
        "agency": "Heritage Preservation Commission",
        "committee_id": 56,
        "meeting_type": 4,
    },
    {
        "class_name": "MinnLbaeSpider",
        "name": "minn_lbae",
        "agency": "Local Board of Appeal and Equalization",
        "committee_id": 173,
        "meeting_type": 4,
    },
    {
        "class_name": "MinnLhsdabSpider",
        "name": "minn_lhsdab",
        "agency": "Lowry Hill Special Service District Advisory Board",
        "committee_id": 160,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnLlssdabSpider",
        "name": "minn_llssdab",
        "agency": "Lyndale-Lake Special Service District Advisory Board",
        "committee_id": 161,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnMacSpider",
        "name": "minn_mac",
        "agency": "Minneapolis Arts Commission",
        "committee_id": 68,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnMacaSpider",
        "name": "minn_maca",
        "agency": "Minneapolis Advisory Committee on Aging",
        "committee_id": 66,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnMachSpider",
        "name": "minn_mach",
        "agency": "Minneapolis Advisory Committee on Housing",
        "committee_id": 183,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnMacopwdSpider",
        "name": "minn_macopwd",
        "agency": "Minneapolis Advisory Committee On People With Disabilities",
        "committee_id": 67,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnMwdbSpider",
        "name": "minn_mwdb",
        "agency": "Minneapolis Workforce Development Board",
        "committee_id": 72,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnNgztfSpider",
        "name": "minn_ngztf",
        "agency": "Northside Green Zone Task Force",
        "committee_id": 187,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnNrppbSpider",
        "name": "minn_nrppb",
        "agency": "Neighborhood Revitalization Program Policy Board",
        "committee_id": 78,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnPacSpider",
        "name": "minn_pac",
        "agency": "Pedestrian Advisory Committee",
        "committee_id": 80,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnPcrpSpider",
        "name": "minn_pcrp",
        "agency": "Police Conduct Review Panel",
        "committee_id": 83,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnPhacSpider",
        "name": "minn_phac",
        "agency": "Public Health Advisory Committee",
        "committee_id": 72,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnPhsCommSpider",
        "name": "minn_phs_comm",
        "agency": "Public Health & Safety (PHS) Committee",
        "committee_id": 219,
        "meeting_type": 1,
    },
    {
        "class_name": "MinnPlannCoSpider",
        "name": "minn_plann_co",
        "agency": "Planning Commission",
        "committee_id": 81,
        "meeting_type": 4,
    },
    {
        "class_name": "MinnPogoCommSpider",
        "name": "minn_pogo_comm",
        "agency": "Policy & Government Oversight (POGO) Committee",
        "committee_id": 205,
        "meeting_type": 1,
    },
    {
        "class_name": "MinnSgzcSpider",
        "name": "minn_sgzc",
        "agency": "Southside Green Zone Council",
        "committee_id": 188,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnTecSpider",
        "name": "minn_tec",
        "agency": "Transgender Equity Council",
        "committee_id": 146,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnWacSpider",
        "name": "minn_wac",
        "agency": "Workplace Advisory Committee",
        "committee_id": 147,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnZba50fssdabSpider",
        "name": "minn_zba_50fssdab",
        "agency": "50th & France Special Service District Advisory Board",
        "committee_id": 149,
        "meeting_type": 2,
    },
    {
        "class_name": "MinnZbaSpider",
        "name": "minn_zba",
        "agency": "Zoning Board of Adjustment",
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