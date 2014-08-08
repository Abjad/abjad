# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class AttributeDetail(AbjadObject):
    r'''Attribute detail.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_display_string',
        '_editor',
        '_is_keyword',
        '_command',
        '_name',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        display_string=None,
        editor=None,
        is_keyword=True,
        command=None,
        name=None,
        ):
        if not display_string and name:
            display_string = name.replace('_', ' ')
        self._display_string = display_string
        self._editor = editor
        self._is_keyword = is_keyword
        self._command = command
        self._name = name

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of attribute detail.

        Returns string.
        '''
        parts = []
        if self.display_string:
            parts.append(self.display_string)
        if self.command:
            parts.append(self.command)
        if self.editor:
            parts.append(self.editor.__name__)
        parts = ', '.join(parts)
        return '{}({})'.format(type(self).__name__, parts)

    ### PUBLIC PROPERTIES ###

    @property
    def command(self):
        r'''Gets menu key of attribute detail.

        Returns string.
        '''
        return self._command

    @property
    def display_string(self):
        r'''Gets display string of attribute detail.

        Returns string.
        '''
        return self._display_string

    @property
    def editor(self):
        r'''Gets editor callable of attribute detail.

        Returns callable.
        '''
        return self._editor

    @property
    def is_keyword(self):
        r'''Is true when attribute detail is keyword.

        Returns boolean.
        '''
        return self._is_keyword

    @property
    def name(self):
        r'''Gets name of attribute detail.

        Returns string.
        '''
        return self._name