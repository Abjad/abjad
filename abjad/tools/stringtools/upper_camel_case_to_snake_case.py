# -*- encoding: utf-8 -*-


def upper_camel_case_to_snake_case(string):
    r'''Change uppercamelcase `string` to underscore-delimited lowercase:

    ::

        >>> string = 'KeySignatureMark'

    ::

        >>> stringtools.upper_camel_case_to_snake_case(string)
        'key_signature_mark'

    Returns string.
    '''

    words = []
    current_word = string[0].lower()
    for letter in string[1:]:
        if letter.isupper():
            words.append(current_word)
            current_word = letter.lower()
        else:
            current_word = current_word + letter
    words.append(current_word)
    result = '_'.join(words)
    return result
