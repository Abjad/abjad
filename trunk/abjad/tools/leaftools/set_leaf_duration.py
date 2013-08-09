# -*- encoding: utf-8 -*-
from abjad.tools import componenttools
from abjad.tools import durationtools


def set_leaf_duration(leaf, new_preprolated_duration):
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
            [Note("d'8"), Note("d'32")]
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
            ContiguousSelection(Note("d'8"),)
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
            [Note("d'8"), Note("d'32")]
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
    from abjad.tools import leaftools
    from abjad.tools import notetools
    from abjad.tools import spannertools
    from abjad.tools import tuplettools

    assert isinstance(leaf, leaftools.Leaf)
    new_preprolated_duration = durationtools.Duration(new_preprolated_duration)

    # if leaf carries LilyPond multiplier, change only LilyPond multiplier.
    if leaf.lilypond_duration_multiplier is not None:
        leaf.lilypond_duration_multiplier = new_preprolated_duration / leaf.written_duration
        return [leaf]

    # if leaf does not carry LilyPond multiplier, change other values.
    try:
        leaf.written_duration = new_preprolated_duration
        all_leaves = [leaf]
    except AssignabilityError:
        components = notetools.make_notes(0, new_preprolated_duration)
        if isinstance(components[0], leaftools.Leaf):
            num_tied_leaves = len(components) - 1
            tied_leaves = componenttools.copy_components_and_detach_spanners(
                [leaf], num_tied_leaves)
            all_leaves = [leaf] + tied_leaves
            for x, component in zip(all_leaves, components):
                x.written_duration = component.written_duration
            leaf._splice(tied_leaves, grow_spanners=True)
            if not spannertools.get_spanners_attached_to_any_improper_parent_of_component(
                leaf, spanner_classes=(spannertools.TieSpanner,)):
                spannertools.TieSpanner(all_leaves)
        elif isinstance(components[0], tuplettools.Tuplet):
            fmtuplet = components[0]
            components = fmtuplet[:]
            num_tied_leaves = len(components) - 1
            tied_leaves = componenttools.copy_components_and_detach_spanners(
                [leaf], num_tied_leaves)
            all_leaves = [leaf] + tied_leaves
            for x, component in zip(all_leaves, components):
                x.written_duration = component.written_duration
            leaf._splice(tied_leaves, grow_spanners=True)
            if not spannertools.is_component_with_spanner_attached(
                leaf, spannertools.TieSpanner):
                spannertools.TieSpanner(all_leaves)
            tuplet_multiplier = fmtuplet.multiplier
            tuplettools.Tuplet(tuplet_multiplier, all_leaves)
        else:
            raise ValueError('unexpected output from notetools.make_notes.')

    return all_leaves
