# -*- encoding: utf-8 -*-
from abjad import *


def test_componenttools_move_parentage_and_spanners_from_components_to_components_01():
    r'''Move parentage and spanners from two old notes to five new notes.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    b1 = spannertools.BeamSpanner(staff[:2])
    b2 = spannertools.BeamSpanner(staff[2:])
    crescendo = spannertools.CrescendoSpanner(staff[:])

    r'''
    \new Staff {
        c'8 [ \<
        d'8 ]
        e'8 [
        f'8 ] \!
    }
    '''

    old_notes = staff[1:3]
    new_notes = Note(12, (1, 16)) * 5
    componenttools.move_parentage_and_spanners_from_components_to_components(old_notes, new_notes)

    "Equivalent to staff[1:3] = new_notes"

    r'''
    \new Staff {
        c'8 [ ] \<
        c''16
        c''16
        c''16
        c''16
        c''16
        f'8 [ ] \!
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            c'8 [ ] \<
            c''16
            c''16
            c''16
            c''16
            c''16
            f'8 [ ] \!
        }
        '''
        )


def test_componenttools_move_parentage_and_spanners_from_components_to_components_02():
    r'''Move parentage and spanners from one old note to five new notes.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    b1 = spannertools.BeamSpanner(staff[:2])
    b2 = spannertools.BeamSpanner(staff[2:])
    crescendo = spannertools.CrescendoSpanner(staff[:])

    r'''
    \new Staff {
        c'8 [ \<
        d'8 ]
        e'8 [
        f'8 ] \!
    }
    '''

    new_notes = Note(12, (1, 16)) * 5
    componenttools.move_parentage_and_spanners_from_components_to_components(staff[:1], new_notes)
    #staff[:1] = new_notes

    "Equivalent to staff[:1] = new_notes."

    r'''
    \new Staff {
        c''16 [ \<
        c''16
        c''16
        c''16
        c''16
        d'8 ]
        e'8 [
        f'8 ] \!
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            c''16 [ \<
            c''16
            c''16
            c''16
            c''16
            d'8 ]
            e'8 [
            f'8 ] \!
        }
        '''
        )


def test_componenttools_move_parentage_and_spanners_from_components_to_components_03():
    r'''Move parentage and spanners from two old notes to five new notes.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    b1 = spannertools.BeamSpanner(staff[:2])
    b2 = spannertools.BeamSpanner(staff[2:])
    crescendo = spannertools.CrescendoSpanner(staff[:])

    r'''
    \new Staff {
        c'8 [ \<
        d'8 ]
        e'8 [
        f'8 ] \!
    }
    '''

    new_notes = Note(12, (1, 16)) * 5
    componenttools.move_parentage_and_spanners_from_components_to_components(staff[:2], new_notes)
    #staff[:2] = new_notes

    "Equivalent to staff[:2] = new_notes."

    r'''
    \new Staff {
        c''16 [ \<
        c''16
        c''16
        c''16
        c''16 ]
        e'8 [
        f'8 ] \!
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            c''16 [ \<
            c''16
            c''16
            c''16
            c''16 ]
            e'8 [
            f'8 ] \!
        }
        '''
        )


def test_componenttools_move_parentage_and_spanners_from_components_to_components_04():
    r'''Move parentage and spanners from three old notes to five new notes.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    b1 = spannertools.BeamSpanner(staff[:2])
    b2 = spannertools.BeamSpanner(staff[2:])
    crescendo = spannertools.CrescendoSpanner(staff[:])

    r'''
    \new Staff {
        c'8 [ \<
        d'8 ]
        e'8 [
        f'8 ] \!
    }
    '''

    new_notes = Note(12, (1, 16)) * 5
    componenttools.move_parentage_and_spanners_from_components_to_components(staff[:3], new_notes)
    #staff[:3] = new_notes

    "Equivalent to staff[:3] = new_notes."

    r'''
    \new Staff {
        c''16 \<
        c''16
        c''16
        c''16
        c''16
        f'8 [ ] \!
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            c''16 \<
            c''16
            c''16
            c''16
            c''16
            f'8 [ ] \!
        }
        '''
        )


def test_componenttools_move_parentage_and_spanners_from_components_to_components_05():
    r'''Move parentage and spanners from four old notes to five new notes.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    b1 = spannertools.BeamSpanner(staff[:2])
    b2 = spannertools.BeamSpanner(staff[2:])
    crescendo = spannertools.CrescendoSpanner(staff[:])

    r'''
    \new Staff {
        c'8 [ \<
        d'8 ]
        e'8 [
        f'8 ] \!
    }
    '''

    new_notes = Note(12, (1, 16)) * 5
    componenttools.move_parentage_and_spanners_from_components_to_components(staff[:], new_notes)
    #staff[:] = new_notes

    "Equivalent to staff[:] = new_notes."

    r'''
    \new Staff {
        c''16 \<
        c''16
        c''16
        c''16
        c''16 \!
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            c''16 \<
            c''16
            c''16
            c''16
            c''16 \!
        }
        '''
        )


def test_componenttools_move_parentage_and_spanners_from_components_to_components_06():
    r'''Move parentage and spanners from container to children of container.
    '''

    staff = Staff([Voice("c'8 d'8 e'8 f'8")])
    spannertools.BeamSpanner(staff[0])

    r'''
    \new Staff {
        \new Voice {
            c'8 [
            d'8
            e'8
            f'8 ]
        }
    }
    '''

    voice_selection = staff[:1]
    voice = voice_selection[0]
    old_components = \
        componenttools.move_parentage_and_spanners_from_components_to_components(
        voice_selection, staff[0][:])

    "Equivalent to staff[:1] = staff[0][:]."

    r'''
    \new Staff {
        c'8 [
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
            d'8
            e'8
            f'8 ]
        }
        '''
        )
    assert len(voice) == 0
