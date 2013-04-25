from abjad.tools import stringtools
from abjad.tools import mathtools
from experimental.tools.scoremanagertools.menuing.MenuObject import MenuObject


class MenuSection(MenuObject):

    def __init__(self, is_hidden=False, is_internally_keyed=False, is_keyed=True,
        is_numbered=False, is_parenthetically_numbered=False, is_ranged=False,
        is_read_only=False, session=None, where=None, title=None):
        MenuObject.__init__(self, session=session, where=where, title=title)
        self._is_hidden = is_hidden
        self._is_internally_keyed = is_internally_keyed
        self._is_keyed = is_keyed
        self._is_numbered = is_numbered
        self._is_parenthetically_numbered = is_parenthetically_numbered
        self._is_ranged = is_ranged
        self._return_value_attribute = 'key'
        self.default_index = None
        self.indent_level = 1
        self.show_existing_values = False
        self.tokens = None

    ### SPECIAL METHODS ###

    # TODO: write test
    def __len__(self):
        return len(self.tokens)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def default_value(self):
        assert self.has_default_value
        return self.menu_entry_return_values[self.default_index]

    @property
    def has_default_value(self):
        return self.default_index is not None

    @property
    def has_existing_value_tuple_tokens(self):
        return any([isinstance(x, tuple) and len(x) == 3 for x in self.tokens])

    @property
    def has_prepopulated_return_value_tuple_tokens(self):
        return any([isinstance(x, tuple) and len(x) == 4 for x in self.tokens])

    @property
    def has_string_tokens(self):
        return any([isinstance(x, str) for x in self.tokens])

    @property
    def has_tuple_tokens(self):
        return any([isinstance(x, tuple) for x in self.tokens])

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
    def is_parenthetically_numbered(self):
        return self._is_parenthetically_numbered

    @property
    def is_ranged(self):
        return self._is_ranged

    @property
    def is_read_only(self):
        return self._is_read_only

    @property
    def menu_entry_bodies(self):
        return [self.token_to_key_and_body(x)[1] for x in self.tokens]

    @property
    def menu_entry_keys(self):
        return [self.token_to_key_and_body(x)[0] for x in self.tokens]

    @property
    def menu_entry_return_values(self):
        return [self.token_to_menu_entry_return_value(x) for x in self.tokens]

    # TODO: rename these two properties to something more sensible when testing resumes
    @property
    def unpacked_menu_entries(self):
        result = []
        for token in self.tokens:
            result.append(self.unpack_token(token) + (self,))
        return result

    # TODO: rename these two properties to something more sensible when testing resumes
    @property
    def unpacked_menu_entries_optimized(self):
        result = []
        total_empty_tokens = 0
        for i, token in enumerate(self.tokens):
            if token == ():
                total_empty_tokens += 1
                continue
            number = key = body = None
            if self.is_numbered or self.is_parenthetically_numbered:
                number = i + 1 - total_empty_tokens
            if isinstance(token, str):
                body = token
            elif isinstance(token, tuple) and len(token) == 2:
                key, body = token
            elif isinstance(token, tuple) and len(token) == 3:
                key, body, existing_value = token
            elif isinstance(token, tuple) and len(token) == 4:
                key, body, existing_value, prepopulated_return_value = token
            else:
                raise ValueError
            assert body
            if self.is_keyed and key is None:
                key = body
            if self.return_value_attribute == 'number':
                if number is not None:
                    return_value = str(number)
                elif key is not None:
                    return_value = key
                else:
                    return_value = body
            elif self.return_value_attribute == 'key':
                if key is not None:
                    return_value = key
                else:
                    return_value = body
            elif self.return_value_attribute == 'body':
                return_value = body
            elif self.return_value_attribute == 'prepopulated':
                return_value = prepopulated_return_value
            else:
                raise ValueError
            assert return_value is not None
            if not self.is_keyed and key:
                key = None
            unpacked_entry = (number, key, body, return_value, self)
            result.append(unpacked_entry)
        return result

    ### READ / WRITE PUBLIC PROPERTIES ###

    @apply
    def default_index():
        def fget(self):
            return self._default_index
        def fset(self, default_index):
            assert isinstance(default_index, (int, type(None)))
            if isinstance(default_index, int):
                count = len(self.tokens)
                if default_index < 0:
                    raise ValueError('default index must be positive integer.')
                if count <= default_index:
                    raise ValueError('only {} menu entry tokens in section.'.format(count))
            self._default_index = default_index
        return property(**locals())

    @apply
    def return_value_attribute():
        def fget(self):
            return self._return_value_attribute
        def fset(self, return_value_attribute):
            assert return_value_attribute in ('body', 'key', 'number', 'prepopulated')
            self._return_value_attribute = return_value_attribute
        return property(**locals())

    @apply
    def tokens():
        def fget(self):
            return self._tokens
        def fset(self, tokens):
            if tokens is None:
                self._tokens = []
            else:
                self._tokens = tokens[:]
        return property(**locals())

    ### PUBLIC METHODS ###

    def append(self, token):
        assert not (isinstance(token, str) and self.has_tuple_tokens)
        assert not (isinstance(token, tuple) and self.has_string_tokens)
        self.tokens.append(token)

    def argument_range_string_to_numbers(self, argument_range_string):
        '''Return list of positive integers on success. Otherwise none.
        '''
        assert self.tokens
        numbers = []
        argument_range_string = argument_range_string.replace(' ', '')
        range_parts = argument_range_string.split(',')
        for range_part in range_parts:
            if range_part == 'all':
                numbers.extend(range(1, len(self.tokens) + 1))
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
        assert self.tokens
        numbers = []
        argument_range_string = argument_range_string.replace(' ', '')
        range_parts = argument_range_string.split(',')
        for range_part in range_parts:
            if range_part == 'all':
                numbers.extend(range(1, len(self.tokens) + 1))
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
            if menu_number <= len(self.tokens):
                return menu_number
        for menu_index, menu_return_value in enumerate(self.menu_entry_return_values):
            if argument_string == menu_return_value:
                return menu_index + 1
            elif 3 <= len(argument_string) and menu_return_value.startswith(argument_string):
                return menu_index + 1
        for menu_index, menu_key in enumerate(self.menu_entry_keys):
            if argument_string == menu_key:
                return menu_index + 1

    def argument_string_to_number_optimized(self, argument_string):
        for entry_index, unpacked_entry in enumerate(self.unpacked_menu_entries):
            number, key, body, return_value, section = unpacked_entry
            body = stringtools.strip_diacritics_from_binary_string(body).lower()
            if  (mathtools.is_integer_equivalent_expr(argument_string) and int(argument_string) == number) or \
                (argument_string == key) or \
                (3 <= len(argument_string) and body.startswith(argument_string)):
                entry_number = entry_index + 1
                return entry_number

    def extend(self, tokens):
        assert isinstance(tokens, (tuple, list))
        assert not (any([isinstance(x, str) for x in tokens]) and self.has_tuple_tokens)
        assert not (any([isinstance(x, tuple) for x in tokens]) and self.has_string_tokens)
        self.tokens.extend(tokens)

    def is_token(self, expr):
        if isinstance(expr, str):
            return True
        elif isinstance(expr, tuple) and len(expr) in (0, 2, 3, 4):
            return True
        return False

    def make_menu_lines(self):
        '''KEYS. Keys are optionally shown in parentheses in each entry;
        keys are designed to be textual instead of numeric;
        not every entry need have a key because entries may be numbered instead of keyed;
        note that entries may be both numbered and keyed.

        BODIES. Bodies are those things shown in each entry;
        bodies are positional and every entry must be supplied with a body.

        RESULT. Result is the thing ultimately returned by Menu.run().

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
        assert all([self.is_token(x) for x in self.tokens])
        total_empty_tokens = 0
        for entry_index, token in enumerate(self.tokens):
            menu_line = self.make_tab(self.indent_level) + ' '
            if token == ():
                menu_lines.append(menu_line)
                total_empty_tokens += 1
                continue
            key, body, existing_value = self.token_to_key_body_and_existing_value(token)
            if self.is_parenthetically_numbered:
                entry_number = entry_index + 1 - total_empty_tokens
                menu_line += '({}) '.format(str(entry_number))
            elif self.is_numbered:
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
        if self.tokens:
            menu_lines.append('')
        return menu_lines

    # TODO: this can probably deprecate in favor of self.token_to_key_body_and_existing_value
    def token_to_key_and_body(self, token):
        if isinstance(token, str):
            key, body = None, token
        elif isinstance(token, tuple):
            key, body = token[:2]
        else:
            raise ValueError
        return key, body

    def token_to_key_body_and_existing_value(self, token):
        if isinstance(token, str):
            key, body, existing_value = None, token, None
        elif isinstance(token, tuple) and len(token) == 2:
            key, body, existing_value = token[0], token[1], None
        elif isinstance(token, tuple) and len(token) == 3:
            key, body, existing_value = token
        elif isinstance(token, tuple) and len(token) == 4:
            key, body, existing_value = token[:3]
        else:
            raise ValueError
        return key, body, existing_value

    def token_to_menu_entry_number(self, token):
        if self.is_numbered or self.is_parenthetically_numbered:
            for i, x in enumerate(self.tokens):
                if x == token:
                    return i + 1

    def token_to_menu_entry_return_value(self, token):
        if isinstance(token, str):
            return token
        elif isinstance(token, tuple):
            if self.return_value_attribute == 'key':
                return token[0]
            elif self.return_value_attribute == 'body':
                return token[1]
            elif self.return_value_attribute == 'number':
                pass
            elif self.return_value_attribute == 'prepopulated':
                return token[3]
            else:
                raise ValueError
        else:
            raise ValueError

    # TODO: replace self.token_to_key_and_body() and also
    #       replace self.token_to_menu_entry_return_value().
    # TODO: unpack all menu entry tokens only once at runtime.
    def unpack_token(self, token):
        number = self.token_to_menu_entry_number(token)
        key, body = self.token_to_key_and_body(token)
        return_value = self.token_to_menu_entry_return_value(token)
        return number, key, body, return_value
