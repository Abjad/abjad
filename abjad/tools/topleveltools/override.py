def override(expr):
    r'''Overrides `expr`.

    Returns LilyPond grob manager.
    '''
    from abjad.tools import lilypondnametools

    if getattr(expr, '_lilypond_grob_name_manager', None) is None:
        manager = lilypondnametools.LilyPondGrobNameManager()
        expr._lilypond_grob_name_manager = manager

    return expr._lilypond_grob_name_manager
