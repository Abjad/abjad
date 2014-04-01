# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class AttributeDetail(AbjadObject):
    r'''Attribute detail.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_display_string',
        '_editor_callable',
        '_is_positional',
        '_menu_key',
        '_name',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        display_string=None,
        editor_callable=None,
        is_positional=False,
        menu_key=None,
        name=None,
        ):
        assert isinstance(name, str)
        assert isinstance(menu_key, str)
        assert editor_callable
        display_string = display_string or name.replace('_', ' ')
        self._display_string = display_string
        self._editor_callable = editor_callable
        self._is_positional = is_positional
        self._menu_key = menu_key
        self._name = name

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of attribute detail.

        Returns string.
        '''
        parts = [
            repr(self.display_string),
            repr(self.menu_key),
            self.editor_callable.__name__,
            ]
        parts = ', '.join(parts)
        return '{}({})'.format(type(self).__name__, parts)

    ### PUBLIC PROPERTIES ###

    @property
    def display_string(self):
        r'''Gets display string of attribute detail.

        Returns string.
        '''
        return self._display_string

    @property
    def editor_callable(self):
        r'''Gets editor callable of attribute detail.

        Returns callable.
        '''
        return self._editor_callable

    @property
    def is_positional(self):
        r'''Is true when attribute detail is positional.

        Returns boolean.
        '''
        return self._is_positional

    @property
    def menu_key(self):
        r'''Gets menu key of attribute detail.

        Returns string.
        '''
        return self._menu_key

    @property
    def name(self):
        r'''Gets name of attribute detail.

        Returns string.
        '''
        return self._name