from abjad import *

def test_leaftools_fuse_tied_leaves_in_components_once_by_prolated_durations_without_overhang_01():
    '''Tied leaves inside containers can be fused.'''

    t = Voice(notetools.make_repeated_notes(4))
    tie = tietools.TieSpanner(t.leaves)
    leaftools.fuse_tied_leaves_in_components_once_by_prolated_durations_without_overhang(t.leaves, [Duration(1, 4)])

    r'''
    \new Voice {
        c'4 ~
        c'8 ~
        c'8
    }
    '''

    assert len(t) == 3
    assert t[0].prolated_duration == Duration(1, 4)
    assert t[1].prolated_duration == Duration(1, 8)
    assert t[2].prolated_duration == Duration(1, 8)
    assert t[0] in tie
    assert t[1] in tie
    assert t[2] in tie

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'4 ~\n\tc'8 ~\n\tc'8\n}"


def test_leaftools_fuse_tied_leaves_in_components_once_by_prolated_durations_without_overhang_02():
    '''Tied leaves inside containers can be fused.'''

    t = Voice(notetools.make_repeated_notes(4))
    tie = tietools.TieSpanner(t.leaves[1:])
    leaftools.fuse_tied_leaves_in_components_once_by_prolated_durations_without_overhang(t.leaves, [Duration(1, 4)])

    r'''
    \new Voice {
        c'8
        c'8 ~
        c'8 ~
        c'8
    }
    '''

    assert len(t) == 4
    assert t[0].prolated_duration == Duration(1, 8)
    assert t[1].prolated_duration == Duration(1, 8)
    assert t[2].prolated_duration == Duration(1, 8)
    assert t[3].prolated_duration == Duration(1, 8)
    assert t[0] not in tie
    assert t[1] in tie
    assert t[2] in tie
    assert t[3] in tie

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8\n\tc'8 ~\n\tc'8 ~\n\tc'8\n}"


def test_leaftools_fuse_tied_leaves_in_components_once_by_prolated_durations_without_overhang_03():
    '''multiple ties inside the same duration span are independently fused.'''

    t = Voice(notetools.make_repeated_notes(4))
    tie1 = tietools.TieSpanner(t.leaves[0:2])
    tie2 = tietools.TieSpanner(t.leaves[2:])
    leaftools.fuse_tied_leaves_in_components_once_by_prolated_durations_without_overhang(t.leaves, [Duration(1, 4)] * 2)

    r'''
    \new Voice {
        c'4
        c'4
    }
    '''

    assert len(t) == 2
    assert t[0].prolated_duration == Duration(1, 4)
    assert t[1].prolated_duration == Duration(1, 4)
    assert t[0] in tie1
    assert t[1] in tie2

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'4\n\tc'4\n}"


def test_leaftools_fuse_tied_leaves_in_components_once_by_prolated_durations_without_overhang_04():
    '''multiple ties inside the same duration span are independently fused.'''

    t = Voice(notetools.make_repeated_notes(8))
    tietools.TieSpanner(t.leaves[0:4])
    tietools.TieSpanner(t.leaves[4:])

    r'''
    \new Voice {
        c'8 ~
        c'8 ~
        c'8 ~
        c'8
        c'8 ~
        c'8 ~
        c'8 ~
        c'8
    }
    '''

    leaftools.fuse_tied_leaves_in_components_once_by_prolated_durations_without_overhang(t.leaves[1:-1], [Duration(1, 4)] * 3)

    r'''
    \new Voice {
        c'8 ~
        c'4 ~
        c'8
        c'8 ~
        c'4 ~
        c'8
    }
    '''

    assert t.format == "\\new Voice {\n\tc'8 ~\n\tc'4 ~\n\tc'8\n\tc'8 ~\n\tc'4 ~\n\tc'8\n}"


def test_leaftools_fuse_tied_leaves_in_components_once_by_prolated_durations_without_overhang_05():
    '''Steve Lehman's "Rai" slicing example.'''
    durations = [5, 7, 2, 11, 13, 5, 13, 3]
    durations = zip(durations, [16] * len(durations))

    notes = notetools.make_notes(0, durations)
    t = stafftools.make_rhythmic_sketch_staff(notes)

    meters = [(1, 4)] * 4 + [(2, 4)] + [(1, 4)] * 6 + [(2, 4)] + [(3, 16)]
    meters = [Duration(*meter) for meter in meters]

    componenttools.split_components_once_by_prolated_durations_and_do_not_fracture_crossing_spanners(t.leaves, meters, tie_after=True)

    r'''
    \new RhythmicStaff \with {
        \override BarLine #'transparent = ##t
        \override TimeSignature #'transparent = ##t
    } {
        c'4 ~
        c'16
        c'8. ~
        c'4
        c'8
        c'8 ~
        c'4. ~
        c'8 ~
        c'16
        c'8. ~
        c'4 ~
        c'4 ~
        c'16 ~
        c'16
        c'8 ~
        c'8 ~
        c'16
        c'16 ~
        c'4 ~
        c'4 ~
        c'8. ~
        c'16
        c'8.
    }
    '''

    leaftools.fuse_tied_leaves_in_components_once_by_prolated_durations_without_overhang(t.leaves, meters)

    componenttools.is_well_formed_component(t)
    assert t.format == "\\new RhythmicStaff \\with {\n\t\\override BarLine #'transparent = ##t\n\t\\override TimeSignature #'transparent = ##t\n} {\n\tc'4 ~\n\tc'16\n\tc'8. ~\n\tc'4\n\tc'8\n\tc'8 ~\n\tc'2 ~\n\tc'16\n\tc'8. ~\n\tc'4 ~\n\tc'4 ~\n\tc'8\n\tc'8 ~\n\tc'8.\n\tc'16 ~\n\tc'4 ~\n\tc'2\n\tc'8.\n}"


    r'''
        \new RhythmicStaff \with {
        \override BarLine #'transparent = ##t
        \override TimeSignature #'transparent = ##t
    } {
        c'4 ~
        c'16
        c'8. ~
        c'4
        c'8
        c'8 ~
        c'2 ~
        c'16
        c'8. ~
        c'4 ~
        c'4 ~
        c'8
        c'8 ~
        c'8.
        c'16 ~
        c'4 ~
        c'2
        c'8.
    }
    '''
