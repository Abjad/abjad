import typing
from abjad.mathtools.Infinity import Infinity
from abjad.mathtools.NegativeInfinity import NegativeInfinity


Infinities = typing.Union[Infinity, NegativeInfinity]

IntegerPair = typing.Tuple[int, int]

Number = typing.Union[int, float]

NumberPair = typing.Tuple[Number, Number]
