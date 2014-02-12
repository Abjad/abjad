# -*- encoding: utf-8 -*-
from abjad.tools import stringtools
from abjad.tools.abctools.AbjadObject import AbjadObject


class MenuEntry(AbjadObject):
    r'''Menu entry.

        >>> score_manager = scoremanager.core.ScoreManager()
        >>> menu = score_manager._make_repository_menu()
        >>> menu
        <Menu (2)>

        >>> menu_section = menu.menu_sections[1]
        >>> menu_section
        <MenuSection (4)>

        >>> for menu_entry in menu_section.menu_entries:
        ...     menu_entry
        <MenuEntry: 'add'>
        <MenuEntry: 'commit'>
        <MenuEntry: 'status'>
        <MenuEntry: 'update'>

        >>> menu_entry = menu_section.menu_entries[-1]
        >>> menu_entry
        <MenuEntry: 'update'>

    '''

    ### INITIALIZER ###

    def __init__(
        self, 
        menu_section,
        display_string,
        key=None,
        prepopulated_value=None,
        explicit_return_value=None,
        ):
        self._menu_section = menu_section
        self._display_string = display_string
        self._key = key
        self._prepopulated_value = prepopulated_value
        self._explicit_return_value = explicit_return_value

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of menu entry.

        Returns string.
        '''
        return '<{}: {!r}>'.format(type(self).__name__, self.display_string)

    ### PUBLIC PROPERTIES ###

    @property
    def display_string(self):
        r'''Menu entry display string.

        ::

            >>> menu_entry.display_string
            'update'

        Returns string.
        '''
        return self._display_string

    @property
    def explicit_return_value(self):
        r'''Menu entry prepopulated return value.

        ::

            >>> menu_entry.explicit_return_value is None
            True

        Returns arbitrary value or none.
        '''
        return self._explicit_return_value

    @property
    def key(self):
        r'''Menu entry key.

        ::

            >>> menu_entry.key
            'up'

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

            >>> menu_entry.number is None
            True
    
        Returns nonnegative integer or none.
        '''
        if self.menu_section.is_numbered:
            return self.menu_section.menu_entries.index(self) + 1

    @property
    def prepopulated_value(self):
        r'''Menu entry existing value.

        ::

            >>> menu_entry.prepopulated_value is None
            True

        Returns arbitrary value or none.
        '''
        return self._prepopulated_value

    @property
    def return_value(self):
        r'''Menu entry return value.

        ::

            >>> menu_entry.return_value
            'up'

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

            >>> menu_entry.matches('update')
            True

        ::

            >>> menu_entry.matches('up')
            True

        Otherwise false:

        ::

            >>> menu_entry.matches('foo')
            False

        Returns boolean.
        '''
        if self.key is not None and user_input == self.key:
            return True
        if self.menu_section.is_numbered and user_input == str(self.number):
            return True
        if 3 <= len(user_input):
            normalized_display_string = \
                stringtools.strip_diacritics_from_binary_string(
                self.display_string)
            normalized_display_string = normalized_display_string.lower()
            if normalized_display_string.startswith(user_input):
                return True
        return False 
