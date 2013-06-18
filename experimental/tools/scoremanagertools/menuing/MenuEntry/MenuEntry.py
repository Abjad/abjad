from abjad.tools import stringtools
from abjad.tools.abctools.AbjadObject import AbjadObject


class MenuEntry(AbjadObject):
    '''Menu entry.

        >>> score_manager = scoremanagertools.scoremanager.ScoreManager()
        >>> menu = score_manager._make_svn_menu()
        >>> menu
        <Menu (2)>

        >>> menu_section = menu.menu_sections[1]
        >>> menu_section
        <MenuSection (4)>

        >>> for menu_entry in menu_section.menu_entries:
        ...     menu_entry
        <MenuEntry: 'svn add scores'>
        <MenuEntry: 'svn commit scores'>
        <MenuEntry: 'svn status scores'>
        <MenuEntry: 'svn update scores'>

        >>> menu_entry = menu_section.menu_entries[-1]
        >>> menu_entry
        <MenuEntry: 'svn update scores'>

    Return menu entry.
    '''

    ### INITIALIZER ###

    def __init__(self, 
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
        '''Menu entry interpreter representation.

        Return string.
        '''
        return '<{}: {!r}>'.format(self._class_name, self.display_string)

    ### PUBLIC PROPERTIES ###

    @property
    def display_string(self):
        '''Menu entry display string:

        ::

            >>> menu_entry.display_string
            'svn update scores'

        Return string.
        '''
        return self._display_string

    @property
    def prepopulated_value(self):
        '''Menu entry existing value:

        ::

            >>> menu_entry.prepopulated_value is None
            True

        Return arbitrary value or none.
        '''
        return self._prepopulated_value

    @property
    def key(self):
        '''Menu entry key:

        ::

            >>> menu_entry.key
            'up'

        Return string without spaces or none.
        '''
        return self._key

    @property
    def menu_section(self):
        return self._menu_section

    @property
    def number(self):
        '''Menu entry number:

        ::

            >>> menu_entry.number is None
            True
    
        Return nonnegative integer or none.
        '''
        if self.menu_section.is_numbered:
            return self.menu_section.menu_entries.index(self) + 1

    @property
    def explicit_return_value(self):
        '''Menu entry prepopulated return value:

        ::

            >>> menu_entry.explicit_return_value is None
            True

        Return arbitrary value or none.
        '''
        return self._explicit_return_value

    @property
    def return_value(self):
        '''Menu entry return value:

        ::

            >>> menu_entry.return_value
            'up'

        Return arbitrary value.
        '''
        if self.menu_section.return_value_attribute == 'number':
            return_value = str(self.number)
        elif self.menu_section.return_value_attribute == 'display_string':
            return_value = self.display_string
        elif self.menu_section.return_value_attribute == 'key':
            return_value = self.key
        elif self.menu_section.return_value_attribute == 'explicit':
            return_value = self.explicit_return_value
        assert return_value
        return return_value

    @property
    def storage_format(self):
        '''Menu entry storage format:

            >>> z(menu_entry)
            menuing.MenuEntry(
                menuing.MenuSection(
                    menu_entries=[<MenuEntry: 'svn add scores'>, <MenuEntry: 'svn commit scores'>, <MenuEntry: 'svn status scores'>, <MenuEntry: 'svn update scores'>],
                    return_value_attribute='key',
                    is_numbered=False,
                    is_ranged=False,
                    is_hidden=False
                    ),
                'svn update scores',
                key='up'
                )

        Return string.
        '''
        return super(MenuEntry, self).storage_format

    ### PUBLIC METHODS ###

    def matches(self, user_input):
        '''True when menu entry matches `user_input` string:

        ::

            >>> menu_entry.matches('svn update scores')
            True

        ::

            >>> menu_entry.matches('up')
            True

        Otherwise false:

        ::

            >>> menu_entry.matches('foo')
            False

        Return boolean.
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
