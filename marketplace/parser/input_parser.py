"""Input parser for the marketplace CLI."""

import shlex
from typing import List, Tuple


class InputParser:
    """Tokenizes a raw CLI input line into command name and arguments.

    Uses ``shlex.split`` from the standard library to correctly handle
    single-quoted arguments (e.g. 'Phone model 8') as required by the
    marketplace protocol.

    Example:
        >>> parser = InputParser()
        >>> parser.parse("CREATE_LISTING user1 'Phone model 8' 'desc' 1000 'Electronics'")
        ('CREATE_LISTING', ['user1', 'Phone model 8', 'desc', '1000', 'Electronics'])
    """

    @staticmethod
    def parse(line: str) -> Tuple[str, List[str]]:
        """Parse a raw input line into (command_name, args).

        Args:
            line: The raw string from STDIN (prompt already stripped).

        Returns:
            A tuple of (command_name, list_of_arguments).

        Raises:
            ValueError: If the line is empty or cannot be tokenized.
        """
        tokens = shlex.split(line)
        if not tokens:
            raise ValueError("Empty command")
        return tokens[0], tokens[1:]
