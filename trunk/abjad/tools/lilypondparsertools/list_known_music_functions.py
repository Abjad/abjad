def list_known_music_functions():
    '''List all music functions recognized by ``LilyPondParser``:

    ::

        >>> for x in lilypondparsertools.list_known_music_functions():
        ...     print x
        ...
        acciaccatura
        appoggiatura
        bar
        breathe
        clef
        grace
        key
        language
        makeClusters
        mark
        relative
        skip
        time
        times
        transpose

    Return list.
    '''
    from abjad.ly import current_module
    from abjad.tools import lilypondparsertools

    music_functions = []
    for name in current_module:
        if isinstance(current_module[name], dict) and 'type' in current_module[name]:
            if current_module[name]['type'] == 'ly:music-function?':
                if hasattr(lilypondparsertools.GuileProxy, name):
                    music_functions.append(name)

    return sorted(music_functions)
