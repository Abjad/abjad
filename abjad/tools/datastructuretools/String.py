import pathlib
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
            underscore_delimited_lowercase_regex_body,
            )

    underscore_delimited_lowercase_package_regex = re.compile(
        '^{}$'.format(underscore_delimited_lowercase_package_regex_body),
        re.VERBOSE,
        )

    uppercamelcase_regex = re.compile(
        '^([A-Z,0-9]+[a-z,0-9]*)*$',
        re.VERBOSE,
        )

    ### PRIVATE METHODS ###

    def _is_wrapper_directory_name(self):
        if self in ('.git', '.DS_Store'):
            return False
        return True

    ### PUBLIC METHODS ###

    def capitalize_start(self):
        r'''Capitalizes start of string.

        ..  container:: example

            >>> abjad.String('violin I').capitalize_start()
            'Violin I'

        Function differs from built-in ``string.capitalize()``.

        This function affects only ``string[0]`` and leaves noninitial
        characters as-is.

        Built-in ``string.capitalize()`` forces noninitial characters to
        lowercase.

        ..  container:: example

            >>> 'violin I'.capitalize()
            'Violin i'

        Returns new string.
        '''
        if not self:
            return type(self)('')
        return type(self)(self[0].upper() + self[1:])

    def delimit_words(self, separate_caps=False):
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

        ..  container:: example

            Separates capital letters when keyword is true:

            >>> string = abjad.String('MRM')
            >>> string.delimit_words()
            ['MRM']

            >>> string.delimit_words(separate_caps=True)
            ['M', 'R', 'M']

        ..  container:: example

            Separates capital letters when keyword is true:

            >>> string = abjad.String('MRhM')
            >>> string.delimit_words()
            ['MRh', 'M']

            >>> string.delimit_words(separate_caps=True)
            ['M', 'Rh', 'M']

        Returns list.
        '''
        wordlike_characters = ('<', '>', '!')
        words = []
        current_word = ''
        for character in self:
            if (not character.isalpha() and
                not character.isdigit() and
                character not in wordlike_characters):
                if current_word:
                    words.append(current_word)
                    current_word = ''
            elif not current_word:
                current_word = current_word + character
            elif character.isupper():
                if current_word[-1].isupper() and not separate_caps:
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
        return [type(self)(_) for _ in words]

    def is_build_directory_name(self):
        r'''Is true when string is build directory name.

        Returns true or false.
        '''
        if not self == self.lower():
            return False
        if self[0] == '.':
            return False
        if self[0] == '_':
            return False
        return True

    def is_classfile_name(self):
        r'''Is true when string is classfile name.

        Returns true or false.
        '''
        path = pathlib.Path(self)
        if not type(self)(path.stem).is_upper_camel_case():
            return False
        if not path.suffix == '.py':
            return False
        return True

    def is_dash_case(self):
        r'''Is true when string is hyphen-delimited lowercase.

        ..  container:: example

            >>> abjad.String('foo-bar').is_dash_case()
            True

        Otherwise false:

        ..  container:: example

            >>> abjad.String('foo bar').is_dash_case()
            False

        Returns true or false.
        '''
        return bool(String.hyphen_delimited_lowercase_regex.match(self))

    def is_dash_case_file_name(self):
        r'''Is true when string is hyphen-delimited lowercase file name with
        extension.

        ..  container:: example

            >>> abjad.String('foo-bar').is_dash_case_file_name()
            True

        Otherwise false:

        ..  container:: example

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

            >>> abjad.String('fooBar').is_lower_camel_case()
            True

        Otherwise false:

        ..  container:: example

            >>> abjad.String('FooBar').is_lower_camel_case()
            False

        Returns true or false.
        '''
        return bool(String.lowercamelcase_regex.match(self))

    def is_lowercase_file_name(self):
        r'''Is true when string is lowercase file name.

        Returns true or false.
        '''
        if not self == self.lower():
            return False
        path = pathlib.Path(self)
        if not (type(self)(path.stem).is_snake_case() or
            type(self)(path.stem).is_dash_case()):
            return False
#        if path.suffix not in ('.py', '.ly', '.pdf'):
#            return False
        return True

    def is_module_file_name(self):
        r'''Is true when string is module file name.

        Returns true or false.
        '''
        path = pathlib.Path(self)
        if not path.name == path.name.lower():
            return False
        if not type(self)(path.stem).is_snake_case():
            return False
        if not path.suffix == '.py':
            return False
        return True

    def is_package_name(self):
        r'''Is true when string is package name.

        Returns true or false.
        '''
        if not self == self.lower():
            return False
        if not self.is_snake_case():
            return False
        return True

    def is_public_python_file_name(self):
        r'''Is true when string is public Python file name.

        Returns true or false.
        '''
        path = pathlib.Path(self)
        if path.stem.startswith('_'):
            return False
        if not path.suffix == '.py':
            return False
        return True

    def is_segment_name(self):
        r'''Is true when string is segment name or package name.

        ..  container:: example

            >>> abjad.String('A').is_segment_name()
            True

            >>> abjad.String('A1').is_segment_name()
            True

            >>> abjad.String('A99').is_segment_name()
            True

            >>> abjad.String('segment_01').is_segment_name()
            True

        ..  container:: example

            >>> abjad.String('_').is_segment_name()
            True

        Otherwise false:

        ..  container:: example

            >>> abjad.String('A_1').is_segment_name()
            False

        Returns true or false.
        '''
        if self.is_package_name():
            return True
        if self and (self[0].isupper() or self[0] == '_'):
            if len(self) == 1:
                return True
            if self[1:].isdigit():
                return True
        return False

    def is_snake_case(self):
        r'''Is true when string is underscore-delimited lowercase.

        ..  container:: example

            >>> abjad.String('foo_bar').is_snake_case()
            True

        Otherwise false:

        ..  container:: example

            >>> abjad.String('foo bar').is_snake_case()
            False

        Returns true or false.
        '''
        return bool(String.underscore_delimited_lowercase_regex.match(self))

    def is_snake_case_file_name(self):
        r'''Is true when string is underscore-delimited lowercase file name.

        ..  container:: example

            >>> abjad.String('foo_bar').is_snake_case_file_name()
            True

        Otherwise false:

        ..  container:: example

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

            >>> string = abjad.String('foo_bar.blah')
            >>> string.is_snake_case_file_name_with_extension()
            True

        Otherwise false:

        ..  container:: example

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

            >>> string = abjad.String('foo.bar.blah_package')
            >>> string.is_snake_case_package_name()
            True

        Otherwise false:

        ..  container:: example

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

            >>> abjad.String('foo bar').is_space_delimited_lowercase()
            True

        Otherwise false:

        ..  container:: example

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

    def is_stylesheet_name(self):
        r'''Is true when string is stylesheet name.

        Returns true or false.
        '''
        path = pathlib.Path(self)
        if not path.name == path.name.lower():
            return False
        if not type(self)(path.stem).is_dash_case():
            return False
        if not path.suffix == '.ily':
            return False
        return True

    def is_tools_file_name(self):
        r'''Is true when string is tools file name.

        Returns true or false.
        '''
        if self.is_classfile_name():
            return True
        if self.is_module_file_name():
            return True
        return False

    def is_upper_camel_case(self):
        r'''Is true when string upper camel case.

        ..  container:: example

            >>> abjad.String('FooBar').is_upper_camel_case()
            True

        Otherwise false:

        ..  container:: example

            >>> abjad.String('fooBar').is_upper_camel_case()
            False

        Returns true or false.
        '''
        return bool(String.uppercamelcase_regex.match(self))

    @staticmethod
    def match_strings(strings, pattern):
        r'''Matches `pattern` against `strings`.

        ..  container:: example

            >>> strings = [
            ...     'AcciaccaturaSpecifier.py',
            ...     'AnchorCommand.py',
            ...     'ArpeggiationSpacingSpecifier.py',
            ...     'AttachCommand.py',
            ...     'ChordalSpacingSpecifier.py',
            ...     ]

            >>> abjad.String.match_strings(strings, 'A')
            []

            >>> for i in abjad.String.match_strings(strings, 'At'):
            ...     strings[i]
            'AttachCommand.py'

            >>> for i in abjad.String.match_strings(strings, 'AtC'):
            ...     strings[i]
            'AttachCommand.py'

            >>> for i in abjad.String.match_strings(strings, 'ASS'):
            ...     strings[i]
            'ArpeggiationSpacingSpecifier.py'

            >>> for i in abjad.String.match_strings(strings, 'AC'):
            ...     strings[i]
            'AnchorCommand.py'
            'AttachCommand.py'

            >>> for i in abjad.String.match_strings(strings, '.py'):
            ...     strings[i]
            'AcciaccaturaSpecifier.py'
            'AnchorCommand.py'
            'ArpeggiationSpacingSpecifier.py'
            'AttachCommand.py'
            'ChordalSpacingSpecifier.py'

            >>> abjad.String.match_strings(strings, '@AC')
            []

        ..  container:: example

            Regressions:

            >>> abjad.String.match_strings(strings, '||')
            []

            >>> strings = ['_allegro', '-allegro', '.allegro', 'allegro']
            >>> for i in abjad.String.match_strings(strings, '_al'):
            ...     strings[i]
            '_allegro'

            >>> for i in abjad.String.match_strings(strings, '-al'):
            ...     strings[i]
            '-allegro'

            >>> for i in abjad.String.match_strings(strings, '.al'):
            ...     strings[i]
            '.allegro'

            >>> for i in abjad.String.match_strings(strings, 'egro'):
            ...     strings[i]
            '_allegro'
            '-allegro'
            '.allegro'
            'allegro'

        Returns string or none.
        '''
        if not pattern:
            return []
        if not pattern[0].isalpha() and not pattern[0] in list('_-.'):
            return []
        pattern = String(pattern)
        indices = []
        for i, string in enumerate(strings):
            if string == pattern:
                indices.append(i)
        strings = [String(_) for _ in strings]
        if 3 <= len(pattern):
            for i, string in enumerate(strings):
                if string.startswith(pattern):
                    if i not in indices:
                        indices.append(i)
            for i, string in enumerate(strings):
                string = string.strip_diacritics().lower()
                if string.startswith(pattern.lower()):
                    if i not in indices:
                        indices.append(i)
        if len(pattern) <= 1:
            return indices
        if not pattern.islower() or any(_.isdigit() for _ in pattern):
            pattern_words = pattern.delimit_words(separate_caps=True)
            if pattern_words:
                for i, string in enumerate(strings):
                    if (string.startswith(pattern_words[0]) and
                        string.match_word_starts(pattern_words)):
                        if i not in indices:
                            indices.append(i)
                for i, string in enumerate(strings):
                    if string.match_word_starts(pattern_words):
                        if i not in indices:
                            indices.append(i)
        if pattern.islower():
            pattern_characters = list(pattern)
            if pattern_characters:
                for i, string in enumerate(strings):
                    if (string.startswith(pattern_characters[0]) and
                        string.match_word_starts(pattern_characters)):
                        if i not in indices:
                            indices.append(i)
                for i, string in enumerate(strings):
                    if string.match_word_starts(pattern_characters):
                        if i not in indices:
                            indices.append(i)
        if len(pattern) < 3:
            return indices
        for i, string in enumerate(strings):
            if pattern in string.strip_diacritics().lower():
                if i not in indices:
                    indices.append(i)
        return indices

    def match_word_starts(self, words):
        r'''Matches word starts.

        ..  container:: example

            >>> string = abjad.String('StringQuartetScoreTemplate')

            >>> string.match_word_starts(['Str', 'Quar', 'Temp'])
            True

            >>> string.match_word_starts(['S', 'Q', 'S', 'T'])
            True

            >>> string.match_word_starts(['Quartet'])
            True

            >>> string.match_word_starts(['Q'])
            True

        ..  container:: example

            >>> string = abjad.String('StringQuartetScoreTemplate')

            >>> string.match_word_starts(['Quar', 'Str'])
            False

            >>> string.match_word_starts(['uartet'])
            False

        ..  container:: example

            Regressions:

            >>> string = abjad.String('IOManager')
            >>> string.match_word_starts(['I', 'O'])
            True

            >>> string = abjad.String('StringQuartetScoreTemplate')
            >>> string.match_word_starts(['S', 'Q', 'S', 'T', 'T'])
            False

            >>> string = abjad.String('AcciaccaturaSpecifier.py')
            >>> string.match_word_starts(['A', 'S', 'S'])
            False

        Returns true or false.
        '''
        my_words = self.delimit_words(separate_caps=True)
        indices = []
        last_index = 0
        for word in words:
            for i, my_word in enumerate(my_words):
                if i < last_index:
                    continue
                if my_word.startswith(word) and i not in indices:
                    indices.append(i)
                    last_index = i
                    break
            else:
                return False
        return indices == sorted(indices)

    @staticmethod
    def normalize(argument, indent=None):
        r"""Normalizes string.

        ..  container:: example

            >>> string = r'''
            ...     foo
            ...         bar
            ... '''
            >>> print(string)
            <BLANKLINE>
                foo
                    bar
            <BLANKLINE>

            >>> print(abjad.String.normalize(string))
            foo
                bar

            >>> print(abjad.String.normalize(string, indent=4))
                foo
                    bar

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
        return String(string)

    def pluralize(self, count=None):
        r'''Pluralizes English string.

        ..  container:: example

            Changes terminal `-y` to `-ies`:

            >>> abjad.String('catenary').pluralize()
            'catenaries'

        ..  container:: example

            Adds `-es` to terminal `-s`, `-sh`, `-x` and `-z`:

            >>> abjad.String('brush').pluralize()
            'brushes'

        ..  container:: example

            Adds `-s` to all other strings:

            >>> abjad.String('shape').pluralize()
            'shapes'

        ..  container:: example

            Does not pluralize:

            >>> abjad.String('shape').pluralize(count=1)
            'shape'

        Returns string.
        '''
        if count == 1:
            result = self
        elif self.endswith('y'):
            result = self[:-1] + 'ies'
        elif self.endswith(('s', 'sh', 'x', 'z')):
            result = self + 'es'
        else:
            result = self + 's'
        return type(self)(result)

    def strip_diacritics(self):
        r'''Strips diacritics from binary string.

        ..  container:: example

            >>> binary_string = abjad.String('Dvořák')

            >>> print(binary_string)
            Dvořák

            >>> binary_string.strip_diacritics()
            'Dvorak'

        Returns ASCII string.
        '''
        normalized_unicode_string = unicodedata.normalize('NFKD', self)
        ascii_string = normalized_unicode_string.encode('ascii', 'ignore')
        return type(self)(ascii_string.decode('utf-8'))

    def to_accent_free_snake_case(self):
        '''Changes string to accent-free snake case.

        ..  container:: example

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
        return type(self)(string)

    @staticmethod
    def to_bidirectional_direction_string(argument):
        r'''Changes `argument` to bidirectional direction string.

        ..  container:: example:

            >>> abjad.String.to_bidirectional_direction_string('^')
            'up'

        ..  container:: example:

            >>> abjad.String.to_bidirectional_direction_string('_')
            'down'

        ..  container:: example:

            >>> abjad.String.to_bidirectional_direction_string(1)
            'up'

        ..  container:: example:

            >>> abjad.String.to_bidirectional_direction_string(-1)
            'down'

        Returns `argument` when `argument` is `'up'` or `'down'`.

        Returns string or none.
        '''
        import abjad
        lookup = {
            1: 'up',
            -1: 'down',
            abjad.Up: 'up',
            abjad.Down: 'down',
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

            >>> abjad.String.to_tridirectional_lilypond_symbol(abjad.Up)
            '^'

        ..  container:: example

            >>> abjad.String.to_tridirectional_lilypond_symbol(abjad.Down)
            '_'

        ..  container:: example

            >>> abjad.String.to_tridirectional_lilypond_symbol(1)
            '^'

        ..  container:: example

            >>> abjad.String.to_tridirectional_lilypond_symbol(-1)
            '_'

        Returns `argument` when `argument` is `'^'` or `'_'`.

        Returns string or none.
        '''
        lookup = {
            1: '^',
            -1: '_',
            abjad.Up: '^',
            abjad.Down: '_',
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

            >>> abjad.String('scale degrees 4 and 5').to_dash_case()
            'scale-degrees-4-and-5'

        ..  container:: example

            Changes snake case to dash case:

            >>> abjad.String('scale_degrees_4_and_5').to_dash_case()
            'scale-degrees-4-and-5'

        ..  container:: example

            Changes dash case to dash case:

            >>> abjad.String('scale-degrees-4-and-5').to_dash_case()
            'scale-degrees-4-and-5'

        ..  container:: example

            Changes upper camel case to dash case:

            >>> abjad.String('ScaleDegrees4And5').to_dash_case()
            'scale-degrees-4-and-5'

        Returns string.
        '''
        words = self.delimit_words()
        words = [_.lower() for _ in words]
        string = '-'.join(words)
        return type(self)(string)

    def to_lower_camel_case(self):
        r'''Changes string to lower camel case.

        ..  container:: example

            Changes words to lower camel case:

            >>> abjad.String('scale degrees 4 and 5').to_lower_camel_case()
            'scaleDegrees4And5'

        ..  container:: example

            Changes snake case to lower camel case:

            >>> abjad.String('scale_degrees_4_and_5').to_lower_camel_case()
            'scaleDegrees4And5'

        ..  container:: example

            Changes dash case to lower camel case:

            >>> abjad.String('scale-degrees-4-and-5').to_lower_camel_case()
            'scaleDegrees4And5'

        ..  container:: example

            Changes upper camel case to lower camel case:

            >>> abjad.String('ScaleDegrees4And5').to_lower_camel_case()
            'scaleDegrees4And5'

        Returns string.
        '''
        string = self.to_upper_camel_case()
        if string == '':
            pass
        else:
            string = string[0].lower() + string[1:]
        return type(self)(string)

    def to_snake_case(self):
        r'''Changes string to snake case.

        ..  container:: example

            Changes words to snake case:

            >>> abjad.String('scale degrees 4 and 5').to_snake_case()
            'scale_degrees_4_and_5'

        ..  container:: example

            Changes snake case to snake case:

            >>> abjad.String('scale_degrees_4_and_5').to_snake_case()
            'scale_degrees_4_and_5'

        ..  container:: example

            Changes dash case to snake case:

            >>> abjad.String('scale-degrees-4-and-5').to_snake_case()
            'scale_degrees_4_and_5'

        ..  container:: example

            Changes upper camel case to snake case:

            >>> abjad.String('ScaleDegrees4And5').to_snake_case()
            'scale_degrees_4_and_5'

        Returns string.
        '''
        words = self.delimit_words()
        words = [_.lower() for _ in words]
        string = '_'.join(words)
        return type(self)(string)

    def to_space_delimited_lowercase(self):
        r'''Changes string to space-delimited lowercase.

        ..  container:: example

            Changes upper camel case `string` to space-delimited lowercase:

            >>> abjad.String('LogicalTie').to_space_delimited_lowercase()
            'logical tie'

        ..  container:: example

            Changes underscore-delimited `string` to space-delimited lowercase:

            >>> abjad.String('logical_tie').to_space_delimited_lowercase()
            'logical tie'

        ..  container:: example

            Returns space-delimited string unchanged:

            >>> abjad.String('logical tie').to_space_delimited_lowercase()
            'logical tie'

        ..  container:: example

            Returns empty string unchanged:

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
        else:
            string = self.replace('_', ' ')
        return type(self)(string)

    @staticmethod
    def to_tridirectional_direction_string(argument):
        r'''Changes `argument` to tridirectional direction string.

        ..  container:: example

            >>> abjad.String.to_tridirectional_direction_string('^')
            'up'

        ..  container:: example

            >>> abjad.String.to_tridirectional_direction_string('-')
            'center'

        ..  container:: example

            >>> abjad.String.to_tridirectional_direction_string('_')
            'down'

        ..  container:: example

            >>> abjad.String.to_tridirectional_direction_string(1)
            'up'

        ..  container:: example

            >>> abjad.String.to_tridirectional_direction_string(0)
            'center'

        ..  container:: example

            >>> abjad.String.to_tridirectional_direction_string(-1)
            'down'

        ..  container:: example

            >>> abjad.String.to_tridirectional_direction_string('default')
            'center'

        Returns none when `argument` is none.

        Returns string or none.
        '''
        import abjad
        lookup = {
            abjad.Up: 'up',
            '^': 'up',
            'up': 'up',
            1: 'up',
            abjad.Down: 'down',
            '_': 'down',
            'down': 'down',
            -1: 'down',
            abjad.Center: 'center',
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

            >>> abjad.String.to_tridirectional_lilypond_symbol(abjad.Up)
            '^'

        ..  container:: example

            >>> abjad.String.to_tridirectional_lilypond_symbol('neutral')
            '-'

        ..  container:: example

            >>> abjad.String.to_tridirectional_lilypond_symbol('default')
            '-'

        ..  container:: example

            >>> abjad.String.to_tridirectional_lilypond_symbol(abjad.Down)
            '_'

        ..  container:: example

            >>> abjad.String.to_tridirectional_lilypond_symbol(1)
            '^'

        ..  container:: example

            >>> abjad.String.to_tridirectional_lilypond_symbol(0)
            '-'

        ..  container:: example

            >>> abjad.String.to_tridirectional_lilypond_symbol(-1)
            '_'

        Returns none when `argument` is none.

        Returns `argument` when `argument` is `'^'`, `'-'` or `'_'`.

        Returns string or none.
        '''
        import abjad
        lookup = {
            abjad.Up: '^',
            '^': '^',
            'up': '^',
            1: '^',
            abjad.Down: '_',
            '_': '_',
            'down': '_',
            -1: '_',
            abjad.Center: '-',
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

            >>> abjad.String.to_tridirectional_ordinal_constant('_')
            Down

        ..  container:: example

            >>> abjad.String.to_tridirectional_ordinal_constant(1)
            Up

        ..  container:: example

            >>> abjad.String.to_tridirectional_ordinal_constant(-1)
            Down

        Returns `argument` when `argument` is `Up`', `Center` or `Down`.

        Returns ordinal constant or none.
        '''
        import abjad
        lookup = {
            abjad.Up: abjad.Up,
            '^': abjad.Up,
            'up': abjad.Up,
            1: abjad.Up,
            abjad.Down: abjad.Down,
            '_': abjad.Down,
            'down': abjad.Down,
            -1: abjad.Down,
            abjad.Center: abjad.Center,
            '-': abjad.Center,
            0: abjad.Center,
            'center': abjad.Center,
            'default': abjad.Center,
            'neutral': abjad.Center,
            }
        if argument is None:
            return None
        elif argument in lookup:
            return lookup[argument]
        message = 'unrecognized expression: {!r}.'
        message = message.format(
            argument)
        raise ValueError(message)

    def to_upper_camel_case(self):
        r'''Changes string to upper camel case.

        ..  container:: example

            Changes words to upper camel case:

            >>> abjad.String('scale degrees 4 and 5').to_upper_camel_case()
            'ScaleDegrees4And5'

        ..  container:: example

            Changes snake case to upper camel case:

            >>> abjad.String('scale_degrees_4_and_5').to_upper_camel_case()
            'ScaleDegrees4And5'

        ..  container:: example

            Changes dash case to upper camel case:

            >>> abjad.String('scale-degrees-4-and-5').to_upper_camel_case()
            'ScaleDegrees4And5'

        ..  container:: example

            Changes upper camel case to upper camel case:

            >>> abjad.String('ScaleDegrees4And5').to_upper_camel_case()
            'ScaleDegrees4And5'

        Returns new string.
        '''
        words = self.delimit_words()
        words = [_.capitalize() for _ in words]
        string = ''.join(words)
        return type(self)(string)
