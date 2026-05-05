from city_scrapers.mixins.minn_ramsey_county import MinnRamseyCountyMixin

# Configuration for each spider
# Classification is derived from meeting title in the mixin's _parse_classification
spider_configs = [
    # Board of Commissioners
    {
        "class_name": "MinnRamseyCountyBoardOfCommissionersSpider",
        "name": "minn_ramsey_boc",
        "agency": "Board of Commissioners",
    },
    # Board Workshop / Discussion
    {
        "class_name": "MinnRamseyCountyBoardWorkshopSpider",
        "name": "minn_ramsey_bwd",
        "agency": "Board Workshop / Discussion",
    },
    # Budget Committee of the Whole
    {
        "class_name": "MinnRamseyCountyBudgetCommitteeSpider",
        "name": "minn_ramsey_bcw",
        "agency": "Budget Committee of the Whole",
    },
    # Housing and Redevelopment Authority
    {
        "class_name": "MinnRamseyCountyHraSpider",
        "name": "minn_ramsey_hra",
        "agency": "Housing and Redevelopment Authority",
    },
    # Legislative Committee of the Whole
    {
        "class_name": "MinnRamseyCountyLegislativeCommitteeSpider",
        "name": "minn_ramsey_lcw",
        "agency": "Legislative Committee of the Whole",
    },
    # Regional Railroad Authority
    {
        "class_name": "MinnRamseyCountyRegionalRailroadSpider",
        "name": "minn_ramsey_rra",
        "agency": "Regional Railroad Authority",
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
