# -*- coding: utf-8 -*-
from abjad.tools import markuptools
from abjad.tools import schemetools
from abjad.tools.abctools import AbjadValueObject


class ExampleWrapper(AbjadValueObject):
    r'''Example wrapper.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Illustration helpers'

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
        command.force_quotes = True
        pair = schemetools.SchemePair('font-name', 'Courier')
        command = markuptools.MarkupCommand('override', pair, command)
        markup = markuptools.Markup(command, direction=Up)
        return markup

    ### PUBLIC PROPERTIES ###

    @property
    def arguments(self):
        r'''Gets arguments.

        Returns dictionary.
        '''
        return self._arguments

    @property
    def division_lists(self):
        r'''Gets division lists.

        Returns tuple.
        '''
        return self._division_lists