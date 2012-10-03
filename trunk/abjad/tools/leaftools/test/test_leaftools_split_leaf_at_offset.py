from abjad import *
import py


def test_leaftools_split_leaf_at_offset_01():
    '''Split note into assignable notes. 
    Don't fracture spanners. Don't tie split notes.
    '''

    staff = Staff("c'8 [ d'8 e'8 ]")

    r'''
    \new Staff {
        c'8 [
        d'8
        e'8 ]
    }
    '''

    halves = leaftools.split_leaf_at_offset(
        staff.leaves[1], (1, 32), fracture_spanners=False, tie_split_notes=False)

    r'''
    \new Staff {
        c'8 [
        d'32
        d'16.
        e'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.lilypond_format == "\\new Staff {\n\tc'8 [\n\td'32\n\td'16.\n\te'8 ]\n}"


def test_leaftools_split_leaf_at_offset_02():
    '''Split note into assignable notes. 
    Fracture spanners. But don't tie split notes.
    '''

    staff = Staff("c'8 [ d'8 e'8 ]")

    r'''
    \new Staff {
        c'8 [
        d'8
        e'8 ]
    }
    '''

    halves = leaftools.split_leaf_at_offset(
        staff.leaves[1], (1, 32), fracture_spanners=True, tie_split_notes=False)

    r'''
    \new Staff {
        c'8 [
        d'32 ]
        d'16. [
        e'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.lilypond_format == "\\new Staff {\n\tc'8 [\n\td'32 ]\n\td'16. [\n\te'8 ]\n}"


def test_leaftools_split_leaf_at_offset_03():
    '''Split note into assignable notes. 
    Don't fracture spanners. But do tie split notes.
    '''

    staff = Staff("c'8 [ d'8 e'8 ]")

    r'''
    \new Staff {
        c'8 [
        d'8
        e'8 ]
    }
    '''

    halves = leaftools.split_leaf_at_offset(
        staff.leaves[1], (1, 32), fracture_spanners=False, tie_split_notes=True)

    r'''
    \new Staff {
        c'8 [
        d'32 ~
        d'16.
        e'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.lilypond_format == "\\new Staff {\n\tc'8 [\n\td'32 ~\n\td'16.\n\te'8 ]\n}"


def test_leaftools_split_leaf_at_offset_04():
    '''Split note into assignable notes. 
    Fracture spanners and tie split notes.
    '''

    staff = Staff("c'8 [ d'8 e'8 ]")

    r'''
    \new Staff {
        c'8 [
        d'8
        e'8 ]
    }
    '''

    halves = leaftools.split_leaf_at_offset(
        staff.leaves[1], (1, 32), fracture_spanners=True, tie_split_notes=True)

    r'''
    \new Staff {
        c'8 [
        d'32 ] ~
        d'16. [
        e'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.lilypond_format == "\\new Staff {\n\tc'8 [\n\td'32 ] ~\n\td'16. [\n\te'8 ]\n}"


def test_leaftools_split_leaf_at_offset_05():
    '''Split note into tuplet monads.
    Don't fracture spanners. Don't tie split notes.
    '''

    staff = Staff("c'8 [ d'8 e'8 ]")

    r'''
    \new Staff {
        c'8 [
        d'8
        e'8 ]
    }
    '''

    halves = leaftools.split_leaf_at_offset(
        staff.leaves[1], (1, 24), tie_split_notes=False)

    r'''
    \new Staff {
        c'8 [
        \times 2/3 {
            d'16
        }
        \times 2/3 {
            d'8
        }
        e'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.lilypond_format == "\\new Staff {\n\tc'8 [\n\t\\times 2/3 {\n\t\td'16\n\t}\n\t\\times 2/3 {\n\t\td'8\n\t}\n\te'8 ]\n}"


def test_leaftools_split_leaf_at_offset_06():
    '''Notehead-assignable duration produces two notes.
    This test comes from a container-crossing spanner bug.
    '''

    t = Voice(notetools.make_repeated_notes(1) + [tuplettools.FixedDurationTuplet(Duration(2, 8), notetools.make_repeated_notes(3))])
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    beamtools.BeamSpanner(t.leaves)

    r'''
    \new Voice {
        c'8 [
        \times 2/3 {
            d'8
            e'8
            f'8 ]
        }
    }
    '''

    halves = leaftools.split_leaf_at_offset(t.leaves[1], Duration(1, 24), tie_split_notes=False)

    r'''
    \new Voice {
        c'8 [
        \times 2/3 {
            d'16
            d'16
            e'8
            f'8 ]
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Voice {\n\tc'8 [\n\t\\times 2/3 {\n\t\td'16\n\t\td'16\n\t\te'8\n\t\tf'8 ]\n\t}\n}"


def test_leaftools_split_leaf_at_offset_07():
    '''Split duration equal to zero produces no change.
    '''

    t = Note("c'4")

    halves = leaftools.split_leaf_at_offset(t, Duration(0))
    left, right = halves

    assert len(halves) == 2
    assert len(left) == 0
    assert len(right) == 1
    assert isinstance(right[0], Note)
    assert right[0].written_duration == Duration(1, 4)


def test_leaftools_split_leaf_at_offset_08():
    '''Leaf duration less than split duration produces no change.
    '''

    t = Note("c'4")

    halves = leaftools.split_leaf_at_offset(t, Duration(3, 4))
    left, right = halves

    assert len(halves) == 2
    assert len(left) == 1
    assert isinstance(left[0], Note)
    assert left[0].written_duration == Duration(1, 4)
    assert len(right) == 0


def test_leaftools_split_leaf_at_offset_09():
    '''Split returns two lists of zero or more leaves.
    '''

    t = Note("c'4")
    halves = leaftools.split_leaf_at_offset(t, (1, 8), tie_split_notes=False)

    assert isinstance(halves, tuple)
    assert len(halves) == 2
    assert len(halves[0]) == 1
    assert len(halves[1]) == 1
    assert halves[0][0] is t
    assert halves[1][0] is not t
    assert isinstance(halves[0][0], Note)
    assert isinstance(halves[1][0], Note)
    assert halves[0][0].written_duration == Duration(1, 8)
    assert halves[1][0].written_duration == Duration(1, 8)
    assert not tietools.is_component_with_tie_spanner_attached(halves[0][0])
    assert not tietools.is_component_with_tie_spanner_attached(halves[1][0])


def test_leaftools_split_leaf_at_offset_10():
    '''Split returns two lists of zero or more.
    '''

    t = Note("c'4")
    halves = leaftools.split_leaf_at_offset(t, Duration(1, 16))

    assert isinstance(halves, tuple)
    assert len(halves) == 2
    assert len(halves[0]) == 1
    assert len(halves[1]) == 1
    assert isinstance(halves[0][0], Note)
    assert isinstance(halves[1][0], Note)
    assert halves[0][0].written_duration == Duration(1, 16)
    assert halves[1][0].written_duration == Duration(3, 16)


def test_leaftools_split_leaf_at_offset_11():
    '''Nonassignable binary split duration produces two lists.
    Left list contains two notes tied together.
    Right list contains only one note.
    '''

    t = Note("c'4")
    halves = leaftools.split_leaf_at_offset(t, (5, 32), tie_split_notes=False)

    assert isinstance(halves, tuple)
    assert len(halves) == 2
    assert len(halves[0]) == 2
    assert len(halves[1]) == 1
    assert isinstance(halves[0][0], Note)
    assert isinstance(halves[0][1], Note)
    assert isinstance(halves[1][0], Note)
    assert halves[0][0].written_duration == Duration(4, 32)
    assert halves[0][1].written_duration == Duration(1, 32)
    assert halves[1][0].written_duration == Duration(3, 32)
    assert tietools.is_component_with_tie_spanner_attached(halves[0][0])
    assert tietools.is_component_with_tie_spanner_attached(halves[0][1])
    assert spannertools.get_the_only_spanner_attached_to_component(
        halves[0][0], tietools.TieSpanner) is \
        spannertools.get_the_only_spanner_attached_to_component(
        halves[0][1], tietools.TieSpanner)
    assert not tietools.is_component_with_tie_spanner_attached(halves[1][0])


def test_leaftools_split_leaf_at_offset_12():
    '''Lone spanned Leaf results in two spanned leaves.
    '''

    t = Staff([Note("c'4")])
    s = tietools.TieSpanner(t.leaves)
    halves = leaftools.split_leaf_at_offset(t[0], Duration(1, 8))

    assert len(t) == 2
    for leaf in t.leaves:
        assert leaf.spanners == set([s])
        assert spannertools.get_the_only_spanner_attached_to_component(
            leaf, tietools.TieSpanner) is s
    assert componenttools.is_well_formed_component(t)


def test_leaftools_split_leaf_at_offset_13():
    '''Spanners are unaffected by leaf split.
    '''

    t = Staff(notetools.make_repeated_notes(4))
    b = beamtools.BeamSpanner(t.leaves)

    halves = leaftools.split_leaf_at_offset(t[0], (1, 16), tie_split_notes=False)

    assert len(t) == 5
    for l in t.leaves:
        assert l.spanners == set([b])
        assert beamtools.get_beam_spanner_attached_to_component(l) is b
    assert componenttools.is_well_formed_component(t)


def test_leaftools_split_leaf_at_offset_14():
    '''Split returns three leaves, two are tied.
    Spanner is shared by all 3 leaves.
    '''

    t = Staff([Note("c'4")])
    s = tietools.TieSpanner(t.leaves)
    halves = leaftools.split_leaf_at_offset(t[0], Duration(5, 32))

    assert len(halves) == 2
    assert len(halves[0]) == 2
    assert len(halves[1]) == 1
    for l in t.leaves:
        assert l.spanners == set([s])
        assert spannertools.get_the_only_spanner_attached_to_component(
            l, tietools.TieSpanner) is s
    assert componenttools.is_well_formed_component(t)


def test_leaftools_split_leaf_at_offset_15():
    '''Split leaf is not tied again when a container containing it is already tie-spanned.
    '''

    t = Staff(notetools.make_repeated_notes(4))
    s = tietools.TieSpanner(t)
    halves = leaftools.split_leaf_at_offset(t[0], Duration(5, 64))

    assert spannertools.get_the_only_spanner_attached_to_component(t, tietools.TieSpanner) is s
    assert s.components == (t, )
    for l in t.leaves:
        assert not l.spanners
    assert componenttools.is_well_formed_component(t)


def test_leaftools_split_leaf_at_offset_16():
    '''Split leaf is not tied again when a container containing it is already tie-spanned.
    '''

    t = Staff(Container(notetools.make_repeated_notes(4)) * 2)
    s = tietools.TieSpanner(t[:])
    halves = leaftools.split_leaf_at_offset(t[0][0], Duration(5, 64))

    assert s.components == tuple(t[:])
    for v in t:
        assert v.spanners == set([s])
        for l in v.leaves:
            assert not l.spanners
            assert l._parent is v
    assert componenttools.is_well_formed_component(t)


def test_leaftools_split_leaf_at_offset_17():
    '''After grace notes are removed from first leaf in bipartition.
    '''

    t = Note("c'4")
    gracetools.GraceContainer([Note(0, (1, 32))], kind = 'after')(t)
    halves = leaftools.split_leaf_at_offset(t, Duration(1, 8))

    assert not hasattr(halves[0][0], 'after_grace')
    assert len(halves[1][0].after_grace) == 1


def test_leaftools_split_leaf_at_offset_18():
    '''After grace notes are removed from first tied leaves in bipartition.
    '''

    t = Note("c'4")
    gracetools.GraceContainer([Note(0, (1, 32))], kind = 'after')(t)
    halves = leaftools.split_leaf_at_offset(t, Duration(5, 32))

    assert len(halves) == 2
    assert not hasattr(halves[0][0], 'after_grace')
    assert not hasattr(halves[0][1], 'after_grace')
    assert len(halves[1]) == 1
    assert len(halves[1][0].after_grace) == 1


def test_leaftools_split_leaf_at_offset_19():
    '''Grace notes are removed from second leaf in bipartition.
    '''

    t = Note("c'4")
    gracetools.GraceContainer([Note(0, (1, 32))])(t)
    halves = leaftools.split_leaf_at_offset(t, Duration(1, 16))

    assert len(halves[0]) == 1
    assert len(halves[1]) == 1
    assert len(halves[0][0].grace) == 1
    assert not hasattr(halves[1][0], 'grace')
