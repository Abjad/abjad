def override(expr):
    r'''Overrides `expr`.

    Returns LilyPond grob manager.
    '''
    from abjad.tools import lilypondproxytools

    if not hasattr(expr, '_override'):
        plug_in = lilypondproxytools.LilyPondGrobManager()
        expr._override = plug_in

    return expr._override
