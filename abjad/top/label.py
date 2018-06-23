def label(client=None, deactivate=None, tag=None):
    r"""
    Makes label agent or label expression.

    ..  container:: example

        Labels logical ties with start offsets:

        >>> staff = abjad.Staff(r"\times 2/3 { c'4 d'4 e'4 ~ } e'4 ef'4")
        >>> abjad.label(staff).with_start_offsets(direction=abjad.Up)
        Duration(1, 1)

        >>> abjad.override(staff).text_script.staff_padding = 4
        >>> abjad.override(staff).tuplet_bracket.staff_padding = 0
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                \override TextScript.staff-padding = #4
                \override TupletBracket.staff-padding = #0
            }
            {
                \times 2/3 {
                    c'4
                    ^ \markup { 0 }
                    d'4
                    ^ \markup { 1/6 }
                    e'4
                    ^ \markup { 1/3 }
                    ~
                }
                e'4
                ef'4
                ^ \markup { 3/4 }
            }

        See the ``Label`` API entry for many more examples.

    ..  container:: example expression

        Initializes positionally:

        >>> expression = abjad.label()
        >>> expression(staff)
        Label(client=<Staff{3}>)

        Initializes from keyword:

        >>> expression = abjad.label()
        >>> expression(client=staff)
        Label(client=<Staff{3}>)

        Makes label expression:

            >>> expression = abjad.label()
            >>> expression = expression.with_start_offsets()

        >>> staff = abjad.Staff(r"\times 2/3 { c'4 d'4 e'4 ~ } e'4 ef'4")
        >>> expression(staff)
        Duration(1, 1)

        >>> abjad.override(staff).text_script.staff_padding = 4
        >>> abjad.override(staff).tuplet_bracket.staff_padding = 0
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                \override TextScript.staff-padding = #4
                \override TupletBracket.staff-padding = #0
            }
            {
                \times 2/3 {
                    c'4
                    ^ \markup { 0 }
                    d'4
                    ^ \markup { 1/6 }
                    e'4
                    ^ \markup { 1/3 }
                    ~
                }
                e'4
                ef'4
                ^ \markup { 3/4 }
            }

        See the ``Label`` API entry for many more examples.

    Returns label agent when ``client`` is not none.

    Returns label expression when ``client`` is none.
    """
    import abjad
    if client is not None:
        return abjad.Label(
            client=client,
            deactivate=deactivate,
            tag=tag,
            )
    expression = abjad.Expression()
    expression = expression.label(tag=tag)
    return expression
