"""
Utilities for typehinting.
"""
import typing

from . import duration as _duration
from . import ratio as _ratio

IntegerPair: typing.TypeAlias = tuple[int, int]

IntegerSequence: typing.TypeAlias = typing.Sequence[int]

DurationTyping: typing.TypeAlias = _duration.Duration | IntegerPair

DurationSequenceTyping: typing.TypeAlias = typing.Sequence[DurationTyping]

Number: typing.TypeAlias = int | float

NumberPair: typing.TypeAlias = tuple[Number, Number]

PatternTyping: typing.TypeAlias = typing.Union[
    tuple[IntegerSequence], tuple[IntegerSequence, int]
]

Prototype: typing.TypeAlias = typing.Union[typing.Type | tuple[typing.Type, ...]]

RatioTyping: typing.TypeAlias = _duration.Duration | _ratio.Ratio | tuple[int, ...]

RatioSequenceTyping: typing.TypeAlias = typing.Sequence[RatioTyping]

Strings: typing.TypeAlias = str | typing.Sequence[str]
