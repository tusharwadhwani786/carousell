# ID:CAROUSELL-002; feat: data and business logic layers

## Changes
- `marketplace/repositories/in_memory_user_repository.py`: In-memory implementation of `IUserRepository`.
- `marketplace/repositories/in_memory_listing_repository.py`: In-memory implementation of `IListingRepository` with auto-incrementing IDs and category counters.
- `marketplace/services/marketplace_service.py`: Core service orchestrating registration, listing CRUD, category queries, and top-category computation.
- `marketplace/sorting/sort_strategy.py`: Abstract sorting strategy interface.
- `marketplace/sorting/price_sort_strategy.py`: Sort listings by price (asc/desc).
- `marketplace/sorting/time_sort_strategy.py`: Sort listings by creation time (asc/desc).

## Intent
Implement the Repository and Strategy patterns to encapsulate data access and sorting behaviour, then wire them into a service layer that enforces all business rules.
