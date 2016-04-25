# -*- coding: utf-8 -*-
from abjad.tools.abctools import AbjadValueObject


class IsUnpitched(AbjadValueObject):
    r'''Unpitched indicator.

    ..  container:: example

        ::

            >>> indicator = indicatortools.IsUnpitched()

    Attach to score selection to denote unpitched music.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_default_scope',
        )

    ### INITIALIZER ###

    def __init__(self):
        self._default_scope = None

    ### PUBLIC PROPERTIES ###

    @property
    def default_scope(self):
        r'''Gets default scope of unpitched music indicator.

        ..  container:: example

            ::

                >>> indicator = indicatortools.IsUnpitched()
                >>> indicator.default_scope is None
                True

        Returns none.
        '''
        return self._default_scope
