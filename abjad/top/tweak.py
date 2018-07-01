from abjad import enums


def tweak(argument):
    r"""
    Makes LilyPond tweak manager.

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
                - \tweak color #red
                ^ \markup { "Allegro assai ..." }
                - \tweak color #blue
                - \tweak staff-padding #4
                ^ \markup { "... ma non troppo" }
                d'4
                e'4
                f'4
            }

    ..  container:: example

        Tweaks note-head:

        >>> staff = abjad.Staff("c'4 cs' d' ds'")
        >>> abjad.tweak(staff[1].note_head).color = 'red'
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                \tweak color #red
                cs'4
                d'4
                ds'4
            }

        Tweaks grob aggregated to note-head:

        >>> staff = abjad.Staff("c'4 cs' d' ds'")
        >>> abjad.tweak(staff[1].note_head).accidental.color = 'red'
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                \tweak Accidental.color #red
                cs'4
                d'4
                ds'4
            }

    ..  container:: example

        Returns LilyPond tweak manager:

        >>> abjad.tweak(markup_1)
        LilyPondTweakManager(('color', 'red'))

    ..  container:: example

        Tweak expressions work like this:

        >>> abjad.tweak('red').color
        LilyPondTweakManager(('color', 'red'))

        >>> abjad.tweak(6).Y_offset
        LilyPondTweakManager(('Y_offset', 6))

        >>> abjad.tweak(False).bound_details__left_broken__text
        LilyPondTweakManager(('bound_details__left_broken__text', False))

    """
    import abjad
    constants = (enums.Down, enums.Left, enums.Right, enums.Up)
    prototype = (bool, int, float, str, tuple, abjad.Scheme)
    if argument in constants or isinstance(argument, prototype):
        manager = abjad.LilyPondTweakManager()
        manager._pending_value = argument
        return manager
    if not hasattr(argument, '_tweaks'):
        name = type(argument).__name__
        raise NotImplementedError(f'{name} does not allow tweaks (yet).')
    if argument._tweaks is None:
        argument._tweaks = abjad.LilyPondTweakManager()
    return argument._tweaks
