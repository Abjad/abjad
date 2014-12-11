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
        '_period',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        indices=None,
        period=None,
        ):
        if indices is not None:
            assert all(isinstance(_, int) for _ in indices), repr(indices)
            indices = tuple(indices)
        self._indices = indices
        if period is not None:
            assert mathtools.is_positive_integer(period), repr(period)
        self._period = period

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

    def _matches_index(self, index, total_length):
        assert 0 <= total_length
        if 0 <= index:
            nonnegative_index = index
        else:
            nonnegative_index = total_length - abs(index)
        if self.period is None:
            for index in self.indices:
                if 0 <= index:
                    if index == nonnegative_index and index < total_length:
                        return True
                else:
                    index = total_length - abs(index)
                    if index == nonnegative_index and index < total_length:
                        return True
        else:
            nonnegative_index = nonnegative_index % self.period
            for index in self.indices:
                if 0 <= index:
                    index = index % self.period
                    if index == nonnegative_index and index < total_length:
                        return True
                else:
                    index = total_length - abs(index)
                    index = index % self.period
                    if index == nonnegative_index and index < total_length:
                        return True
        return False

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