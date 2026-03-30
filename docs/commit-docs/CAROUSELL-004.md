# ID:CAROUSELL-004; test: comprehensive unit and integration test suite

## Changes
- `tests/test_models.py`: Unit tests for `User` and `Listing` dataclass behaviour and formatting.
- `tests/test_exceptions.py`: Unit tests for the custom exception hierarchy.
- `tests/test_repositories.py`: Unit tests for in-memory repository semantics and category counters.
- `tests/test_sorting.py`: Unit tests for price and time sorting strategies.
- `tests/test_services.py`: Unit tests for `MarketplaceService` business rules and edge cases.
- `tests/test_commands.py`: Unit tests for individual commands and registry dispatch.
- `tests/test_integration.py`: End-to-end tests exercising the full REPL via `main()` with piped input.

## Intent
Lock in behaviour across every layer and guard against regressions with 103 tests covering happy paths, error cases, and boundary conditions.
