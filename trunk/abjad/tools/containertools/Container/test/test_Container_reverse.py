# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_Container_reverse_01():
    r'''Retrograde works on a depth-0 container with no spanners and no parent.
    '''

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    leaves_rev = reversed(staff.select_leaves())
    staff.reverse()

    assert list(leaves_rev) == list(staff.select_leaves())
    assert select(staff).is_well_formed()


def test_Container_reverse_02():
    r'''Retrograde works on a depth-0 container with one spanner 
    attached and no parent.
    '''

    container = Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    beam = spannertools.BeamSpanner(container)
    leaves_rev = reversed(container.select_leaves())
    container.reverse()

    assert list(leaves_rev) == list(container.select_leaves())
    assert beam.components == (container, )
    assert select(container).is_well_formed()


def test_Container_reverse_03():
    r'''Retrograde works on a depth-0 container with one spanner attached
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
    r'''Retrograde works on a depth-0 container with one spanner
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
    r'''Retrograde works on a depth-0 container with one spanner
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
    r'''Retrograde works on a depth-0 container with one spanner 
    attached to its parent.
    '''

    notes = [Note("c'8"), Note("d'8")]
    container = Container(
        [Measure((4, 4), "c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")] + notes)
    beam = spannertools.BeamSpanner(container)
    leaves_rev = reversed(container[0].select_leaves())
    container[0].reverse()
    assert list(leaves_rev) == list(container[0].select_leaves())
    assert beam.components == tuple([container])
    assert select(container).is_well_formed()


def test_Container_reverse_07():
    r'''Retrograde works on a depth-0 container with one spanner
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
    r'''Retrograde works on a depth-2 container with no parent 
    and with spanners at all levels.
    '''

    m1 = Measure((4, 8), "c'8 d'8 e'8 f'8")
    m2 = Measure((3, 8), "c'8 d'8 e'8")
    container = Container([m1, m2])
    pedal = spannertools.PianoPedalSpanner(container)
    trill = spannertools.TrillSpanner(container[:])
    beam1 = spannertools.BeamSpanner(container[0])
    beam2 = spannertools.BeamSpanner(container[1])
    gliss = spannertools.GlissandoSpanner(container.select_leaves())

    assert testtools.compare(
        container,
        r'''
        {
            {
                \time 4/8
                \set Staff.pedalSustainStyle = #'mixed
                c'8 [ \glissando \sustainOn \startTrillSpan
                d'8 \glissando
                e'8 \glissando
                f'8 ] \glissando
            }
            {
                \time 3/8
                c'8 [ \glissando
                d'8 \glissando
                e'8 ] \sustainOff \stopTrillSpan
            }
        }
        '''
        )

    container.reverse()

    assert testtools.compare(
        container,
        r'''
        {
            {
                \time 3/8
                \set Staff.pedalSustainStyle = #'mixed
                c'8 [ \glissando \sustainOn \startTrillSpan
                d'8 \glissando
                e'8 ] \glissando
            }
            {
                \time 4/8
                c'8 [ \glissando
                d'8 \glissando
                e'8 \glissando
                f'8 ] \sustainOff \stopTrillSpan
            }
        }
        '''
        )

    assert container[0] is m2
    assert container[1] is m1
    assert len(m2) == 3
    assert len(m1) == 4
    assert pedal.components == (container, )
    assert trill.components == tuple(container[:])
    assert beam1.components == (m1, )
    assert beam2.components == (m2, )
    assert gliss.components == tuple(container.select_leaves())
    assert select(container).is_well_formed()
