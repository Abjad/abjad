def uppercamelcase_to_underscore_delimited_lowercase(string):
    r'''.. versionadded:: 2.6

    Change uppercamelcase `string` to underscore-delimited lowercase::

        >>> string = 'KeySignatureMark'

    ::

        >>> stringtools.uppercamelcase_to_underscore_delimited_lowercase(string)
        'key_signature_mark'

    Return string.
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
