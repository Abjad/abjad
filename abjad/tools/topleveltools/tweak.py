# -*- coding: utf-8 -*-


def tweak(argument):
    r'''Makes LilyPond tweak manager.

    ..  container:: example

        Tweaks markup:

        ::

            >>> staff = Staff("c'4 d' e' f'")
            >>> markup = Markup('Allegro assai', direction=Up)
            >>> tweak(markup).color = 'red'
            >>> attach(markup, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'4
                    - \tweak color #red
                    ^ \markup { "Allegro assai" }
                d'4
                e'4
                f'4
            }

        Survives copy:

        ::

            >>> import copy
            >>> staff = Staff("c'4 d' e' f'")
            >>> markup_1 = Markup('Allegro assai', direction=Up)
            >>> tweak(markup_1).color = 'red'
            >>> markup_2 = copy.copy(markup_1)
            >>> attach(markup_2, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'4
                    - \tweak color #red
                    ^ \markup { "Allegro assai" }
                d'4
                e'4
                f'4
            }

        Survives dot-chaining:

        ::

            >>> staff = Staff("c'4 d' e' f'")
            >>> markup = Markup('Allegro assai', direction=Up)
            >>> tweak(markup).color = 'red'
            >>> markup = markup.italic()
            >>> attach(markup, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'4
                    - \tweak color #red
                    ^ \markup {
                        \italic
                            "Allegro assai"
                        }
                d'4
                e'4
                f'4
            }

        Works for opposite-directed coincident markup:

        ::

            >>> staff = Staff("c'4 d' e' f'")
            >>> markup_1 = Markup('Allegro assai ...', direction=Up)
            >>> tweak(markup_1).color = 'red'
            >>> attach(markup_1, staff[0])
            >>> markup_2 = Markup('... ma non troppo', direction=Down)
            >>> tweak(markup_2).color = 'blue'
            >>> tweak(markup_2).staff_padding = 4
            >>> attach(markup_2, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'4
                    - \tweak color #red
                    ^ \markup { "Allegro assai ..." }
                    - \tweak color #blue
                    - \tweak staff-padding #4
                    _ \markup { "... ma non troppo" }
                d'4
                e'4
                f'4
            }

        Ignored for same-directed coincident markup:

        ::

            >>> staff = Staff("c'4 d' e' f'")
            >>> markup_1 = Markup('Allegro assai ...', direction=Up)
            >>> tweak(markup_1).color = 'red'
            >>> attach(markup_1, staff[0])
            >>> markup_2 = Markup('... ma non troppo', direction=Up)
            >>> tweak(markup_2).color = 'blue'
            >>> tweak(markup_2).staff_padding = 4
            >>> attach(markup_2, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'4
                    ^ \markup {
                        \column
                            {
                                \line
                                    {
                                        "Allegro assai ..."
                                    }
                                \line
                                    {
                                        "... ma non troppo"
                                    }
                            }
                        }
                d'4
                e'4
                f'4
            }

        ..  todo:: Remove courtesy autocolumn in favor of explicit tweaks?

    ..  container:: example

        Returns LilyPond tweak manager:

        ::

            >>> tweak(markup_1)
            LilyPondTweakManager(('color', 'red'))

    ''' 
    from abjad.tools import lilypondnametools
    if getattr(argument, '_lilypond_tweak_manager', None) is None:
        manager = lilypondnametools.LilyPondTweakManager()
        argument._lilypond_tweak_manager = manager
    return argument._lilypond_tweak_manager
