"""
Type aliases.
"""
import typing

from . import duration as _duration
from . import ratio as _ratio

Duration: typing.TypeAlias = typing.Union[_duration.Duration, tuple[int, int]]

Offset: typing.TypeAlias = typing.Union[_duration.Offset, int, float, tuple[int, int]]

Pattern: typing.TypeAlias = typing.Union[
    tuple[typing.Sequence[int]], tuple[typing.Sequence[int], int]
]

Prototype: typing.TypeAlias = typing.Union[typing.Type | tuple[typing.Type, ...]]

Ratio: typing.TypeAlias = _duration.Duration | _ratio.Ratio | tuple[int, ...]

Strings: typing.TypeAlias = str | typing.Sequence[str]
