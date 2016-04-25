# -*- coding: utf-8 -*-
import six


def delimit_words(string):
    r'''Delimits words in `string`.

    ..  container:: example

        Delimits words::

            >>> stringtools.delimit_words('scale degrees 4 and 5.')
            ['scale', 'degrees', '4', 'and', '5']

    ..  container:: example

        Delimits conjoined words::

            >>> stringtools.delimit_words('scale degrees 4and5.')
            ['scale', 'degrees', '4', 'and', '5']

    ..  container:: example

        Delimits lower camel case::

            >>> stringtools.delimit_words('scaleDegrees4and5.')
            ['scale', 'Degrees', '4', 'and', '5']

    ..  container:: example

        Delimits upper camel case::

            >>> stringtools.delimit_words('ScaleDegrees4and 5.')
            ['Scale', 'Degrees', '4', 'and', '5']

    ..  container:: example

        Delimits dash case::

            >>> stringtools.delimit_words('scale-degrees-4-and-5.')
            ['scale', 'degrees', '4', 'and', '5']

    ..  container:: example

        Delimits shout case::

            >>> stringtools.delimit_words('SCALE_DEGREES_4_AND_5.')
            ['SCALE', 'DEGREES', '4', 'AND', '5']

    ..  container:: example

        Works with greater-than and less-than signs:

            >>> stringtools.delimit_words('one < two')
            ['one', '<', 'two']

    ..  container:: example

        Works with exclamation points:

            >>> stringtools.delimit_words('one! two!')
            ['one', '!', 'two', '!']

    Returns list.
    '''
    assert isinstance(string, six.string_types), repr(string)
    wordlike_characters = ('<', '>', '!')
    words = []
    current_word = ''
    for character in string:
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
