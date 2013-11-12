def override(expr):
    r'''Overrides `expr`.

    Returns LilyPond grob manager.
    '''
    from abjad.tools import lilypondnametools

    if not hasattr(expr, '_override'):
        plug_in = lilypondnametools.LilyPondGrobNameManager()
        expr._override = plug_in

    return expr._override
