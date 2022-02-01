"""
Utilities for typehinting.
"""
import typing

from . import duration as _duration
from . import ratio as _ratio

IntegerPair = typing.Tuple[int, int]

IntegerSequence = typing.Sequence[int]

DurationTyping = typing.Union[_duration.Duration, IntegerPair]

DurationSequenceTyping = typing.Sequence[DurationTyping]

Number = typing.Union[int, float]

NumberPair = typing.Tuple[Number, Number]

PatternTyping = typing.Union[
    typing.Tuple[IntegerSequence], typing.Tuple[IntegerSequence, int]
]

Prototype = typing.Union[typing.Type, typing.Tuple[typing.Type, ...]]

RatioTyping = typing.Union[_duration.Duration, _ratio.Ratio, typing.Tuple[int, ...]]

RatioSequenceTyping = typing.Sequence[RatioTyping]

Strings = typing.Union[str, typing.Sequence[str]]
