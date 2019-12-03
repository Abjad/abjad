from abjad import enums


def tweak(argument, *, deactivate=None, expression=None, literal=None, tag=None):
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

        Tweaks can be tagged:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> dynamic = abjad.Dynamic("f")
        >>> abjad.tweak(dynamic, tag=abjad.Tag("RED")).color = "red"
        >>> abjad.attach(dynamic, staff[0])

        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            - \tweak color #red %! RED
            \f
            d'4
            e'4
            f'4
        }

        >>> abjad.show(staff) # doctest: +SKIP

        REGRESSION. Tweaked tags can be set multiple times:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> dynamic = abjad.Dynamic('f')
        >>> abjad.tweak(dynamic, tag=abjad.Tag("RED")).color = "red"
        >>> abjad.tweak(dynamic, tag=abjad.Tag("BLUE")).color = "blue"
        >>> abjad.attach(dynamic, staff[0])

        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            - \tweak color #blue %! BLUE
            \f
            d'4
            e'4
            f'4
        }

        >>> abjad.show(staff) # doctest: +SKIP

    ..  container:: example

        Returns LilyPond tweak manager:

        >>> abjad.tweak(markup_1)
        LilyPondTweakManager(('_literal', None), ('color', 'red'))

    ..  container:: example

        Tweak expressions work like this:

        >>> abjad.tweak('red').color
        LilyPondTweakManager(('_literal', None), ('color', 'red'))

        >>> abjad.tweak(6).Y_offset
        LilyPondTweakManager(('Y_offset', 6), ('_literal', None))

        >>> abjad.tweak(False).bound_details__left_broken__text
        LilyPondTweakManager(('_literal', None), ('bound_details__left_broken__text', False))

    """
    import abjad

    if tag is not None and not isinstance(tag, abjad.Tag):
        raise Exception(f"must be be tag: {repr(tag)}")

    constants = (enums.Down, enums.Left, enums.Right, enums.Up)
    prototype = (bool, int, float, str, tuple, abjad.Scheme)
    if expression is True or argument in constants or isinstance(argument, prototype):
        manager = abjad.LilyPondTweakManager(
            deactivate=deactivate, literal=literal, tag=tag
        )
        manager._pending_value = argument
        return manager
    if not hasattr(argument, "_tweaks"):
        name = type(argument).__name__
        raise NotImplementedError(f"{name} does not allow tweaks (yet).")
    if argument._tweaks is None:
        manager = abjad.LilyPondTweakManager(
            deactivate=deactivate, literal=literal, tag=tag
        )
        argument._tweaks = manager
    else:
        manager = argument._tweaks
        manager.__init__(deactivate=deactivate, literal=literal, tag=tag)
    return manager
