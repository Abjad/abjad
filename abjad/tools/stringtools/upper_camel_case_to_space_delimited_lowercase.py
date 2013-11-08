# -*- encoding: utf-8 -*-


def upper_camel_case_to_space_delimited_lowercase(string):
    r'''Change uppercamelcase `string` to space-delimited lowercase:

    ::

        >>> string = 'KeySignature'

    ::

        >>> stringtools.upper_camel_case_to_space_delimited_lowercase(string)
        'key signature'

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
    result = ' '.join(words)
    return result
