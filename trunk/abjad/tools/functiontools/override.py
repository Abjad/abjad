def override(expr):
    r'''Overrides `expr`.

    Returns LilyPond grob manager.
    '''

    if not hasattr(expr, '_override'):
        plug_in = lilypondproxytools.LilyPondGrobOverrideComponentPlugIn()
        expr._override = plug_in

    return expr._override
