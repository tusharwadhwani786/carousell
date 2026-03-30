# ID:CAROUSELL-003; feat: CLI layer -- commands, parser, and REPL

## Changes
- `marketplace/commands/`: Six concrete `ICommand` implementations (register, create/delete/get listing, get category, get top category) plus `CommandRegistry` and `build_registry` factory.
- `marketplace/parser/input_parser.py`: Tokenises raw input lines using `shlex.split`, handling quoted strings.
- `main.py`: REPL entry point with conditional prompt display (`sys.stdin.isatty()`), graceful EOF/interrupt handling, and dependency wiring.

## Intent
Complete the application by connecting the domain and service layers to a user-facing CLI through the Command pattern and a lightweight input parser.
