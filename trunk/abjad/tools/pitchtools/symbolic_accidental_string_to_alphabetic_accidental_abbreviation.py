def symbolic_accidental_string_to_alphabetic_accidental_abbreviation(symbolic_accidental_string):
    '''.. versionadded:: 2.5

    Change `symbolic_accidental_string` to alphabetic accidental abbreviation::

        abjad> pitchtools.symbolic_accidental_string_to_alphabetic_accidental_abbreviation('#+')
        'tqs'

    None when `symbolic_accidental_string` is not a valid symbolic accidental string.

    Return string or none.
    '''

    return _symbolic_accidental_string_to_alphabetic_accidental_abbreviation.get(
        symbolic_accidental_string)

_symbolic_accidental_string_to_alphabetic_accidental_abbreviation = {
    ''   : '',
    '!'  : '!',
    'bb' : 'ff',
    'b~' : 'tqf',
    'b'  : 'f',
    '~'  : 'qf',
    '##' : 'ss',
    '#+' : 'tqs',
    '#'  : 's',
    '+'  : 'qs',
    }
