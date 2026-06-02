from city_scrapers.mixins.minn_ramsey_county import MinnRamseyCountyMixin

"""
The value of `agency_name` has to match with the scraper's corresponding
resquest record in the Airtable backlog. This value is used by the
'Airtable sync workflow' to link the scraper's PR to the correct request
record in Airtable.
"""

# dept_id and guid come from https://ramseycountymn.legistar.com/Departments.aspx
spider_configs = [
    # Board of Commissioners
    {
        "class_name": "MinnRamseyCountyBoardOfCommissionersSpider",
        "name": "minn_ramsey_boc",
        "agency": "Ramsey County Board of Commissioners",
        "agency_name": "Ramsey County Board",
        "dept_id": "41635",
        "guid": "342EB836-C0D1-463A-8A12-C5C1B8BB0EBF",
    },
    # Board Workshop / Discussion
    {
        "class_name": "MinnRamseyCountyBoardWorkshopSpider",
        "name": "minn_ramsey_bwd",
        "agency": "Ramsey County Board Workshop / Discussion",
        "agency_name": "Ramsey County Board",
        "dept_id": "44588",
        "guid": "87E5EA0B-060D-423E-B656-A0557147DB5A",
    },
    # Budget Committee of the Whole
    {
        "class_name": "MinnRamseyCountyBudgetCommitteeSpider",
        "name": "minn_ramsey_bcw",
        "agency": "Ramsey County Budget Committee of the Whole",
        "agency_name": "Ramsey County Board",
        "dept_id": "42189",
        "guid": "98D0D44A-168E-4676-B714-BFED6022EF17",
    },
    # Housing and Redevelopment Authority
    {
        "class_name": "MinnRamseyCountyHraSpider",
        "name": "minn_ramsey_hra",
        "agency": "Ramsey County Housing and Redevelopment Authority",
        "agency_name": "Ramsey County Board",
        "dept_id": "42188",
        "guid": "CDDF294F-8FC8-4162-AE1C-6309552C4427",
    },
    # Legislative Committee of the Whole
    {
        "class_name": "MinnRamseyCountyLegislativeCommitteeSpider",
        "name": "minn_ramsey_lcw",
        "agency": "Ramsey County Legislative Committee of the Whole",
        "agency_name": "Ramsey County Board",
        "dept_id": "42190",
        "guid": "AE0EDFEA-0EE4-4FFD-A92A-BD3857E2B442",
    },
    # Regional Railroad Authority
    {
        "class_name": "MinnRamseyCountyRegionalRailroadSpider",
        "name": "minn_ramsey_rra",
        "agency": "Ramsey County Regional Railroad Authority",
        "agency_name": "Ramsey County Board",
        "dept_id": "42187",
        "guid": "7029D254-4F33-4FE0-B34A-C8AB0ABC3D54",
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
            # Build attributes dict without class_name
            attrs = {k: v for k, v in config.items() if k != "class_name"}

            # Dynamically create the spider class
            spider_class = type(
                class_name,
                (MinnRamseyCountyMixin,),
                attrs,
            )

            # Register the class in the global namespace
            globals()[class_name] = spider_class


# Create all spider classes at module load
create_spiders()
