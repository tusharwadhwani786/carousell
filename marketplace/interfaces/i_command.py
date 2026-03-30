"""Abstract interface for marketplace CLI commands."""

from abc import ABC, abstractmethod
from typing import List


class ICommand(ABC):
    """Interface for all marketplace CLI commands.

    Each concrete command parses its arguments, delegates to the
    service layer, and returns a string response for STDOUT.
    """

    @abstractmethod
    def execute(self, args: List[str]) -> str:
        """Execute the command with the given arguments.

        Args:
            args: Tokenized arguments from the CLI input
                  (command name already stripped).

        Returns:
            The string to print to STDOUT.
        """
