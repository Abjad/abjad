def uppercamelcase_to_underscore_delimited_lowercase(string):
    r'''.. versionadded:: 2.6

    Change uppercamelcase `string` to underscore-delimited lowercase::

        >>> string = 'KeySignatureMark'

    ::

        >>> stringtools.uppercamelcase_to_underscore_delimited_lowercase(string)
        'key_signature_mark'

    Return string.

    .. versionchanged:: 2.9
        renamed ``iotools.uppercamelcase_to_underscore_delimited_lowercase()`` to
        ``stringtools.uppercamelcase_to_underscore_delimited_lowercase()``.
    '''

    words = []
    cur_word = string[0].lower()
    for letter in string[1:]:
        if letter.isupper():
            words.append(cur_word)
            cur_word = letter.lower()
        else:
            cur_word = cur_word + letter
    words.append(cur_word)
    result = '_'.join(words)
    return result
