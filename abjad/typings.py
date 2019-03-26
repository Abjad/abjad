"""
Utilities for typehinting.
"""

import typing
from abjad.utilities.Duration import Duration
from abjad.utilities.Expression import Expression


IntegerPair = typing.Tuple[int, int]

DurationTyping = typing.Union[Duration, IntegerPair]

Number = typing.Union[int, float]

NumberPair = typing.Tuple[Number, Number]

Prototype = typing.Union[typing.Type, typing.Tuple[typing.Type, ...]]

Selector = typing.Union[str, Expression]

Strings = typing.Union[str, typing.Sequence[str]]
