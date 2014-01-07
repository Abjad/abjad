def set_(expr):
    r'''Applies LilyPond context setting to `expr`.

    Returns LilyPond context setting manager.
    '''
    from abjad.tools import lilypondnametools

    if getattr(expr, '_lilypond_setting_name_manager', None) is None:
        manager = lilypondnametools.LilyPondSettingNameManager()
        expr._lilypond_setting_name_manager = manager

    return expr._lilypond_setting_name_manager
