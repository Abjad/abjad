from abjad.tools import mathtools
from abjad.tools import stringtools
from abjad.tools.abctools.AbjadObject import AbjadObject


class MenuSection(AbjadObject):
    '''Menu section.

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

    Return menu section.
    '''

    ### CLASS VARIABLES ###

    return_value_attributes = (
        'display_string', 
        'key', 
        'number', 
        'explicit',
        )

    ### INITIALIZER ###

    def __init__(self,
        return_value_attribute='display_string',
        default_index=None,
        indent_level=1,
        is_hidden=False,
        is_numbered=False,
        is_ranged=False,
        display_prepopulated_values=True,
        title=None,
        ):
        AbjadObject.__init__(self)
        self.menu_entries = []
        assert return_value_attribute in self.return_value_attributes
        self.return_value_attribute = return_value_attribute
        self.default_index = default_index
        self.indent_level = indent_level
        self.is_hidden = is_hidden
        self.is_numbered = is_numbered
        self.is_ranged = is_ranged
        self.display_prepopulated_values = display_prepopulated_values
        self.title = title

    ### SPECIAL METHODS ###

    def __len__(self):
        '''Number of menu entries in menu section:

        Return nonnegative integer.
        '''
        return len(self.menu_entries)

    def __repr__(self):
        '''Menu section interpreter representation.

        Return string.
        '''
        return '<{} ({})>'.format(self._class_name, len(self))

    ### PRIVATE PROPERTIES ###


    @property
    def _default_value(self):
        default_menu_entry = self.menu_entries[self.default_index]
        return default_menu_entry.return_value

    @property
    def _has_default_value(self):
        return self.default_index is not None

    @property
    def _menu_entry_display_strings(self):
        return [menu_entry.display_string for menu_entry in self.menu_entries]

    @property
    def _menu_entry_keys(self):
        return [menu_entry.key for menu_entry in self.menu_entries]

    @property
    def _menu_entry_return_values(self):
        return [menu_entry.return_value for menu_entry in self.menu_entries]

    ### PRIVATE METHODS ###

    def _argument_range_string_to_numbers(self, argument_range_string):
        assert self.menu_entries
        numbers = []
        argument_range_string = argument_range_string.replace(' ', '')
        range_parts = argument_range_string.split(',')
        for range_part in range_parts:
            if range_part == 'all':
                numbers.extend(range(1, len(self.menu_entries) + 1))
            elif '-' in range_part:
                start, stop = range_part.split('-')
                start = self._argument_string_to_number(start)
                stop = self._argument_string_to_number(stop)
                if start is None or stop is None:
                    break
                if start <= stop:
                    new_numbers = range(start, stop + 1)
                    numbers.extend(new_numbers)
                else:
                    new_numbers = range(start, stop - 1, -1)
                    numbers.extend(new_numbers)
            else:
                number = self._argument_string_to_number(range_part)
                if number is None:
                    break
                numbers.append(number)
        return numbers

    def _argument_string_to_number(self, argument_string):
        for menu_entry_index, menu_entry in enumerate(self.menu_entries):
            if menu_entry.matches(argument_string):
                menu_entry_number = menu_entry_index + 1
                return menu_entry_number

    def _make_menu_lines(self):
        menu_lines = []
        menu_lines.extend(self._make_title_lines())
        for menu_entry in self.menu_entries:
            menu_line = self._make_tab(self.indent_level) + ' '
            display_string = menu_entry.display_string
            key = menu_entry.key
            prepopulated_value = menu_entry.prepopulated_value
            if self.is_numbered:
                menu_line += '{}: '.format(menu_entry.number)
            menu_line += display_string
            if key:
                menu_line += ' ({})'.format(key)
            if self.display_prepopulated_values and prepopulated_value:
                menu_line += ':'
                if prepopulated_value not in (None, 'None'):
                    menu_line += ' {}'.format(prepopulated_value)
            menu_lines.append(menu_line)
        if self.menu_entries:
            menu_lines.append('')
        return menu_lines

    def _make_tab(self, n):
        return 4 * n * ' '

    def _make_title_lines(self):
        menu_lines = []
        if isinstance(self.title, str):
            title_lines = [stringtools.capitalize_string_start(self.title)]
        elif isinstance(self.title, list):
            title_lines = self.title
        else:
            title_lines = []
        for title_line in title_lines:
            if self.indent_level:
                line = '{} {}'.format(
                    self._make_tab(self.indent_level), title_line)
                menu_lines.append(line)
            else:
                menu_lines.append(title_line)
        if menu_lines:
            menu_lines.append('')
        return menu_lines

    ### PUBLIC PROPERTIES ###

    @apply
    def default_index():
        def fget(self):
            '''Menu section default index:

            ::

                >>> menu_section.default_index is None
                True

            Return nonnegative integer or none.
            '''
            return self._default_index
        def fset(self, default_index):
            assert isinstance(default_index, (int, type(None)))
            if isinstance(default_index, int):
                count = len(self.menu_entries)
                if default_index < 0:
                    message = 'default index must be positive integer.'
                    raise ValueError(message)
                if count <= default_index:
                    message = 'only {} menu entry menu_entries '
                    message += 'in menu_section.'
                    message = message.format(count)
                    raise ValueError(message)
            self._default_index = default_index
        return property(**locals())

    @apply
    def display_prepopulated_values():
        def fget(self):
            '''True when menu section should show prepopulated values.
            Otherwise false:

            ::

                >>> menu_section.display_prepopulated_values
                True

            Return boolean.
            '''
            return self._display_prepopulated_values
        def fset(self, display_prepopulated_values):
            assert isinstance(display_prepopulated_values, bool)
            self._display_prepopulated_values = display_prepopulated_values
        return property(**locals())

    @apply
    def indent_level():
        def fget(self):
            '''Menu section indent level:

            ::

                >>> menu_section.indent_level
                1

            Return nonnegative integer.
            '''
            return self._indent_level
        def fset(self, indent_level):
            assert isinstance(indent_level, int) and 0 <= indent_level
            self._indent_level = indent_level
        return property(**locals())

    @apply
    def is_hidden():
        def fget(self):
            '''True when menu section is hidden. Otherwise false:

            ::

                >>> menu_section.is_hidden
                False

            Return boolean.
            '''
            return self._is_hidden
        def fset(self, expr):
            if not self.menu_entries:
                self._is_hidden = expr
        return property(**locals())

    @apply
    def is_numbered():
        def fget(self):
            '''True when menu section is numbered. Otherwise false:

            ::

                >>> menu_section.is_numbered
                False

            Return boolean.
            '''
            return self._is_numbered
        def fset(self, expr):
            if not self.menu_entries:
                self._is_numbered = expr
        return property(**locals())

    @apply
    def is_ranged():
        def fget(self):
            '''True when menu section is ranged. Otherwise false:

            ::

                >>> menu_section.is_ranged
                False

            Return boolean.
            '''
            return self._is_ranged
        def fset(self, expr):
            if not self.menu_entries:
                self._is_ranged = expr
        return property(**locals())

    @apply
    def menu_entries():
        def fget(self):
            '''Menu section menu entries:

            ::

                >>> for menu_entry in menu_section.menu_entries:
                ...     menu_entry
                <MenuEntry: 'svn add scores'>
                <MenuEntry: 'svn commit scores'>
                <MenuEntry: 'svn status scores'>
                <MenuEntry: 'svn update scores'>

            Return list.
            '''
            return self._menu_entries
        def fset(self, menu_entries):
            if menu_entries is None:
                self._menu_entries = []
            elif isinstance(menu_entries, list):
                self._menu_entries = []
                for menu_entry in menu_entries:
                    self.append(menu_entry)
            else:
                raise TypeError(menu_entries)
        return property(**locals())

    @apply
    def return_value_attribute():
        def fget(self):
            '''Menu section return value attribute:

            ::

                >>> menu_section.return_value_attribute
                'key'

            Acceptable values:

            ::

                'display_string' 
                'key' 
                'number' 
                'explicit'

            Return string.
            '''
            return self._return_value_attribute
        def fset(self, expr):
            if not self.menu_entries:
                self._return_value_attribute = expr
        return property(**locals())
    
    @property
    def storage_format(self):
        '''Menu section storage format:

        ::

            >>> z(menu_section)
            menuing.MenuSection(
                return_value_attribute='key',
                indent_level=1,
                is_hidden=False,
                is_numbered=False,
                is_ranged=False,
                display_prepopulated_values=True
                )

        Return string.
        '''
        return super(MenuSection, self).storage_format

    @apply
    def title():
        def fget(self):
            '''Menu section title:

            ::

                >>> menu_section.title is None
                True

            Return string or none.
            '''
            return self._title
        def fset(self, title):
            assert isinstance(title, (str, list, type(None)))
            self._title = title
        return property(**locals())

    ### PUBLIC METHODS ###

    def append(self, expr):
        '''Append `expr` to menu section:

        ::

            >>> menu_section.append(('svn mkdir', 'mkdir'))

        ::

            >>> for menu_entry in menu_section.menu_entries:
            ...     menu_entry
            <MenuEntry: 'svn add scores'>
            <MenuEntry: 'svn commit scores'>
            <MenuEntry: 'svn status scores'>
            <MenuEntry: 'svn update scores'>
            <MenuEntry: 'svn mkdir'>

        Return none.
        '''
        from experimental.tools import scoremanagertools
        assert isinstance(expr, (str, tuple))
        number = None
        if isinstance(expr, str):
            expr = (expr, )
        keys = (
            'display_string',
            'key',
            'prepopulated_value',
            'explicit_return_value',
            )
        kwargs = dict(zip(keys, expr))
        kwargs['menu_section'] = self
        menu_entry = scoremanagertools.menuing.MenuEntry(**kwargs)
        self.menu_entries.append(menu_entry)
