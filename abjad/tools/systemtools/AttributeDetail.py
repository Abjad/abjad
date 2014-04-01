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
        '_retrievable_name',
        )

    ### INITIALIZER ###

    # TODO: make is_positional default to False instead of True
    def __init__(
        self, 
        *args,
        **kwargs
        ):
        display_string = kwargs.get('display_string', None)
        editor_callable = kwargs.get('editor_callable', None)
        is_positional = kwargs.get('is_positional', True)
        menu_key = kwargs.get('menu_key', None)
        name = kwargs.get('name', None)
        retrievable_name = kwargs.get('retrievable_name', None)
        if not args:
            pass
        elif len(args) == 3:
            name = args[0]
            menu_key = args[1]
            editor_callable = args[2]
        elif len(args) == 5:
            name = args[0]
            display_string = args[1]
            menu_key = args[2]
            editor_callable = args[3]
            is_positional = args[4]

        elif len(args) == 6:
            name = args[0]
            retrievable_name = args[1]
            display_string = args[2]
            menu_key = args[3]
            editor_callable = args[4]
            is_positional = args[5]
        else:
            message = 'can not parse attribute detail: {!r}.'
            message = message.format(args)
            raise ValueError(message)
        retrievable_name = retrievable_name or name
        display_string = display_string or name.replace('_', ' ')
        self._display_string = display_string
        self._editor_callable = editor_callable
        self._is_positional = is_positional
        self._menu_key = menu_key
        self._name = name
        self._retrievable_name = retrievable_name

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

    @property
    def retrievable_name(self):
        r'''Gets retrievable name of attribute detail.

        Returns string.
        '''
        return self._retrievable_name