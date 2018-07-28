import pathlib
import re
import roman  # type: ignore
import six
import textwrap
import typing
import unicodedata
from abjad import enums
from .TypedList import TypedList


class String(str):
    """
    String.
    """

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

    @staticmethod
    def base_26(n: int) -> 'String':
        """
        Gets base-26 representation of nonnegative integer ``n``.

        :param n: integer.

        ..  container:: example

            >>> abjad.String.base_26(1)
            'A'
            >>> abjad.String.base_26(2)
            'B'
            >>> abjad.String.base_26(3)
            'C'

            >>> abjad.String.base_26(26)
            'Z'
            >>> abjad.String.base_26(27)
            'AA'
            >>> abjad.String.base_26(28)
            'AB'

            >>> abjad.String.base_26(52)
            'AZ'
            >>> abjad.String.base_26(53)
            'BA'
            >>> abjad.String.base_26(54)
            'BB'

            >>> abjad.String.base_26(78)
            'BZ'
            >>> abjad.String.base_26(79)
            'CA'
            >>> abjad.String.base_26(80)
            'CB'

        """
        assert 0 < n, repr(n)
        if 1 <= n <= 26:
            result = chr(ord('A') + n - 1)
        elif 26 < n < 676:
            left = int(n / 26)
            right = n - (26 * left)
            if right == 0:
                left -= 1
                right = 26
            left_ = chr(ord('A') + left - 1)
            right_ = chr(ord('A') + right - 1)
            result = left_ + right_
        else:
            raise NotImplementedError(n)
        return String(result)

    def capitalize_start(self) -> 'String':
        """
        Capitalizes start of string.

        ..  container:: example

            >>> abjad.String('violin I').capitalize_start()
            'Violin I'

        Capitalizes only ``string[0]``; leaves noninitial characters unchanged.

        ..  container:: example

            Built-in ``string.capitalize()`` forces noninitial characters to
            lowercase:

            >>> 'violin I'.capitalize()
            'Violin i'

        """
        if not self:
            return type(self)('')
        return type(self)(self[0].upper() + self[1:])

    def delimit_words(self, separate_caps=False) -> typing.List['String']:
        """
        Delimits words in string.

        ..  container:: example

            >>> string = abjad.String('scale degrees 4 and 5.')
            >>> string.delimit_words()
            ['scale', 'degrees', '4', 'and', '5']

            >>> string = abjad.String('scale degrees 4and5.')
            >>> string.delimit_words()
            ['scale', 'degrees', '4', 'and', '5']

            >>> string = abjad.String('scaleDegrees4and5.')
            >>> string.delimit_words()
            ['scale', 'Degrees', '4', 'and', '5']

            >>> string = abjad.String('ScaleDegrees4and 5.')
            >>> string.delimit_words()
            ['Scale', 'Degrees', '4', 'and', '5']

            >>> string = abjad.String('scale-degrees-4-and-5.')
            >>> string.delimit_words()
            ['scale', 'degrees', '4', 'and', '5']

            >>> string = abjad.String('SCALE_DEGREES_4_AND_5.')
            >>> string.delimit_words()
            ['SCALE', 'DEGREES', '4', 'AND', '5']

        ..  container:: example

            >>> string = abjad.String('one < two')
            >>> string.delimit_words()
            ['one', '<', 'two']

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

            >>> string = abjad.String('MRhM')
            >>> string.delimit_words()
            ['MRh', 'M']
            >>> string.delimit_words(separate_caps=True)
            ['M', 'Rh', 'M']

        """
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

    def from_roman(self) -> int:
        """
        Changes string from Roman numeral to digits.

        ..  container:: example

            >>> abjad.String('IX').from_roman()
            9
            >>> abjad.String('ix').from_roman()
            9

        ..  container:: example

            Raises Roman numeral error when string is not Roman numeral:

            >>> abjad.String('Allegro').from_roman()
            Traceback (most recent call last):
                ...
            roman.InvalidRomanNumeralError: Invalid Roman numeral: Allegro

        """
        if self.is_roman():
            return roman.fromRoman(self.upper())
        number = roman.fromRoman(self)
        return number

    def is_build_directory_name(self) -> bool:
        """
        Is true when string is build directory name.

        ..  container:: example

            >>> abjad.String('letter-score').is_build_directory_name()
            True
            >>> abjad.String('letter_score').is_build_directory_name()
            True

            >>> abjad.String('Letter_score').is_build_directory_name()
            False
            >>> abjad.String('-letter-score').is_build_directory_name()
            False
            >>> abjad.String('_letter-score').is_build_directory_name()
            False
            >>> abjad.String('letter score').is_build_directory_name()
            False

        """
        if not self == self.lower():
            return False
        if ' ' in self:
            return False
        if not self[0].isalpha():
            return False
        return True

    def is_classfile_name(self) -> bool:
        """
        Is true when string is classfile name.

        ..  container:: example

            >>> abjad.String('BeamSpecifier.py').is_classfile_name()
            True

            >>> abjad.String('BeamSpecifier').is_classfile_name()
            False
            >>> abjad.String('beamSpecifier.py').is_classfile_name()
            False
            >>> abjad.String('Beam_Specifier.py').is_classfile_name()
            False

        """
        path = pathlib.Path(self)
        if not type(self)(path.stem).is_upper_camel_case():
            return False
        if not path.suffix == '.py':
            return False
        return True

    def is_dash_case(self) -> bool:
        """
        Is true when string is hyphen-delimited lowercase.

        ..  container:: example

            >>> abjad.String('foo-bar').is_dash_case()
            True

            >>> abjad.String('foo bar').is_dash_case()
            False

        """
        return bool(String.hyphen_delimited_lowercase_regex.match(self))

    def is_dash_case_file_name(self) -> bool:
        """
        Is true when string is hyphen-delimited lowercase file name with
        extension.

        ..  container:: example

            >>> abjad.String('foo-bar').is_dash_case_file_name()
            True

            >>> abjad.String('foo.bar.blah').is_dash_case_file_name()
            False

        """
        if self == '':
            return True
        return bool(
            String.hyphen_delimited_lowercase_file_name_regex.match(self)
            )

    def is_introduction_segment_name(self) -> bool:
        """
        Is true when string is introductory segment name.

        ..  container:: example

            >>> abjad.String('_').is_introduction_segment_name()
            True
            >>> abjad.String('_1').is_introduction_segment_name()
            True
            >>> abjad.String('_2').is_introduction_segment_name()
            True
            >>> abjad.String('_99').is_introduction_segment_name()
            True

            >>> abjad.String('__').is_introduction_segment_name()
            False
            >>> abjad.String('__1').is_introduction_segment_name()
            False

            >>> abjad.String('A').is_introduction_segment_name()
            False
            >>> abjad.String('1').is_introduction_segment_name()
            False

        """
        if not self:
            return False
        if self[0] != '_':
            return False
        if bool(self[1:]) and not self[1:].isdigit():
            return False
        return True

    def is_lilypond_identifier(self) -> bool:
        """
        Is true when string starts with a letter and contains only letters
        and underscores thereafter.

        ..  container:: example

            >>> abjad.String('ViolinOne').is_lilypond_identifier()
            True
            >>> abjad.String('Violin_One').is_lilypond_identifier()
            True

            >>> abjad.String('Violin One').is_lilypond_identifier()
            False

        ..  container:: example

            >>> abjad.String('ViolinI').is_lilypond_identifier()
            True
            >>> abjad.String('Violin_I').is_lilypond_identifier()
            True

            >>> abjad.String('Violin I').is_lilypond_identifier()
            False

        ..  container:: example

            >>> abjad.String('Violin1').is_lilypond_identifier()
            False
            >>> abjad.String('Violin_1').is_lilypond_identifier()
            False
            >>> abjad.String('Violin 1').is_lilypond_identifier()
            False

        """
        if self and self[0] == '_':
            return False
        for character in self:
            if not (character.isalpha() or character == '_'):
                return False
        return True

    def is_lower_camel_case(self) -> bool:
        """
        Is true when string and is lower camel case.

        ..  container:: example

            >>> abjad.String('fooBar').is_lower_camel_case()
            True

            >>> abjad.String('FooBar').is_lower_camel_case()
            False

        """
        return bool(String.lowercamelcase_regex.match(self))

    def is_lowercase_file_name(self) -> bool:
        """
        Is true when string is lowercase file name.

        ..  container:: example

            Is true when string is dash case:

            >>> abjad.String('back-cover').is_lowercase_file_name()
            True
            >>> abjad.String('back-cover.tex').is_lowercase_file_name()
            True

            Is true when string is underscore-delimited:

            >>> abjad.String('compile_source').is_lowercase_file_name()
            True
            >>> abjad.String('compile_source.py').is_lowercase_file_name()
            True

        ..  container:: example

            >>> abjad.String('back cover').is_lowercase_file_name()
            False
            >>> abjad.String('Back-Cover').is_lowercase_file_name()
            False

        """
        if not self == self.lower():
            return False
        path = pathlib.Path(self)
        if not (type(self)(path.stem).is_snake_case() or
            type(self)(path.stem).is_dash_case()):
            return False
        return True

    def is_module_file_name(self) -> bool:
        """
        Is true when string is module file name.

        ..  container:: example

            >>> abjad.String('compile_source.py').is_module_file_name()
            True

            >>> abjad.String('compile_source').is_module_file_name()
            False
            >>> abjad.String('compile-source').is_module_file_name()
            False
            >>> abjad.String('compile-source.py').is_module_file_name()
            False

            >>> abjad.String('Compile_Source.py').is_module_file_name()
            False

        """
        path = pathlib.Path(self)
        if not path.name == path.name.lower():
            return False
        if not type(self)(path.stem).is_snake_case():
            return False
        if not path.suffix == '.py':
            return False
        return True

    def is_package_name(self) -> bool:
        """
        Is true when string is package name.

        ..  container:: example

            >>> abjad.String('pitches').is_package_name()
            True
            >>> abjad.String('pitch_classes').is_package_name()
            True

            >>> abjad.String('Pitches').is_package_name()
            False
            >>> abjad.String('pitch-classes').is_package_name()
            False

        """
        if not self == self.lower():
            return False
        if not self.is_snake_case():
            return False
        return True

    def is_public_python_file_name(self) -> bool:
        """
        Is true when string is public Python file name.

        ..  container:: example

            >>> abjad.String('pitches.py').is_public_python_file_name()
            True
            >>> abjad.String('pitch_classes.py').is_public_python_file_name()
            True
            >>> abjad.String('Pitches.py').is_public_python_file_name()
            True
            >>> abjad.String('PitchClasses.py').is_public_python_file_name()
            True

            >>> abjad.String('.pitches.py').is_public_python_file_name()
            False
            >>> abjad.String('_pitches.py').is_public_python_file_name()
            False
            >>> abjad.String('pitch-classes.py').is_public_python_file_name()
            False

        """
        path = pathlib.Path(self)
        if path.stem and not path.stem[0].isalpha():
            return False
        if not path.suffix == '.py':
            return False
        for character in path.stem[1:]:
            if not character.isalpha() and character != '_':
                return False
        return True

    def is_rehearsal_mark(self, forbid_i=False) -> bool:
        """
        Is true when string is one- or two-character rehearsal mark.

        ..  container:: example

            >>> abjad.String('A').is_rehearsal_mark()
            True
            >>> abjad.String('B').is_rehearsal_mark()
            True
            >>> abjad.String('Z').is_rehearsal_mark()
            True
            >>> abjad.String('AA').is_rehearsal_mark()
            True
            >>> abjad.String('AB').is_rehearsal_mark()
            True
            >>> abjad.String('AZ').is_rehearsal_mark()
            True
            >>> abjad.String('ZZ').is_rehearsal_mark()
            True

            >>> abjad.String('A1').is_rehearsal_mark()
            False
            >>> abjad.String('AAA').is_rehearsal_mark()
            False

        ..  container:: example

            >>> abjad.String('I').is_rehearsal_mark()
            True
            >>> abjad.String('J').is_rehearsal_mark()
            True

        ..  container:: example

            >>> abjad.String('I').is_rehearsal_mark(forbid_i=True)
            False

            >>> abjad.String('J').is_rehearsal_mark(forbid_i=True)
            True

        """
        if len(self) not in (1, 2):
            return False
        if not self.isalpha():
            return False
        if not self.isupper():
            return False
        if forbid_i is True and 'I' in self:
            return False
        return True

    def is_roman(self) -> bool:
        """
        Is true when string is Roman numeral.

        ..  container:: example

            >>> abjad.String('I').is_roman()
            True
            >>> abjad.String('II').is_roman()
            True
            >>> abjad.String('X').is_roman()
            True
            >>> abjad.String('XI').is_roman()
            True
            >>> abjad.String('C').is_roman()
            True
            >>> abjad.String('CI').is_roman()
            True

            >>> abjad.String('i').is_roman()
            True

            >>> abjad.String('F').is_roman()
            False

        """
        try:
            roman.fromRoman(self.upper())
            return True
        except roman.InvalidRomanNumeralError:
            return False

    def is_segment_name(self) -> bool:
        """
        Is true when string is segment name or package name.

        ..  container:: example

            >>> abjad.String('_').is_segment_name()
            True
            >>> abjad.String('_1').is_segment_name()
            True
            >>> abjad.String('_99').is_segment_name()
            True

        ..  container:: example

            >>> abjad.String('A').is_segment_name()
            True
            >>> abjad.String('A1').is_segment_name()
            True
            >>> abjad.String('A99').is_segment_name()
            True

        ..  container:: example

            >>> abjad.String('AB').is_segment_name()
            True
            >>> abjad.String('AB1').is_segment_name()
            True
            >>> abjad.String('AB99').is_segment_name()
            True

        ..  container:: example

            >>> abjad.String('segment_01').is_segment_name()
            True

        ..  container:: example

            >>> abjad.String('__1').is_segment_name()
            False
            >>> abjad.String('A_1').is_segment_name()
            False
            >>> abjad.String('AB_1').is_segment_name()
            False

        """
        if self.is_package_name():
            return True
        if self.is_introduction_segment_name():
            return True
        if self.is_rehearsal_mark():
            return True
        if String(self[0]).is_rehearsal_mark() and self[1:].isdigit():
            return True
        if String(self[:2]).is_rehearsal_mark() and self[2:].isdigit():
            return True
        return False

    def is_shout_case(self) -> bool:
        """
        Is true when string and is shoutcase.

        ..  container:: example

            >>> abjad.String('FOO_BAR').is_shout_case()
            True

            >>> abjad.String('FooBar').is_shout_case()
            False

        """
        return self == self.to_shout_case()

    def is_snake_case(self) -> bool:
        """
        Is true when string is underscore-delimited lowercase.

        ..  container:: example

            >>> abjad.String('foo_bar').is_snake_case()
            True

            >>> abjad.String('foo bar').is_snake_case()
            False

        """
        return bool(String.underscore_delimited_lowercase_regex.match(self))

    def is_snake_case_file_name(self) -> bool:
        """
        Is true when string is underscore-delimited lowercase file name.

        ..  container:: example

            >>> abjad.String('foo_bar').is_snake_case_file_name()
            True

            >>> abjad.String('foo.bar.blah').is_snake_case_file_name()
            False

        """
        if self == '':
            return True
        return bool(
            String.underscore_delimited_lowercase_file_name_regex.match(self)
            )

    def is_snake_case_file_name_with_extension(self) -> bool:
        """
        Is true when string is underscore-delimited lowercase file name
        with extension.

        ..  container:: example

            >>> string = abjad.String('foo_bar.blah')
            >>> string.is_snake_case_file_name_with_extension()
            True

            >>> string = abjad.String('foo.bar.blah')
            >>> string.is_snake_case_file_name_with_extension()
            False

        """
        if self == '':
            return True
        return bool(
            String.underscore_delimited_lowercase_file_name_with_extension_regex.match(
                self))

    def is_snake_case_package_name(self) -> bool:
        """
        Is true when string is underscore-delimited lowercase package name.

        ..  container:: example

            >>> string = abjad.String('foo.bar.blah_package')
            >>> string.is_snake_case_package_name()
            True

            >>> string = abjad.String('foo.bar.BlahPackage')
            >>> string.is_snake_case_package_name()
            False

        """
        return bool(
            String.underscore_delimited_lowercase_package_regex.match(self)
            )

    def is_space_delimited_lowercase(self) -> bool:
        """
        Is true when string is space-delimited lowercase.

        ..  container:: example

            >>> abjad.String('foo bar').is_space_delimited_lowercase()
            True

            >>> abjad.String('foo_bar').is_space_delimited_lowercase()
            False

        """
        return bool(String.space_delimited_lowercase_regex.match(self))

    @staticmethod
    def is_string(argument) -> bool:
        """
        Is true when ``argument`` is a string.

        ..  container:: example

            >>> abjad.String.is_string('Allegro')
            True
            >>> abjad.String.is_string('')
            True

            >>> abjad.String.is_string(99)
            False

        """
        return isinstance(argument, six.string_types)

    def is_stylesheet_name(self) -> bool:
        """
        Is true when string is stylesheet name.

        ..  container:: example

            >>> abjad.String('articulations.ily').is_stylesheet_name()
            True

            >>> abjad.String('Articulations.ily').is_stylesheet_name()
            False
            >>> abjad.String('articulations.ly').is_stylesheet_name()
            False
            >>> abjad.String('articulations').is_stylesheet_name()
            False
            >>> abjad.String('_articulations.ily').is_stylesheet_name()
            False

        """
        path = pathlib.Path(self)
        if not path.name == path.name.lower():
            return False
        if not type(self)(path.stem).is_dash_case():
            return False
        if not path.suffix == '.ily':
            return False
        return True

    def is_tools_file_name(self) -> bool:
        """
        Is true when string is tools file name.

        ..  container:: example

            >>> abjad.String('beam_specifier.py').is_tools_file_name()
            True
            >>> abjad.String('BeamSpecifier.py').is_tools_file_name()
            True

            >>> abjad.String('BeamSpecifier').is_tools_file_name()
            False
            >>> abjad.String('beamSpecifier.py').is_tools_file_name()
            False
            >>> abjad.String('Beam_Specifier.py').is_tools_file_name()
            False

        """
        if self.is_classfile_name():
            return True
        if self.is_module_file_name():
            return True
        return False

    def is_upper_camel_case(self) -> bool:
        """
        Is true when string upper camel case.

        ..  container:: example

            >>> abjad.String('FooBar').is_upper_camel_case()
            True

            >>> abjad.String('fooBar').is_upper_camel_case()
            False

        """
        return bool(String.uppercamelcase_regex.match(self))

    @staticmethod
    def match_strings(strings, pattern) -> typing.List[int]:
        """
        Matches ``pattern`` against ``strings``.

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

            REGRESSION:

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

        """
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

    def match_word_starts(self, words) -> bool:
        """
        Matches word starts.

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

            REGRESSION:

            >>> string = abjad.String('IOManager')
            >>> string.match_word_starts(['I', 'O'])
            True

            >>> string = abjad.String('StringQuartetScoreTemplate')
            >>> string.match_word_starts(['S', 'Q', 'S', 'T', 'T'])
            False

            >>> string = abjad.String('AcciaccaturaSpecifier.py')
            >>> string.match_word_starts(['A', 'S', 'S'])
            False

        """
        my_words = self.delimit_words(separate_caps=True)
        indices: typing.List[int] = []
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
    def normalize(argument, indent=None) -> 'String':
        """
        Normalizes string.

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
                    lines[i] = f'{indent}{line}'
            string = '\n'.join(lines)
        return String(string)

    def pluralize(self, count=None) -> 'String':
        """
        Pluralizes English string.

        ..  container:: example

            Changes terminal ``-y`` to ``-ies``:

            >>> abjad.String('catenary').pluralize()
            'catenaries'

            Adds ``-es`` to terminal ``-s``, ``-sh``, ``-x`` and ``-z``:

            >>> abjad.String('brush').pluralize()
            'brushes'

            Adds ``-s`` to all other strings:

            >>> abjad.String('shape').pluralize()
            'shapes'

        ..  container:: example

            Does not pluralize when ``count`` is 1:

            >>> abjad.String('shape').pluralize(count=1)
            'shape'

        """
        if count == 1:
            return self
        elif self.endswith('y'):
            result = self[:-1] + 'ies'
        elif self.endswith(('s', 'sh', 'x', 'z')):
            result = self + 'es'
        else:
            result = self + 's'
        return type(self)(result)

    def remove_zfill(self) -> 'String':
        """
        Removes zfill from numbers in string.

        ..  container:: example

            >>> abjad.String('Horn1').remove_zfill()
            'Horn1'

            >>> abjad.String('Horn01').remove_zfill()
            'Horn1'

            >>> abjad.String('Horn001').remove_zfill()
            'Horn1'

        """
        words = []
        for word in self.delimit_words():
            try:
                number = int(word)
                words.append(str(number))
            except ValueError:
                words.append(word)
        result = ''.join(words)
        return type(self)(result)

    def segment_letter(self):
        """
        Gets segment letter.

        ..  container:: example

            >>> abjad.String('_').segment_letter()
            '_'
            >>> abjad.String('_1').segment_letter()
            '_'
            >>> abjad.String('_12').segment_letter()
            '_'

            >>> abjad.String('A').segment_letter()
            'A'
            >>> abjad.String('A1').segment_letter()
            'A'
            >>> abjad.String('A12').segment_letter()
            'A'

            >>> abjad.String('AB').segment_letter()
            'AB'
            >>> abjad.String('AB1').segment_letter()
            'AB'
            >>> abjad.String('AB12').segment_letter()
            'AB'

        """
        if not self.is_segment_name():
            raise ValueError(f'must be segment name (not {self!r}).')
        if len(self) == 1:
            return self
        elif len(self) == 2:
            if self[1].isdigit():
                return self[:1]
            else:
                return self
        elif len(self) == 3:
            if self[1].isdigit():
                return self[:1]
            else:
                return self[:2]
        else:
            return self[:2]

    def segment_rank(self):
        """
        Gets segment index.

        ..  container:: example

            >>> abjad.String('_').segment_rank()
            0
            >>> abjad.String('_1').segment_rank()
            1
            >>> abjad.String('_12').segment_rank()
            12

            >>> abjad.String('A').segment_rank()
            0
            >>> abjad.String('A1').segment_rank()
            1
            >>> abjad.String('A12').segment_rank()
            12

            >>> abjad.String('AB').segment_rank()
            0
            >>> abjad.String('AB1').segment_rank()
            1
            >>> abjad.String('AB12').segment_rank()
            12

        """
        if not self.is_segment_name():
            raise ValueError(f'must be segment name (not {self!r}).')
        prefix = 'segment_'
        if self.startswith(prefix):
            index = int(self[len(prefix):])
            return index
        letter = self.segment_letter()
        if letter == self:
            return 0
        index = int(self[len(letter):])
        return index

    @staticmethod
    def sort_roman(strings) -> typing.List['String']:
        """
        Sorts strings containing Roman numerals.
        
        ..  container:: example

            >>> strings = ['TromboneII', 'TromboneIII', 'TromboneI']
            >>> abjad.String.sort_roman(strings)
            ['TromboneI', 'TromboneII', 'TromboneIII']

            >>> strings = ['ViolinXI', 'ViolinX', 'ViolinIX']
            >>> abjad.String.sort_roman(strings)
            ['ViolinIX', 'ViolinX', 'ViolinXI']

        """
        lists = []
        for string in strings:
            list_ = []
            for word in String(string).delimit_words():
                try:
                    number = roman.fromRoman(word)
                    list_.append(number)
                except roman.InvalidRomanNumeralError:
                    list_.append(word)
            lists.append(list_)
        pairs = list(zip(strings, lists))
        pairs.sort(key=lambda pair: pair[1])
        strings_ = [pair[0] for pair in pairs]
        return strings_

    @staticmethod
    def sort_segment_names(strings) -> typing.List['String']:
        """
        Sorts segment name ``strings``.
        
        ..  container:: example

            >>> strings = ['AA', 'Z', '_11', '_9']
            >>> abjad.String.sort_segment_names(strings)
            ['_9', '_11', 'Z', 'AA']

        """
        names = []
        for string in strings:
            name = String(string)
            if not name.is_segment_name():
                raise ValueError(f'must be segment name (not {string!r}).')
            names.append(name)
        def _compare(name_1, name_2):
            letter_1 = name_1.segment_letter()
            letter_2 = name_2.segment_letter()
            rank_1 = name_1.segment_rank()
            rank_2 = name_2.segment_rank()
            if letter_1 == letter_2:
                if rank_1 < rank_2:
                    return -1
                if rank_1 == rank_2:
                    return 0
                if rank_1 > rank_2:
                    return 1
            if letter_1 == '_':
                return -1
            if letter_2 == '_':
                return 1
            if len(letter_1) == len(letter_2):
                if letter_1 < letter_2:
                    return -1
                if letter_2 < letter_1:
                    return 1
            if len(letter_1) < len(letter_2):
                return -1
            assert len(letter_2) < len(letter_1)
            return 1
        names_ = TypedList(names)
        names_.sort(cmp=_compare)
        return list(names_)

    def strip_diacritics(self) -> 'String':
        """
        Strips diacritics from string.

        ..  container:: example

            >>> string = abjad.String('Dvořák')
            >>> print(string)
            Dvořák

            >>> string.strip_diacritics()
            'Dvorak'

        """
        normalized_unicode_string = unicodedata.normalize('NFKD', self)
        ascii_string = normalized_unicode_string.encode('ascii', 'ignore')
        return type(self)(ascii_string.decode('utf-8'))

    def strip_roman(self) -> 'String':
        """
        Strips roman numerals from right of string.

        ..  container:: example

            >>> abjad.String('Trombone').strip_roman()
            'Trombone'

            >>> abjad.String('TromboneI').strip_roman()
            'Trombone'

            >>> abjad.String('TromboneII').strip_roman()
            'Trombone'

            >>> abjad.String('TromboneIII').strip_roman()
            'Trombone'

            >>> abjad.String('TromboneIV').strip_roman()
            'Trombone'

        """
        words = self.delimit_words()
        try:
            roman.fromRoman(words[-1])
            words = words[:-1]
        except roman.InvalidRomanNumeralError:
            pass
        return String(''.join(words))

    def to_accent_free_snake_case(self) -> 'String':
        """
        Changes string to accent-free snake case.

        ..  container:: example

            >>> abjad.String('Déja vu').to_accent_free_snake_case()
            'deja_vu'

        """
        string = self.strip_diacritics()
        string_ = string.replace(' ', '_')
        string_ = string_.replace("'", '_')
        string_ = string_.lower()
        return type(self)(string_)

    @staticmethod
    def to_bidirectional_direction_string(argument) -> 'String':
        """
        Changes ``argument`` to bidirectional direction string.

        ..  container:: example:

            >>> abjad.String.to_bidirectional_direction_string('^')
            'Up'

            >>> abjad.String.to_bidirectional_direction_string('_')
            'Down'

            >>> abjad.String.to_bidirectional_direction_string(1)
            'Up'

            >>> abjad.String.to_bidirectional_direction_string(-1)
            'Down'

        """
        try:
            alignment = enums.VerticalAlignment.from_expr(argument)
        except Exception:
            raise ValueError(repr(argument))
        if alignment is enums.Center:
            raise ValueError(repr(argument))
        return String(alignment)

    @staticmethod
    def to_bidirectional_lilypond_symbol(argument) -> 'String':
        """
        Changes ``argument`` to bidirectional LilyPond symbol.

        ..  container:: example

            >>> abjad.String.to_bidirectional_lilypond_symbol(abjad.Up)
            '^'

            >>> abjad.String.to_bidirectional_lilypond_symbol(abjad.Down)
            '_'

            >>> abjad.String.to_bidirectional_lilypond_symbol(1)
            '^'

            >>> abjad.String.to_bidirectional_lilypond_symbol(-1)
            '_'

        """
        try:
            alignment = enums.VerticalAlignment.from_expr(argument)
        except Exception:
            raise ValueError(repr(argument))
        if alignment is enums.Center:
            raise ValueError(repr(argument))
        return String(format(alignment, 'lilypond'))

    def to_dash_case(self) -> 'String':
        """
        Changes string to dash case.

        ..  container:: example

            >>> abjad.String('scale degrees 4 and 5').to_dash_case()
            'scale-degrees-4-and-5'

            >>> abjad.String('scale_degrees_4_and_5').to_dash_case()
            'scale-degrees-4-and-5'

            >>> abjad.String('scale-degrees-4-and-5').to_dash_case()
            'scale-degrees-4-and-5'

            >>> abjad.String('ScaleDegrees4And5').to_dash_case()
            'scale-degrees-4-and-5'

        """
        words = self.delimit_words()
        words_ = [_.lower() for _ in words]
        string = '-'.join(words_)
        return type(self)(string)

    @staticmethod
    def to_indicator_stem(indicator) -> 'String':
        """
        Changes ``indicator`` to stem.

        ..  container:: example

            >>> abjad.String.to_indicator_stem(abjad.Clef('alto'))
            'CLEF'

            >>> abjad.String.to_indicator_stem(abjad.Clef('treble'))
            'CLEF'

            >>> abjad.String.to_indicator_stem(abjad.Dynamic('f'))
            'DYNAMIC'

            >>> abjad.String.to_indicator_stem(abjad.Cello())
            'INSTRUMENT'

            >>> abjad.String.to_indicator_stem(abjad.Violin())
            'INSTRUMENT'

            >>> metronome_mark = abjad.MetronomeMark((1, 4), 58)
            >>> abjad.String.to_indicator_stem(metronome_mark)
            'METRONOME_MARK'

        """
        parameter = getattr(indicator, 'parameter', None)
        if isinstance(parameter, str):
            stem = parameter.lstrip('abjad.')
        else:
            stem = type(indicator).__name__
        return String(stem).to_shout_case()

    def to_lower_camel_case(self) -> 'String':
        """
        Changes string to lower camel case.

        ..  container:: example

            >>> abjad.String('scale degrees 4 and 5').to_lower_camel_case()
            'scaleDegrees4And5'

            >>> abjad.String('scale_degrees_4_and_5').to_lower_camel_case()
            'scaleDegrees4And5'

            >>> abjad.String('scale-degrees-4-and-5').to_lower_camel_case()
            'scaleDegrees4And5'

            >>> abjad.String('ScaleDegrees4And5').to_lower_camel_case()
            'scaleDegrees4And5'

        """
        string = self.to_upper_camel_case()
        if string == '':
            pass
        else:
            string = type(self)(string[0].lower() + string[1:])
        return string

    def to_segment_lilypond_identifier(self) -> 'String':
        """
        Changes string to segment LilyPond identifier.

        ..  container:: example

            >>> abjad.String('_').to_segment_lilypond_identifier()
            'i'
            >>> abjad.String('_1').to_segment_lilypond_identifier()
            'i_a'
            >>> abjad.String('_2').to_segment_lilypond_identifier()
            'i_b'

            >>> abjad.String('A').to_segment_lilypond_identifier()
            'A'
            >>> abjad.String('A1').to_segment_lilypond_identifier()
            'A_a'
            >>> abjad.String('A2').to_segment_lilypond_identifier()
            'A_b'

            >>> abjad.String('B').to_segment_lilypond_identifier()
            'B'
            >>> abjad.String('B1').to_segment_lilypond_identifier()
            'B_a'
            >>> abjad.String('B2').to_segment_lilypond_identifier()
            'B_b'

            >>> abjad.String('AA').to_segment_lilypond_identifier()
            'AA'
            >>> abjad.String('AA1').to_segment_lilypond_identifier()
            'AA_a'
            >>> abjad.String('AA2').to_segment_lilypond_identifier()
            'AA_b'

        """
        name = self.replace('_', 'i')
        words = []
        for word in String(name).delimit_words():
            if word.isdigit():
                word_ = String.base_26(int(word)).lower()
                words.append(word_)
            else:
                words.append(word)
        identifier = '_'.join(words)
        return String(identifier)

    def to_shout_case(self) -> 'String':
        """
        Changes string to shout case.

        ..  container:: example

            >>> abjad.String('scale degrees 4 and 5').to_shout_case()
            'SCALE_DEGREES_4_AND_5'

            >>> abjad.String('scale_degrees_4_and_5').to_shout_case()
            'SCALE_DEGREES_4_AND_5'

            >>> abjad.String('scale-degrees-4-and-5').to_shout_case()
            'SCALE_DEGREES_4_AND_5'

            >>> abjad.String('ScaleDegrees4And5').to_shout_case()
            'SCALE_DEGREES_4_AND_5'

        """
        words = self.delimit_words()
        words_ = [_.upper() for _ in words]
        string = '_'.join(words_)
        return type(self)(string)

    def to_snake_case(self) -> 'String':
        """
        Changes string to snake case.

        ..  container:: example

            >>> abjad.String('scale degrees 4 and 5').to_snake_case()
            'scale_degrees_4_and_5'

            >>> abjad.String('scale_degrees_4_and_5').to_snake_case()
            'scale_degrees_4_and_5'

            >>> abjad.String('scale-degrees-4-and-5').to_snake_case()
            'scale_degrees_4_and_5'

            >>> abjad.String('ScaleDegrees4And5').to_snake_case()
            'scale_degrees_4_and_5'

        """
        words = self.delimit_words()
        words_ = [_.lower() for _ in words]
        string = '_'.join(words_)
        return type(self)(string)

    def to_space_delimited_lowercase(self) -> 'String':
        """
        Changes string to space-delimited lowercase.

        ..  container:: example

            >>> abjad.String('LogicalTie').to_space_delimited_lowercase()
            'logical tie'

            >>> abjad.String('logical_tie').to_space_delimited_lowercase()
            'logical tie'

            >>> abjad.String('logical tie').to_space_delimited_lowercase()
            'logical tie'

        ..  container:: example

            >>> abjad.String('').to_space_delimited_lowercase()
            ''

        """
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
    def to_tridirectional_direction_string(argument) -> typing.Optional[
        'String']:
        """
        Changes ``argument`` to tridirectional direction string.

        ..  container:: example

            >>> abjad.String.to_tridirectional_direction_string('^')
            'Up'

            >>> abjad.String.to_tridirectional_direction_string('-')
            'Center'

            >>> abjad.String.to_tridirectional_direction_string('_')
            'Down'

            >>> abjad.String.to_tridirectional_direction_string(1)
            'Up'

            >>> abjad.String.to_tridirectional_direction_string(0)
            'Center'

            >>> abjad.String.to_tridirectional_direction_string(-1)
            'Down'

        ..  container:: example

            Returns none when ``argument`` is none:

            >>> abjad.String.to_tridirectional_direction_string(None) is None
            True

        """
        if argument is None:
            return None
        try:
            alignment = enums.VerticalAlignment.from_expr(argument)
        except Exception:
            raise ValueError(repr(argument))
        return String(alignment)

    @staticmethod
    def to_tridirectional_lilypond_symbol(
        argument: typing.Any,
        ) -> typing.Optional['String']:
        """
        Changes ``argument`` to tridirectional LilyPond symbol.

        ..  container:: example

            >>> abjad.String.to_tridirectional_lilypond_symbol(abjad.Up)
            '^'

            >>> abjad.String.to_tridirectional_lilypond_symbol('center')
            '-'

            >>> abjad.String.to_tridirectional_lilypond_symbol(abjad.Down)
            '_'

            >>> abjad.String.to_tridirectional_lilypond_symbol(1)
            '^'

            >>> abjad.String.to_tridirectional_lilypond_symbol(0)
            '-'

            >>> abjad.String.to_tridirectional_lilypond_symbol(-1)
            '_'

            >>> abjad.String.to_tridirectional_lilypond_symbol('^')
            '^'

            >>> abjad.String.to_tridirectional_lilypond_symbol('-')
            '-'

            >>> abjad.String.to_tridirectional_lilypond_symbol('_')
            '_'

        ..  container:: example

            Returns none when ``argument`` is none:

            >>> abjad.String.to_tridirectional_lilypond_symbol(None) is None
            True

        """
        if argument is None:
            return None
        try:
            alignment = enums.VerticalAlignment.from_expr(argument)
        except Exception:
            raise ValueError(repr(argument))
        return String(format(alignment, 'lilypond'))

    @staticmethod
    def to_tridirectional_ordinal_constant(
        argument,
        ) -> typing.Union[None, enums.VerticalAlignment, 'String']:
        """
        Changes ``argument`` to tridirectional ordinal constant.

        ..  container:: example

            >>> abjad.String.to_tridirectional_ordinal_constant('^')
            Up

            >>> abjad.String.to_tridirectional_ordinal_constant('_')
            Down

            >>> abjad.String.to_tridirectional_ordinal_constant(1)
            Up

            >>> abjad.String.to_tridirectional_ordinal_constant(-1)
            Down

            >>> abjad.String.to_tridirectional_ordinal_constant(abjad.Up)
            Up

            >>> abjad.String.to_tridirectional_ordinal_constant(abjad.Down)
            Down

            >>> abjad.String.to_tridirectional_ordinal_constant(abjad.Center)
            Center

        ..  container:: example

            >>> abjad.String.to_tridirectional_ordinal_constant(None) is None
            True

        """
        if argument is None:
            return None
        return enums.VerticalAlignment.from_expr(argument)

    def to_upper_camel_case(self) -> 'String':
        """
        Changes string to upper camel case.

        ..  container:: example

            >>> abjad.String('scale degrees 4 and 5').to_upper_camel_case()
            'ScaleDegrees4And5'

            >>> abjad.String('scale_degrees_4_and_5').to_upper_camel_case()
            'ScaleDegrees4And5'

            >>> abjad.String('scale-degrees-4-and-5').to_upper_camel_case()
            'ScaleDegrees4And5'

            >>> abjad.String('ScaleDegrees4And5').to_upper_camel_case()
            'ScaleDegrees4And5'

        """
        words = self.delimit_words()
        words_ = [_.capitalize() for _ in words]
        string = ''.join(words_)
        return type(self)(string)
