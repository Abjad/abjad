from abjad.tools import stringtools
from abjad.tools import mathtools
from experimental.tools.scoremanagertools.core.ScoreManagerObject.ScoreManagerObject import \
    ScoreManagerObject


class MenuSection(ScoreManagerObject):

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
        title=None,
        is_numbered=False,
        is_ranged=False,
        is_hidden=False,
        menu_tokens=None,
        return_value_attribute='display_string',
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
        self.menu_tokens = menu_tokens
        self.title = title
        self.where = where

    ### SPECIAL METHODS ###

    def __len__(self):
        return len(self.menu_tokens)

    def __repr__(self):
        return '{}({!r})'.format(self._class_name, self.menu_tokens)

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
                count = len(self.menu_tokens)
                if default_index < 0:
                    message = 'default index must be positive integer.'
                    raise ValueError(message)
                if count <= default_index:
                    message = 'only {} menu entry menu_tokens '
                    message += 'in menu_section.'
                    message = message.format(count)
                    raise ValueError(message)
            self._default_index = default_index
        return property(**locals())

    @property
    def default_value(self):
        assert self.has_default_value
        return self.menu_token_return_values[self.default_index]

    @property
    def has_default_value(self):
        return self.default_index is not None

    @apply
    def is_hidden():
        def fget(self):
            return self._is_hidden
        def fset(self, expr):
            if not self.menu_tokens:
                self._is_hidden = expr
        return property(**locals())

    @apply
    def is_numbered():
        def fget(self):
            return self._is_numbered
        def fset(self, expr):
            if not self.menu_tokens:
                self._is_numbered = expr
        return property(**locals())

    @apply
    def is_ranged():
        def fget(self):
            return self._is_ranged
        def fset(self, expr):
            if not self.menu_tokens:
                self._is_ranged = expr
        return property(**locals())

    @property
    def menu_token_display_strings(self):
        return [menu_token.display_string for menu_token in self.menu_tokens]

    @property
    def menu_token_keys(self):
        return [menu_token.key for menu_token in self.menu_tokens]

    @property
    def menu_token_return_values(self):
        return [menu_token.return_value for menu_token in self.menu_tokens]

    @apply
    def menu_tokens():
        def fget(self):
            return self._tokens
        def fset(self, menu_tokens):
            if menu_tokens is None:
                self._tokens = []
            elif isinstance(menu_tokens, list):
                self._tokens = []
                for menu_token in menu_tokens:
                    self.append(menu_token)
            else:
                raise TypeError(menu_tokens)
        return property(**locals())

    @apply
    def return_value_attribute():
        def fget(self):
            return self._return_value_attribute
        def fset(self, expr):
            if not self.menu_tokens:
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
            number = len(self.menu_tokens) + 1
        menu_token = scoremanagertools.menuing.MenuToken(
            expr,
            number=number,
            return_value_attribute=self.return_value_attribute,
            )
        self.menu_tokens.append(menu_token)
        
    def argument_range_string_to_numbers(self, argument_range_string):
        assert self.menu_tokens
        numbers = []
        argument_range_string = argument_range_string.replace(' ', '')
        range_parts = argument_range_string.split(',')
        for range_part in range_parts:
            if range_part == 'all':
                numbers.extend(range(1, len(self.menu_tokens) + 1))
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
        for menu_entry_index, menu_token in enumerate(self.menu_tokens):
            if menu_token.matches(argument_string):
                menu_entry_number = menu_entry_index + 1
                return menu_entry_number

    def make_menu_lines(self):
        menu_lines = []
        menu_lines.extend(self.make_title_lines())
        for menu_token in self.menu_tokens:
            menu_line = self._make_tab(self.indent_level) + ' '
            display_string = menu_token.display_string
            key = menu_token.key
            existing_value = menu_token.existing_value
            if self.is_numbered:
                menu_line += '{}: '.format(menu_token.number)
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
        if self.menu_tokens:
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
