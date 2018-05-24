import typing
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject
from abjad.tools.datastructuretools.CyclicTuple import CyclicTuple
from abjad.tools.datastructuretools.Duration import Duration
from abjad.tools.datastructuretools.Sequence import Sequence
from abjad.tools.mathtools.NonreducedFraction import NonreducedFraction
from abjad.tools.topleveltools.new import new
from abjad.tools import mathtools


class Talea(AbjadValueObject):
    """
    Talea.

    ..  container:: example

        >>> talea = abjad.rmakers.Talea(
        ...     counts=[2, 1, 3, 2, 4, 1, 1],
        ...     denominator=16,
        ...     preamble=[1, 1, 1, 1],
        ...     )

        >>> abjad.f(talea)
        abjad.rmakers.Talea(
            counts=[2, 1, 3, 2, 4, 1, 1],
            denominator=16,
            preamble=[1, 1, 1, 1],
            )

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_counts',
        '_denominator',
        '_preamble',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        counts: typing.Iterable[int] = (1,),
        denominator: int = 16,
        preamble: typing.List[int] = None,
        ) -> None:
        assert all(isinstance(_, int) for _ in counts)
        self._counts = counts
        if not mathtools.is_nonnegative_integer_power_of_two(denominator):
            message = f'denominator {denominator} must be integer power of 2.'
            raise Exception(message)
        self._denominator = denominator
        if preamble is not None:
            assert all(isinstance(_, int) for _ in preamble), repr(preamble)
        self._preamble = preamble

    ### SPECIAL METHODS ###

    def __contains__(self, argument: int) -> bool:
        """
        Is true when talea contains ``argument``.

        ..  container:: example

            With preamble:

            >>> talea = abjad.rmakers.Talea(
            ...     counts=[10],
            ...     denominator=16,
            ...     preamble=[1, -1, 1],
            ...     )

            >>> for i in range(1, 23 + 1):
            ...     i, i in talea
            ...
            (1, True)
            (2, True)
            (3, True)
            (4, False)
            (5, False)
            (6, False)
            (7, False)
            (8, False)
            (9, False)
            (10, False)
            (11, False)
            (12, False)
            (13, True)
            (14, False)
            (15, False)
            (16, False)
            (17, False)
            (18, False)
            (19, False)
            (20, False)
            (21, False)
            (22, False)
            (23, True)

        """
        assert isinstance(argument, int), repr(argument)
        assert 0 < argument, repr(argument)
        if self.preamble:
            preamble = Sequence([abs(_) for _ in self.preamble])
            cumulative = mathtools.cumulative_sums(preamble)[1:]
            if argument in cumulative:
                return True
            preamble_weight = preamble.weight()
        else:
            preamble_weight = 0
        if self.counts is not None:
            counts = [abs(_) for _ in self.counts]
        else:
            counts = []
        cumulative = mathtools.cumulative_sums(counts)[:-1]
        argument -= preamble_weight
        argument %= self.period
        return argument in cumulative
    
    def __getitem__(self, argument) -> typing.Union[
        NonreducedFraction, typing.List[NonreducedFraction]
        ]:
        """
        Gets item or slice identified by ``argument``.

        ..  container:: example

            Gets item at index:

            >>> talea = abjad.rmakers.Talea(
            ...     counts=[2, 1, 3, 2, 4, 1, 1],
            ...     denominator=16,
            ...     preamble=[1, 1, 1, 1],
            ...     )

            >>> talea[0]
            NonreducedFraction(1, 16)

            >>> talea[1]
            NonreducedFraction(1, 16)

        ..  container:: example

            Gets items in slice:

            >>> for duration in talea[:6]:
            ...     duration
            ...
            NonreducedFraction(1, 16)
            NonreducedFraction(1, 16)
            NonreducedFraction(1, 16)
            NonreducedFraction(1, 16)
            NonreducedFraction(2, 16)
            NonreducedFraction(1, 16)

            >>> for duration in talea[2:8]:
            ...     duration
            ...
            NonreducedFraction(1, 16)
            NonreducedFraction(1, 16)
            NonreducedFraction(2, 16)
            NonreducedFraction(1, 16)
            NonreducedFraction(3, 16)
            NonreducedFraction(2, 16)

        """
        if self.preamble:
            preamble = self.preamble
        else:
            preamble = []
        if self.counts:
            counts = self.counts
        else:
            counts = []
        counts_ = CyclicTuple(preamble + counts)
        if isinstance(argument, int):
            count = counts_.__getitem__(argument)
            return NonreducedFraction(count, self.denominator)
        elif isinstance(argument, slice):
            counts_ = counts_.__getitem__(argument)
            result = [
                NonreducedFraction(count, self.denominator)
                for count in counts_
                ]
            return result
        raise ValueError(argument)

    def __iter__(self) -> typing.Generator:
        """
        Iterates talea.

        ..  container:: example

            >>> talea = abjad.rmakers.Talea(
            ...     counts=[2, 1, 3, 2, 4, 1, 1],
            ...     denominator=16,
            ...     preamble=[1, 1, 1, 1],
            ...     )

            >>> for duration in talea:
            ...     duration
            ...
            Duration(1, 16)
            Duration(1, 16)
            Duration(1, 16)
            Duration(1, 16)
            Duration(1, 8)
            Duration(1, 16)
            Duration(3, 16)
            Duration(1, 8)
            Duration(1, 4)
            Duration(1, 16)
            Duration(1, 16)

        """
        for count in self.preamble or []:
            duration = Duration(count, self.denominator)
            yield duration
        for count in self.counts or []:
            duration = Duration(count, self.denominator)
            yield duration

    def __len__(self) -> int:
        """
        Gets length.

        ..  container:: example

            >>> talea = abjad.rmakers.Talea(
            ...     counts=[2, 1, 3, 2, 4, 1, 1],
            ...     denominator=16,
            ...     )

            >>> len(talea)
            7

        Defined equal to length of counts.
        """
        return len(self.counts or [])

    ### PUBLIC PROPERTIES ###

    @property
    def counts(self) -> typing.Optional[typing.List[int]]:
        """
        Gets counts.

        ..  container:: example

            >>> talea = abjad.rmakers.Talea(
            ...     counts=[2, 1, 3, 2, 4, 1, 1],
            ...     denominator=16,
            ...     )

            >>> talea.counts
            [2, 1, 3, 2, 4, 1, 1]

        """
        if self._counts:
            return list(self._counts)
        else:
            return None

    @property
    def denominator(self) -> int:
        """
        Gets denominator.

        ..  container:: example

            >>> talea = abjad.rmakers.Talea(
            ...     counts=[2, 1, 3, 2, 4, 1, 1],
            ...     denominator=16,
            ...     )

            >>> talea.denominator
            16

        Set to nonnegative integer power of two.

        Defaults to 16.
        """
        return self._denominator

    @property
    def period(self) -> int:
        """
        Gets period of talea.

        ..  container:: example

            Equal to weight of counts:

            >>> talea = abjad.rmakers.Talea(
            ...     counts=[1, 2, 3, 4],
            ...     denominator=16,
            ...     )

            >>> talea.period
            10

            Rests make no difference:

            >>> talea = abjad.rmakers.Talea(
            ...     counts=[1, 2, -3, 4],
            ...     denominator=16,
            ...     )

            >>> talea.period
            10

            Denominator makes no difference:

            >>> talea = abjad.rmakers.Talea(
            ...     counts=[1, 2, -3, 4],
            ...     denominator=32,
            ...     )

            >>> talea.period
            10

            Preamble makes no difference:

            >>> talea = abjad.rmakers.Talea(
            ...     counts=[1, 2, -3, 4],
            ...     denominator=32,
            ...     preamble=[1, 1, 1],
            ...     )

            >>> talea.period
            10

        """
        return Sequence(self.counts).weight()

    @property
    def preamble(self) -> typing.Optional[typing.List[int]]:
        """
        Gets preamble.
                    
        ..  container:: example

            >>> talea = abjad.rmakers.Talea(
            ...     counts=[2, 1, 3, 2, 4, 1, 1],
            ...     denominator=16,
            ...     preamble=[1, 1, 1, 1], 
            ...     )

            >>> talea.preamble
            [1, 1, 1, 1]

        ..  container:: example

            >>> talea = abjad.rmakers.Talea(
            ...     counts=[16, -4, 16],
            ...     denominator=16,
            ...     preamble=[1],
            ...     )

            >>> for i, duration in enumerate(talea):
            ...     duration
            ...
            Duration(1, 16)
            Duration(1, 1)
            Duration(-1, 4)
            Duration(1, 1)

        """
        if self._preamble:
            return list(self._preamble)
        else:
            return None

    ### PUBLIC METHODS ###

    def advance(self, weight: int) -> 'Talea':
        """
        Advances talea by ``weight``.

        ..  container:: example

            >>> talea = abjad.rmakers.Talea(
            ...     counts=[2, 1, 3, 2, 4, 1, 1],
            ...     denominator=16,
            ...     preamble=[1, 1, 1, 1],
            ...     )

            >>> abjad.f(talea.advance(0))
            abjad.rmakers.Talea(
                counts=[2, 1, 3, 2, 4, 1, 1],
                denominator=16,
                preamble=[1, 1, 1, 1],
                )

            >>> abjad.f(talea.advance(1))
            abjad.rmakers.Talea(
                counts=[2, 1, 3, 2, 4, 1, 1],
                denominator=16,
                preamble=[1, 1, 1],
                )

            >>> abjad.f(talea.advance(2))
            abjad.rmakers.Talea(
                counts=[2, 1, 3, 2, 4, 1, 1],
                denominator=16,
                preamble=[1, 1],
                )

            >>> abjad.f(talea.advance(3))
            abjad.rmakers.Talea(
                counts=[2, 1, 3, 2, 4, 1, 1],
                denominator=16,
                preamble=[1],
                )

            >>> abjad.f(talea.advance(4))
            abjad.rmakers.Talea(
                counts=[2, 1, 3, 2, 4, 1, 1],
                denominator=16,
                )

            >>> abjad.f(talea.advance(5))
            abjad.rmakers.Talea(
                counts=[2, 1, 3, 2, 4, 1, 1],
                denominator=16,
                preamble=[1, 1, 3, 2, 4, 1, 1],
                )

            >>> abjad.f(talea.advance(6))
            abjad.rmakers.Talea(
                counts=[2, 1, 3, 2, 4, 1, 1],
                denominator=16,
                preamble=[1, 3, 2, 4, 1, 1],
                )

            >>> abjad.f(talea.advance(7))
            abjad.rmakers.Talea(
                counts=[2, 1, 3, 2, 4, 1, 1],
                denominator=16,
                preamble=[3, 2, 4, 1, 1],
                )

            >>> abjad.f(talea.advance(8))
            abjad.rmakers.Talea(
                counts=[2, 1, 3, 2, 4, 1, 1],
                denominator=16,
                preamble=[2, 2, 4, 1, 1],
                )

        ..  container:: example

            REGRESSION. Works when talea advances by period of talea:

            >>> talea = abjad.rmakers.Talea(
            ...     counts=[1, 2, 3, 4],
            ...     denominator=16,
            ...     )

            >>> abjad.f(talea.advance(10))
            abjad.rmakers.Talea(
                counts=[1, 2, 3, 4],
                denominator=16,
                )

            >>> abjad.f(talea.advance(20))
            abjad.rmakers.Talea(
                counts=[1, 2, 3, 4],
                denominator=16,
                )

        """
        assert isinstance(weight, int), repr(weight)
        if weight < 0:
            raise Exception(f'weight {weight} must be nonnegative.')
        if weight == 0:
            return new(self)
        preamble = Sequence(self.preamble or ())
        counts = Sequence(self.counts or ())
        preamble_: typing.Optional[Sequence]
        if weight < preamble.weight():
            consumed, remaining = preamble.split([weight], overhang=True)
            preamble_ = remaining
        elif weight == preamble.weight():
            preamble_ = None
        else:
            assert preamble.weight() < weight
            weight -= preamble.weight()
            preamble = counts[:]
            while True:
                if weight <= preamble.weight():
                    break
                preamble += counts
            if preamble.weight() == weight:
                consumed, remaining = preamble[:], None
            else:
                consumed, remaining = preamble.split([weight], overhang=True)
            preamble_ = remaining
        return new(
            self,
            counts=counts,
            denominator=self.denominator,
            preamble=preamble_,
            )
