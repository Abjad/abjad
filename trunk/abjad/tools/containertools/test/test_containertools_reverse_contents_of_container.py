from abjad import *
import py.test


def test_containertools_reverse_contents_of_container_01():
    r'''Retrograde works on a depth-0 Container with no spanners and no parent.
    '''

    t = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    leaves_rev = reversed(t.select_leaves())
    containertools.reverse_contents_of_container(t)

    assert list(leaves_rev) == list(t.select_leaves())
    assert select(t).is_well_formed()


def test_containertools_reverse_contents_of_container_02():
    r'''Retrograde works on a depth-0 Container with one spanner attached and no parent.
    '''

    t = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    beam = spannertools.BeamSpanner(t)
    leaves_rev = reversed(t.select_leaves())
    containertools.reverse_contents_of_container(t)

    assert list(leaves_rev) == list(t.select_leaves())
    assert beam.components == (t, )
    assert select(t).is_well_formed()


def test_containertools_reverse_contents_of_container_03():
    r'''Retrograde works on a depth-0 Container with one spanner attached
    to its leaves and with no parent.
    '''

    t = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    beam = spannertools.BeamSpanner(t.select_leaves())
    leaves_rev = reversed(t.select_leaves())
    containertools.reverse_contents_of_container(t)

    assert list(leaves_rev) == list(t.select_leaves())
    assert beam.components == tuple(t.select_leaves())
    assert select(t).is_well_formed()


def test_containertools_reverse_contents_of_container_04():
    r'''Retrograde works on a depth-0 Container with one spanner
    attached to itself and with a parent.
    '''

    t = Staff([Measure((4, 4), "c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")] + notetools.make_repeated_notes(2))
    beam = spannertools.BeamSpanner(t[0])
    leaves_rev = reversed(t[0].select_leaves())
    containertools.reverse_contents_of_container(t[0])
    assert list(leaves_rev) == list(t[0].select_leaves())
    assert beam.components == (t[0], )
    assert select(t).is_well_formed()


def test_containertools_reverse_contents_of_container_05():
    r'''Retrograde works on a depth-0 Container with one spanner
    attached to its leaves and with a parent.
    '''

    t = Staff([Measure((4, 4), "c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")] + notetools.make_repeated_notes(2))
    beam = spannertools.BeamSpanner(t[0].select_leaves())
    leaves_rev = reversed(t[0].select_leaves())
    containertools.reverse_contents_of_container(t[0])
    assert list(leaves_rev) == list(t[0].select_leaves())
    assert beam.components == tuple(t[0].select_leaves())
    assert select(t).is_well_formed()


def test_containertools_reverse_contents_of_container_06():
    r'''Retrograde works on a depth-0 Container with one spanner attached to its parent.
    '''

    notes = [Note("c'8"), Note("d'8")]
    t = Staff([Measure((4, 4), "c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")] + notes)
    beam = spannertools.BeamSpanner(t)
    leaves_rev = reversed(t[0].select_leaves())
    containertools.reverse_contents_of_container(t[0])
    assert list(leaves_rev) == list(t[0].select_leaves())
    assert beam.components == tuple([t])
    assert select(t).is_well_formed()


def test_containertools_reverse_contents_of_container_07():
    r'''Retrograde works on a depth-0 Container with one spanner
    attached to its parent's contents.
    '''

    notes = [Note("c'8"), Note("d'8")]
    measure = Measure((4, 4), "c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    t = Staff([measure] + notes)
    beam = spannertools.BeamSpanner(t[:])
    leaves_rev = reversed(t[0].select_leaves())
    containertools.reverse_contents_of_container(t[0])
    assert list(leaves_rev) == list(t[0].select_leaves())
    assert beam.components == tuple([measure] + notes)
    assert select(t).is_well_formed()


# TODO: Add well-formedness check for measure contiguity
def test_containertools_reverse_contents_of_container_08():
    r'''Retrograde unable to apply because of measure contiguity.
    '''

    notes = [Note("c'8"), Note("d'8")]
    measure = Measure((4, 4), "c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    t = Staff([measure] + notes)
    beam = spannertools.BeamSpanner(t[:])

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

#   assert py.test.raises(MeasureContiguityError,
#      'containertools.reverse_contents_of_container(t)')


def test_containertools_reverse_contents_of_container_09():
    r'''Retrograde works on a depth-2 Container with no parent and with spanners at all levels.
    '''

    m1 = Measure((4, 8), "c'8 d'8 e'8 f'8")
    m2 = Measure((3, 8), "c'8 d'8 e'8")
    staff = Staff([m1, m2])
    pedal = spannertools.PianoPedalSpanner(staff)
    trill = spannertools.TrillSpanner(staff[:])
    beam1 = spannertools.BeamSpanner(staff[0])
    beam2 = spannertools.BeamSpanner(staff[1])
    gliss = spannertools.GlissandoSpanner(staff.select_leaves())
    containertools.reverse_contents_of_container(staff)
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
