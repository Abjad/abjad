# -*- coding: utf-8 -*-


def override(expr):
    r'''Makes LilyPond grob name manager.

    ..  container:: example

        Overrides staff symbol color:

        ::

            >>> staff = Staff("c'4 e'4 d'4 f'4")
            >>> override(staff).staff_symbol.color = 'red'
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

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

            >>> override(staff)
            LilyPondGrobNameManager(('staff_symbol', LilyPondNameManager(('color', 'red'))))

    '''
    from abjad.tools import lilypondnametools
    if getattr(expr, '_lilypond_grob_name_manager', None) is None:
        manager = lilypondnametools.LilyPondGrobNameManager()
        expr._lilypond_grob_name_manager = manager
    return expr._lilypond_grob_name_manager
