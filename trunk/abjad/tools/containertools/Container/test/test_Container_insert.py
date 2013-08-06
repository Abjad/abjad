# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_Container_insert_01():
    r'''Insert component into container at index i.
    Fracture spanners to the left of index i.
    Fracture spanners to the right of index i.
    Return Python list of fractured spanners.
    '''

    "Insert works just before a spanner."

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])
    t.insert(0, Rest((1, 8)))

    r'''
    \new Voice {
        r8
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Voice {
            r8
            c'8 [
            d'8
            e'8
            f'8 ]
        }
        '''
        )


def test_Container_insert_02():
    r'''Insert works inside a spanner.
    '''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])
    t.insert(1, Note(1, (1, 8)))

    r'''
    \new Voice {
        c'8 [
        cs'8
        d'8
        e'8
        f'8 ]
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Voice {
            c'8 [
            cs'8
            d'8
            e'8
            f'8 ]
        }
        '''
        )



def test_Container_insert_03():
    r'''Insert works just after a spanner.
    '''

    t = Staff([Note(n, (1, 8)) for n in range(4)])
    spannertools.BeamSpanner(t[:])
    t.insert(4, Rest((1, 4)))

    r'''
    \new Staff {
        c'8 [
        cs'8
        d'8
        ef'8 ]
        r4
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Staff {
            c'8 [
            cs'8
            d'8
            ef'8 ]
            r4
        }
        '''
        )


def test_Container_insert_04():
    r'''Insert works with really big positive values.
    '''

    t = Staff([Note(n, (1, 8)) for n in range(4)])
    spannertools.BeamSpanner(t[:])
    t.insert(1000, Rest((1, 4)))

    r'''
    \new Staff {
        c'8 [
        cs'8
        d'8
        ef'8 ]
    r4
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Staff {
            c'8 [
            cs'8
            d'8
            ef'8 ]
            r4
        }
        '''
        )


def test_Container_insert_05():
    r'''Insert works with negative values.
    '''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])
    t.insert(-1, Note(4.5, (1, 8)))

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8
        eqs'8
        f'8 ]
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Voice {
            c'8 [
            d'8
            e'8
            eqs'8
            f'8 ]
        }
        '''
        )


def test_Container_insert_06():
    r'''Insert works with really big negative values.
    '''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])
    t.insert(-1000, Rest((1, 8)))

    r'''
    \new Voice {
        r8
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Voice {
            r8
            c'8 [
            d'8
            e'8
            f'8 ]
        }
        '''
        )


def test_Container_insert_07():
    r'''Inserting a note from one container into another container
    changes note parent from first container to second.
    '''

    v = Voice("c'8 d'8 e'8 f'8")
    t = Staff(notetools.make_repeated_notes(8))
    note = v[0]
    t.insert(1, v[0])

    assert select(v).is_well_formed()
    assert select(t).is_well_formed()
    assert not note in v
    assert note._parent is t


def test_Container_insert_08():

    staff = Staff("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(staff.select_leaves())
    staff.insert(1, Note("cs'8"), fracture_spanners=False)

    r'''
    \new Staff {
        c'8 [
        cs'8
        d'8
        e'8
        f'8 ]
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            c'8 [
            cs'8
            d'8
            e'8
            f'8 ]
        }
        '''
        )


def test_Container_insert_09():
    r'''Insert component into container at index i.
    Fracture spanners to the left of index i.
    Fracture spanners to the right of index i.
    Return Python list of fractured spanners.
    '''

    "Insert works just before a spanner."

    t = Staff([Note(n, (1, 8)) for n in range(4)])
    spannertools.BeamSpanner(t[:])
    t.insert(0, Rest('r4'), fracture_spanners=True)

    r'''
    \new Staff {
        r4
        c'8 [
        cs'8
        d'8
        ef'8 ]
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Staff {
            r4
            c'8 [
            cs'8
            d'8
            ef'8 ]
        }
        '''
        )


def test_Container_insert_10():
    r'''Insert works inside a spanner.
    '''

    t = Staff([Note(n, (1, 8)) for n in range(4)])
    spannertools.BeamSpanner(t[:])
    t.insert(1, Rest('r4'), fracture_spanners=True)

    r'''
    \new Staff {
        c'8 [ ]
        r4
        cs'8 [
        d'8
        ef'8 ]
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Staff {
            c'8 [ ]
            r4
            cs'8 [
            d'8
            ef'8 ]
        }
        '''
        )


def test_Container_insert_11():
    r'''Insert works just after a spanner.
    '''

    t = Staff([Note(n, (1, 8)) for n in range(4)])
    spannertools.BeamSpanner(t[:])
    t.insert(4, Rest('r4'), fracture_spanners=True)

    r'''
    \new Staff {
        c'8 [
        cs'8
        d'8
        ef'8 ]
        r4
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Staff {
            c'8 [
            cs'8
            d'8
            ef'8 ]
            r4
        }
        '''
        )


def test_Container_insert_12():
    r'''Insert works with really big positive values.
    '''

    t = Staff([Note(n, (1, 8)) for n in range(4)])
    spannertools.BeamSpanner(t[:])
    t.insert(1000, Rest('r4'), fracture_spanners=True)

    r'''
    \new Staff {
        c'8 [
        cs'8
        d'8
        ef'8 ]
    r4
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Staff {
            c'8 [
            cs'8
            d'8
            ef'8 ]
            r4
        }
        '''
        )


def test_Container_insert_13():
    r'''Insert works with negative values.
    '''

    t = Staff([Note(n, (1, 8)) for n in range(4)])
    spannertools.BeamSpanner(t[:])
    t.insert(-1, Rest('r4'), fracture_spanners=True)

    r'''
    \new Staff {
        c'8 [
        cs'8
        d'8 ]
        r4
        ef'8 [ ]
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Staff {
            c'8 [
            cs'8
            d'8 ]
            r4
            ef'8 [ ]
        }
        '''
        )


def test_Container_insert_14():
    r'''Insert works with really big negative values.
    '''

    t = Staff([Note(n, (1, 8)) for n in range(4)])
    spannertools.BeamSpanner(t[:])
    t.insert(-1000, Rest('r4'), fracture_spanners=True)

    r'''
    \new Staff {
        r4
        c'8 [
        cs'8
        d'8
        ef'8 ]
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Staff {
            r4
            c'8 [
            cs'8
            d'8
            ef'8 ]
        }
        '''
        )


def test_Container_insert_15():
    r'''Inserting a note from one container into another container
    changes note parent from first container to second.
    '''

    v = Voice("c'8 d'8 e'8 f'8")
    t = Staff(notetools.make_repeated_notes(8))
    note = v[0]
    t.insert(1, v[0], fracture_spanners=True)

    assert select(v).is_well_formed()
    assert select(t).is_well_formed()
    assert not note in v
    assert note._parent is t
