# -*- encoding: utf-8 -*-
from abjad.tools import markuptools
from abjad.tools import schemetools
from abjad.tools.abctools import AbjadObject


class ExampleWrapper(AbjadObject):
    r'''A gallery input specifier.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_division_lists',
        '_arguments',
        )

    ### INITIALIZER ###

    def __init__(self, arguments=None, division_lists=None):
        division_lists = division_lists or ()
        self._arguments = arguments
        self._division_lists = tuple(division_lists)

    ### PRIVATE METHODS ###

    def _to_markup(self, class_):
        instance = class_(**self.arguments)
        string = format(instance, 'storage')
        string = string.replace('rhythmmakertools.', '')
        lines = string.split('\n')
        command = markuptools.MarkupCommand('column', lines)
        pair = schemetools.SchemePair('font-name', 'Courier')
        command = markuptools.MarkupCommand('override', pair, command)
        markup = markuptools.Markup(command)
        return markup

    ### PUBLIC PROPERTIES ###

    @property
    def division_lists(self):
        r'''Gets division lists of gallery input block.

        Returns tuple.
        '''
        return self._division_lists

    @property
    def arguments(self):
        r'''Gets input to gallery input block.

        Returns dictionary.
        '''
        return self._arguments
