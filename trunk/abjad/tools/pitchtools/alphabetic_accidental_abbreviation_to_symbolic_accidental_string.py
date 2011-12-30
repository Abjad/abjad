def alphabetic_accidental_abbreviation_to_symbolic_accidental_string(alphabetic_accidental_abbreviation):
    '''.. versionadded:: 2.5

    Change `alphabetic_accidental_abbreviation` to symbolic accidental string::

        abjad> pitchtools.alphabetic_accidental_abbreviation_to_symbolic_accidental_string('tqs')
        '#+'

    None when `alphabetic_accidental_abbreviation` is not a valid alphabetic accidental
    abbreviation.

    Return string or none.
    '''

    return _alphabetic_accidental_abbreviation_to_symbolic_accidental_string.get(
        alphabetic_accidental_abbreviation)

_alphabetic_accidental_abbreviation_to_symbolic_accidental_string = {
    'ff'  : 'bb',
    'tqf' : 'b~',
    'f'   : 'b',
    'qf'  : '~',
    ''    : '',
    '!'   : '!',
    'qs'  : '+',
    's'   : '#',
    'tqs' : '#+',
    'ss'  : '##',
    }
