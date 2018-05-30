def setting(argument):
    r"""
    Makes LilyPond setting name manager.

    ..  container:: example

        Sets instrument name:

        >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
        >>> abjad.setting(staff).instrument_name = abjad.Markup('Vn. I')
        >>> abjad.show(staff) # doctest: +SKIP


        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                instrumentName = \markup { "Vn. I" }
            }
            {
                c'4
                e'4
                d'4
                f'4
            }

    ..  container:: example

        Returns LilyPond setting name manager:

        >>> abjad.setting(staff)
        LilyPondSettingNameManager(('instrument_name', Markup(contents=['Vn. I'])))

    """
    import abjad
    if getattr(argument, '_lilypond_setting_name_manager', None) is None:
        manager = abjad.lilypondnames.LilyPondSettingNameManager()
        argument._lilypond_setting_name_manager = manager
    return argument._lilypond_setting_name_manager
