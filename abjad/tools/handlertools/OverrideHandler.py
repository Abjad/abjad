# -*- encoding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools import durationtools
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
        '_attribute_value',
        '_grob_name',
        '_maximum_settings',
        '_maximum_written_duration',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        grob_name=None, 
        attribute_name=None,
        attribute_value=None,
        maximum_written_duration=None,
        maximum_settings=None,
        ):
        if grob_name is not None:
            assert isinstance(grob_name, str), repr(grob_name)
        self._grob_name = grob_name
        if attribute_name is not None:
            assert isinstance(attribute_name, str), repr(attribute_name)
        self._attribute_name = attribute_name
        if attribute_value is not None:
            assert isinstance(attribute_value, str), repr(attribute_value)
        self._attribute_value = attribute_value
        if maximum_written_duration is not None:
            maximum_written_duration = durationtools.Duration(
                maximum_written_duration)
        self._maximum_written_duration = maximum_written_duration
        if maximum_settings is not None:
            assert isinstance(maximum_settings, dict), maximum_settings
        self._maximum_settings = maximum_settings

    ### SPECIAL METHODS ###

    def __call__(self, expr, timespan=None):
        r'''Calls handler on `expr`.

        Returns none.
        '''
        leaves = iterate(expr).by_class(scoretools.Leaf)
        statement = 'override(leaf).{}.{} = {}'
        statement = statement.format(
            self._grob_name,
            self._attribute_name,
            self._attribute_value,
            )
        if self.maximum_written_duration is not None:
            maximum_statement = 'override(leaf).{}.{} = {}'
            maximum_statement = maximum_statement.format(
                self.maximum_settings['grob_name'],
                self.maximum_settings['attribute_name'],
                self.maximum_settings['attribute_value'],
                )
        for leaf in leaves:
            if self.maximum_written_duration is not None:
                if self.maximum_written_duration <= leaf.written_duration:
                    if maximum_statement is not None:
                        exec(maximum_statement, globals(), locals())
                    continue
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

    @property
    def maximum_settings(self):
        r'''Gets maximum settings for leaves with written duration
        greater than or equal to maximum written duration of handler.

        ..  todo: Write examples and tests.

        Set to dictionary or none.
        '''
        return self._maximum_settings

    @property
    def maximum_written_duration(self):
        r'''Gets maximum written duration of override handler.

        Written durations equal to or greater than this will
        not be handled.

        Set to duration or none.
        '''
        return self._maximum_written_duration