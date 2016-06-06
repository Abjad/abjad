# -*- coding: utf-8 -*-


def label(expr=None):
    r'''Labels `expr` or makes label expression.

    ..  container:: example

        **Example 1.** Labels logical ties with start offsets:

        ::

            >>> staff = Staff(r"\times 2/3 { c'4 d'4 e'4 ~ } e'4 ef'4")
            >>> label(staff).with_start_offsets(direction=Up)
            >>> override(staff).text_script.staff_padding = 4
            >>> override(staff).tuplet_bracket.staff_padding = 0
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
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

    ..  container:: example
        
        **Example 2.** Makes label expression:

            >>> expression = label()
            >>> expression = expression.with_start_offsets()

        ::

            >>> staff = Staff(r"\times 2/3 { c'4 d'4 e'4 ~ } e'4 ef'4")
            >>> expression(staff)
            >>> override(staff).text_script.staff_padding = 4
            >>> override(staff).tuplet_bracket.staff_padding = 0
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
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

        See the ``LabelExpression`` API entry for many more examples.

    Returns label agent when `expr` is not none.

    Returns label expression when `expr` is none.
    '''
    from abjad.tools import agenttools
    from abjad.tools import expressiontools
    if expr is None:
        return expressiontools.LabelExpression()
    else:
        return agenttools.LabelAgent(expr)
