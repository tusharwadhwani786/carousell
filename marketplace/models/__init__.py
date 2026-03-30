"""Domain models for the Carousell Marketplace.

Contains immutable value objects representing the core entities:
User and Listing. All models use frozen dataclasses to enforce
immutability and value semantics.
"""

from marketplace.models.listing import Listing
from marketplace.models.user import User

__all__ = ["User", "Listing"]
