from abjad import *


def test_componenttools_move_parentage_and_spanners_from_components_to_components_01():
    '''Move parentage and spanners from two old notes to five new notes.'''

    t = Staff("c'8 d'8 e'8 f'8")
    b1 = spannertools.BeamSpanner(t[:2])
    b2 = spannertools.BeamSpanner(t[2:])
    crescendo = spannertools.CrescendoSpanner(t[:])

    r'''
    \new Staff {
        c'8 [ \<
        d'8 ]
        e'8 [
        f'8 ] \!
    }
    '''

    old_notes = t[1:3]
    new_notes = Note(12, (1, 16)) * 5
    componenttools.move_parentage_and_spanners_from_components_to_components(old_notes, new_notes)

    "Equivalent to t[1:3] = new_notes"

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

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc'8 [ ] \\<\n\tc''16\n\tc''16\n\tc''16\n\tc''16\n\tc''16\n\tf'8 [ ] \\!\n}"


def test_componenttools_move_parentage_and_spanners_from_components_to_components_02():
    '''Move parentage and spanners from one old note to five new notes.'''

    t = Staff("c'8 d'8 e'8 f'8")
    b1 = spannertools.BeamSpanner(t[:2])
    b2 = spannertools.BeamSpanner(t[2:])
    crescendo = spannertools.CrescendoSpanner(t[:])

    r'''
    \new Staff {
        c'8 [ \<
        d'8 ]
        e'8 [
        f'8 ] \!
    }
    '''

    new_notes = Note(12, (1, 16)) * 5
    componenttools.move_parentage_and_spanners_from_components_to_components(t[:1], new_notes)
    #t[:1] = new_notes

    "Equivalent to t[:1] = new_notes."

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

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc''16 [ \\<\n\tc''16\n\tc''16\n\tc''16\n\tc''16\n\td'8 ]\n\te'8 [\n\tf'8 ] \\!\n}"


def test_componenttools_move_parentage_and_spanners_from_components_to_components_03():
    '''Move parentage and spanners from two old notes to five new notes.'''

    t = Staff("c'8 d'8 e'8 f'8")
    b1 = spannertools.BeamSpanner(t[:2])
    b2 = spannertools.BeamSpanner(t[2:])
    crescendo = spannertools.CrescendoSpanner(t[:])

    r'''
    \new Staff {
        c'8 [ \<
        d'8 ]
        e'8 [
        f'8 ] \!
    }
    '''

    new_notes = Note(12, (1, 16)) * 5
    componenttools.move_parentage_and_spanners_from_components_to_components(t[:2], new_notes)
    #t[:2] = new_notes

    "Equivalent to t[:2] = new_notes."

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

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc''16 [ \\<\n\tc''16\n\tc''16\n\tc''16\n\tc''16 ]\n\te'8 [\n\tf'8 ] \\!\n}"


def test_componenttools_move_parentage_and_spanners_from_components_to_components_04():
    '''Move parentage and spanners from three old notes to five new notes.'''

    t = Staff("c'8 d'8 e'8 f'8")
    b1 = spannertools.BeamSpanner(t[:2])
    b2 = spannertools.BeamSpanner(t[2:])
    crescendo = spannertools.CrescendoSpanner(t[:])

    r'''
    \new Staff {
        c'8 [ \<
        d'8 ]
        e'8 [
        f'8 ] \!
    }
    '''

    new_notes = Note(12, (1, 16)) * 5
    componenttools.move_parentage_and_spanners_from_components_to_components(t[:3], new_notes)
    #t[:3] = new_notes

    "Equivalent to t[:3] = new_notes."

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

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc''16 \\<\n\tc''16\n\tc''16\n\tc''16\n\tc''16\n\tf'8 [ ] \\!\n}"


def test_componenttools_move_parentage_and_spanners_from_components_to_components_05():
    '''Move parentage and spanners from four old notes to five new notes.'''

    t = Staff("c'8 d'8 e'8 f'8")
    b1 = spannertools.BeamSpanner(t[:2])
    b2 = spannertools.BeamSpanner(t[2:])
    crescendo = spannertools.CrescendoSpanner(t[:])

    r'''
    \new Staff {
        c'8 [ \<
        d'8 ]
        e'8 [
        f'8 ] \!
    }
    '''

    new_notes = Note(12, (1, 16)) * 5
    componenttools.move_parentage_and_spanners_from_components_to_components(t[:], new_notes)
    #t[:] = new_notes

    "Equivalent to t[:] = new_notes."

    r'''
    \new Staff {
        c''16 \<
        c''16
        c''16
        c''16
        c''16 \!
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc''16 \\<\n\tc''16\n\tc''16\n\tc''16\n\tc''16 \\!\n}"


def test_componenttools_move_parentage_and_spanners_from_components_to_components_06():
    '''Move parentage and spanners from container to children of container.'''

    t = Staff([Voice("c'8 d'8 e'8 f'8")])
    spannertools.BeamSpanner(t[0])

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

    old_components = componenttools.move_parentage_and_spanners_from_components_to_components(t[0:1], t[0][:])
    voice = old_components[0]

    #voice = t[0]
    #t[:1] = t[0][:]

    "Equivalent to t[:1] = t[0][:]."

    r'''
    \new Staff {
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"
    assert len(voice) == 0
