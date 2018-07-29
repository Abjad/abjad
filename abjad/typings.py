"""
Utilities for typehinting.
"""

import typing
from abjad.utilities.Expression import Expression


IntegerPair = typing.Tuple[int, int]

Number = typing.Union[int, float]

NumberPair = typing.Tuple[Number, Number]

Selector = typing.Union[str, Expression]
