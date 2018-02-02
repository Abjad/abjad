from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Talea(AbjadValueObject):
    '''Talea.

    >>> from abjad.tools import rhythmmakertools as rhythmos

    ..  container:: example

        >>> talea = abjad.rhythmmakertools.Talea(
        ...     counts=[2, 1, 3, 2, 4, 1, 1],
        ...     denominator=16,
        ...     preamble=[1, 1, 1, 1],
        ...     )

        >>> abjad.f(talea)
        abjad.rhythmmakertools.Talea(
            counts=[2, 1, 3, 2, 4, 1, 1],
            denominator=16,
            preamble=[1, 1, 1, 1],
            )

    The medieval plural of 'talea' is 'talee'. Abjad documentation uses
    'taleas' instead.
    '''

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
        counts=(1,),
        denominator=16,
        preamble=None,
        ):
        import abjad
        assert all(isinstance(_, int) for _ in counts)
        self._counts = counts
        if not abjad.mathtools.is_nonnegative_integer_power_of_two(
            denominator):
            message = f'denominator {denominator} must be integer power of 2.'
            raise Exception(message)
        self._denominator = denominator
        if preamble is not None:
            assert all(isinstance(_, int) for _ in preamble), repr(preamble)
        self._preamble = preamble

    ### SPECIAL METHODS ###

    def __getitem__(self, argument):
        r'''Gets item or slice identified by `argument`.

        ..  container:: example

            Gets item at index:

            >>> talea = abjad.rhythmmakertools.Talea(
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

        Returns nonreduced fraction or nonreduced fractions.
        '''
        import abjad
        preamble = self.preamble or []
        counts = abjad.CyclicTuple(preamble + self.counts)
        if isinstance(argument, int):
            count = counts.__getitem__(argument)
            return abjad.NonreducedFraction(count, self.denominator)
        elif isinstance(argument, slice):
            counts = counts.__getitem__(argument)
            result = [
                abjad.NonreducedFraction(count, self.denominator)
                for count in counts
                ]
            return result
        raise ValueError(argument)

    def __iter__(self):
        r'''Iterates talea.

        ..  container:: example

            >>> talea = abjad.rhythmmakertools.Talea(
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

        Yields durations.
        '''
        import abjad
        for count in self.preamble or []:
            duration = abjad.Duration(count, self.denominator)
            yield duration
        for count in self.counts:
            duration = abjad.Duration(count, self.denominator)
            yield duration

    def __len__(self):
        r'''Gets length.

        ..  container:: example

            >>> talea = abjad.rhythmmakertools.Talea(
            ...     counts=[2, 1, 3, 2, 4, 1, 1],
            ...     denominator=16,
            ...     )

            >>> len(talea)
            7

        Defined equal to length of counts.

        Returns nonnegative integer.
        '''
        return len(self.counts)

    ### PUBLIC PROPERTIES ###

    @property
    def counts(self):
        r'''Gets counts.

        ..  container:: example

            >>> talea = abjad.rhythmmakertools.Talea(
            ...     counts=[2, 1, 3, 2, 4, 1, 1],
            ...     denominator=16,
            ...     )

            >>> talea.counts
            [2, 1, 3, 2, 4, 1, 1]

        Set to integers.

        Defaults to `[1]`.

        Returns list.
        '''
        if self._counts:
            return list(self._counts)

    @property
    def denominator(self):
        r'''Gets denominator.

        ..  container:: example

            >>> talea = abjad.rhythmmakertools.Talea(
            ...     counts=[2, 1, 3, 2, 4, 1, 1],
            ...     denominator=16,
            ...     )

            >>> talea.denominator
            16

        Set to nonnegative integer power of two.

        Defaults to 16.

        Returns nonnegative integer power of two.
        '''
        return self._denominator

    @property
    def preamble(self):
        r'''Gets preamble.
                    
        ..  container:: example

            >>> talea = abjad.rhythmmakertools.Talea(
            ...     counts=[2, 1, 3, 2, 4, 1, 1],
            ...     denominator=16,
            ...     preamble=[1, 1, 1, 1], 
            ...     )

            >>> talea.preamble
            [1, 1, 1, 1]

        Set to integers or none.

        Defaults to none.

        Returns list.
        '''
        if self._preamble:
            return list(self._preamble)

    ### PUBLIC METHODS ###

    def advance(self, weight):
        r'''Advances talea by `weight`.

        ..  container:: example

            >>> talea = abjad.rhythmmakertools.Talea(
            ...     counts=[2, 1, 3, 2, 4, 1, 1],
            ...     denominator=16,
            ...     preamble=[1, 1, 1, 1],
            ...     )

            >>> abjad.f(talea.advance(0))
            abjad.rhythmmakertools.Talea(
                counts=[2, 1, 3, 2, 4, 1, 1],
                denominator=16,
                preamble=[1, 1, 1, 1],
                )

            >>> abjad.f(talea.advance(1))
            abjad.rhythmmakertools.Talea(
                counts=[2, 1, 3, 2, 4, 1, 1],
                denominator=16,
                preamble=[1, 1, 1],
                )

            >>> abjad.f(talea.advance(2))
            abjad.rhythmmakertools.Talea(
                counts=[2, 1, 3, 2, 4, 1, 1],
                denominator=16,
                preamble=[1, 1],
                )

            >>> abjad.f(talea.advance(3))
            abjad.rhythmmakertools.Talea(
                counts=[2, 1, 3, 2, 4, 1, 1],
                denominator=16,
                preamble=[1],
                )

            >>> abjad.f(talea.advance(4))
            abjad.rhythmmakertools.Talea(
                counts=[2, 1, 3, 2, 4, 1, 1],
                denominator=16,
                )

            >>> abjad.f(talea.advance(5))
            abjad.rhythmmakertools.Talea(
                counts=[2, 1, 3, 2, 4, 1, 1],
                denominator=16,
                preamble=[1, 1, 3, 2, 4, 1, 1],
                )

            >>> abjad.f(talea.advance(6))
            abjad.rhythmmakertools.Talea(
                counts=[2, 1, 3, 2, 4, 1, 1],
                denominator=16,
                preamble=[1, 3, 2, 4, 1, 1],
                )

            >>> abjad.f(talea.advance(7))
            abjad.rhythmmakertools.Talea(
                counts=[2, 1, 3, 2, 4, 1, 1],
                denominator=16,
                preamble=[3, 2, 4, 1, 1],
                )

            >>> abjad.f(talea.advance(8))
            abjad.rhythmmakertools.Talea(
                counts=[2, 1, 3, 2, 4, 1, 1],
                denominator=16,
                preamble=[2, 2, 4, 1, 1],
                )

        '''
        import abjad
        assert isinstance(weight, int), repr(weight)
        if weight < 0:
            raise Exception(f'weight {weight} must be nonnegative.')
        if weight == 0:
            return abjad.new(self)
        preamble = abjad.sequence(self.preamble or ())
        talea = abjad.sequence(self.counts or ())
        if weight < preamble.weight():
            consumed, remaining = preamble.split([weight], overhang=True)
            preamble = remaining
        elif weight == preamble.weight():
            preamble = None
        else:
            assert preamble.weight() < weight
            weight -= preamble.weight()
            preamble = talea[:]
            while True:
                if weight <= preamble.weight():
                    break
                preamble += talea
            consumed, remaining = preamble.split([weight], overhang=True)
            preamble = remaining
        return abjad.new(
            self,
            counts=talea,
            denominator=self.denominator,
            preamble=preamble,
            )
