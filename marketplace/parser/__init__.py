"""Input parser for the marketplace CLI.

Uses ``shlex.split`` from the standard library to correctly handle
single-quoted arguments (e.g. 'Phone model 8') as required by the
marketplace protocol.
"""

from marketplace.parser.input_parser import InputParser

__all__ = ["InputParser"]
