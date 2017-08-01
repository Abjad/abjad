# -*- coding: utf-8 -*-


def tweak(argument):
    r'''Makes LilyPond tweak manager.

    ::

        >>> import abjad

    ..  container:: example

        Tweaks markup:

        ::

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> markup = abjad.Markup('Allegro assai', direction=Up)
            >>> abjad.tweak(markup).color = 'red'
            >>> abjad.attach(markup, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

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
            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> markup_1 = abjad.Markup('Allegro assai', direction=Up)
            >>> abjad.tweak(markup_1).color = 'red'
            >>> markup_2 = copy.copy(markup_1)
            >>> abjad.attach(markup_2, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

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

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> markup = abjad.Markup('Allegro assai', direction=Up)
            >>> abjad.tweak(markup).color = 'red'
            >>> markup = markup.italic()
            >>> abjad.attach(markup, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

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

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> markup_1 = abjad.Markup('Allegro assai ...', direction=Up)
            >>> abjad.tweak(markup_1).color = 'red'
            >>> abjad.attach(markup_1, staff[0])
            >>> markup_2 = abjad.Markup('... ma non troppo', direction=Down)
            >>> abjad.tweak(markup_2).color = 'blue'
            >>> abjad.tweak(markup_2).staff_padding = 4
            >>> abjad.attach(markup_2, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

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

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> markup_1 = abjad.Markup('Allegro assai ...', direction=Up)
            >>> abjad.tweak(markup_1).color = 'red'
            >>> abjad.attach(markup_1, staff[0])
            >>> markup_2 = abjad.Markup('... ma non troppo', direction=Up)
            >>> abjad.tweak(markup_2).color = 'blue'
            >>> abjad.tweak(markup_2).staff_padding = 4
            >>> abjad.attach(markup_2, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

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

            >>> abjad.tweak(markup_1)
            LilyPondTweakManager(('color', 'red'))

    ''' 
    from abjad.tools import lilypondnametools
    if getattr(argument, '_lilypond_tweak_manager', None) is None:
        manager = lilypondnametools.LilyPondTweakManager()
        argument._lilypond_tweak_manager = manager
    return argument._lilypond_tweak_manager
