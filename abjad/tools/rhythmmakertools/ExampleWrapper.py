# -*- encoding: utf-8 -*-
from abjad.tools import markuptools
from abjad.tools import schemetools
from abjad.tools.abctools import AbjadObject


class ExampleWrapper(AbjadObject):
    r'''Example wrapper.
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

    ### SPECIAL METHODS ###

    def __makenew__(self, *args, **kwargs):
        r'''Makes new example wrapper with optional `kwargs`.

        Returns new example wrapper.
        '''
        from abjad.tools import systemtools
        assert not args
        arguments = {}
        manager = systemtools.StorageFormatManager
        argument_names = manager.get_keyword_argument_names(self)
        for argument_name in argument_names:
            arguments[argument_name] = getattr(self, argument_name)
        arguments.update(kwargs)
        return type(self)(**arguments)

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
    def division_lists(self):
        r'''Gets division lists of example wrapper.

        Returns tuple.
        '''
        return self._division_lists

    @property
    def arguments(self):
        r'''Gets arguments of example wrapper.

        Returns dictionary.
        '''
        return self._arguments
