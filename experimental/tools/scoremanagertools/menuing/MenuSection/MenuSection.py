from abjad.tools import stringtools
from abjad.tools import mathtools
from experimental.tools.scoremanagertools.menuing.MenuObject import MenuObject
from experimental.tools.scoremanagertools.menuing.MenuToken import MenuToken


class MenuSection(MenuObject):

    ### CLASS VARIABLES ###

    return_value_attributes = ('body', 'key', 'number', 'prepopulated')

    ### INITIALIZER ###

    def __init__(self,
        is_hidden=False,
        is_internally_keyed=False,
        is_keyed=False,
        is_numbered=False,
        is_ranged=False,
        is_read_only=False,
        session=None,
        where=None,
        title=None,
        menu_tokens=None,
        return_value_attribute='body',
        ):
        MenuObject.__init__(self, session=session, where=where, title=title)
        self._is_hidden = is_hidden
        self._is_internally_keyed = is_internally_keyed
        self._is_keyed = is_keyed
        self._is_numbered = is_numbered
        self._is_ranged = is_ranged
        assert return_value_attribute in self.return_value_attributes, repr(return_value_attribute)
        self._return_value_attribute = return_value_attribute
        self.default_index = None
        self.indent_level = 1
        self.show_existing_values = False
        self.menu_tokens = menu_tokens

    ### SPECIAL METHODS ###

    def __len__(self):
        return len(self.menu_tokens)

    def __repr__(self):
        return '{}({!r})'.format(self._class_name, self.menu_tokens)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def default_value(self):
        assert self.has_default_value
        return self.menu_token_return_values[self.default_index]

    @property
    def has_default_value(self):
        return self.default_index is not None

    @property
    def is_hidden(self):
        return self._is_hidden

    @property
    def is_internally_keyed(self):
        return self._is_internally_keyed

    @property
    def is_keyed(self):
        return self._is_keyed

    @property
    def is_numbered(self):
        return self._is_numbered

    @property
    def is_ranged(self):
        return self._is_ranged

    @property
    def is_read_only(self):
        return self._is_read_only

    @property
    def menu_token_bodies(self):
        return [menu_token.body for menu_token in self.menu_tokens]

    @property
    def menu_token_keys(self):
        return [menu_token.key for menu_token in self.menu_tokens]

    @property
    def menu_token_return_values(self):
        return [menu_token.return_value for menu_token in self.menu_tokens]

    ### READ / WRITE PUBLIC PROPERTIES ###

    @apply
    def default_index():
        def fget(self):
            return self._default_index
        def fset(self, default_index):
            assert isinstance(default_index, (int, type(None)))
            if isinstance(default_index, int):
                count = len(self.menu_tokens)
                if default_index < 0:
                    raise ValueError('default index must be positive integer.')
                if count <= default_index:
                    raise ValueError('only {} menu entry menu_tokens in menu_section.'.format(count))
            self._default_index = default_index
        return property(**locals())

    @apply
    def menu_tokens():
        def fget(self):
            return self._tokens
        def fset(self, menu_tokens):
            if menu_tokens is None:
                self._tokens = []
            elif isinstance(menu_tokens, list):
                new_tokens = []
                for i, menu_token in enumerate(menu_tokens):
                    if isinstance(menu_token, MenuToken):
                        menu_token = menu_token._to_tuple()
                    assert isinstance(menu_token, (str, tuple))
                    if self.is_numbered:
                        number = i + 1
                    else:
                        number = None
                    new_token = MenuToken(
                        menu_token,
                        number=number,
                        is_keyed=self.is_keyed,
                        return_value_attribute=self.return_value_attribute)
                    new_tokens.append(new_token)
                self._tokens = new_tokens
            else:
                raise TypeError(menu_tokens)
        return property(**locals())

    @property
    def return_value_attribute(self):
        return self._return_value_attribute

    ### PUBLIC METHODS ###

    def argument_range_string_to_numbers(self, argument_range_string):
        '''Return list of positive integers on success. Otherwise none.
        '''
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

    def argument_range_string_to_numbers_optimized(self, argument_range_string):
        assert self.menu_tokens
        numbers = []
        argument_range_string = argument_range_string.replace(' ', '')
        range_parts = argument_range_string.split(',')
        for range_part in range_parts:
            if range_part == 'all':
                numbers.extend(range(1, len(self.menu_tokens) + 1))
            elif '-' in range_part:
                start, stop = range_part.split('-')
                start = self.argument_string_to_number_optimized(start)
                stop = self.argument_string_to_number_optimized(stop)
                if start is None or stop is None:
                    return
                if start <= stop:
                    new_numbers = range(start, stop + 1)
                    numbers.extend(new_numbers)
                else:
                    new_numbers = range(start, stop - 1, -1)
                    numbers.extend(new_numbers)
            else:
                number = self.argument_string_to_number_optimized(range_part)
                if number is None:
                    return
                numbers.append(number)
        return numbers

    def argument_string_to_number(self, argument_string):
        '''Return number when successful. Otherwise none.
        '''
        if mathtools.is_integer_equivalent_expr(argument_string):
            menu_number = int(argument_string)
            if menu_number <= len(self.menu_tokens):
                return menu_number
        for menu_index, menu_return_value in enumerate(self.menu_token_return_values):
            if argument_string == menu_return_value:
                return menu_index + 1
            elif 3 <= len(argument_string) and menu_return_value.startswith(argument_string):
                return menu_index + 1
        for menu_index, menu_key in enumerate(self.menu_token_keys):
            if argument_string == menu_key:
                return menu_index + 1

    def argument_string_to_number_optimized(self, argument_string):
        for menu_entry_index, menu_token in enumerate(self.menu_tokens):
            if menu_token.matches(argument_string):
                menu_entry_number = menu_entry_index + 1
                return menu_entry_number

    def make_menu_lines(self):
        '''KEYS. Keys are optionally shown in parentheses in each entry;
        keys are designed to be textual instead of numeric;
        not every entry need have a key because entries may be numbered instead of keyed;
        note that entries may be both numbered and keyed.

        BODIES. Bodies are those things shown in each entry;
        bodies are positional and every entry must be supplied with a body.

        RESULT. Result is the thing ultimately returned by Menu._run().

        Match determination:
        1. Numeric user input checked against numbered entries.
        2. If key exists, textual user input checked for exact match against key.
        3. Textual user input checked for 3-char match against body.
        4. Otherwise, no match found.

        Return value resolution:
        Keyed entries (numbered or not) supply key as return value.
        Nonkeyed entries (always numbered) supply body as return value.
        '''
        menu_lines = []
        menu_lines.extend(self.make_title_lines())
        assert all(isinstance(menu_token, MenuToken) for menu_token in self.menu_tokens), repr(self.menu_tokens)
        total_empty_tokens = 0
        for entry_index, menu_token in enumerate(self.menu_tokens):
            menu_line = self.make_tab(self.indent_level) + ' '
            if menu_token == ():
                menu_lines.append(menu_line)
                total_empty_tokens += 1
                continue
            key, body, existing_value = menu_token.key, menu_token.body, menu_token.existing_value
            if self.is_numbered:
                entry_number = entry_index + 1 - total_empty_tokens
                menu_line += '{}: '.format(str(entry_number))
            if key and self.is_keyed:
                if self.show_existing_values and existing_value:
                    if existing_value in (None, 'None'):
                        menu_line += '{} ({}):'.format(body, key)
                    else:
                        menu_line += '{} ({}): {}'.format(body, key, existing_value)
                else:
                    menu_line += '{} ({})'.format(body, key)
            else:
                if self.show_existing_values and existing_value:
                    if existing_value in (None, 'None'):
                        menu_line += '{}:'.format(body)
                    else:
                        menu_line += '{}: {}'.format(body, existing_value)
                else:
                    menu_line += '{}'.format(body)
            menu_lines.append(menu_line)
        if self.menu_tokens:
            menu_lines.append('')
        return menu_lines
