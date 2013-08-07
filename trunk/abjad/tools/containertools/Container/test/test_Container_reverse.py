# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_Container_reverse_01():
    r'''Retrograde works on a depth-0 Container with no spanners and no parent.
    '''

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    leaves_rev = reversed(staff.select_leaves())
    staff.reverse()

    assert list(leaves_rev) == list(staff.select_leaves())
    assert select(staff).is_well_formed()


def test_Container_reverse_02():
    r'''Retrograde works on a depth-0 Container with one spanner 
    attached and no parent.
    '''

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    beam = spannertools.BeamSpanner(staff)
    leaves_rev = reversed(staff.select_leaves())
    staff.reverse()

    assert list(leaves_rev) == list(staff.select_leaves())
    assert beam.components == (staff, )
    assert select(staff).is_well_formed()


def test_Container_reverse_03():
    r'''Retrograde works on a depth-0 Container with one spanner attached
    to its leaves and with no parent.
    '''

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    beam = spannertools.BeamSpanner(staff.select_leaves())
    leaves_rev = reversed(staff.select_leaves())
    staff.reverse()

    assert list(leaves_rev) == list(staff.select_leaves())
    assert beam.components == tuple(staff.select_leaves())
    assert select(staff).is_well_formed()


def test_Container_reverse_04():
    r'''Retrograde works on a depth-0 Container with one spanner
    attached to itself and with a parent.
    '''

    staff = Staff([Measure((4, 4), "c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")] + notetools.make_repeated_notes(2))
    beam = spannertools.BeamSpanner(staff[0])
    leaves_rev = reversed(staff[0].select_leaves())
    staff[0].reverse()
    assert list(leaves_rev) == list(staff[0].select_leaves())
    assert beam.components == (staff[0], )
    assert select(staff).is_well_formed()


def test_Container_reverse_05():
    r'''Retrograde works on a depth-0 Container with one spanner
    attached to its leaves and with a parent.
    '''

    staff = Staff([Measure((4, 4), "c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")] + 
        notetools.make_repeated_notes(2))
    beam = spannertools.BeamSpanner(staff[0].select_leaves())
    leaves_rev = reversed(staff[0].select_leaves())
    staff[0].reverse()
    assert list(leaves_rev) == list(staff[0].select_leaves())
    assert beam.components == tuple(staff[0].select_leaves())
    assert select(staff).is_well_formed()


def test_Container_reverse_06():
    r'''Retrograde works on a depth-0 Container with one spanner 
    attached to its parent.
    '''

    notes = [Note("c'8"), Note("d'8")]
    staff = Staff([Measure((4, 4), "c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")] + notes)
    beam = spannertools.BeamSpanner(staff)
    leaves_rev = reversed(staff[0].select_leaves())
    staff[0].reverse()
    assert list(leaves_rev) == list(staff[0].select_leaves())
    assert beam.components == tuple([staff])
    assert select(staff).is_well_formed()


def test_Container_reverse_07():
    r'''Retrograde works on a depth-0 Container with one spanner
    attached to its parent's contents.
    '''

    notes = [Note("c'8"), Note("d'8")]
    measure = Measure((4, 4), "c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    staff = Staff([measure] + notes)
    beam = spannertools.BeamSpanner(staff[:])
    leaves_rev = reversed(staff[0].select_leaves())
    staff[0].reverse()
    assert list(leaves_rev) == list(staff[0].select_leaves())
    assert beam.components == tuple([measure] + notes)
    assert select(staff).is_well_formed()


# TODO: Add well-formedness check for measure contiguity
def test_Container_reverse_08():
    r'''Retrograde unable to apply because of measure contiguity.
    '''

    notes = [Note("c'8"), Note("d'8")]
    measure = Measure((4, 4), "c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    staff = Staff([measure] + notes)
    beam = spannertools.BeamSpanner(staff[:])

    r'''
    \new Staff {
            \time 1/1
            c'8 [
            d'8
            e'8
            f'8
            g'8
            a'8
            b'8
            c''8
        c'8
        d'8 ]
    }
    '''

    # TODO: Make MeasureContiguityError raise here #
    #assert py.test.raises(MeasureContiguityError, 'staff.reverse()')


def test_Container_reverse_09():
    r'''Retrograde works on a depth-2 Container with no parent 
    and with spanners at all levels.
    '''

    m1 = Measure((4, 8), "c'8 d'8 e'8 f'8")
    m2 = Measure((3, 8), "c'8 d'8 e'8")
    staff = Staff([m1, m2])
    pedal = spannertools.PianoPedalSpanner(staff)
    trill = spannertools.TrillSpanner(staff[:])
    beam1 = spannertools.BeamSpanner(staff[0])
    beam2 = spannertools.BeamSpanner(staff[1])
    gliss = spannertools.GlissandoSpanner(staff.select_leaves())
    staff.reverse()
    assert staff[0] is m2
    assert staff[1] is m1
    assert len(m2) == 3
    assert len(m1) == 4
    assert pedal.components == (staff, )
    assert trill.components == tuple(staff[:])
    assert beam1.components == (m1, )
    assert beam2.components == (m2, )
    assert gliss.components == tuple(staff.select_leaves())
    assert select(staff).is_well_formed()
