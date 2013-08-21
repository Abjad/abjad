# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools.selectiontools import mutate


def copy_and_trim(
    component, start_offset=0, stop_offset=None):
    r'''Copies `component` and trims from `start_offset`
    to `stop_offset` (both relative to the start of `component`).

    ..  container:: example

        **Example 1.**

        ::

            >>> voice = Voice(r"c'8 d'8 \times 2/3 { e'8 f'8 g'8 }")
            >>> show(voice) # doctest: +SKIP

        ..  doctest::

            >>> f(voice)
            \new Voice {
                c'8
                d'8
                \times 2/3 {
                    e'8
                    f'8
                    g'8
                }
            }

        ::

            >>> new_voice = \
            ...     componenttools.copy_and_trim(
            ...     voice, Offset(0, 8), Offset(3, 8))
            >>> show(new_voice) # doctest: +SKIP

        ..  doctest::

            >>> f(new_voice)
            \new Voice {
                c'8
                d'8
                \times 2/3 {
                    e'8
                    f'16
                }
            }

    ..  container:: example

        **Example 2.** Creates ad hoc tuplets as required:

        ::

            >>> voice = Voice([Note("c'4")])
            >>> show(voice) # doctest: +SKIP

        ..  doctest::

            >>> f(voice)
            \new Voice {
                c'4
            }

        ::

            >>> new_voice = \
            ...     componenttools.copy_and_trim(
            ...     voice, Offset(0), Offset(1, 12))
            >>> show(new_voice) # doctest: +SKIP

        ..  doctest::

            >>> f(new_voice)
            \new Voice {
                \times 2/3 {
                    c'8
                }
            }

    ..  container:: example

        **Example 3.** Slices tuplets as required:

        ::

            >>> voice = Voice(r"\times 2/3 { c'4 ( d'4 e'4 ) }")
            >>> show(voice) # doctest: +SKIP

        ..  doctest::

            >>> f(voice)
            \new Voice {
                \times 2/3 {
                    c'4 (
                    d'4
                    e'4 )
                }
            }

        ::

            >>> new_voice = \
            ...     componenttools.copy_and_trim(
            ...     voice[0], Offset(0), Offset(1, 8))
            >>> show(new_voice) # doctest: +SKIP

        ..  doctest::

            >>> f(new_voice)
            \times 2/3 {
                c'8. ( )
            }

    ..  container:: example

        **Example 4.** Does not copy parentage of `component` 
        when `component` is a leaf:

        ::

            >>> voice = Voice(r"\times 2/3 { c'4 ( d'4 e'4 ) }")
            >>> show(voice) # doctest: +SKIP

        ..  doctest::

            >>> f(voice)
            \new Voice {
                \times 2/3 {
                    c'4 (
                    d'4
                    e'4 )
                }
            }

        ::

            >>> new_leaf = \
            ... componenttools.copy_and_trim(
            ...     voice[0][0], Offset(0), Offset(1, 8))
            >>> new_leaf
            Note("c'8")
            >>> show(new_leaf) # doctest: +SKIP

        ..  doctest::

            >>> f(new_leaf)
            c'8 ( )

    Returns new component.
    '''
    from abjad.tools import componenttools
    from abjad.tools.selectiontools import mutate

    part_to_keep = mutate(component).copy()
    start_offset = durationtools.Duration(start_offset)
    stop_offset = durationtools.Duration(stop_offset)

    if stop_offset and 0 < stop_offset < part_to_keep._get_duration():
        left_half, right_half = componenttools.split(
            [part_to_keep],
            [stop_offset],
            fracture_spanners=True,
            tie_split_notes=False,
            )
        part_to_keep = left_half[0]

    if start_offset and 0 < start_offset < part_to_keep._get_duration():
        left_half, right_half = componenttools.split(
            [part_to_keep],
            [start_offset],
            fracture_spanners=True,
            tie_split_notes=False,
            )
        part_to_keep = right_half[0]

    return part_to_keep
