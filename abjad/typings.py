"""
Utilities for typehinting.
"""

import typing
from abjad.utilities.Expression import Expression


IntegerPair = typing.Tuple[int, int]

Number = typing.Union[int, float]

NumberPair = typing.Tuple[Number, Number]

Prototype = typing.Union[typing.Type, typing.Tuple[typing.Type, ...]]

Selector = typing.Union[str, Expression]
