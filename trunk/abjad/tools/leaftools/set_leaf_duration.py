# -*- encoding: utf-8 -*-
import copy
from abjad.tools import componenttools
from abjad.tools import durationtools


def set_leaf_duration(leaf, new_duration):
    r'''Set `leaf` duration.

    ..  container:: example

        **Example 1.** Set `leaf` duration:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> spannertools.BeamSpanner(staff.select_leaves())
            BeamSpanner(c'8, d'8, e'8, f'8)
            >>> leaftools.set_leaf_duration(staff[1], Duration(3, 16))
            [Note("d'8.")]
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'8 [
                d'8.
                e'8
                f'8 ]
            }

    ..  container:: example

        **Example 2.** Set tied `leaf` duration:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> spannertools.BeamSpanner(staff.select_leaves())
            BeamSpanner(c'8, d'8, e'8, f'8)
            >>> leaftools.set_leaf_duration(staff[1], Duration(5, 32))
            Selection(Note("d'8"), Note("d'32"))
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'8 [
                d'8 ~
                d'32
                e'8
                f'8 ]
            }

    ..  container:: example

        **Example 3.** Set `leaf` duration without power-of-two denominator:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> spannertools.BeamSpanner(staff.select_leaves())
            BeamSpanner(c'8, d'8, e'8, f'8)
            >>> leaftools.set_leaf_duration(staff[1], Duration(1, 12))
            [Tuplet(2/3, [c'8])]
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'8 [
                \times 2/3 {
                    d'8
                }
                e'8
                f'8 ]
            }

    ..  container:: example

        **Example 4.** Set `leaf` duration without power-of-two denominator:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> spannertools.BeamSpanner(staff.select_leaves())
            BeamSpanner(c'8, d'8, e'8, f'8)
            >>> leaftools.set_leaf_duration(staff[1], Duration(5, 48))
            [Tuplet(2/3, [c'8, c'32])]
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'8 [
                \times 2/3 {
                    d'8 ~
                    d'32
                }
                e'8
                f'8 ]
            }

    ..  container:: example

        **Example 5.** Set `leaf` duration with LilyPond multiplier:

        ::

            >>> note = Note(0, (1, 8))
            >>> note.lilypond_duration_multiplier = Duration(1, 2)
            >>> leaftools.set_leaf_duration(note, Duration(5, 48))
            [Note("c'8 * 5/6")]
            >>> show(note) # doctest: +SKIP

        ..  doctest::

            >>> f(note)
            c'8 * 5/6

    Return list of `leaf` and leaves newly tied to `leaf`.
    '''

    return leaf._set_duration(new_duration)
