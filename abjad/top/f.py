def f(argument, strict=None):
    r"""
    Formats ``argument`` and prints result.
    
    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup = abjad.Markup('Allegro', direction=abjad.Up)
        >>> markup = markup.with_color('blue')
        >>> abjad.attach(markup, staff[0])
        >>> for leaf in staff:
        ...     abjad.attach(abjad.Articulation('.'), leaf)
        ...
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            -\staccato
            ^ \markup {
                \with-color
                    #blue
                    Allegro
                }
            d'4
            -\staccato
            e'4
            -\staccato
            f'4
            -\staccato
        }

        >>> abjad.show(staff) # doctest: +SKIP

    """
    import abjad
    if strict is not None:
        assert isinstance(strict, int), repr(strict)
    if hasattr(argument, '_publish_storage_format'):
        string = format(argument, 'storage')
    else:
        string = format(argument, 'lilypond')
    realign = None
    if isinstance(strict, int):
        string = abjad.LilyPondFormatManager.align_tags(string, strict)
        realign = strict
    string = abjad.LilyPondFormatManager.left_shift_tags(
        string,
        realign=realign,
        )
    print(string)
