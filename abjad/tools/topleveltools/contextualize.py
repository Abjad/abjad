def contextualize(expr):
    r'''Applies LilyPond context setting to `expr`.

    Returns LilyPond context setting manager.
    '''
    from abjad.tools import lilypondnametools

    if getattr(expr, '_set', None) is None:
    #if not hasattr(expr, '_set'):
        manager = lilypondnametools.LilyPondSettingNameManager()
        expr._set = manager

    return expr._set
