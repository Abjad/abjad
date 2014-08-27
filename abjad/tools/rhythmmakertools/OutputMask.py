# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.abctools import AbjadValueObject


class OutputMask(AbjadValueObject):
    r'''Output mask.

    ..  container:: example

        ::

            >>> mask = rhythmmakertools.OutputMask(
            ...     indices=[0, 1, 7],
            ...     period=16,
            ...     )

        ::

            >>> print(format(mask))
            rhythmmakertools.OutputMask(
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
        from scoremanager import idetools
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

    ### PUBLIC PROPERTIES ###

    @property
    def indices(self):
        r'''Gets indices of ouput mask.

        ..  container:: example

            ::

                >>> mask = rhythmmakertools.OutputMask(
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

                >>> mask = rhythmmakertools.OutputMask(
                ...     indices=[0, 1, 7],
                ...     period=16,
                ...     )

            ::

                >>> mask.period
                16

        Set to positive integer or none.
        '''
        return self._period