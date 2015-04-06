# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.abctools import AbjadValueObject


class BooleanPattern(AbjadValueObject):
    r'''Output mask.

    ..  container:: example

        ::

            >>> mask = rhythmmakertools.BooleanPattern(
            ...     indices=[0, 1, 7],
            ...     period=16,
            ...     )

        ::

            >>> print(format(mask))
            rhythmmakertools.BooleanPattern(
                indices=(0, 1, 7),
                period=16,
                )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_indices',
        '_invert',
        '_period',
        '_start',
        '_stop',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        indices=None,
        invert=None,
        period=None,
        start=None,
        stop=None,
        ):
        if indices is not None:
            assert all(isinstance(_, int) for _ in indices), repr(indices)
            indices = tuple(indices)
        self._indices = indices
        if invert is not None:
            invert = bool(invert)
        self._invert = invert
        if period is not None:
            assert mathtools.is_positive_integer(period), repr(period)
        self._period = period
        if start is not None:
            start = int(start)
        self._start = start
        if stop is not None:
            stop = int(stop)
        self._stop = stop

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        from ide import idetools
        return systemtools.AttributeManifest(
            systemtools.AttributeDetail(
                name='indices',
                command='i',
                editor=idetools.getters.get_integers,
                ),
            systemtools.AttributeDetail(
                name='period',
                command='p',
                editor=idetools.getters.get_integer,
                ),
            )

    ### PRIVATE METHODS ###

    def _matches_index(self, index, total_length, seed=None):
        assert 0 <= total_length
        if 0 <= index:
            nonnegative_index = index
        else:
            nonnegative_index = total_length - abs(index)
        invert = bool(self.invert)
        if self.start is not None or self.stop is not None:
            start, stop, _ = slice(self.start, self.stop).indices(total_length)
            if stop <= start:
                return False
            if self.start is not None and nonnegative_index < start:
                return False
            if self.stop is not None and stop <= nonnegative_index:
                return False
            nonnegative_index -= start
        if self.period is None:
            for index in self.indices:
                if index < 0:
                    index = total_length - abs(index)
                if index == nonnegative_index and index < total_length:
                    return True ^ invert
        else:
            if seed is not None:
                nonnegative_index += seed
            nonnegative_index = nonnegative_index % self.period
            for index in self.indices:
                if index < 0:
                    index = total_length - abs(index)
                    index = index % self.period
                if index == nonnegative_index and index < total_length:
                    return True ^ invert
        return False ^ invert

    ### PUBLIC METHODS ###

    @classmethod
    def from_sequence(cls, sequence):
        r'''Creates a boolean pattern from a sequence.

        ..  container:: example

            ::

                >>> mask = [1, 0, 0, 1, 1]
                >>> mask = rhythmmakertools.BooleanPattern.from_sequence(mask)
                >>> print(format(mask))
                rhythmmakertools.BooleanPattern(
                    indices=(0, 3, 4),
                    period=5,
                    )

        Returns boolean sequence.
        '''
        sequence = [bool(_) for _ in sequence]
        period = len(sequence)
        indices = [i for i, x in enumerate(sequence) if x]
        return cls(
            period=period,
            indices=indices,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def indices(self):
        r'''Gets indices of ouput mask.

        ..  container:: example

            ::

                >>> mask = rhythmmakertools.BooleanPattern(
                ...     indices=[0, 1, 7],
                ...     period=16,
                ...     )

            ::

                >>> mask.indices
                (0, 1, 7)

        Set to integers or none.
        '''
        return self._indices

    @property
    def invert(self):
        r'''Gets inversion flag of ouput mask.

        ..  container:: example

            ::

                >>> mask = rhythmmakertools.BooleanPattern(
                ...     indices=[0, 1, 7],
                ...     period=16,
                ...     invert=True
                ...     )

            ::

                >>> mask.invert
                True

        Set to boolean or none.
        '''
        return self._invert

    @property
    def period(self):
        r'''Gets period of ouput mask.

        ..  container:: example

            ::

                >>> mask = rhythmmakertools.BooleanPattern(
                ...     indices=[0, 1, 7],
                ...     period=16,
                ...     )

            ::

                >>> mask.period
                16

        Set to positive integer or none.
        '''
        return self._period

    @property
    def start(self):
        r'''Gets start index of ouput mask.

        ..  container:: example

            ::

                >>> mask = rhythmmakertools.BooleanPattern(
                ...     indices=[0, 1, 7],
                ...     period=16,
                ...     start=1,
                ...     stop=-1,
                ...     )

            ::

                >>> mask.start
                1

        Set to integer or none.
        '''
        return self._start

    @property
    def stop(self):
        r'''Gets stop index of ouput mask.

        ..  container:: example

            ::

                >>> mask = rhythmmakertools.BooleanPattern(
                ...     indices=[0, 1, 7],
                ...     period=16,
                ...     start=1,
                ...     stop=-1,
                ...     )

            ::

                >>> mask.stop
                -1

        Set to integer or none.
        '''
        return self._stop