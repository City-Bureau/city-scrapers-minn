from datetime import datetime
from os.path import dirname, join
from datetime import date
from dateutil.relativedelta import relativedelta
import pytest
from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.minn_hcg_boc import MinnHcgBocSpider

test_response = file_response(
    join(dirname(__file__), "files", "minn_hcg_boc.html"),
    url="https://prodboarddocsrch-hc-api.azurewebsites.net/api/Values/-1/-1/2021-10-01/2023-12-29/none/true",
)
spider = MinnHcgBocSpider()

freezer = freeze_time("2021-12-15")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_count():
    assert len(parsed_items) == 6

def test_title():
    assert parsed_items[0]["title"] == "Board Meeting"


def test_start():
    assert parsed_items[0]["start"] == datetime(2021, 12, 14, 18, 30)


def test_status():
    assert parsed_items[0]["status"] == "passed"

def test_classification():
    assert parsed_items[0]["classification"] == "Board"

#
# # @pytest.mark.parametrize("item", parsed_items)
def test_all_day():
    assert parsed_items[0]["all_day"] is False


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Online Meeting",
        "address": "Virtually via hennepin.us"
    }


def test_source():
    assert parsed_items[0]["source"] == "https://www.hennepin.us/your-government/leadership/county-board-meetings"


def test_links():
    assert parsed_items[0]["links"] == [{
        "title": "Agenda Document",
      "href": "https://hennepin.novusagenda.com/agendapublic/DisplayAgendaPDF.ashx?MeetingID=1265"
    }]

