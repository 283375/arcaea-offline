from decimal import Decimal
from typing import Dict, List

from bs4 import BeautifulSoup
from bs4.element import Tag


class WikiArcaeaCnConstantParser:
    HEADERS = ["曲目", "PST", "PRS", "FTR", "BYD"]

    def __init__(self, filepath):
        self.filepath = filepath

    def parse(self) -> Dict[str, List[int]]:
        with open(self.filepath, "r", encoding="utf-8") as html_f:
            html = BeautifulSoup(html_f.read(), "html.parser")

        result = {}

        for table in html.find_all("table"):
            # check if the table is constant table
            if not isinstance(table, Tag):
                continue

            tbody = table.find("tbody")
            if not isinstance(tbody, Tag):
                continue

            first_tr = tbody.find("tr")
            if not isinstance(first_tr, Tag):
                continue

            header_match = all(
                expected_header in th.string
                for expected_header, th in zip(self.HEADERS, first_tr.find_all("th"))
            )
            if not header_match:
                continue

            rows = list(tbody.find_all("tr"))[1:]
            for row in rows:
                title = row.td.a.string
                constants = []
                for td in row.find_all("td")[1:5]:
                    constant_string = td.string.replace("\n", "")
                    if "-" in constant_string or not constant_string:
                        constants.append(None)
                    else:
                        constants.append(int(Decimal(constant_string) * 10))
                result[title] = constants

        return result
