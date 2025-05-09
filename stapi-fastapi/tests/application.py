from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from stapi_fastapi.conformance import API
from stapi_fastapi.routers.root_router import RootRouter

from tests.backends import (
    mock_get_opportunity_search_record,
    mock_get_opportunity_search_records,
    mock_get_order,
    mock_get_order_statuses,
    mock_get_orders,
)
from tests.shared import (
    InMemoryOpportunityDB,
    InMemoryOrderDB,
    product_test_satellite_provider_sync_opportunity,
    product_test_spotlight_sync_opportunity,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[dict[str, Any]]:
    try:
        yield {"_orders_db": InMemoryOrderDB(), "_opportunities_db": InMemoryOpportunityDB(), "_opportunities": []}
    finally:
        pass


root_router = RootRouter(
    get_orders=mock_get_orders,
    get_order=mock_get_order,
    get_order_statuses=mock_get_order_statuses,
    get_opportunity_search_records=mock_get_opportunity_search_records,
    get_opportunity_search_record=mock_get_opportunity_search_record,
    conformances=[API.core],
)
root_router.add_product(product_test_spotlight_sync_opportunity)
root_router.add_product(product_test_satellite_provider_sync_opportunity)
app: FastAPI = FastAPI(lifespan=lifespan)
app.include_router(root_router, prefix="")
