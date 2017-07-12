# -*- coding: utf-8 -*-
import abjad
import pytest


def test_scoretools_Container_insert_01():
    r'''Insert component into container at index i.
    Fracture spanners to the left of index i.
    Fracture spanners to the right of index i.
    Returns Python list of fractured spanners.
    '''

    "Insert works just before a spanner."

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    beam = abjad.Beam()
    abjad.attach(beam, voice[:])
    voice.insert(0, abjad.Rest((1, 8)))

    r'''
    \new Voice {
        r8
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    assert abjad.inspect(voice).is_well_formed()
    assert format(voice) == abjad.String.normalize(
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


def test_scoretools_Container_insert_02():
    r'''Insert works inside a spanner.
    '''

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    beam = abjad.Beam()
    abjad.attach(beam, voice[:])
    voice.insert(1, abjad.Note(1, (1, 8)))

    r'''
    \new Voice {
        c'8 [
        cs'8
        d'8
        e'8
        f'8 ]
    }
    '''

    assert abjad.inspect(voice).is_well_formed()
    assert format(voice) == abjad.String.normalize(
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



def test_scoretools_Container_insert_03():
    r'''Insert works just after a spanner.
    '''

    staff = abjad.Staff([abjad.Note(n, (1, 8)) for n in range(4)])
    beam = abjad.Beam()
    abjad.attach(beam, staff[:])
    staff.insert(4, abjad.Rest((1, 4)))

    r'''
    \new Staff {
        c'8 [
        cs'8
        d'8
        ef'8 ]
        r4
    }
    '''

    assert abjad.inspect(staff).is_well_formed()
    assert format(staff) == abjad.String.normalize(
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


def test_scoretools_Container_insert_04():
    r'''Insert works with really big positive values.
    '''

    staff = abjad.Staff([abjad.Note(n, (1, 8)) for n in range(4)])
    beam = abjad.Beam()
    abjad.attach(beam, staff[:])
    staff.insert(1000, abjad.Rest((1, 4)))

    r'''
    \new Staff {
        c'8 [
        cs'8
        d'8
        ef'8 ]
    r4
    }
    '''

    assert abjad.inspect(staff).is_well_formed()
    assert format(staff) == abjad.String.normalize(
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


def test_scoretools_Container_insert_05():
    r'''Insert works with negative values.
    '''

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    beam = abjad.Beam()
    abjad.attach(beam, voice[:])
    voice.insert(-1, abjad.Note(4.5, (1, 8)))

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8
        eqs'8
        f'8 ]
    }
    '''

    assert abjad.inspect(voice).is_well_formed()
    assert format(voice) == abjad.String.normalize(
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


def test_scoretools_Container_insert_06():
    r'''Insert works with really big negative values.
    '''

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    beam = abjad.Beam()
    abjad.attach(beam, voice[:])
    voice.insert(-1000, abjad.Rest((1, 8)))

    r'''
    \new Voice {
        r8
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    assert abjad.inspect(voice).is_well_formed()
    assert format(voice) == abjad.String.normalize(
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


def test_scoretools_Container_insert_07():
    r'''Inserting a note from one container into another container
    changes note parent from first container to second.
    '''

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    staff = abjad.Staff("c'8 c'8 c'8 c'8 c'8 c'8 c'8 c'8")
    note = voice[0]
    staff.insert(1, voice[0])

    assert abjad.inspect(voice).is_well_formed()
    assert abjad.inspect(staff).is_well_formed()
    assert not note in voice
    assert note._parent is staff


def test_scoretools_Container_insert_08():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    beam = abjad.Beam()
    abjad.attach(beam, staff[:])
    staff.insert(1, abjad.Note("cs'8"), fracture_spanners=False)

    r'''
    \new Staff {
        c'8 [
        cs'8
        d'8
        e'8
        f'8 ]
    }
    '''

    assert abjad.inspect(staff).is_well_formed()
    assert format(staff) == abjad.String.normalize(
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


def test_scoretools_Container_insert_09():
    r'''Insert component into container at index i.
    Fracture spanners to the left of index i.
    Fracture spanners to the right of index i.
    Returns Python list of fractured spanners.
    '''

    "Insert works just before a spanner."

    staff = abjad.Staff([abjad.Note(n, (1, 8)) for n in range(4)])
    beam = abjad.Beam()
    abjad.attach(beam, staff[:])
    staff.insert(0, abjad.Rest('r4'), fracture_spanners=True)

    r'''
    \new Staff {
        r4
        c'8 [
        cs'8
        d'8
        ef'8 ]
    }
    '''

    assert abjad.inspect(staff).is_well_formed()
    assert format(staff) == abjad.String.normalize(
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


def test_scoretools_Container_insert_10():
    r'''Insert works inside a spanner.
    '''

    staff = abjad.Staff([abjad.Note(n, (1, 8)) for n in range(4)])
    beam = abjad.Beam()
    abjad.attach(beam, staff[:])
    staff.insert(1, abjad.Rest('r4'), fracture_spanners=True)

    r'''
    \new Staff {
        c'8 [ ]
        r4
        cs'8 [
        d'8
        ef'8 ]
    }
    '''

    assert abjad.inspect(staff).is_well_formed()
    assert format(staff) == abjad.String.normalize(
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


def test_scoretools_Container_insert_11():
    r'''Insert works just after a spanner.
    '''

    staff = abjad.Staff([abjad.Note(n, (1, 8)) for n in range(4)])
    beam = abjad.Beam()
    abjad.attach(beam, staff[:])
    staff.insert(4, abjad.Rest('r4'), fracture_spanners=True)

    r'''
    \new Staff {
        c'8 [
        cs'8
        d'8
        ef'8 ]
        r4
    }
    '''

    assert abjad.inspect(staff).is_well_formed()
    assert format(staff) == abjad.String.normalize(
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


def test_scoretools_Container_insert_12():
    r'''Insert works with really big positive values.
    '''

    staff = abjad.Staff([abjad.Note(n, (1, 8)) for n in range(4)])
    beam = abjad.Beam()
    abjad.attach(beam, staff[:])
    staff.insert(1000, abjad.Rest('r4'), fracture_spanners=True)

    r'''
    \new Staff {
        c'8 [
        cs'8
        d'8
        ef'8 ]
    r4
    }
    '''

    assert abjad.inspect(staff).is_well_formed()
    assert format(staff) == abjad.String.normalize(
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


def test_scoretools_Container_insert_13():
    r'''Insert works with negative values.
    '''

    staff = abjad.Staff([abjad.Note(n, (1, 8)) for n in range(4)])
    beam = abjad.Beam()
    abjad.attach(beam, staff[:])
    staff.insert(-1, abjad.Rest('r4'), fracture_spanners=True)

    r'''
    \new Staff {
        c'8 [
        cs'8
        d'8 ]
        r4
        ef'8 [ ]
    }
    '''

    assert abjad.inspect(staff).is_well_formed()
    assert format(staff) == abjad.String.normalize(
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


def test_scoretools_Container_insert_14():
    r'''Insert works with really big negative values.
    '''

    staff = abjad.Staff([abjad.Note(n, (1, 8)) for n in range(4)])
    beam = abjad.Beam()
    abjad.attach(beam, staff[:])
    staff.insert(-1000, abjad.Rest('r4'), fracture_spanners=True)

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Container_insert_15():
    r'''Inserting a note from one container into another container
    changes note parent from first container to second.
    '''

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    staff = abjad.Staff("c'8 c'8 c'8 c'8 c'8 c'8 c'8 c'8")
    note = voice[0]
    staff.insert(1, voice[0], fracture_spanners=True)

    assert abjad.inspect(voice).is_well_formed()
    assert abjad.inspect(staff).is_well_formed()
    assert not note in voice
    assert note._parent is staff