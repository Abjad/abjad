def set_default_accidental_spelling(spelling='mixed'):
    '''.. versionadded:: 1.1

    Set default accidental spelling to sharps::

        >>> from abjad.tools import configurationtools

    ::

        >>> pitchtools.set_default_accidental_spelling('sharps')

    ::

        >>> [Note(13, (1, 4)), Note(15, (1, 4))]
        [Note("cs''4"), Note("ds''4")]

    Set default accidental spelling to flats::

        >>> pitchtools.set_default_accidental_spelling('flats')

    ::

        >>> [Note(13, (1, 4)), Note(15, (1, 4))]
        [Note("df''4"), Note("ef''4")]

    Set default accidental spelling to mixed::

        >>> pitchtools.set_default_accidental_spelling()

    ::

        >>> [Note(13, (1, 4)), Note(15, (1, 4))]
        [Note("cs''4"), Note("ef''4")]

    Mixed is system default.

    Mixed test case must appear last here for doc tests to check correctly.

    Return none.

    .. versionchanged:: 2.0
        renamed ``pitchtools.change_default_accidental_spelling()`` to
        ``pitchtools.set_default_accidental_spelling()``.

    .. versionchanged:: 2.9
        renamed ``configurationtools.set_default_accidental_spelling()`` to
        ``pitchtools.set_default_accidental_spelling()``.
    '''
    from abjad import ABJCFG

    if spelling not in ('mixed', 'sharps', 'flats'):
        raise ValueError

    ABJCFG['accidental_spelling'] = spelling
