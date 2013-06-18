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

    ### CLASS VARIABLES ###

    return_value_attributes = (
        'display_string', 
        'key', 
        'number', 
        'prepopulated',
        )

    ### INITIALIZER ###

    def __init__(self, 
        display_string,
        key=None,
        existing_value=None,
        prepopulated_return_value=None,
        number=None, 
        return_value_attribute=None,
        ):
        assert return_value_attribute in self.return_value_attributes
        self._number = number
        self._return_value_attribute = return_value_attribute
        self._key = key
        self._display_string = display_string
        self._existing_value = existing_value
        self._prepopulated_return_value = prepopulated_return_value
        self._initialize_return_value()
        self._initialize_matching()

    ### SPECIAL METHODS ###

    def __repr__(self):
        '''Menu entry interpreter representation.

        Return string.
        '''
        return '<{}: {!r}>'.format(self._class_name, self.display_string)

    ### PRIVATE METHODS ###
 
    def _initialize_matching(self):
        matches = []
        if self.number:
            matches.append(str(self.number))
        if self.key is not None:
            matches.append(self.key)
        self._matches = tuple(matches)
        normalized_display_string = \
            stringtools.strip_diacritics_from_binary_string(
            self.display_string)
        normalized_display_string = normalized_display_string.lower()
        self._normalized_display_string = normalized_display_string

    def _initialize_return_value(self):
        if self.return_value_attribute == 'number':
            return_value = str(self.number)
        elif self.return_value_attribute == 'display_string':
            return_value = self.display_string
        elif self.return_value_attribute == 'key':
            return_value = self.key
        elif self.return_value_attribute == 'prepopulated':
            return_value = self.prepopulated_return_value
        assert return_value
        self._return_value = return_value

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
    def existing_value(self):
        '''Menu entry existing value:

        ::

            >>> menu_entry.existing_value is None
            True

        Return arbitrary value or none.
        '''
        return self._existing_value

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
    def number(self):
        '''Menu entry number:

        ::

            >>> menu_entry.number is None
            True
    
        Return nonnegative integer or none.
        '''
        return self._number

    @property
    def prepopulated_return_value(self):
        '''Menu entry prepopulated return value:

        ::

            >>> menu_entry.prepopulated_return_value is None
            True

        Return arbitrary value or none.
        '''
        return self._prepopulated_return_value

    @property
    def return_value(self):
        '''Menu entry return value:

        ::

            >>> menu_entry.return_value
            'up'

        Return arbitrary value.
        '''
        return self._return_value

    @property
    def return_value_attribute(self):
        '''Menu entry return value attribute:

        ::

            >>> menu_entry.return_value_attribute
            'key'

        Acceptable values are

        ::

            'display_string'
            'key' 
            'number' 
            'prepopulated'

        Return string.
        '''
        return self._return_value_attribute

    @property
    def storage_format(self):
        '''Menu entry storage format:

            >>> z(menu_entry)
            menuing.MenuEntry(
                'svn update scores',
                key='up',
                return_value_attribute='key'
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
        if user_input in self._matches:
            return True
        if 3 <= len(user_input):
            if self._normalized_display_string.startswith(user_input):
                return True
        return False 
