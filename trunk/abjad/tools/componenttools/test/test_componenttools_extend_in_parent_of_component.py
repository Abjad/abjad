from abjad import *


#def test_componenttools_extend_in_parent_of_component_01():
#
#    t = Voice("c'8 d'8 e'8")
#    beamtools.BeamSpanner(t[:])
#    result = componenttools.extend_in_parent_of_component(
#        t[-1], [Note("c'8"), Note("d'8"), Note("e'8")], grow_spanners=True)
#
#    r'''
#    \new Voice {
#        c'8 [
#        d'8
#        e'8
#        c'8
#        d'8
#        e'8 ]
#    }
#    '''
#
#    assert componenttools.is_well_formed_component(t)
#    assert result == t[-4:]
#    assert t.lilypond_format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tc'8\n\td'8\n\te'8 ]\n}"
#
#
#def test_componenttools_extend_in_parent_of_component_02():
#    '''Splice leaf after interior leaf.'''
#
#    t = Voice("c'8 d'8 e'8")
#    beamtools.BeamSpanner(t[:])
#    result = componenttools.extend_in_parent_of_component(
#        t[1], [Note(2.5, (1, 8))], grow_spanners=True)
#
#    r'''
#    \new Voice {
#        c'8 [
#        d'8
#        dqs'8
#        e'8 ]
#    }
#    '''
#
#    assert componenttools.is_well_formed_component(t)
#    assert t.lilypond_format == "\\new Voice {\n\tc'8 [\n\td'8\n\tdqs'8\n\te'8 ]\n}"
#    assert result == t[1:3]
#
#
#def test_componenttools_extend_in_parent_of_component_03():
#    '''Splice tuplet after tuplet.'''
#
#    t = Voice([tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")])
#    beamtools.BeamSpanner(t[0])
#    result = componenttools.extend_in_parent_of_component(;a
#        t[-1], [tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")], grow_spanners=True)
#
#    r'''
#    \new Voice {
#        \times 2/3 {
#            c'8 [
#            d'8
#            e'8
#        }
#        \times 2/3 {
#            c'8
#            d'8
#            e'8 ]
#        }
#    }
#    '''
#
#    assert componenttools.is_well_formed_component(t)
#    assert result == t[:]
#    assert t.lilypond_format == "\\new Voice {\n\t\\times 2/3 {\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t}\n\t\\times 2/3 {\n\t\tc'8\n\t\td'8\n\t\te'8 ]\n\t}\n}"
#
#
#def test_componenttools_extend_in_parent_of_component_04():
#    '''Splice after container with underspanners.'''
#
#    t = Voice(Container(notetools.make_repeated_notes(2)) * 2)
#    beamtools.BeamSpanner(t.leaves)
#    result = componenttools.extend_in_parent_of_component(
#        t[0], [Note(2.5, (1, 8))], grow_spanners=True)
#
#    r'''
#    \new Voice {
#        {
#            c'8 [
#            c'8
#        }
#        dqs'8
#        {
#            c'8
#            c'8 ]
#        }
#    }
#    '''
#
#    assert componenttools.is_well_formed_component(t)
#    assert t.lilypond_format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\tc'8\n\t}\n\tdqs'8\n\t{\n\t\tc'8\n\t\tc'8 ]\n\t}\n}"
#    assert result == t[0:2]


def test_componenttools_extend_in_parent_of_component_05():
    '''Extend leaves rightwards after leaf.'''

    t = Voice("c'8 d'8 e'8")
    beamtools.BeamSpanner(t[:])
    result = componenttools.extend_in_parent_of_component(
        t[-1], [Note("c'8"), Note("d'8"), Note("e'8")], grow_spanners=False)

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8 ]
        c'8
        d'8
        e'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert result == t[-4:]
    assert t.lilypond_format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8 ]\n\tc'8\n\td'8\n\te'8\n}"


def test_componenttools_extend_in_parent_of_component_06():
    '''Extend leaf rightwards after interior leaf.'''

    t = Voice("c'8 d'8 e'8")
    beamtools.BeamSpanner(t[:])
    result = componenttools.extend_in_parent_of_component(
        t[1], [Note(2.5, (1, 8))], grow_spanners=False)

    r'''
    \new Voice {
        c'8 [
        d'8
        dqs'8
        e'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Voice {\n\tc'8 [\n\td'8\n\tdqs'8\n\te'8 ]\n}"
    assert result == t[1:3]
