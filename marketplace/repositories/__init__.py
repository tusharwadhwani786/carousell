"""In-memory repository implementations for the Carousell Marketplace.

These concrete classes implement the repository interfaces using
plain Python data structures. The design makes it straightforward
to substitute a database-backed implementation without changing
the service or command layers.
"""

from marketplace.repositories.in_memory_listing_repository import (
    InMemoryListingRepository,
)
from marketplace.repositories.in_memory_user_repository import (
    InMemoryUserRepository,
)

__all__ = ["InMemoryUserRepository", "InMemoryListingRepository"]
