# Carousell Marketplace CLI

A command-line marketplace application supporting user registration, listing
management, category queries, and top-category lookup. Built with clean
layered architecture and SOLID design principles.

## Requirements

- **Python 3.7+** (uses dataclasses, f-strings; tested with Python 3.8)
- Standard library only -- no external dependencies

### Debian 9 Setup

Debian 9 (stretch) ships Python 3.5.3 by default. Python 3.7+ is required.
To install on Debian 9:

```bash
sudo apt-get update
sudo apt-get install -y build-essential libffi-dev libssl-dev zlib1g-dev
wget https://www.python.org/ftp/python/3.8.12/Python-3.8.12.tgz
tar xzf Python-3.8.12.tgz
cd Python-3.8.12
./configure --enable-optimizations
make -j$(nproc)
sudo make altinstall
```

After installation, `python3.8` will be available. Update the `run.sh` and
`build.sh` scripts to use `python3.8` instead of `python3` if the default
`python3` still points to 3.5.

## Quick Start

```bash
# Build (validates Python 3 and runs syntax check)
make build

# Run the interactive marketplace
make run

# Run the full test suite (103 tests)
make test
```

### Manual Execution

```bash
# Build
./build.sh

# Run
./run.sh

# Run tests
python3 -m unittest discover -s tests -v
```

### Piped Input

Commands can be piped via STDIN:

```bash
echo "REGISTER user1
CREATE_LISTING user1 'Phone model 8' 'Black color, brand new' 1000 'Electronics'
GET_LISTING user1 100001
GET_TOP_CATEGORY user1" | python3 main.py
```

## Supported Commands

| Command | Syntax | Description |
|---------|--------|-------------|
| REGISTER | `REGISTER <username>` | Register a new user |
| CREATE_LISTING | `CREATE_LISTING <username> <title> <description> <price> <category>` | Create a listing |
| DELETE_LISTING | `DELETE_LISTING <username> <listing_id>` | Delete a listing (owner only) |
| GET_LISTING | `GET_LISTING <username> <listing_id>` | View any listing's details |
| GET_CATEGORY | `GET_CATEGORY <username> <category> <sort_key> <sort_order>` | List all items in a category |
| GET_TOP_CATEGORY | `GET_TOP_CATEGORY <username>` | Get the category with most listings |

**Sort keys**: `sort_price`, `sort_time`
**Sort orders**: `asc`, `dsc`

## Example Session

```
# REGISTER user1
Success
# CREATE_LISTING user1 'Phone model 8' 'Black color, brand new' 1000 'Electronics'
100001
# GET_LISTING user1 100001
Phone model 8|Black color, brand new|1000|2026-03-30 10:30:00|Electronics|user1
# CREATE_LISTING user1 'Black shoes' 'Training shoes' 100 'Sports'
100002
# REGISTER user2
Success
# CREATE_LISTING user2 'T-shirt' 'White color' 20 'Sports'
100003
# GET_CATEGORY user1 'Sports' sort_price dsc
Black shoes|Training shoes|100|2026-03-30 10:30:01|Sports|user1
T-shirt|White color|20|2026-03-30 10:30:02|Sports|user2
# GET_TOP_CATEGORY user1
Sports
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                        │
│  main.py (REPL)  ──►  parser/ (shlex tokenizer)            │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              Application Layer (Command Pattern)             │
│  CommandRegistry                                            │
│    ├── RegisterCommand                                      │
│    ├── CreateListingCommand                                 │
│    ├── DeleteListingCommand                                 │
│    ├── GetListingCommand                                    │
│    ├── GetCategoryCommand                                   │
│    └── GetTopCategoryCommand                                │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                 Domain / Service Layer                        │
│  MarketplaceService                                          │
│    └── uses SortStrategy (Strategy Pattern)                  │
│         ├── PriceSortStrategy                                │
│         └── TimeSortStrategy                                 │
└──────────┬────────────────────────────┬─────────────────────┘
           │                            │
           ▼                            ▼
┌─────────────────────────┐  ┌─────────────────────────────┐
│  IUserRepository (ABC)  │  │  IListingRepository (ABC)   │
│    ▲                    │  │    ▲                        │
│    │                    │  │    │                        │
│  InMemoryUserRepository │  │  InMemoryListingRepository  │
└─────────────────────────┘  └─────────────────────────────┘
           │                            │
           ▼                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Domain Models                           │
│  User (frozen dataclass)    Listing (frozen dataclass)       │
└─────────────────────────────────────────────────────────────┘
```

### Design Patterns

- **Command Pattern**: Each command is a class implementing `ICommand` ABC.
  Adding a new command = one new class + one registry line.
- **Repository Pattern**: Abstract interfaces decouple storage from business
  logic. Swap in-memory for a database with zero service-layer changes.
- **Strategy Pattern**: Sort logic is isolated into strategy classes.
  Adding a new sort dimension = one new strategy class.
- **Dependency Injection**: Repositories are injected into the service;
  the service is injected into commands. Fully testable.
- **Typed Exception Hierarchy**: Domain-specific exceptions for each error
  condition, avoiding brittle string matching.

### Complexity Analysis

| Operation         | Time     | Notes                                   |
|-------------------|----------|-----------------------------------------|
| REGISTER          | O(1)     | Hash table insertion                    |
| CREATE_LISTING    | O(1)     | Hash table insertion + counter update   |
| DELETE_LISTING    | O(1)     | Hash table deletion + counter update    |
| GET_LISTING       | O(1)     | Hash table lookup                       |
| GET_CATEGORY      | O(n log n) | n = listings in category (sorting)    |
| GET_TOP_CATEGORY  | O(k)     | k = distinct categories (optimized)     |

## Project Structure

The `marketplace/` package uses a **single-class-per-file** layout: each
module is a sub-package (folder) containing one file per class, with an
`__init__.py` that re-exports all public symbols. This eliminates merge
conflicts when multiple developers work on different classes, makes every
abstraction instantly locatable by filename, and keeps diffs focused on
exactly one responsibility.

```
.
├── main.py                          # Entry point: REPL
├── build.sh                         # Build script (root-level)
├── run.sh                           # Run script (root-level)
├── Makefile                         # Build/run/test targets
├── README.md                        # This file
├── marketplace/
│   ├── __init__.py                  # Package metadata
│   ├── models/
│   │   ├── __init__.py              # Re-exports User, Listing
│   │   ├── user.py                  # User dataclass
│   │   └── listing.py               # Listing dataclass
│   ├── exceptions/
│   │   ├── __init__.py              # Re-exports all exception classes
│   │   ├── marketplace_error.py     # MarketplaceError (base)
│   │   ├── user_already_exists_error.py
│   │   ├── unknown_user_error.py
│   │   ├── listing_not_found_error.py
│   │   ├── listing_owner_mismatch_error.py
│   │   └── category_not_found_error.py
│   ├── interfaces/
│   │   ├── __init__.py              # Re-exports all ABCs
│   │   ├── i_user_repository.py     # IUserRepository ABC
│   │   ├── i_listing_repository.py  # IListingRepository ABC
│   │   └── i_command.py             # ICommand ABC
│   ├── repositories/
│   │   ├── __init__.py              # Re-exports both repositories
│   │   ├── in_memory_user_repository.py
│   │   └── in_memory_listing_repository.py
│   ├── sorting/
│   │   ├── __init__.py              # Re-exports + SORT_STRATEGIES registry
│   │   ├── sort_strategy.py         # SortStrategy ABC
│   │   ├── price_sort_strategy.py   # PriceSortStrategy
│   │   └── time_sort_strategy.py    # TimeSortStrategy
│   ├── services/
│   │   ├── __init__.py              # Re-exports MarketplaceService
│   │   └── marketplace_service.py   # Core business logic
│   ├── commands/
│   │   ├── __init__.py              # Re-exports all commands + registry
│   │   ├── register_command.py
│   │   ├── create_listing_command.py
│   │   ├── delete_listing_command.py
│   │   ├── get_listing_command.py
│   │   ├── get_category_command.py
│   │   ├── get_top_category_command.py
│   │   └── command_registry.py      # CommandRegistry + build_registry()
│   └── parser/
│       ├── __init__.py              # Re-exports InputParser
│       └── input_parser.py          # shlex-based tokenizer
├── tests/
│   ├── test_models.py               # Model tests
│   ├── test_exceptions.py           # Exception hierarchy tests
│   ├── test_repositories.py         # Repository tests
│   ├── test_sorting.py              # Sort strategy tests
│   ├── test_services.py             # Service layer tests
│   ├── test_commands.py             # Command + parser tests
│   └── test_integration.py          # End-to-end tests
├── docs/
│   ├── 2026-03-30-architecture.md   # Architecture overview
│   └── 2026-03-30-design-decisions.md # Design rationale
└── screenshots/                     # Terminal output captures
```

## Test Suite

103 tests covering:

- **Models**: Construction, immutability, output formatting
- **Exceptions**: Hierarchy, attributes, messages
- **Repositories**: CRUD, case-insensitive lookup, ID generation, category counters
- **Sorting**: All 4 sort combinations, edge cases
- **Services**: Every happy path and error path for all 6 operations
- **Commands**: Argument parsing, error translation, output formatting
- **Integration**: Full spec example replay, edge cases

## Further Documentation

All supplementary documentation lives in the `docs/` folder.

### Design & Architecture

| Document | Description |
|----------|-------------|
| [Architecture Overview](docs/2026-03-30-architecture.md) | Layered architecture diagram, data flow walkthrough, and key design properties |
| [Design Decisions](docs/2026-03-30-design-decisions.md) | Pattern rationale, SOLID mapping, complexity analysis, and extensibility guide |

### Commit Documentation

Per-commit change logs are in `docs/commit-docs/`, one file per commit:

| Document | Description |
|----------|-------------|
| [CAROUSELL-001](docs/commit-docs/CAROUSELL-001.md) | Domain layer -- models, exceptions, and interface contracts |
| [CAROUSELL-002](docs/commit-docs/CAROUSELL-002.md) | Data and business logic layers (repositories, service, sorting) |
| [CAROUSELL-003](docs/commit-docs/CAROUSELL-003.md) | CLI layer -- commands, parser, and REPL entry point |
| [CAROUSELL-004](docs/commit-docs/CAROUSELL-004.md) | Comprehensive unit and integration test suite (103 tests) |
| [CAROUSELL-005](docs/commit-docs/CAROUSELL-005.md) | Project documentation, build tooling, and screenshots |

### Screenshots

Terminal output captures are in the `screenshots/` folder:

| File | Description |
|------|-------------|
| [01-spec-example.txt](screenshots/01-spec-example.txt) | Full spec example run -- all 18 commands piped through `./run.sh` with expected output |
| [02-test-suite.txt](screenshots/02-test-suite.txt) | Complete test suite run -- 103 tests passing across all layers |
| [03-build.txt](screenshots/03-build.txt) | Build script execution -- Python version check and syntax validation |
