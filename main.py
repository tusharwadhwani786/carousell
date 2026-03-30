"""
Carousell Marketplace CLI -- entry point.

Runs an interactive REPL that accepts marketplace commands on STDIN
and prints results to STDOUT. Handles EOF (Ctrl-D) and keyboard
interrupt (Ctrl-C) gracefully.
"""

import sys

from marketplace.commands import build_registry
from marketplace.parser import InputParser
from marketplace.repositories import (
    InMemoryListingRepository,
    InMemoryUserRepository,
)
from marketplace.services import MarketplaceService


def main() -> None:
    """Run the marketplace interactive REPL.

    Wires up the dependency graph (repositories -> service -> commands ->
    registry) and enters a read-eval-print loop. Each iteration:

    1. Prints the ``# `` prompt (only in interactive/TTY mode).
    2. Reads one line from STDIN.
    3. Parses the line into a command name and arguments.
    4. Dispatches to the matching command handler.
    5. Prints the result to STDOUT.

    The prompt is suppressed when STDIN is piped so that automated
    evaluation can diff the output directly against expected results.

    The loop exits gracefully on EOF (Ctrl-D) or KeyboardInterrupt (Ctrl-C).
    Malformed input is caught and reported as ``Error - invalid command``.
    """
    user_repo = InMemoryUserRepository()
    listing_repo = InMemoryListingRepository()
    service = MarketplaceService(user_repo, listing_repo)
    registry = build_registry(service)
    parser = InputParser()
    interactive = sys.stdin.isatty()

    while True:
        try:
            if interactive:
                sys.stdout.write("# ")
                sys.stdout.flush()
            line = sys.stdin.readline()

            if not line:
                break

            line = line.strip()
            if not line:
                continue

            command_name, args = parser.parse(line)
            result = registry.dispatch(command_name, args)
            print(result)

        except KeyboardInterrupt:
            print()
            break
        except EOFError:
            break
        except (ValueError, KeyError, IndexError):
            print("Error - invalid command")


if __name__ == "__main__":
    main()
