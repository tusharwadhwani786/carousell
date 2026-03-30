"""Marketplace service -- the business logic layer.

MarketplaceService orchestrates all domain operations by coordinating
between repositories and sorting strategies. It depends only on the
abstract interfaces (IUserRepository, IListingRepository), enabling
easy testing with stubs and future persistence swaps.
"""

from marketplace.services.marketplace_service import MarketplaceService

__all__ = ["MarketplaceService"]
