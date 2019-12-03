"""
Utilities for typehinting.
"""

import typing

from abjad.mathtools import Ratio
from abjad.utilities.Duration import Duration
from abjad.utilities.Expression import Expression

IntegerPair = typing.Tuple[int, int]

IntegerSequence = typing.Sequence[int]

DurationTyping = typing.Union[Duration, IntegerPair]

DurationSequenceTyping = typing.Sequence[DurationTyping]

Number = typing.Union[int, float]

NumberPair = typing.Tuple[Number, Number]

PatternTyping = typing.Union[
    typing.Tuple[IntegerSequence], typing.Tuple[IntegerSequence, int]
]

Prototype = typing.Union[typing.Type, typing.Tuple[typing.Type, ...]]

RatioTyping = typing.Union[Duration, Ratio, typing.Tuple[int, ...]]

RatioSequenceTyping = typing.Sequence[RatioTyping]

SelectorTyping = Expression

Strings = typing.Union[str, typing.Sequence[str]]
