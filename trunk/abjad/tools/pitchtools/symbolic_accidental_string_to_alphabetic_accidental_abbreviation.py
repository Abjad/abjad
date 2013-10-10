# -*- encoding: utf-8 -*-


def symbolic_accidental_string_to_alphabetic_accidental_abbreviation(symbolic_accidental_string):
    '''Change `symbolic_accidental_string` to alphabetic accidental abbreviation:

    ::

        >>> pitchtools.symbolic_accidental_string_to_alphabetic_accidental_abbreviation('#+')
        'tqs'

    None when `symbolic_accidental_string` is not a valid symbolic accidental string.

    Return string or none.
    '''
    from abjad.tools import pitchtools
    return pitchtools.Accidental._symbolic_accidental_string_to_alphabetic_accidental_abbreviation.get(
        symbolic_accidental_string)

