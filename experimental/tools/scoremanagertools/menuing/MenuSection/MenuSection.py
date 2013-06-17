from abjad.tools import stringtools
from abjad.tools import mathtools
from experimental.tools.scoremanagertools.core.ScoreManagerObject.ScoreManagerObject import \
    ScoreManagerObject


class MenuSection(ScoreManagerObject):
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
        'prepopulated',
        )

    ### INITIALIZER ###

    def __init__(self,
        session=None,
        where=None,
        menu_entries=None,
        return_value_attribute='display_string',
        is_numbered=False,
        is_ranged=False,
        is_hidden=False,
        title=None,
        ):
        ScoreManagerObject.__init__(self, session=session)
        self._is_hidden = is_hidden
        self._is_numbered = is_numbered
        self._is_ranged = is_ranged
        assert return_value_attribute in self.return_value_attributes
        self._return_value_attribute = return_value_attribute
        self.default_index = None
        self.indent_level = 1
        self.show_existing_values = False
        self.menu_entries = menu_entries
        self.title = title
        self.where = where

    ### SPECIAL METHODS ###

    def __len__(self):
        return len(self.menu_entries)

    def __repr__(self):
        return '<{} ({})>'.format(self._class_name, len(self))

    ### PRIVATE PROPERTIES ###

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

    def _make_tab(self, n):
        return 4 * n * ' '

    ### PUBLIC PROPERTIES ###

    @apply
    def default_index():
        def fget(self):
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

    @property
    def default_value(self):
        default_menu_entry = self.menu_entries[self.default_index]
        return default_menu_entry.return_value

    @property
    def has_default_value(self):
        return self.default_index is not None

    @apply
    def is_hidden():
        def fget(self):
            return self._is_hidden
        def fset(self, expr):
            if not self.menu_entries:
                self._is_hidden = expr
        return property(**locals())

    @apply
    def is_numbered():
        def fget(self):
            return self._is_numbered
        def fset(self, expr):
            if not self.menu_entries:
                self._is_numbered = expr
        return property(**locals())

    @apply
    def is_ranged():
        def fget(self):
            return self._is_ranged
        def fset(self, expr):
            if not self.menu_entries:
                self._is_ranged = expr
        return property(**locals())

    @apply
    def menu_entries():
        def fget(self):
            return self._tokens
        def fset(self, menu_entries):
            if menu_entries is None:
                self._tokens = []
            elif isinstance(menu_entries, list):
                self._tokens = []
                for menu_entry in menu_entries:
                    self.append(menu_entry)
            else:
                raise TypeError(menu_entries)
        return property(**locals())

    @apply
    def return_value_attribute():
        def fget(self):
            return self._return_value_attribute
        def fset(self, expr):
            if not self.menu_entries:
                self._return_value_attribute = expr
        return property(**locals())
    
    @apply
    def title():
        def fget(self):
            return self._title
        def fset(self, title):
            assert isinstance(title, (str, list, type(None)))
            self._title = title
        return property(**locals())

    ### PUBLIC METHODS ###

    def append(self, expr):
        from experimental.tools import scoremanagertools
        assert isinstance(expr, (str, tuple))
        number = None
        if self.is_numbered:
            number = len(self.menu_entries) + 1
        menu_entry = scoremanagertools.menuing.MenuEntry(
            expr,
            number=number,
            return_value_attribute=self.return_value_attribute,
            )
        self.menu_entries.append(menu_entry)
        
    def argument_range_string_to_numbers(self, argument_range_string):
        assert self.menu_entries
        numbers = []
        argument_range_string = argument_range_string.replace(' ', '')
        range_parts = argument_range_string.split(',')
        for range_part in range_parts:
            if range_part == 'all':
                numbers.extend(range(1, len(self.menu_entries) + 1))
            elif '-' in range_part:
                start, stop = range_part.split('-')
                start = self.argument_string_to_number(start)
                stop = self.argument_string_to_number(stop)
                if start is None or stop is None:
                    return
                if start <= stop:
                    new_numbers = range(start, stop + 1)
                    numbers.extend(new_numbers)
                else:
                    new_numbers = range(start, stop - 1, -1)
                    numbers.extend(new_numbers)
            else:
                number = self.argument_string_to_number(range_part)
                if number is None:
                    return
                numbers.append(number)
        return numbers

    def argument_string_to_number(self, argument_string):
        for menu_entry_index, menu_entry in enumerate(self.menu_entries):
            if menu_entry.matches(argument_string):
                menu_entry_number = menu_entry_index + 1
                return menu_entry_number

    def make_menu_lines(self):
        menu_lines = []
        menu_lines.extend(self.make_title_lines())
        for menu_entry in self.menu_entries:
            menu_line = self._make_tab(self.indent_level) + ' '
            display_string = menu_entry.display_string
            key = menu_entry.key
            existing_value = menu_entry.existing_value
            if self.is_numbered:
                menu_line += '{}: '.format(menu_entry.number)
            if key:
                if self.show_existing_values and existing_value:
                    if existing_value in (None, 'None'):
                        menu_line += '{} ({}):'.format(display_string, key)
                    else:
                        menu_line += '{} ({}): {}'.format(
                            display_string, key, existing_value)
                else:
                    menu_line += '{} ({})'.format(display_string, key)
            else:
                if self.show_existing_values and existing_value:
                    if existing_value in (None, 'None'):
                        menu_line += '{}:'.format(display_string)
                    else:
                        menu_line += '{}: {}'.format(
                            display_string, existing_value)
                else:
                    menu_line += '{}'.format(display_string)
            menu_lines.append(menu_line)
        if self.menu_entries:
            menu_lines.append('')
        return menu_lines

    def make_title_lines(self):
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
