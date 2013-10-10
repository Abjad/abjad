# -*- encoding: utf-8 -*-


def alphabetic_accidental_abbreviation_to_symbolic_accidental_string(alphabetic_accidental_abbreviation):
    '''Change `alphabetic_accidental_abbreviation` to symbolic accidental string:

    ::

        >>> pitchtools.alphabetic_accidental_abbreviation_to_symbolic_accidental_string('tqs')
        '#+'

    None when `alphabetic_accidental_abbreviation` is not a valid alphabetic accidental
    abbreviation.

    Return string or none.
    '''
    from abjad.tools import pitchtools
    return pitchtools.Accidental._alphabetic_accidental_abbreviation_to_symbolic_accidental_string.get(
        alphabetic_accidental_abbreviation)

