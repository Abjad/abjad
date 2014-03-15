# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools import stringtools
from abjad.tools.abctools.AbjadObject import AbjadObject


class MenuSection(AbjadObject):
    r'''Menu section.

    ..  container:: example

        ::

            >>> menu = scoremanager.iotools.Menu(
            ...     include_default_hidden_sections=False,
            ...     )
            >>> section = menu.make_command_section(name='test')
            >>> entry = section.append(('foo - add', 'add'))
            >>> entry = section.append(('foo - delete', 'delete'))
            >>> entry = section.append(('foo - modify', 'modify'))

        ::

            >>> section
            <MenuSection 'test' (3)>

    '''

    ### CLASS VARIABLES ###

    return_value_attributes = (
        'display_string', 
        'key', 
        'number', 
        'explicit',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        return_value_attribute='display_string',
        default_index=None,
        indent_level=1,
        is_asset_section=False,
        is_attribute_section=False,
        is_command_section=False,
        is_hidden=False,
        is_numbered=False,
        is_ranged=False,
        display_prepopulated_values=False,
        match_on_display_string=True,
        menu_entries=None,
        name=None,
        title=None,
        ):
        AbjadObject.__init__(self)
        assert name, repr(name)
        self._name = name
        assert return_value_attribute in self.return_value_attributes
        self._return_value_attribute = return_value_attribute
        self._indent_level = indent_level
        self._is_asset_section = is_asset_section
        self._is_attribute_section = is_attribute_section
        self._is_command_section = is_command_section
        self._is_hidden = is_hidden
        self._is_numbered = is_numbered
        self._is_ranged = is_ranged
        self._display_prepopulated_values = display_prepopulated_values
        self._menu_entries = menu_entries or []
        self._title = title
        self._default_index = default_index
        self.match_on_display_string = match_on_display_string

    ### SPECIAL METHODS ###

    def __len__(self):
        r'''Number of menu entries in menu section.

        Returns nonnegative integer.
        '''
        return len(self.menu_entries)

    def __repr__(self):
        r'''Gets interpreter representation of menu section.

        Returns string.
        '''
        left_parenthesis = '('
        right_parenthesis = ')'
        if self.is_hidden:
            left_parenthesis = '['
            right_parenthesis = ']'
        if self.name:
            return '<{} {!r} {}{}{}>'.format(
                type(self).__name__, 
                self.name,
                left_parenthesis,
                len(self),
                right_parenthesis,
                )
        return '<{} {}{}{}>'.format(
            type(self).__name__, 
            left_parenthesis,
            len(self),
            right_parenthesis,
            )

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
        for i, menu_entry in enumerate(self.menu_entries):
            menu_line = self._make_tab(self.indent_level) + ' '
            display_string = menu_entry.display_string
            key = menu_entry.key
            prepopulated_value = menu_entry.prepopulated_value
            if self.is_numbered:
                menu_line += '{}: '.format(menu_entry.number)
            menu_line += display_string
            if key:
                if i == self.default_index:
                    menu_line += ' [{}]'.format(key)
                else:
                    menu_line += ' ({})'.format(key)
            if self.display_prepopulated_values:
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

    @property
    def default_index(self):
        r'''Gets menu section default index.

        ::

            >>> section.default_index is None
            True

        Returns nonnegative integer or none.
        '''
        return self._default_index

    @property
    def display_prepopulated_values(self):
        r'''Is true when menu section should show prepopulated values.
        Otherwise false:

        ::

            >>> section.display_prepopulated_values
            False

        Returns boolean.
        '''
        return self._display_prepopulated_values

    @property
    def indent_level(self):
        r'''Gets menu indent level.

        ::

            >>> section.indent_level
            1

        Returns nonnegative integer.
        '''
        return self._indent_level

    @property
    def is_asset_section(self):
        r'''Is true when menu section lists assets. Otherwise false.

        Returns boolean.
        '''
        return self._is_asset_section

    @property
    def is_attribute_section(self):
        r'''Is true when menu section lists attributes. Otherwise false.

        Returns boolean.
        '''
        return self._is_attribute_section

    @property
    def is_command_section(self):
        r'''Is true when menu section lists commands. Otherwise false.

        Returns boolean.
        '''
        return self._is_command_section

    @property
    def is_hidden(self):
        r'''Is true when menu section is hidden. 
        Otherwise false:

        ::

            >>> section.is_hidden
            False

        Returns boolean.
        '''
        return self._is_hidden

    @property
    def is_numbered(self):
        r'''Is true when menu section is numbered. 
        Otherwise false:

        ::

            >>> section.is_numbered
            False

        Returns boolean.
        '''
        return self._is_numbered

    @property
    def is_ranged(self):
        r'''Is true when menu section is ranged. 
        Otherwise false:

        ::

            >>> section.is_ranged
            False

        Returns boolean.
        '''
        return self._is_ranged

    @property
    def menu_entries(self):
        r'''Menu section menu entries.

        ::

            >>> for menu_entry in section.menu_entries:
            ...     menu_entry
            <MenuEntry: 'foo - add'>
            <MenuEntry: 'foo - delete'>
            <MenuEntry: 'foo - modify'>

        Returns list.
        '''
        return self._menu_entries

    @property
    def name(self):
        r'''Gets name of menu section.

        ..  container:: example

            ::

                >>> section.name
                'test'

        Returns string or none.
        '''
        return self._name

    @property
    def return_value_attribute(self):
        r'''Menu section return value attribute.

        ::

            >>> section.return_value_attribute
            'key'

        Acceptable values:

        ::

            'display_string' 
            'key' 
            'number' 
            'explicit'

        Returns string.
        '''
        return self._return_value_attribute
    
    @property
    def title(self):
        r'''Gets menu section title.

        ::

            >>> section.title is None
            True

        Returns string or none.
        '''
        return self._title

    ### PUBLIC METHODS ###

    def append(self, expr):
        r'''Appends `expr` to menu section.

        ::

            >>> section.append(('foo - stub', 'stub'))
            <MenuEntry: 'foo - stub'>

        ::

            >>> for menu_entry in section.menu_entries:
            ...     menu_entry
            <MenuEntry: 'foo - add'>
            <MenuEntry: 'foo - delete'>
            <MenuEntry: 'foo - modify'>
            <MenuEntry: 'foo - stub'>

        Returns menu entry.
        '''
        from scoremanager import iotools
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
        menu_entry = iotools.MenuEntry(**kwargs)
        self.menu_entries.append(menu_entry)
        if self.is_command_section:
            self.menu_entries.sort()
        return menu_entry
