from abjad.tools import iterationtools
from abjad.tools import tuplettools


def attach_multiplart_beam_spanner_to_bottommost_tuplets_in_expr(expr):
    r'''Apply multiplart beam spanner to bottommost tuplets in `expr`:

    ::

        >>> tuplet_1 = Tuplet((4, 3), "a''8 af'' c''")
        >>> tuplet_2 = Tuplet((4, 5), "g''16 gf'' f'' e''8")
        >>> tuplet_3 = Tuplet((4, 3), "ef''8 d'' gf'")
        >>> tuplet_4 = Tuplet((4, 5), "df''16 c'' b' bf'8")

    ::

        >>> inner_tuplets = [tuplet_1, tuplet_2, tuplet_3, tuplet_4]
        >>> outer_tuplet = Tuplet((5, 6), inner_tuplets)

    ::

        >>> slur_1 = spannertools.SlurSpanner(outer_tuplet[:2])
        >>> slur_2 = spannertools.SlurSpanner(outer_tuplet[2:])

    ::

        >>> measure = Measure((5, 4), [outer_tuplet])
        >>> measure.override.tuplet_bracket.direction = Down
        >>> measure.override.tuplet_bracket.staff_padding = 2
        >>> measure.set.auto_beaming = False

    ::

        >>> f(measure)
        {
            \override TupletBracket #'direction = #down
            \override TupletBracket #'staff-padding = #2
            \set autoBeaming = ##f
            \time 5/4
            \tweak #'text #tuplet-number::calc-fraction-text
            \times 5/6 {
                \tweak #'text #tuplet-number::calc-fraction-text
                \times 4/3 {
                    a''8 (
                    af''8
                    c''8
                }
                \times 4/5 {
                    g''16
                    gf''16
                    f''16
                    e''8 )
                }
                \tweak #'text #tuplet-number::calc-fraction-text
                \times 4/3 {
                    ef''8 (
                    d''8
                    gf'8
                }
                \times 4/5 {
                    df''16
                    c''16
                    b'16
                    bf'8 )
                }
            }
            \revert TupletBracket #'direction
            \revert TupletBracket #'staff-padding
        }

    ::

        >>> show(measure) # doctest: +SKIP

    ::

        >>> beamtools.attach_multiplart_beam_spanner_to_bottommost_tuplets_in_expr(
        ...     measure)

    ::

        >>> f(measure)
        {
            \override TupletBracket #'direction = #down
            \override TupletBracket #'staff-padding = #2
            \set autoBeaming = ##f
            \time 5/4
            \tweak #'text #tuplet-number::calc-fraction-text
            \times 5/6 {
                \tweak #'text #tuplet-number::calc-fraction-text
                \times 4/3 {
                    a''8 [ (
                    af''8
                    c''8 ]
                }
                \times 4/5 {
                    g''16 [
                    gf''16
                    f''16
                    e''8 ] )
                }
                \tweak #'text #tuplet-number::calc-fraction-text
                \times 4/3 {
                    ef''8 [ (
                    d''8
                    gf'8 ]
                }
                \times 4/5 {
                    df''16 [
                    c''16
                    b'16
                    bf'8 ] )
                }
            }
            \revert TupletBracket #'direction
            \revert TupletBracket #'staff-padding
        }

    ::

        >>> show(measure) # doctest: +SKIP

    Return none.
    '''
    from abjad.tools import beamtools

    for tuplet in iterationtools.iterate_tuplets_in_expr(expr):
        for component in tuplet:
            if isinstance(component, tuplettools.Tuplet):
                break
        else:
            beamtools.MultipartBeamSpanner(tuplet)
