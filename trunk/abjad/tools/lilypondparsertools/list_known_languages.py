# -*- encoding: utf-8 -*-

def list_known_languages():
    '''List all note-input languages recognized by ``LilyPondParser``:

    ::

        >>> for x in lilypondparsertools.list_known_languages():
        ...     print x
        ...
        catalan
        deutsch
        english
        espanol
        español
        français
        italiano
        nederlands
        norsk
        portugues
        suomi
        svenska
        vlaams

    Return list.
    '''
    from abjad.ly import language_pitch_names

    return sorted(language_pitch_names.keys())
