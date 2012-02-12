from abjad.tools.leaftools._Leaf import _Leaf
from abjad.tools import componenttools
from abjad.tools import durationtools


def set_preprolated_leaf_duration(leaf, new_preprolated_duration):
    r'''.. versionadded:: 1.1

    Set preprolated `leaf` duration::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> spannertools.BeamSpanner(staff.leaves)
        BeamSpanner(c'8, d'8, e'8, f'8)
        abjad> leaftools.set_preprolated_leaf_duration(staff[1], Duration(3, 16))
        [Note("d'8.")]
        abjad> f(staff)
        \new Staff {
            c'8 [
            d'8.
            e'8
            f'8 ]
        }

    Set tied preprolated `leaf` duration::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> spannertools.BeamSpanner(staff.leaves)
        BeamSpanner(c'8, d'8, e'8, f'8)
        abjad> leaftools.set_preprolated_leaf_duration(staff[1], Duration(5, 32))
        [Note("d'8"), Note("d'32")]
        abjad> f(staff)
        \new Staff {
            c'8 [
            d'8 ~
            d'32
            e'8
            f'8 ]
        }

    Set nonbinary preprolated `leaf` duration::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> spannertools.BeamSpanner(staff.leaves)
        BeamSpanner(c'8, d'8, e'8, f'8)
        abjad> leaftools.set_preprolated_leaf_duration(staff[1], Duration(1, 12))
        [Note("d'8")]
        abjad> f(staff)
        \new Staff {
            c'8 [
            \times 2/3 {
                d'8
            }
            e'8
            f'8 ]
        }

    Set tied nonbinary preprolated `leaf` duration::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> spannertools.BeamSpanner(staff.leaves)
        BeamSpanner(c'8, d'8, e'8, f'8)
        abjad> leaftools.set_preprolated_leaf_duration(staff[1], Duration(5, 48))
        [Note("d'8"), Note("d'32")]
        abjad> f(staff)
        \new Staff {
            c'8 [
            \times 2/3 {
                d'8 ~
                d'32
            }
            e'8
            f'8 ]
        }

    Set preprolated `leaf` duration with LilyPond multiplier::

        abjad> note = Note(0, (1, 8))
        abjad> note.duration_multiplier = Duration(1, 2)
        abjad> leaftools.set_preprolated_leaf_duration(note, Duration(5, 48))
        [Note("c'8 * 5/6")]
        abjad> f(note)
        c'8 * 5/6

    Return list of `leaf` and leaves newly tied to `leaf`.

    .. versionchanged:: 2.0
        renamed ``leaftools.change_leaf_preprolated_duration()`` to
        ``leaftools.set_preprolated_leaf_duration()``.
    '''
    from abjad.tools import tietools
    from abjad.tools.notetools.make_notes import make_notes
    from abjad.tools import spannertools
    from abjad.tools.tuplettools.Tuplet import Tuplet

    assert isinstance(leaf, _Leaf)
    #assert isinstance(new_preprolated_duration, durationtools.Duration)
    new_preprolated_duration = durationtools.Duration(new_preprolated_duration)

    # If leaf carries LilyPond multiplier, change only LilyPond multiplier.
    if leaf.duration_multiplier is not None:
        leaf.duration_multiplier = new_preprolated_duration / leaf.written_duration
        return [leaf]

    # If leaf does not carry LilyPond multiplier, change other values.
    try:
        leaf.written_duration = new_preprolated_duration
        all_leaves = [leaf]
    except AssignabilityError:
        duration_tokens = make_notes(0, new_preprolated_duration)
        if isinstance(duration_tokens[0], _Leaf):
            num_tied_leaves = len(duration_tokens) - 1
            tied_leaves = componenttools.copy_components_and_remove_all_spanners(
                [leaf], num_tied_leaves)
            all_leaves = [leaf] + tied_leaves
            for x, token in zip(all_leaves, duration_tokens):
                x.written_duration = token.written_duration
            componenttools.extend_in_parent_of_component_and_grow_spanners(leaf, tied_leaves)
            if not spannertools.get_spanners_attached_to_any_improper_parent_of_component(
                leaf, tietools.TieSpanner):
                tietools.TieSpanner(all_leaves)
        elif isinstance(duration_tokens[0], Tuplet):
            #print 'debug duration_tokens %s' % duration_tokens
            fmtuplet = duration_tokens[0]
            duration_tokens = fmtuplet[:]
            num_tied_leaves = len(duration_tokens) - 1
            tied_leaves = componenttools.copy_components_and_remove_all_spanners(
                [leaf], num_tied_leaves)
            all_leaves = [leaf] + tied_leaves
            for x, token in zip(all_leaves, duration_tokens):
                x.written_duration = token.written_duration
            componenttools.extend_in_parent_of_component_and_grow_spanners(leaf, tied_leaves)
            if not spannertools.is_component_with_spanner_attached(leaf, tietools.TieSpanner):
                tietools.TieSpanner(all_leaves)
            tuplet_multiplier = fmtuplet.multiplier
            Tuplet(tuplet_multiplier, all_leaves)
        else:
            raise ValueError('unexpected output from notetools.make_notes.')

    return all_leaves
