# ID:CAROUSELL-001; feat: domain layer -- models, exceptions, and interfaces

## Changes
- `marketplace/__init__.py`: Package initialisation with version metadata.
- `marketplace/models/user.py`: Frozen dataclass representing a registered user.
- `marketplace/models/listing.py`: Frozen dataclass for marketplace listings with formatting helpers.
- `marketplace/exceptions/`: Typed exception hierarchy (`MarketplaceError` and five concrete sub-classes).
- `marketplace/interfaces/`: Abstract base classes defining `IUserRepository`, `IListingRepository`, and `ICommand` contracts.

## Intent
Establish the foundational domain vocabulary -- entities, error types, and contracts -- before any infrastructure or application logic is introduced.
