def setting(expr):
    r'''Applies LilyPond context setting to `expr`.

    Returns LilyPond context setting manager.
    '''
    from abjad.tools import lilypondproxytools

    if not hasattr(expr, '_set'):
        manager = lilypondproxytools.LilyPondSettingManager()
        expr._set = manager

    return expr._set
