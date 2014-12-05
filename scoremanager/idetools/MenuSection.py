# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools import stringtools
from abjad.tools.abctools.AbjadObject import AbjadObject


class MenuSection(AbjadObject):
    r'''Menu section.

    ..  container:: example

        ::

            >>> session = scoremanager.idetools.Session()
            >>> menu = scoremanager.idetools.Menu(session=session)
            >>> commands = []
            >>> commands.append(('foo - add', 'add'))
            >>> commands.append(('foo - delete', 'delete'))
            >>> commands.append(('foo - modify', 'modify'))
            >>> section = menu.make_command_section(
            ...     commands=commands,
            ...     name='test',
            ...     )

        ::

            >>> section
            <MenuSection 'test' (3)>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_default_index',
        '_display_prepopulated_values',
        '_group_by_annotation',
        '_indent_level',
        '_is_alphabetized',
        '_is_asset_section',
        '_is_attribute_section',
        '_is_command_section',
        '_is_hidden',
        '_is_information_section',
        '_is_material_summary_section',
        '_is_navigation_section',
        '_is_numbered',
        '_is_ranged',
        '_menu_entries',
        '_name',
        '_return_value_attribute',
        '_title',
        '_match_on_display_string',
        )

    return_value_attributes = (
        'display_string',
        'key',
        'number',
        'explicit',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        default_index=None,
        display_prepopulated_values=False,
        group_by_annotation=True,
        indent_level=1,
        is_alphabetized=True,
        is_asset_section=False,
        is_attribute_section=False,
        is_command_section=False,
        is_hidden=False,
        is_information_section=False,
        is_material_summary_section=False,
        is_navigation_section=False,
        is_numbered=False,
        is_ranged=False,
        match_on_display_string=True,
        menu_entries=None,
        name=None,
        return_value_attribute='display_string',
        title=None,
        ):
        AbjadObject.__init__(self)
        assert menu_entries, repr(name)
        assert name, repr(name)
        assert return_value_attribute in self.return_value_attributes
        self._default_index = default_index
        self._display_prepopulated_values = display_prepopulated_values
        self._group_by_annotation = group_by_annotation
        self._indent_level = indent_level
        self._is_alphabetized = is_alphabetized
        self._is_asset_section = is_asset_section
        self._is_attribute_section = is_attribute_section
        self._is_command_section = is_command_section
        self._is_hidden = is_hidden
        self._is_information_section = is_information_section
        self._is_material_summary_section = is_material_summary_section
        self._is_navigation_section = is_navigation_section
        self._is_numbered = is_numbered
        self._is_ranged = is_ranged
        self._match_on_display_string = match_on_display_string
        self._name = name
        self._menu_entries = []
        for menu_entry in menu_entries:
            self._append(menu_entry)
        self._return_value_attribute = return_value_attribute
        self._title = title

    ### SPECIAL METHODS ###

    def __getitem__(self, expr):
        r'''Gets menu entry indexed by `expr`.

        Returns menu entry.
        '''
        return self.menu_entries.__getitem__(expr)

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
    def _information_message_bullet(self):
        return '=>'

    @property
    def _material_summary_bullet(self):
        return '*'

    @property
    def _menu_entry_display_strings(self):
        return [_.display_string for _ in self]

    @property
    def _menu_entry_keys(self):
        return [_.key for _ in self]

    @property
    def _menu_entry_return_values(self):
        return [_.return_value for _ in self]

    ### PRIVATE METHODS ###

    def _argument_range_string_to_numbers(self, argument_range_string):
        argument_range_string = argument_range_string.strip()
        assert self.menu_entries
        numbers = []
        if ',' in argument_range_string:
            range_parts = argument_range_string.split(',')
        else:
            range_parts = [argument_range_string]
        for range_part in range_parts:
            range_part = range_part.strip()
            matches_entry = False
            for menu_entry in self:
                if menu_entry.matches(range_part):
                    number = self._argument_string_to_number(range_part)
                    numbers.append(number)
                    matches_entry = True
                    break
            if matches_entry:
                continue
            for menu_entry in self:
                if menu_entry.matches(range_part.lower()):
                    number = self._argument_string_to_number(
                        range_part.lower())
                    numbers.append(number)
                    matches_entry = True
                    break
            if matches_entry:
                continue
            if range_part == 'all':
                numbers.extend(range(1, len(self.menu_entries) + 1))
            elif '-' in range_part:
                start, stop = range_part.split('-')
                start = start.strip()
                stop = stop.strip()
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
        for index, menu_entry in enumerate(self):
            if menu_entry.matches(argument_string):
                menu_entry_number = index + 1
                return menu_entry_number
        try:
            number = int(argument_string)
        except (TypeError, ValueError):
            return
        greatest_menu_entry_number = len(self)
        if greatest_menu_entry_number < number:
            return greatest_menu_entry_number

    def _make_lines(self):
        lines = []
        lines.extend(self._make_title_lines())
        for i, menu_entry in enumerate(self):
            line = self._make_tab(self.indent_level)
            display_string = menu_entry.display_string
            key = menu_entry.key
            prepopulated_value = menu_entry.prepopulated_value
            if self.is_numbered:
                number_indicator = '{}: '.format(menu_entry.number)
                tab = self._make_tab(self.indent_level)
                tab_width = len(tab)
                number_width = len(str(number_indicator))
                reduced_tab_width = tab_width - number_width
                reduced_tab = reduced_tab_width * ' '
                line = reduced_tab + number_indicator
            line += display_string
            if key:
                if i == self.default_index:
                    line += ' [{}]'.format(key)
                else:
                    line += ' ({})'.format(key)
            if self.display_prepopulated_values:
                line += ':'
                if prepopulated_value not in (None, 'None'):
                    line += ' {}'.format(prepopulated_value)
            lines.append(line)
        if self.menu_entries:
            lines.append('')
        return lines

    def _make_tab(self, n=1):
        tab_string = 6 * n * ' '
        if self.is_information_section:
            characters = list(tab_string)
            characters[-3:-1] = self._information_message_bullet
            tab_string = ''.join(characters)
        elif self.is_material_summary_section:
            characters = list(tab_string)
            characters[-2] = self._material_summary_bullet
            tab_string = ''.join(characters)
        return tab_string

    def _make_title_lines(self):
        menu_lines = []
        if isinstance(self.title, str):
            title_lines = [stringtools.capitalize_start(self.title)]
        elif isinstance(self.title, list):
            title_lines = self.title
        else:
            title_lines = []
        for title_line in title_lines:
            if self.indent_level:
                tab_string = self._make_tab(self.indent_level)
                line = '{}{}'.format(tab_string, title_line)
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
    def group_by_annotation(self):
        r'''Is true when entries should group by annotation.
        Otherwise false:

        ::

            >>> section.group_by_annotation
            False

        Returns boolean.
        '''
        return self._group_by_annotation

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
    def is_alphabetized(self):
        r'''Is true when menu section alphabetizes entries. Otherwise false.

        Returns boolean.
        '''
        return self._is_alphabetized

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
    def is_information_section(self):
        r'''Is true when menu section is information.
        Otherwise false:

        ::

            >>> section.is_information_section
            False

        Returns boolean.
        '''
        return self._is_information_section

    @property
    def is_material_summary_section(self):
        r'''Is true when menu section is material summary section.
        Otherwise false:

        ::

            >>> section.is_material_summary_section
            False

        Returns boolean.
        '''
        return self._is_material_summary_section

    @property
    def is_navigation_section(self):
        r'''Is true when menu section is navigation section.
        Otherwise false:

        ::

            >>> section.is_navigation_section
            False

        Returns boolean.
        '''
        return self._is_navigation_section

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
    def match_on_display_string(self):
        r'''Is true when section should match on display string. Otherwise
        false.

        ..  container::

            ::

                >>> section.match_on_display_string
                False

        Returns boolean.
        '''
        return self._match_on_display_string

    @property
    def menu_entries(self):
        r'''Menu section menu entries.

        ::

            >>> for menu_entry in section:
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

    def _append(self, expr):
        r'''Appends `expr` to menu section.

        ::

            >>> section._append(('foo - stub', 'stub'))
            <MenuEntry: 'foo - stub'>

        ::

            >>> for menu_entry in section:
            ...     menu_entry
            <MenuEntry: 'foo - add'>
            <MenuEntry: 'foo - delete'>
            <MenuEntry: 'foo - modify'>
            <MenuEntry: 'foo - stub'>

        Returns menu entry.
        '''
        from scoremanager import idetools
        if isinstance(expr, idetools.MenuEntry):
            new_expr = (
                expr.display_string,
                expr.key,
                expr.prepopulated_value,
                expr.explicit_return_value,
                )
            expr = new_expr
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
        menu_entry = idetools.MenuEntry(**kwargs)
        self.menu_entries.append(menu_entry)
        if self.is_command_section:
            if self.is_alphabetized:
                self.menu_entries.sort()
        return menu_entry