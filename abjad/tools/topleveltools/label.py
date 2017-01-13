# -*- coding: utf-8 -*-


def label(client=None):
    r'''Makes label agent or label expression.

    ..  container:: example

        Labels logical ties with start offsets:

        ::

            >>> staff = Staff(r"\times 2/3 { c'4 d'4 e'4 ~ } e'4 ef'4")
            >>> label(staff).with_start_offsets(direction=Up)
            >>> override(staff).text_script.staff_padding = 4
            >>> override(staff).tuplet_bracket.staff_padding = 0
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff \with {
                \override TextScript.staff-padding = #4
                \override TupletBracket.staff-padding = #0
            } {
                \times 2/3 {
                    c'4 ^ \markup { 0 }
                    d'4 ^ \markup { 1/6 }
                    e'4 ~ ^ \markup { 1/3 }
                }
                e'4
                ef'4 ^ \markup { 3/4 }
            }

        See the ``LabelAgent`` API entry for many more examples.

    ..  container:: example expression

        Initializes positionally:

        ::

            >>> expression = label()
            >>> expression(staff)
            LabelAgent(client=<Staff{3}>)

        Initializes from keyword:

        ::

            >>> expression = label()
            >>> expression(client=staff)
            LabelAgent(client=<Staff{3}>)

        Makes label expression:

            >>> expression = label()
            >>> expression = expression.with_start_offsets()

        ::

            >>> staff = Staff(r"\times 2/3 { c'4 d'4 e'4 ~ } e'4 ef'4")
            >>> expression(staff)
            >>> override(staff).text_script.staff_padding = 4
            >>> override(staff).tuplet_bracket.staff_padding = 0
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff \with {
                \override TextScript.staff-padding = #4
                \override TupletBracket.staff-padding = #0
            } {
                \times 2/3 {
                    c'4 ^ \markup { 0 }
                    d'4 ^ \markup { 1/6 }
                    e'4 ~ ^ \markup { 1/3 }
                }
                e'4
                ef'4 ^ \markup { 3/4 }
            }

        See the ``LabelAgent`` API entry for many more examples.

    Returns label agent when `client` is not none.

    Returns label expression when `client` is none.
    '''
    from abjad.tools import agenttools
    from abjad.tools import expressiontools
    if client is not None:
        return agenttools.LabelAgent(client=client)
    expression = expressiontools.Expression()
    expression = expression.label()
    return expression
