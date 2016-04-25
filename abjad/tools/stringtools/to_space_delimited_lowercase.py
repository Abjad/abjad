# -*- coding: utf-8 -*-


def to_space_delimited_lowercase(string):
    r'''Changes `string` to space-delimited lowercase.
    
    ..  container:: example

        Changes upper camel case `string` to space-delimited lowercase:

        ::

            >>> stringtools.to_space_delimited_lowercase('LogicalTie')
            'logical tie'

    ..  container:: example

        Changes underscore-delimited `string` to space-delimited lowercase:

        ::

            >>> stringtools.to_space_delimited_lowercase('logical_tie')
            'logical tie'

    ..  container:: example

        Returns space-delimited string unchanged:

        ::

            >>> stringtools.to_space_delimited_lowercase('logical tie')
            'logical tie'

    ..  container:: example

        Returns empty `string` unchanged:

        ::

            >>> stringtools.to_space_delimited_lowercase('')
            ''

    Returns string.
    '''
    if not string:
        return string
    elif string[0].isupper():
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
    return string.replace('_', ' ')
