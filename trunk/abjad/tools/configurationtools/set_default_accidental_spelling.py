from abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch import NamedChromaticPitch


def set_default_accidental_spelling(spelling='mixed'):
    '''.. versionadded:: 1.1

    Set default accidental spelling to sharps::

        abjad> from abjad.tools import configurationtools

    ::

        abjad> configurationtools.set_default_accidental_spelling('sharps')

    ::

        abjad> [Note(13, (1, 4)), Note(15, (1, 4))]
        [Note("cs''4"), Note("ds''4")]

    Set default accidental spelling to flats::

        abjad> configurationtools.set_default_accidental_spelling('flats')

    ::

        abjad> [Note(13, (1, 4)), Note(15, (1, 4))]
        [Note("df''4"), Note("ef''4")]

    Set default accidental spelling to mixed::

        abjad> configurationtools.set_default_accidental_spelling()

    ::

        abjad> [Note(13, (1, 4)), Note(15, (1, 4))]
        [Note("cs''4"), Note("ef''4")]

    Mixed is system default.

    Mixed test case must appear last here for doc tests to check correctly.

    Return none.

    .. versionchanged:: 2.0
        renamed ``pitchtools.change_default_accidental_spelling()`` to
        ``configurationtools.set_default_accidental_spelling()``.
    '''

    if spelling not in ('mixed', 'sharps', 'flats'):
        raise ValueError

    NamedChromaticPitch.accidental_spelling = spelling
