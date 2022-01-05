from typing import Optional

from fastapi import Query


class CommonQueryParams:
    def __init__(
            self,
            skip: Optional[int] = Query(description="skipの説明", default=0, ge=0, le=9999999),
            limit: Optional[int] = Query(description="limitの説明", default=100, ge=1, le=1000)):
        self.skip = skip
        self.limit = limit
