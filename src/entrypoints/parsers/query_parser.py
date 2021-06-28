from typing import Tuple
from src.config import CONFIG


class QueryParameterParser:
    def __init__(self, query):
        if str(query) == "":
            return

        for param in str(query).split("&"):
            key, value = param.split("=")
            setattr(self, key, value)

    def parse_pagination_parameter(self) -> Tuple[int, int]:
        page = None
        per_page = None
        if hasattr(self, "page") and hasattr(self, "per_page"):
            page = self.page
            per_page = self.per_page
        elif hasattr(self, "page"):
            page = self.page
            per_page = CONFIG.PAGINATION_PER_PAGE
        elif hasattr(self, "per_page"):
            page = 1
            per_page = self.per_page
        else:
            per_page = None
            page = None
        return page, per_page

    def parse_order_by_rule_parameter(self) -> str:
        field = None
        if hasattr(self, "order_by"):
            if self.order_by[0] == "-":
                return self.order_by[1:]
            else:
                return self.order_by
        return field
