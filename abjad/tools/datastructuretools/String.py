# -*- coding: utf-8 -*-
import re
import six
import sys
import textwrap
import unicodedata


class String(str):
    r'''String.
    '''

    ### CLASS VARIABLES ###

    hyphen_delimited_lowercase_regex_body = '(([a-z,0-9]+[-]+)*[a-z,0-9]+)?'
    hyphen_delimited_lowercase_regex = re.compile(
        '^{}$'.format(hyphen_delimited_lowercase_regex_body),
        re.VERBOSE,
        )

    hyphen_delimited_lowercase_file_name_regex_body = """
        {}
        (\.[a-z,0-9]+)?
        """.format(hyphen_delimited_lowercase_regex_body)

    hyphen_delimited_lowercase_file_name_regex = re.compile(
        '^{}$'.format(hyphen_delimited_lowercase_file_name_regex_body),
        re.VERBOSE,
        )

    lowercamelcase_regex = re.compile(
        '^([a-z,0-9]+([A-Z,0-9]+[a-z,0-9]*)*)?$',
        re.VERBOSE,
        )

    space_delimited_lowercase_regex = re.compile(
        '^(([a-z,0-9]+[ ]+)*[a-z,0-9]+)?$',
        re.VERBOSE,
        )

    underscore_delimited_lowercase_regex_body = '(([a-z,0-9]+[_]+)*[a-z,0-9]+)?'
    underscore_delimited_lowercase_regex = re.compile(
        '^{}$'.format(underscore_delimited_lowercase_regex_body),
        re.VERBOSE,
        )

    underscore_delimited_lowercase_file_name_regex_body = """
        {}
        (\.[a-z,0-9]+)?
        """.format(underscore_delimited_lowercase_regex_body)

    underscore_delimited_lowercase_file_name_regex = re.compile(
        '^{}$'.format(underscore_delimited_lowercase_file_name_regex_body),
        re.VERBOSE,
        )

    underscore_delimited_lowercase_file_name_with_extension_regex_body = """
        {}
        \.
        [a-z,0-9]+
        """.format(underscore_delimited_lowercase_regex_body)

    underscore_delimited_lowercase_file_name_with_extension_regex = re.compile(
        '^{}$'.format(underscore_delimited_lowercase_file_name_with_extension_regex_body),
        re.VERBOSE,
        )

    underscore_delimited_lowercase_package_regex_body = """
        ({}\.)*
        {}
        """.format(
            underscore_delimited_lowercase_regex_body,
            underscore_delimited_lowercase_regex_body
            )

    underscore_delimited_lowercase_package_regex = re.compile(
        '^{}$'.format(underscore_delimited_lowercase_package_regex_body),
        re.VERBOSE,
        )

    uppercamelcase_regex = re.compile(
        '^([A-Z,0-9]+[a-z,0-9]*)*$',
        re.VERBOSE,
        )

    ### PUBLIC METHODS ###

    def capitalize_start(self):
        r'''Capitalizes start of string.

        ..  container:: example

            ::

                >>> abjad.String('violin I').capitalize_start()
                'Violin I'

        Function differs from built-in ``string.capitalize()``.

        This function affects only ``string[0]`` and leaves noninitial
        characters as-is.

        Built-in ``string.capitalize()`` forces noninitial characters to
        lowercase.

        ..  container:: example

            ::

                >>> 'violin I'.capitalize()
                'Violin i'

        Returns new string.
        '''
        if not self:
            return ''
        return self[0].upper() + self[1:]

    def delimit_words(self):
        r'''Delimits words in string.

        ..  container:: example

            Delimits words::

                >>> string = abjad.String('scale degrees 4 and 5.')
                >>> string.delimit_words()
                ['scale', 'degrees', '4', 'and', '5']

        ..  container:: example

            Delimits conjoined words::

                >>> string = abjad.String('scale degrees 4and5.')
                >>> string.delimit_words()
                ['scale', 'degrees', '4', 'and', '5']

        ..  container:: example

            Delimits lower camel case::

                >>> string = abjad.String('scaleDegrees4and5.')
                >>> string.delimit_words()
                ['scale', 'Degrees', '4', 'and', '5']

        ..  container:: example

            Delimits upper camel case::

                >>> string = abjad.String('ScaleDegrees4and 5.')
                >>> string.delimit_words()
                ['Scale', 'Degrees', '4', 'and', '5']

        ..  container:: example

            Delimits dash case::

                >>> string = abjad.String('scale-degrees-4-and-5.')
                >>> string.delimit_words()
                ['scale', 'degrees', '4', 'and', '5']

        ..  container:: example

            Delimits shout case::

                >>> string = abjad.String('SCALE_DEGREES_4_AND_5.')
                >>> string.delimit_words()
                ['SCALE', 'DEGREES', '4', 'AND', '5']

        ..  container:: example

            Works with greater-than and less-than signs:

                >>> string = abjad.String('one < two')
                >>> string.delimit_words()
                ['one', '<', 'two']

        ..  container:: example

            Works with exclamation points:

                >>> string = abjad.String('one! two!')
                >>> string.delimit_words()
                ['one', '!', 'two', '!']

        Returns list.
        '''
        wordlike_characters = ('<', '>', '!')
        words = []
        current_word = ''
        for character in self:
            if (not character.isalpha() and
                not character.isdigit() and
                not character in wordlike_characters
                ):
                if current_word:
                    words.append(current_word)
                    current_word = ''
            elif not current_word:
                current_word = current_word + character
            elif character.isupper():
                if current_word[-1].isupper():
                    current_word = current_word + character
                else:
                    words.append(current_word)
                    current_word = character
            elif character.islower():
                if current_word[-1].isalpha():
                    current_word = current_word + character
                else:
                    words.append(current_word)
                    current_word = character
            elif character.isdigit():
                if current_word[-1].isdigit():
                    current_word = current_word + character
                else:
                    words.append(current_word)
                    current_word = character
            elif character in wordlike_characters:
                if current_word[-1] in wordlike_characters:
                    current_word = current_word + character
                else:
                    words.append(current_word)
                    current_word = character
        if current_word:
            words.append(current_word)
        return words

    def is_dash_case(self):
        r'''Is true when string is hyphen-delimited lowercase.

        ..  container:: example

            ::

                >>> abjad.String('foo-bar').is_dash_case()
                True

        Otherwise false:

        ..  container:: example

            ::

                >>> abjad.String('foo bar').is_dash_case()
                False

        Returns true or false.
        '''
        return bool(String.hyphen_delimited_lowercase_regex.match(self))

    def is_dash_case_file_name(self):
        r'''Is true when string is hyphen-delimited lowercase file name with
        extension.

        ..  container:: example

            ::

                >>> abjad.String('foo-bar').is_dash_case_file_name()
                True

        Otherwise false:

        ..  container:: example

            ::

                >>> abjad.String('foo.bar.blah').is_dash_case_file_name()
                False

        Returns true or false.
        '''
        if self == '':
            return True
        return bool(
            String.hyphen_delimited_lowercase_file_name_regex.match(self)
            )

    def is_lower_camel_case(self):
        r'''Is true when string and is lowercamelcase.

        ..  container:: example

            ::

                >>> abjad.String('fooBar').is_lower_camel_case()
                True

        Otherwise false:

        ..  container:: example

            ::

                >>> abjad.String('FooBar').is_lower_camel_case()
                False

        Returns true or false.
        '''
        return bool(String.lowercamelcase_regex.match(self))

    def is_snake_case(self):
        r'''Is true when string is underscore-delimited lowercase.

        ..  container:: example

            ::

                >>> abjad.String('foo_bar').is_snake_case()
                True

        Otherwise false:

        ..  container:: example

            ::

                >>> abjad.String('foo bar').is_snake_case()
                False

        Returns true or false.
        '''
        return bool(String.underscore_delimited_lowercase_regex.match(self))

    def is_snake_case_file_name(self):
        r'''Is true when string is underscore-delimited lowercase file name.

        ..  container:: example

            ::

                >>> abjad.String('foo_bar').is_snake_case_file_name()
                True

        Otherwise false:

        ..  container:: example

            ::

                >>> abjad.String('foo.bar.blah').is_snake_case_file_name()
                False

        Returns true or false.
        '''
        if self == '':
            return True
        return bool(
            String.underscore_delimited_lowercase_file_name_regex.match(self)
            )

    def is_snake_case_file_name_with_extension(self):
        r'''Is true when string is underscore-delimited lowercase file name
        with extension.

        ..  container:: example

            ::

                >>> string = abjad.String('foo_bar.blah')
                >>> string.is_snake_case_file_name_with_extension()
                True

        Otherwise false:

        ..  container:: example

            ::

                >>> string = abjad.String('foo.bar.blah')
                >>> string.is_snake_case_file_name_with_extension()
                False

        Returns true or false.
        '''
        if self == '':
            return True
        return bool(
            String.underscore_delimited_lowercase_file_name_with_extension_regex.match(
                self))

    def is_snake_case_package_name(self):
        r'''Is true when string is underscore-delimited lowercase package name.

        ..  container:: example

            ::

                >>> string = abjad.String('foo.bar.blah_package')
                >>> string.is_snake_case_package_name()
                True

        Otherwise false:

        ..  container:: example

            ::

                >>> string = abjad.String('foo.bar.BlahPackage')
                >>> string.is_snake_case_package_name()
                False

        Returns true or false.
        '''
        return bool(
            String.underscore_delimited_lowercase_package_regex.match(self)
            )

    def is_space_delimited_lowercase(self):
        r'''Is true when string is space-delimited lowercase.

        ..  container:: example

            ::

                >>> abjad.String('foo bar').is_space_delimited_lowercase()
                True

        Otherwise false:

        ..  container:: example

            ::

                >>> abjad.String('foo_bar').is_space_delimited_lowercase()
                False

        Returns true or false.
        '''
        return bool(String.space_delimited_lowercase_regex.match(self))

    @staticmethod
    def is_string(argument):
        r'''Is true when `argument` is a string.

        Otherwise false.

        Returns true or false.
        '''
        return isinstance(argument, six.string_types)

    def is_upper_camel_case(self):
        r'''Is true when string upper camel case.

        ..  container:: example

            ::

                >>> abjad.String('FooBar').is_upper_camel_case()
                True

        Otherwise false:

        ..  container:: example

            ::

                >>> abjad.String('fooBar').is_upper_camel_case()
                False

        Returns true or false.
        '''
        return bool(String.uppercamelcase_regex.match(self))

    @staticmethod
    def normalize(argument, indent=None):
        r"""Normalizes string.

        ..  container:: example

            ::

                >>> string = r'''
                ...     foo
                ...         bar
                ... '''
                >>> print(string)
                <BLANKLINE>
                    foo
                        bar
                <BLANKLINE>

            ::

                >>> print(abjad.String.normalize(string))
                foo
                    bar

            ::

                >>> print(abjad.String.normalize(string, indent=4))
                    foo
                        bar

            ::

                >>> print(abjad.String.normalize(string, indent='* '))
                * foo
                *     bar

        Returns new string.
        """
        string = argument.replace('\t', '    ')
        lines = string.split('\n')
        while lines and (not lines[0] or lines[0].isspace()):
            lines.pop(0)
        while lines and (not lines[-1] or lines[-1].isspace()):
            lines.pop()
        for i, line in enumerate(lines):
            lines[i] = line.rstrip()
        string = '\n'.join(lines)
        string = textwrap.dedent(string)
        if indent:
            if not isinstance(indent, six.string_types):
                indent = ' ' * abs(int(indent))
            lines = string.split('\n')
            for i, line in enumerate(lines):
                if line:
                    lines[i] = '{}{}'.format(indent, line)
            string = '\n'.join(lines)
        return string

    def pluralize(self, count=None):
        r'''Pluralizes English string.
        
        ..  container:: example

            Changes terminal `-y` to `-ies`:

            ::

                >>> abjad.String('catenary').pluralize()
                'catenaries'

        ..  container:: example

            Adds `-es` to terminal `-s`, `-sh`, `-x` and `-z`:

            ::

                >>> abjad.String('brush').pluralize()
                'brushes'

        ..  container:: example

            Adds `-s` to all other strings:

            ::

                >>> abjad.String('shape').pluralize()
                'shapes'

        Returns string.
        '''
        if count == 1:
            return self
        if self.endswith('y'):
            return self[:-1] + 'ies'
        elif self.endswith(('s', 'sh', 'x', 'z')):
            return self + 'es'
        else:
            return self + 's'

    def strip_diacritics(self):
        r'''Strips diacritics from binary string.

        ..  container:: example

            ::

                >>> binary_string = abjad.String('Dvořák')

            ::

                >>> print(binary_string)
                Dvořák

            ::

                >>> binary_string.strip_diacritics()
                'Dvorak'

        Returns ASCII string.
        '''
        if sys.version_info[0] < 3:
            unicode_string = unicode(self, 'utf-8')
        else:
            unicode_string = self
        normalized_unicode_string = unicodedata.normalize('NFKD', unicode_string)
        ascii_string = normalized_unicode_string.encode('ascii', 'ignore')
        if sys.version_info[0] < 3:
            return ascii_string
        else:
            return ascii_string.decode('utf-8')

    def to_accent_free_snake_case(self):
        '''Changes string to accent-free snake case.

        ..  container:: example

            ::

                    
                >>> abjad.String('Déja vu').to_accent_free_snake_case()
                'deja_vu'

        Strips accents from accented characters.

        Changes all punctuation (including spaces) to underscore.

        Sets to lowercase.

        Returns new string.
        '''
        string = self.strip_diacritics()
        string = string.replace(' ', '_')
        string = string.replace("'", '_')
        string = string.lower()
        return string

    @staticmethod
    def to_bidirectional_direction_string(argument):
        r'''Changes `argument` to bidirectional direction string.

        ..  container:: example:

            ::

                >>> abjad.String.to_bidirectional_direction_string('^')
                'up'

        ..  container:: example:

            ::

                >>> abjad.String.to_bidirectional_direction_string('_')
                'down'

        ..  container:: example:

            ::

                >>> abjad.String.to_bidirectional_direction_string(1)
                'up'

        ..  container:: example:

            ::

                >>> abjad.String.to_bidirectional_direction_string(-1)
                'down'

        Returns `argument` when `argument` is `'up'` or `'down'`.

        Returns string or none.
        '''
        lookup = {
            1: 'up',
            -1: 'down',
            Up: 'up',
            Down: 'down',
            '^': 'up',
            '_': 'down',
            'up': 'up',
            'down': 'down'
            }
        if argument in lookup:
            return lookup[argument]
        raise ValueError(argument)

    @staticmethod
    def to_bidirectional_lilypond_symbol(argument):
        r'''Changes `argument` to bidirectional LilyPond symbol.

        ..  container:: example

            ::

                >>> abjad.String.to_tridirectional_lilypond_symbol(Up)
                '^'

        ..  container:: example

            ::

                >>> abjad.String.to_tridirectional_lilypond_symbol(Down)
                '_'

        ..  container:: example

            ::

                >>> abjad.String.to_tridirectional_lilypond_symbol(1)
                '^'

        ..  container:: example

            ::

                >>> abjad.String.to_tridirectional_lilypond_symbol(-1)
                '_'

        Returns `argument` when `argument` is `'^'` or `'_'`.

        Returns string or none.
        '''
        lookup = {
            1: '^',
            -1: '_',
            Up: '^',
            Down: '_',
            'up': '^',
            'down': '_',
            '^': '^',
            '_': '_',
            }
        if argument in lookup:
            return lookup[argument]
        raise ValueError(argument)

    def to_dash_case(self):
        r'''Changes string to dash case.

        ..  container:: example

            Changes words to dash case:

            ::

                >>> abjad.String('scale degrees 4 and 5').to_dash_case()
                'scale-degrees-4-and-5'

        ..  container:: example

            Changes snake case to dash case:

            ::

                >>> abjad.String('scale_degrees_4_and_5').to_dash_case()
                'scale-degrees-4-and-5'

        ..  container:: example

            Changes dash case to dash case:

            ::

                >>> abjad.String('scale-degrees-4-and-5').to_dash_case()
                'scale-degrees-4-and-5'

        ..  container:: example

            Changes upper camel case to dash case:

            ::

                >>> abjad.String('ScaleDegrees4And5').to_dash_case()
                'scale-degrees-4-and-5'

        Returns string.
        '''
        words = self.delimit_words()
        words = [_.lower() for _ in words]
        string = '-'.join(words)
        return string

    def to_lower_camel_case(self):
        r'''Changes string to lower camel case.

        ..  container:: example

            Changes words to lower camel case:

            ::

                >>> abjad.String('scale degrees 4 and 5').to_lower_camel_case()
                'scaleDegrees4And5'

        ..  container:: example

            Changes snake case to lower camel case:

            ::

                >>> abjad.String('scale_degrees_4_and_5').to_lower_camel_case()
                'scaleDegrees4And5'

        ..  container:: example

            Changes dash case to lower camel case:

            ::

                >>> abjad.String('scale-degrees-4-and-5').to_lower_camel_case()
                'scaleDegrees4And5'

        ..  container:: example

            Changes upper camel case to lower camel case:

            ::

                >>> abjad.String('ScaleDegrees4And5').to_lower_camel_case()
                'scaleDegrees4And5'

        Returns string.
        '''
        string = self.to_upper_camel_case()
        if string == '':
            return string
        string = string[0].lower() + string[1:]
        return string

    def to_snake_case(self):
        r'''Changes string to snake case.

        ..  container:: example

            Changes words to snake case:

            ::

                >>> abjad.String('scale degrees 4 and 5').to_snake_case()
                'scale_degrees_4_and_5'

        ..  container:: example

            Changes snake case to snake case:

            ::

                >>> abjad.String('scale_degrees_4_and_5').to_snake_case()
                'scale_degrees_4_and_5'

        ..  container:: example

            Changes dash case to snake case:

            ::

                >>> abjad.String('scale-degrees-4-and-5').to_snake_case()
                'scale_degrees_4_and_5'

        ..  container:: example

            Changes upper camel case to snake case:

            ::

                >>> abjad.String('ScaleDegrees4And5').to_snake_case()
                'scale_degrees_4_and_5'

        Returns string.
        '''
        words = self.delimit_words()
        words = [_.lower() for _ in words]
        string = '_'.join(words)
        return string

    def to_space_delimited_lowercase(self):
        r'''Changes string to space-delimited lowercase.
        
        ..  container:: example

            Changes upper camel case `string` to space-delimited lowercase:

            ::

                >>> abjad.String('LogicalTie').to_space_delimited_lowercase()
                'logical tie'

        ..  container:: example

            Changes underscore-delimited `string` to space-delimited lowercase:

            ::

                >>> abjad.String('logical_tie').to_space_delimited_lowercase()
                'logical tie'

        ..  container:: example

            Returns space-delimited string unchanged:

            ::

                >>> abjad.String('logical tie').to_space_delimited_lowercase()
                'logical tie'

        ..  container:: example

            Returns empty string unchanged:

            ::

                >>> abjad.String('').to_space_delimited_lowercase()
                ''

        Returns string.
        '''
        if not self:
            return self
        elif self[0].isupper():
            words = []
            current_word = self[0].lower()
            for letter in self[1:]:
                if letter.isupper():
                    words.append(current_word)
                    current_word = letter.lower()
                else:
                    current_word = current_word + letter
            words.append(current_word)
            string = ' '.join(words)
            return string
        return self.replace('_', ' ')

    @staticmethod
    def to_tridirectional_direction_string(argument):
        r'''Changes `argument` to tridirectional direction string.

        ..  container:: example

            ::

                >>> abjad.String.to_tridirectional_direction_string('^')
                'up'

        ..  container:: example

            ::

                >>> abjad.String.to_tridirectional_direction_string('-')
                'center'

        ..  container:: example

            ::

                >>> abjad.String.to_tridirectional_direction_string('_')
                'down'

        ..  container:: example

            ::

                >>> abjad.String.to_tridirectional_direction_string(1)
                'up'

        ..  container:: example

            ::

                >>> abjad.String.to_tridirectional_direction_string(0)
                'center'

        ..  container:: example

            ::

                >>> abjad.String.to_tridirectional_direction_string(-1)
                'down'

        ..  container:: example

            ::

                >>> abjad.String.to_tridirectional_direction_string('default')
                'center'

        Returns none when `argument` is none.

        Returns string or none.
        '''
        lookup = {
            Up: 'up',
            '^': 'up',
            'up': 'up',
            1: 'up',
            Down: 'down',
            '_': 'down',
            'down': 'down',
            -1: 'down',
            Center: 'center',
            '-': 'center',
            0: 'center',
            'center': 'center',
            'default': 'center',
            'neutral': 'center',
            }
        if argument is None:
            return None
        elif argument in lookup:
            return lookup[argument]
        raise ValueError(argument)
        
    @staticmethod
    def to_tridirectional_lilypond_symbol(argument):
        r'''Changes `argument` to tridirectional LilyPond symbol.

        ..  container:: example

            ::

                >>> abjad.String.to_tridirectional_lilypond_symbol(Up)
                '^'

        ..  container:: example

            ::

                >>> abjad.String.to_tridirectional_lilypond_symbol('neutral')
                '-'

        ..  container:: example

            ::

                >>> abjad.String.to_tridirectional_lilypond_symbol('default')
                '-'

        ..  container:: example

            ::

                >>> abjad.String.to_tridirectional_lilypond_symbol(Down)
                '_'

        ..  container:: example

            ::

                >>> abjad.String.to_tridirectional_lilypond_symbol(1)
                '^'

        ..  container:: example

            ::

                >>> abjad.String.to_tridirectional_lilypond_symbol(0)
                '-'

        ..  container:: example

            ::

                >>> abjad.String.to_tridirectional_lilypond_symbol(-1)
                '_'

        Returns none when `argument` is none.

        Returns `argument` when `argument` is `'^'`, `'-'` or `'_'`.

        Returns string or none.
        '''
        lookup = {
            Up: '^',
            '^': '^',
            'up': '^',
            1: '^',
            Down: '_',
            '_': '_',
            'down': '_',
            -1: '_',
            Center: '-',
            '-': '-',
            0: '-',
            'center': '-',
            'default': '-',
            'neutral': '-',
            }
        if argument is None:
            return None
        elif argument in lookup:
            return lookup[argument]
        raise ValueError(argument)

    @staticmethod
    def to_tridirectional_ordinal_constant(argument):
        r'''Changes `argument` to tridirectional ordinal constant.

        ..  container:: example

                >>> abjad.String.to_tridirectional_ordinal_constant('^')
                Up

        ..  container:: example

            ::

                >>> abjad.String.to_tridirectional_ordinal_constant('_')
                Down

        ..  container:: example

            ::

                >>> abjad.String.to_tridirectional_ordinal_constant(1)
                Up

        ..  container:: example

            ::

                >>> abjad.String.to_tridirectional_ordinal_constant(-1)
                Down

        Returns `argument` when `argument` is `Up`', `Center` or `Down`.

        Returns ordinal constant or none.
        '''
        lookup = {
            Up: Up,
            '^': Up,
            'up': Up,
            1: Up,
            Down: Down,
            '_': Down,
            'down': Down,
            -1: Down,
            Center: Center,
            '-': Center,
            0: Center,
            'center': Center,
            'default': Center,
            'neutral': Center,
            }
        if argument is None:
            return None
        elif argument in lookup:
            return lookup[argument]
        message = 'unrecognized expression: {!r}.'
        message = message.format(argument)
        raise ValueError(message)

    def to_upper_camel_case(self):
        r'''Changes string to upper camel case.

        ..  container:: example

            Changes words to upper camel case:

            ::

                >>> abjad.String('scale degrees 4 and 5').to_upper_camel_case()
                'ScaleDegrees4And5'

        ..  container:: example

            Changes snake case to upper camel case:

            ::

                >>> abjad.String('scale_degrees_4_and_5').to_upper_camel_case()
                'ScaleDegrees4And5'

        ..  container:: example

            Changes dash case to upper camel case:

            ::

                >>> abjad.String('scale-degrees-4-and-5').to_upper_camel_case()
                'ScaleDegrees4And5'

        ..  container:: example

            Changes upper camel case to upper camel case:

            ::

                >>> abjad.String('ScaleDegrees4And5').to_upper_camel_case()
                'ScaleDegrees4And5'

        Returns new string.
        '''
        words = self.delimit_words()
        words = [_.capitalize() for _ in words]
        string = ''.join(words)
        return string
