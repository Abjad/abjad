# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class GalleryInputBlock(AbjadObject):
    r'''A gallery input block.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_division_lists',
        '_input_',
        )

    ### INITIALIZER ###

    def __init__(self, input_=None, division_lists=None):
        division_lists = division_lists or ()
        self._input_ = input_
        self._division_lists = tuple(division_lists)

    ### PRIVATE METHODS ###

    def _to_markup(self, class_):
        from abjad.tools import markuptools
        from abjad.tools import schemetools
        instance = class_(**self.input_)
        string = format(instance, 'storage')
        string = string.replace('rhythmmakertools.', '')
        lines = string.split('\n')
        column = markuptools.MarkupCommand('column', lines)
        pair = schemetools.SchemePair('font-name', 'Courier')
        override_ = markuptools.MarkupCommand('override', pair, column)
        markup = markuptools.Markup(override_)
        return markup

    ### PUBLIC PROPERTIES ###

    @property
    def division_lists(self):
        r'''Gets division lists of gallery input block.

        Returns tuple.
        '''
        return self._division_lists

    @property
    def input_(self):
        r'''Gets input to gallery input block.

        Returns dictionary.
        '''
        return self._input_
