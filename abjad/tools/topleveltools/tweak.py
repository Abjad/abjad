from abjad.tools.lilypondnametools.LilyPondTweakManager import \
    LilyPondTweakManager


def tweak(argument):
    r'''Makes LilyPond tweak manager.

    ..  container:: example

        Tweaks markup:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup = abjad.Markup('Allegro assai', direction=abjad.Up)
        >>> abjad.tweak(markup).color = 'red'
        >>> abjad.attach(markup, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                - \tweak color #red
                ^ \markup { "Allegro assai" }
                d'4
                e'4
                f'4
            }

        Survives copy:

        >>> import copy
        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup_1 = abjad.Markup('Allegro assai', direction=abjad.Up)
        >>> abjad.tweak(markup_1).color = 'red'
        >>> markup_2 = copy.copy(markup_1)
        >>> abjad.attach(markup_2, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                - \tweak color #red
                ^ \markup { "Allegro assai" }
                d'4
                e'4
                f'4
            }

        Survives dot-chaining:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup = abjad.Markup('Allegro assai', direction=abjad.Up)
        >>> abjad.tweak(markup).color = 'red'
        >>> markup = markup.italic()
        >>> abjad.attach(markup, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
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

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup_1 = abjad.Markup('Allegro assai ...', direction=abjad.Up)
        >>> abjad.tweak(markup_1).color = 'red'
        >>> abjad.attach(markup_1, staff[0])
        >>> markup_2 = abjad.Markup('... ma non troppo', direction=abjad.Down)
        >>> abjad.tweak(markup_2).color = 'blue'
        >>> abjad.tweak(markup_2).staff_padding = 4
        >>> abjad.attach(markup_2, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
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

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup_1 = abjad.Markup('Allegro assai ...', direction=abjad.Up)
        >>> abjad.tweak(markup_1).color = 'red'
        >>> abjad.attach(markup_1, staff[0])
        >>> markup_2 = abjad.Markup('... ma non troppo', direction=abjad.Up)
        >>> abjad.tweak(markup_2).color = 'blue'
        >>> abjad.tweak(markup_2).staff_padding = 4
        >>> abjad.attach(markup_2, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
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

        >>> abjad.tweak(markup_1)
        LilyPondTweakManager(('color', 'red'))

    ..  container:: example

        Tweaks text spanner:

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> spanner = abjad.TextSpanner()
        >>> abjad.attach(spanner, staff[:])
        >>> spanner.attach(abjad.Markup('pont.').upright(), spanner[0])
        >>> spanner.attach(abjad.Markup('tasto').upright(), spanner[-1])
        >>> abjad.tweak(spanner).staff_padding = 2.5
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                - \tweak staff-padding #2.5
                - \tweak Y-extent ##f
                - \tweak bound-details.left.text \markup {
                    \concat
                        {
                            \upright
                                pont.
                            \hspace
                                #0.25
                        }
                    }
                - \tweak dash-period 0
                - \tweak bound-details.left-broken.text ##f
                - \tweak bound-details.left.stencil-align-dir-y #center
                - \tweak bound-details.right-broken.padding 0
                - \tweak bound-details.right-broken.text ##f
                - \tweak bound-details.right.padding 1.5
                - \tweak bound-details.right.stencil-align-dir-y #center
                - \tweak bound-details.right.text \markup {
                    \concat
                        {
                            \hspace
                                #1.0
                            \upright
                                tasto
                        }
                    }
                \startTextSpan
                d'4
                e'4
                f'4
                \stopTextSpan
            }

    '''
    if not hasattr(argument, '_lilypond_tweak_manager'):
        name = type(argument).__name__
        raise NotImplementedError(f'{name} does not allow tweaks (yet).')
    if argument._lilypond_tweak_manager is None:
        argument._lilypond_tweak_manager = LilyPondTweakManager()
    return argument._lilypond_tweak_manager
