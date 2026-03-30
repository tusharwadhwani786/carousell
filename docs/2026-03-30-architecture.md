# Architecture Overview

## Summary

This document describes the layered architecture of the Carousell Marketplace
CLI application. The system follows a clean separation of concerns across
four layers: Presentation, Application, Domain/Service, and Data Access.

## Impacted Services

- marketplace (CLI application)

## Created

- Date: 2026-03-30
- Author: Tushar Wadhwani

## Last Modified

- Date: 2026-03-30
- Updated by: Tushar Wadhwani

---

## Layered Architecture

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

## Data Flow

1. **Input**: `main.py` reads a line from STDIN (with `# ` prompt).
2. **Parsing**: `InputParser` uses `shlex.split()` to tokenize the line,
   handling quoted strings correctly.
3. **Dispatch**: `CommandRegistry` looks up the command name and delegates
   to the appropriate `ICommand` implementation.
4. **Business Logic**: The command calls the relevant `MarketplaceService`
   method, which validates the user, performs the operation, and returns
   a result or raises a typed exception.
5. **Output**: The command catches any exceptions and returns the
   appropriate error string, or the successful result. `main.py` prints
   the result to STDOUT.

## Key Design Properties

- **Extensibility**: Adding a new command requires only a new `ICommand`
  class and one `registry.register()` call.
- **Testability**: Every layer can be tested independently. Services accept
  repository interfaces via constructor injection.
- **Separation of Concerns**: Parsing, command routing, business logic,
  and data storage are each isolated in their own sub-package.
- **Single-Class-Per-File**: Each sub-package under `marketplace/` places
  one class per file, named in snake_case to match the class. This
  eliminates merge conflicts between developers working on different
  classes, makes every abstraction instantly locatable, and keeps diffs
  focused on exactly one responsibility. Re-exporting `__init__.py` files
  preserve clean package-level imports (e.g. `from marketplace.models import User`).
