# -*- coding: utf-8 -*-


def set_(argument):
    r'''Makes LilyPond setting name manager.

    ..  container:: example

        Sets instrument name:

        ::

            >>> staff = Staff("c'4 e'4 d'4 f'4")
            >>> set_(staff).instrument_name = Markup('Vn. I')
            >>> show(staff) # doctest: +SKIP


        ..  doctest::

            >>> f(staff)
            \new Staff \with {
                instrumentName = \markup { "Vn. I" }
            } {
                c'4
                e'4
                d'4
                f'4
            }

    ..  container:: example

        Returns LilyPond setting name manager:

        ::

            >>> set_(staff)
            LilyPondSettingNameManager(('instrument_name', Markup(contents=['Vn. I'])))

    '''
    from abjad.tools import lilypondnametools
    if getattr(argument, '_lilypond_setting_name_manager', None) is None:
        manager = lilypondnametools.LilyPondSettingNameManager()
        argument._lilypond_setting_name_manager = manager
    return argument._lilypond_setting_name_manager
