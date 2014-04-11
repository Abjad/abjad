# -*- encoding: utf-8 -*-
from abjad.tools import stringtools
from abjad.tools.abctools.AbjadObject import AbjadObject


class MenuEntry(AbjadObject):
    r'''Menu entry.

    ..  container:: example

        ::

            >>> menu = scoremanager.iotools.Menu()
            >>> commands = []
            >>> commands.append(('foo - add', 'add'))
            >>> commands.append(('foo - delete', 'delete'))
            >>> commands.append(('foo - modify', 'modify'))
            >>> section = menu.make_command_section(
            ...     menu_entries=commands,
            ...     name='test',
            ...     )

        ::

            >>> for entry in section.menu_entries:
            ...     entry
            <MenuEntry: 'foo - add'>
            <MenuEntry: 'foo - delete'>
            <MenuEntry: 'foo - modify'>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_display_string',
        '_explicit_return_value',
        '_key',
        '_menu_section',
        '_prepopulated_value',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        menu_section,
        display_string=None,
        explicit_return_value=None,
        key=None,
        prepopulated_value=None,
        ):
        if menu_section.is_command_section:
            assert '-' in display_string, repr(menu_section)
        self._menu_section = menu_section
        self._display_string = display_string
        self._explicit_return_value = explicit_return_value
        self._key = key
        self._prepopulated_value = prepopulated_value

    ### SPECIAL METHODS ###

    def __lt__(self, expr):
        r'''Is true when `expr` is a menu entry with a display string greater
        than that of this menu entry. Otherwise false.

        Raises type error when `expr` is not a menu entry.

        Returns boolean.
        '''
        if not isinstance(expr, type(self)):
            raise TypeError(expr)
        return self.display_string < expr.display_string

    def __repr__(self):
        r'''Gets interpreter representation of menu entry.

        Returns string.
        '''
        return '<{}: {!r}>'.format(type(self).__name__, self.display_string)

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        positional_argument_values = ()
        return systemtools.StorageFormatSpecification(
            self,
            positional_argument_values=positional_argument_values,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def display_string(self):
        r'''Menu entry display string.

        ::

            >>> entry.display_string
            'foo - modify'

        Returns string.
        '''
        return self._display_string

    @property
    def explicit_return_value(self):
        r'''Menu entry prepopulated return value.

        ::

            >>> entry.explicit_return_value is None
            True

        Returns arbitrary value or none.
        '''
        return self._explicit_return_value

    @property
    def key(self):
        r'''Menu entry key.

        ::

            >>> entry.key
            'modify'

        Returns string without spaces or none.
        '''
        return self._key

    @property
    def menu_section(self):
        r'''Menu entry menu section.

        Returns menu section.
        '''
        return self._menu_section

    @property
    def number(self):
        r'''Menu entry number.

        ::

            >>> entry.number is None
            True

        Returns nonnegative integer or none.
        '''
        if self.menu_section.is_numbered:
            return self.menu_section.menu_entries.index(self) + 1

    @property
    def prepopulated_value(self):
        r'''Menu entry existing value.

        ::

            >>> entry.prepopulated_value is None
            True

        Returns arbitrary value or none.
        '''
        return self._prepopulated_value

    @property
    def return_value(self):
        r'''Menu entry return value.

        ::

            >>> entry.return_value
            'modify'

        Returns arbitrary value.
        '''
        if self.menu_section.return_value_attribute == 'number':
            return_value = str(self.number)
        elif self.menu_section.return_value_attribute == 'display_string':
            return_value = self.display_string
        elif self.menu_section.return_value_attribute == 'key':
            return_value = self.key
        elif self.menu_section.return_value_attribute == 'explicit':
            return_value = self.explicit_return_value
        assert return_value, repr((
            self.menu_section,
            self.menu_section.return_value_attribute,
            self,
            ))
        return return_value

    ### PUBLIC METHODS ###

    def matches(self, user_input):
        r'''Is true when menu entry matches `user_input` string.

        ::

            >>> entry.matches('modify')
            True

        Otherwise false:

        ::

            >>> entry.matches('asdf')
            False

        Returns boolean.
        '''
        if self.key is not None and user_input == self.key:
            return True
        if self.menu_section.is_numbered and user_input == str(self.number):
            return True
        if self.menu_section.match_on_display_string:
            if 3 <= len(user_input):
                normalized_display_string = \
                    stringtools.strip_diacritics_from_binary_string(
                    self.display_string)
                normalized_display_string = normalized_display_string.lower()
                if normalized_display_string.startswith(user_input):
                    return True
        return False