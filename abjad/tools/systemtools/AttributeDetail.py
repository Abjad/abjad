# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class AttributeDetail(AbjadObject):
    r'''Attribute detail.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_allow_none',
        '_editor_callable',
        '_is_null',
        '_is_positional',
        '_menu_key',
        '_name',
        '_retrievable_name',
        '_space_delimited_lowercase_name',
        )

    ### INITIALIZER ###

    # TODO: space_delimited_lowercase_name is a misnomer because
    #       of 'sounding pitch of written middle C';
    #       maybe change to self._display_name
    def __init__(self, *args):
        is_null = False
        if len(args) == 3:
            name, menu_key, editor_callable = args
            space_delimited_lowercase_name = None
            is_positional = True
            retrievable_name = name
        elif len(args) == 5:
            name = args[0]
            space_delimited_lowercase_name = args[1]
            menu_key = args[2]
            editor_callable = args[3]
            is_positional = args[4]
            retrievable_name = name
        elif len(args) == 6:
            name = args[0]
            retrievable_name = args[1]
            space_delimited_lowercase_name = args[2]
            menu_key = args[3]
            editor_callable = args[4]
            is_positional = args[5]
        else:
            message = 'can not parse attribute detail: {!r}.'
            message = message.format(args)
            raise ValueError(message)
        if not space_delimited_lowercase_name and name:
            space_delimited_lowercase_name = name.replace('_', ' ')
        self._allow_none = True
        self._editor_callable = editor_callable
        self._menu_key = menu_key
        self._name = name
        self._is_null = is_null
        self._is_positional = is_positional
        self._retrievable_name = retrievable_name
        self._space_delimited_lowercase_name = space_delimited_lowercase_name

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of attribute detail.

        Returns string.
        '''
        parts = [
            repr(self.space_delimited_lowercase_name),
            repr(self.menu_key),
            self.editor_callable.__name__,
            ]
        if not self.allow_none:
            parts.append('allow_none=False')
        parts = ', '.join(parts)
        return '{}({})'.format(type(self).__name__, parts)

    ### PUBLIC PROPERTIES ###

    @property
    def allow_none(self):
        r'''Is true when none is allowed. Otherwise false.

        Returns boolean.
        '''
        return self._allow_none

    @property
    def editor_callable(self):
        r'''Gets editor callable of attribute detail.

        Returns callable.
        '''
        return self._editor_callable

    @property
    def is_null(self):
        r'''Is true when detail is null. Otherwise false.

        Returns boolean.
        '''
        return self._is_null

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

    @property
    def space_delimited_lowercase_name(self):
        r'''Gets space-delimited lowercase name.

        Returns string.
        '''
        return self._space_delimited_lowercase_name