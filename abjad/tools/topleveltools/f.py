def f(argument, strict=False):
    r'''Formats `argument` and prints result.
    
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

    ..  container:: example

        Set `strict` to true to force only one item per line:

        >>> abjad.f(staff, strict=True)
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

    Returns none.
    '''
    import abjad
    if hasattr(argument, '_publish_storage_format'):
        string = format(argument, 'storage')
    elif strict is True:
        string = format(argument, 'lilypond:strict')
    elif strict is not False and isinstance(strict, int):
        string = format(argument, 'lilypond:strict')
        string = abjad.LilyPondFormatManager.align_tags(string, strict)
    else:
        string = format(argument, 'lilypond')
    if strict:
        if isinstance(strict, int):
            realign = strict
        else:
            realign = None
        string = abjad.LilyPondFormatManager.left_shift_tags(
            string,
            realign=realign,
            )
    print(string)
