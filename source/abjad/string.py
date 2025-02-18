import textwrap

import roman

from . import enums as _enums


def capitalize_start(string: str) -> str:
    """
    Capitalizes start of string.

    ..  container:: example

        Capitalizes only ``string[0]``; leaves noninitial characters unchanged:

        >>> abjad.string.capitalize_start("violin I")
        'Violin I'

        Built-in ``str.capitalize()`` forces noninitial characters to lowercase:

        >>> "violin I".capitalize()
        'Violin i'

    """
    if not string:
        return string
    return string[0].upper() + string[1:]


def delimit_words(string: str, separate_caps: bool = False) -> list[str]:
    """
    Delimits words in string.

    ..  container:: example

        >>> abjad.string.delimit_words('scale degrees 4 and 5.')
        ['scale', 'degrees', '4', 'and', '5']

        >>> abjad.string.delimit_words('scale degrees 4and5.')
        ['scale', 'degrees', '4', 'and', '5']

        >>> abjad.string.delimit_words('scaleDegrees4and5.')
        ['scale', 'Degrees', '4', 'and', '5']

        >>> abjad.string.delimit_words('ScaleDegrees4and 5.')
        ['Scale', 'Degrees', '4', 'and', '5']

        >>> abjad.string.delimit_words('scale-degrees-4-and-5.')
        ['scale', 'degrees', '4', 'and', '5']

        >>> abjad.string.delimit_words('SCALE_DEGREES_4_AND_5.')
        ['SCALE', 'DEGREES', '4', 'AND', '5']

    ..  container:: example

        >>> abjad.string.delimit_words('one < two')
        ['one', '<', 'two']

        >>> abjad.string.delimit_words('one! two!')
        ['one', '!', 'two', '!']

    ..  container:: example

        Separates capital letters when keyword is true:

        >>> abjad.string.delimit_words('MRM')
        ['MRM']

        >>> abjad.string.delimit_words("MRM", separate_caps=True)
        ['M', 'R', 'M']

        >>> abjad.string.delimit_words('MRhM')
        ['MRh', 'M']

        >>> abjad.string.delimit_words("MRhM", separate_caps=True)
        ['M', 'Rh', 'M']

    """
    wordlike_characters = ("<", ">", "!")
    words = []
    current_word = ""
    for character in string:
        if (
            not character.isalpha()
            and not character.isdigit()
            and character not in wordlike_characters
        ):
            if current_word:
                words.append(current_word)
                current_word = ""
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
    return words


def from_roman(string: str) -> int:
    """
    Changes string from Roman numeral to digits.

    ..  container:: example

        >>> abjad.string.from_roman('IX')
        9
        >>> abjad.string.from_roman('ix')
        9

        Raises Roman numeral error when string is not Roman numeral:

        >>> abjad.string.from_roman('Allegro')
        Traceback (most recent call last):
            ...
        roman.InvalidRomanNumeralError...

    """
    if is_roman(string):
        return roman.fromRoman(string.upper())
    number = roman.fromRoman(string)
    return number


def is_lilypond_identifier(string: str) -> bool:
    """
    Is true when string starts with a letter and either 1. contains only letters and
    underscores thereafter, or 2. contains only letters, numbers and dots thereafter.

    ..  container:: example

        >>> abjad.string.is_lilypond_identifier("ViolinOne")
        True

        >>> abjad.string.is_lilypond_identifier("Violin_One")
        True

        >>> abjad.string.is_lilypond_identifier("Violin One")
        False

    ..  container:: example

        >>> abjad.string.is_lilypond_identifier("ViolinI")
        True

        >>> abjad.string.is_lilypond_identifier("Violin_I")
        True

        >>> abjad.string.is_lilypond_identifier("Violin I")
        False

    ..  container:: example

        >>> abjad.string.is_lilypond_identifier("Violin1")
        False

        >>> abjad.string.is_lilypond_identifier("Violin_1")
        False

        >>> abjad.string.is_lilypond_identifier("Violin 1")
        False

    ..  container:: example

        >>> abjad.string.is_lilypond_identifier("Violin.1")
        True

        >>> abjad.string.is_lilypond_identifier("Violin.1.1")
        False

        >>> abjad.string.is_lilypond_identifier("Violin.1_1")
        False

        >>> abjad.string.is_lilypond_identifier("Violin_1.1")
        False

    ..  container:: example

        >>> abjad.string.is_lilypond_identifier("Violin.1.MusicVoice.1")
        True

        >>> abjad.string.is_lilypond_identifier("Violin.1.1.MusicVoice")
        False

        >>> abjad.string.is_lilypond_identifier("Violin.1_Music_Voice")
        False

        >>> abjad.string.is_lilypond_identifier("Violin.Music_Voice_1")
        False

        >>> abjad.string.is_lilypond_identifier("Violin.1_Music_Voice")
        False

    """
    if not string:
        return False
    if string[0] in "_.":
        return False
    if string[0].isdigit():
        return False
    for character in string:
        if not (character.isalnum() or character == "_" or character == "."):
            return False
    words = string.split(".")
    if words[0].isdigit():
        return False
    previous_word_ends_in_digit = False
    for word in words:
        if previous_word_ends_in_digit and word[0].isdigit():
            return False
        if any(_.isdigit() for _ in word):
            if any(not _.isdigit() for _ in word):
                return False
        if word[-1].isdigit():
            previous_word_ends_in_digit = True
        else:
            previous_word_ends_in_digit = False
    return True


def is_roman(string: str) -> bool:
    """
    Is true when string is Roman numeral.

    ..  container:: example

        >>> abjad.string.is_roman('I')
        True

        >>> abjad.string.is_roman('II')
        True

        >>> abjad.string.is_roman('X')
        True

        >>> abjad.string.is_roman('XI')
        True

        >>> abjad.string.is_roman('C')
        True

        >>> abjad.string.is_roman('CI')
        True

        >>> abjad.string.is_roman('i')
        True

        >>> abjad.string.is_roman('F')
        False

    """
    try:
        roman.fromRoman(string.upper())
        return True
    except roman.InvalidRomanNumeralError:
        return False


def is_shout_case(string: str) -> bool:
    """
    Is true when string and is shoutcase.

    ..  container:: example

        >>> abjad.string.is_shout_case('FOO_BAR')
        True

        >>> abjad.string.is_shout_case('FooBar')
        False

    """
    return string == to_shout_case(string)


def normalize(argument: str, indent: int | str | None = None) -> str:
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

        >>> print(abjad.string.normalize(string))
        foo
            bar

        >>> print(abjad.string.normalize(string, indent=4))
            foo
                bar

        >>> print(abjad.string.normalize(string, indent='* '))
        * foo
        *     bar

    """
    string = argument.replace("\t", "    ")
    lines = string.split("\n")
    while lines and (not lines[0] or lines[0].isspace()):
        lines.pop(0)
    while lines and (not lines[-1] or lines[-1].isspace()):
        lines.pop()
    for i, line in enumerate(lines):
        lines[i] = line.rstrip()
    string = "\n".join(lines)
    string = textwrap.dedent(string)
    if indent:
        if isinstance(indent, str):
            indent_string = indent
        else:
            assert isinstance(indent, int)
            indent_string = abs(int(indent)) * " "
        lines = string.split("\n")
        for i, line in enumerate(lines):
            if line:
                lines[i] = f"{indent_string}{line}"
        string = "\n".join(lines)
    return string


def pluralize(string: str, count: int | None = None) -> str:
    """
    Pluralizes English string.

    Changes terminal ``-y`` to ``-ies``:

    ..  container:: example

        >>> abjad.string.pluralize('catenary')
        'catenaries'

        Adds ``-es`` to terminal ``-s``, ``-sh``, ``-x`` and ``-z``:

        >>> abjad.string.pluralize('brush')
        'brushes'

        Adds ``-s`` to all other strings:

        >>> abjad.string.pluralize('shape')
        'shapes'

    ..  container:: example

        Does not pluralize when ``count`` is 1:

        >>> abjad.string.pluralize('shape', count=1)
        'shape'

    """
    if count == 1:
        return string
    elif string.endswith("y"):
        result = string[:-1] + "ies"
    elif string.endswith(("s", "sh", "x", "z")):
        result = string + "es"
    else:
        result = string + "s"
    return result


def sort_roman(strings: list[str]) -> list[str]:
    """
    Sorts strings containing Roman numerals.

    ..  container:: example

        >>> strings = ['TromboneII', 'TromboneIII', 'TromboneI']
        >>> abjad.string.sort_roman(strings)
        ['TromboneI', 'TromboneII', 'TromboneIII']

        >>> strings = ['ViolinXI', 'ViolinX', 'ViolinIX']
        >>> abjad.string.sort_roman(strings)
        ['ViolinIX', 'ViolinX', 'ViolinXI']

    """
    lists = []
    for string in strings:
        list_ = []
        for word in delimit_words(string):
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


def strip_roman(string: str) -> str:
    """
    Strips roman numerals from right of string.

    ..  container:: example

        >>> abjad.string.strip_roman('Trombone')
        'Trombone'

        >>> abjad.string.strip_roman('TromboneI')
        'Trombone'

        >>> abjad.string.strip_roman('TromboneII')
        'Trombone'

        >>> abjad.string.strip_roman('TromboneIII')
        'Trombone'

        >>> abjad.string.strip_roman('TromboneIV')
        'Trombone'

    """
    words = delimit_words(string)
    try:
        roman.fromRoman(words[-1])
        words = words[:-1]
    except roman.InvalidRomanNumeralError:
        pass
    return "".join(words)


def to_shout_case(string: str) -> str:
    """
    Changes string to shout case.

    ..  container:: example

        >>> abjad.string.to_shout_case('scale degrees 4 and 5')
        'SCALE_DEGREES_4_AND_5'

        >>> abjad.string.to_shout_case('scale_degrees_4_and_5')
        'SCALE_DEGREES_4_AND_5'

        >>> abjad.string.to_shout_case('scale-degrees-4-and-5')
        'SCALE_DEGREES_4_AND_5'

        >>> abjad.string.to_shout_case('ScaleDegrees4And5')
        'SCALE_DEGREES_4_AND_5'

    """
    words = delimit_words(string)
    words_ = [_.upper() for _ in words]
    string = "_".join(words_)
    return string


def to_tridirectional_lilypond_symbol(
    argument: int | str | None,
) -> str | None:
    """
    Changes ``argument`` to tridirectional LilyPond symbol.

    ..  container:: example

        >>> abjad.string.to_tridirectional_lilypond_symbol(abjad.UP)
        '^'

        >>> abjad.string.to_tridirectional_lilypond_symbol(abjad.DOWN)
        '_'

        >>> abjad.string.to_tridirectional_lilypond_symbol(1)
        '^'

        >>> abjad.string.to_tridirectional_lilypond_symbol(0)
        '-'

        >>> abjad.string.to_tridirectional_lilypond_symbol(-1)
        '_'

        >>> abjad.string.to_tridirectional_lilypond_symbol('^')
        '^'

        >>> abjad.string.to_tridirectional_lilypond_symbol('-')
        '-'

        >>> abjad.string.to_tridirectional_lilypond_symbol('_')
        '_'

        Returns none when ``argument`` is none:

        >>> abjad.string.to_tridirectional_lilypond_symbol(None) is None
        True

    """
    if argument is None:
        return None
    elif argument in (_enums.UP, 1, "^"):
        return "^"
    elif argument in (_enums.DOWN, -1, "_"):
        return "_"
    elif argument in (_enums.CENTER, 0, "-"):
        return "-"
    else:
        raise ValueError(repr(argument))


def to_tridirectional_ordinal_constant(
    argument: int | str | None,
) -> _enums.Vertical | None:
    """
    Changes ``argument`` to tridirectional ordinal constant.

    ..  container:: example

        >>> abjad.string.to_tridirectional_ordinal_constant('^')
        <Vertical.UP: 1>

        >>> abjad.string.to_tridirectional_ordinal_constant('_')
        <Vertical.DOWN: -1>

        >>> abjad.string.to_tridirectional_ordinal_constant(1)
        <Vertical.UP: 1>

        >>> abjad.string.to_tridirectional_ordinal_constant(-1)
        <Vertical.DOWN: -1>

        >>> abjad.string.to_tridirectional_ordinal_constant(abjad.UP)
        <Vertical.UP: 1>

        >>> abjad.string.to_tridirectional_ordinal_constant(abjad.DOWN)
        <Vertical.DOWN: -1>

        >>> abjad.string.to_tridirectional_ordinal_constant(abjad.CENTER)
        <Vertical.CENTER: 0>

        >>> abjad.string.to_tridirectional_ordinal_constant(None) is None
        True

    """
    if argument is None:
        return None
    elif argument in ("^", _enums.UP, 1):
        return _enums.UP
    elif argument in ("_", _enums.DOWN, -1):
        return _enums.DOWN
    elif argument in ("-", _enums.CENTER, 0):
        return _enums.CENTER
    else:
        raise ValueError(repr(argument))


def to_upper_camel_case(string: str) -> str:
    """
    Changes string to upper camel case.

    ..  container:: example

        >>> abjad.string.to_upper_camel_case('scale degrees 4 and 5')
        'ScaleDegrees4And5'

        >>> abjad.string.to_upper_camel_case('scale_degrees_4_and_5')
        'ScaleDegrees4And5'

        >>> abjad.string.to_upper_camel_case('scale-degrees-4-and-5')
        'ScaleDegrees4And5'

        >>> abjad.string.to_upper_camel_case('ScaleDegrees4And5')
        'ScaleDegrees4And5'

    """
    words = delimit_words(string)
    words_ = [_.capitalize() for _ in words]
    string = "".join(words_)
    return string
