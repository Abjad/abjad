# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class TupletSpellingSpecifier(AbjadObject):
    r'''Tuplet spelling specifier.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_avoid_dots',
        '_is_diminution',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        avoid_dots=False,
        is_diminution=True,
        ):
        assert isinstance(avoid_dots, bool), avoid_dots
        assert isinstance(is_diminution, bool), is_diminution
        self._avoid_dots = avoid_dots
        self._is_diminution = is_diminution

    ### PUBLIC PROPERTIES ###

    @property
    def avoid_dots(self):
        r'''Is true when tuplet spelling should avoid dotted rhythmic values.
        Otherwise false.

        Defaults to false.

        Returns boolean.
        '''
        return self._avoid_dots

    @property
    def is_diminution(self):
        r'''Is true when tuplet should be spelled as diminution. Otherwise
        false.

        Defaults to true.

        Returns boolean.
        '''
        return self._is_diminution
