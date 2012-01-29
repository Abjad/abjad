from abjad.tools.pitchtools.is_named_chromatic_pitch_token import is_named_chromatic_pitch_token


def all_are_named_chromatic_pitch_tokens(expr):
    '''.. versionadded:: 2.6

    True when `expr` is a sequence of named chromatic pitch tokens::

        abjad> named_chromatic_pitch_tokens = [('c', 4), pitchtools.NamedChromaticPitch("a'")]

    ::

        abjad> pitchtools.all_are_named_chromatic_pitch_tokens(named_chromatic_pitch_tokens)
        True

    True when `expr` is an empty sequence::

        abjad> pitchtools.all_are_named_chromatic_pitch_tokens([])
        True

    Otherwise false::

        abjad> pitchtools.all_are_named_chromatic_pitch_tokens('foo')
        False

    Return boolean.
    '''

    return all([is_named_chromatic_pitch_token(x) for x in expr])
