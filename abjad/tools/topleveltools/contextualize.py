def contextualize(expr):
    r'''Applies LilyPond context contextualize to `expr`.

    Returns LilyPond context contextualize manager.
    '''
    from abjad.tools import lilypondproxytools

    if not hasattr(expr, '_set'):
        manager = lilypondproxytools.LilyPondSettingManager()
        expr._set = manager

    return expr._set
