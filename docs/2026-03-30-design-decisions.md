# Design Decisions

## Summary

Documents the key design decisions, patterns, and trade-offs made in the
Carousell Marketplace CLI application, including SOLID principle mapping,
complexity analysis, and extensibility guidelines.

## Impacted Services

- marketplace (CLI application)

## Created

- Date: 2026-03-30
- Author: Tushar Wadhwani

## Last Modified

- Date: 2026-03-30
- Updated by: Tushar Wadhwani

---

## Design Patterns and SOLID Mapping

### 1. Command Pattern (Open/Closed Principle)

Each CLI command is a class implementing the `ICommand` ABC. A
`CommandRegistry` maps command names to handler instances.

**Why**: Adding a new command requires zero changes to existing code --
create a new class and register it. This directly satisfies the
Open/Closed Principle.

### 2. Repository Pattern (Dependency Inversion Principle)

`IUserRepository` and `IListingRepository` define abstract contracts.
`InMemoryUserRepository` and `InMemoryListingRepository` are the
concrete implementations.

**Why**: The service layer depends on abstractions, not implementations.
Swapping to a database backend (e.g., SQLite, PostgreSQL) requires only
a new repository class -- no service or command changes. Tests can inject
stub repositories for isolation.

### 3. Strategy Pattern (Open/Closed + Single Responsibility)

Sorting logic is encapsulated in `SortStrategy` subclasses
(`PriceSortStrategy`, `TimeSortStrategy`).

**Why**: Isolates sort logic from business logic. Adding a new sort
dimension (e.g., by title) is one new class. The `GET_CATEGORY` command
selects the strategy at runtime based on the sort argument.

### 4. Dependency Injection (Dependency Inversion Principle)

`MarketplaceService` receives repositories via constructor injection.
Commands receive the service via constructor injection.

**Why**: Full testability without mocking frameworks. Each component can
be instantiated with controlled dependencies.

### 5. Typed Exception Hierarchy (Liskov Substitution Principle)

`MarketplaceError` base with specific subclasses for each error condition.

**Why**: Commands catch specific exceptions and return exact error strings
from the spec. No brittle string matching. Any `MarketplaceError` can be
caught generically if needed.

## Complexity Analysis

| Operation         | Time Complexity | Notes                                  |
|-------------------|----------------|----------------------------------------|
| REGISTER          | O(1)           | Hash table insertion                   |
| CREATE_LISTING    | O(1)           | Hash table insertion + counter update  |
| DELETE_LISTING    | O(1)           | Hash table deletion + counter update   |
| GET_LISTING       | O(1)           | Hash table lookup                      |
| GET_CATEGORY      | O(n log n)     | n = listings in category (sorting)     |
| GET_TOP_CATEGORY  | O(k)           | k = distinct categories (counter scan) |

### GET_TOP_CATEGORY Optimization

The spec notes this is a "read heavy operation" suitable for home page use.
Instead of scanning all listings (O(n)), we maintain a `category_counts`
dictionary updated on every `CREATE_LISTING` (+1) and `DELETE_LISTING` (-1).
`GET_TOP_CATEGORY` simply finds the max in this dictionary -- O(k) where
k is the number of distinct categories (typically much smaller than n).

## Technical Decisions

### Immutable Models

`@dataclass(frozen=True)` is used for `User` and `Listing`. This prevents
accidental mutation and enables safe use as dictionary keys or set members.

### Type Hints

All function signatures, return types, and class attributes are annotated
using the `typing` module. This serves as documentation, enables static
analysis, and catches bugs early.

### Input Parsing

`shlex.split()` from the standard library correctly handles single-quoted
arguments like `'Phone model 8'` as required by the protocol. The
`InputParser` class wraps this for testability.

### Username Case Insensitivity

Usernames are stored with original case but normalized to lowercase for
lookups. This means "Alice" and "alice" are the same user, but the original
casing is preserved in output.

### Listing IDs

Auto-incremented from 100001 using `itertools.count`. IDs are never reused,
even after deletion.

### Price Storage

Stored as `int` rather than `float`. The spec examples use whole numbers,
and integer storage avoids floating-point formatting issues (e.g., 1000 vs
1000.0).

## Single-Class-Per-File Structure

Every module under `marketplace/` is a sub-package (folder) containing one
file per class, named in snake_case to match the class name (e.g.
`InMemoryUserRepository` → `in_memory_user_repository.py`).

**Why**:

- **Merge-conflict elimination**: Two engineers modifying different classes
  never touch the same file.
- **Navigability**: `ls marketplace/commands/` instantly lists every command
  the system supports.
- **Focused diffs**: A pull request changing `PriceSortStrategy` only shows
  changes to `price_sort_strategy.py`, not an unrelated 200-line file.
- **Backward-compatible imports**: Each `__init__.py` re-exports all public
  symbols, so `from marketplace.models import User` continues to work
  without consumers knowing about the internal file split.

## How to Add a New Command

To add a hypothetical `UPDATE_LISTING` command:

1. **Create the command file** at `marketplace/commands/update_listing_command.py`:

```python
class UpdateListingCommand(ICommand):
    def __init__(self, service: MarketplaceService) -> None:
        self._service = service

    def execute(self, args: List[str]) -> str:
        # Parse args and delegate to service
        ...
```

2. **Add the service method** in `marketplace/services/marketplace_service.py`:

```python
def update_listing(self, username: str, listing_id: int, ...) -> str:
    self._validate_user(username)
    # Business logic here
    ...
```

3. **Register the command** in `build_registry()` inside `command_registry.py`:

```python
registry.register("UPDATE_LISTING", UpdateListingCommand(service))
```

4. **Re-export** in `marketplace/commands/__init__.py`:

```python
from marketplace.commands.update_listing_command import UpdateListingCommand
```

No existing code needs to change. This is the Open/Closed Principle in action.
