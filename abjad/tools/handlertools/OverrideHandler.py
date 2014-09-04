# -*- encoding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools import indicatortools
from abjad.tools import mathtools
from abjad.tools import scoretools
from abjad.tools.handlertools.Handler import Handler
from abjad.tools.topleveltools.attach import attach
from abjad.tools.topleveltools.iterate import iterate
from abjad.tools.topleveltools.override import override


class OverrideHandler(Handler):
    r'''LilyPond grob override handler.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_attribute_name',
        '_grob_name',
        '_attribute_value',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        grob_name=None, 
        attribute_name=None,
        attribute_value=None,
        ):
        assert isinstance(grob_name, str), repr(grob_name)
        self._grob_name = grob_name
        assert isinstance(attribute_name, str), repr(attribute_name)
        self._attribute_name = attribute_name
        assert isinstance(attribute_value, str), repr(attribute_value)
        self._attribute_value = attribute_value

    ### SPECIAL METHODS ###

    def __call__(self, expr, timespan=None):
        r'''Calls handler on `expr`.

        Returns none.
        '''
        prototype = (scoretools.Note, scoretools.Chord)
        leaves = iterate(expr).by_class(prototype)
        statement = 'override(leaf).{}.{} = {}'
        statement = statement.format(
            self._grob_name,
            self._attribute_name,
            self._attribute_value,
            )
        for leaf in leaves:
            exec(statement, globals(), locals())

    ### PUBLIC PROPERTIES ###

    @property
    def attribute_name(self):
        r'''Gets attribute name of override handler.

        Set to string or none.
        '''
        return self._attribute_name

    @property
    def attribute_value(self):
        r'''Gets attribute value of override handler.

        Set to string or none.
        '''
        return self._attribute_value

    @property
    def grob_name(self):
        r'''Gets grob name of override handler.

        Set to string or none.
        '''
        return self._grob_name