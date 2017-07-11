# -*- coding: utf-8 -*-


def override(argument):
    r'''Makes LilyPond grob name manager.

    ..  container:: example

        Overrides staff symbol color:

        ::

            >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
            >>> abjad.override(staff).staff_symbol.color = 'red'
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff \with {
                \override StaffSymbol.color = #red
            } {
                c'4
                e'4
                d'4
                f'4
            }

    ..  container:: example

        Returns LilyPond grob name manager:

        ::

            >>> abjad.override(staff)
            LilyPondGrobNameManager(('staff_symbol', LilyPondNameManager(('color', 'red'))))

    '''
    from abjad.tools import lilypondnametools
    if getattr(argument, '_lilypond_grob_name_manager', None) is None:
        manager = lilypondnametools.LilyPondGrobNameManager()
        argument._lilypond_grob_name_manager = manager
    return argument._lilypond_grob_name_manager
