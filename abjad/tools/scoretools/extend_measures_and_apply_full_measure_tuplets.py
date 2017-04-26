# -*- coding: utf-8 -*-


def extend_measures_and_apply_full_measure_tuplets(argument, supplement):
    r'''Extends measures in `argument` with `supplement` and applies
    full-measure tuplets to contents of measures.

    ..  container:: example

        ::

            >>> staff = Staff([Measure((2, 8), "c'8 d'8"), Measure((3, 8), "e'8 f'8 g'8")])

        ..  doctest::

            >>> f(staff)
            \new Staff {
                {
                    \time 2/8
                    c'8
                    d'8
                }
                {
                    \time 3/8
                    e'8
                    f'8
                    g'8
                }
            }

        ::

            >>> supplement = [Rest((1, 16))]
            >>> scoretools.extend_measures_and_apply_full_measure_tuplets(
            ...     staff,
            ...     supplement,
            ...     )

        ..  doctest::

            >>> f(staff)
            \new Staff {
                {
                    \time 2/8
                    \times 4/5 {
                        c'8
                        d'8
                        r16
                    }
                }
                {
                    \time 3/8
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/7 {
                        e'8
                        f'8
                        g'8
                        r16
                    }
                }
            }

    Returns none.
    '''
    from abjad.tools import scoretools

    return scoretools.apply_full_measure_tuplets_to_contents_of_measures(
        argument, supplement)
