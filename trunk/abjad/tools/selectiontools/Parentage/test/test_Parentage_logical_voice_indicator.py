# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_Parentage_logical_voice_indicator_01():
    r'''An anonymous staff and its contained unvoiced leaves share 
    the same signature.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")

    containment = more(staff).select_parentage().logical_voice_indicator
    for component in iterationtools.iterate_components_in_expr(staff):
        assert more(component).select_parentage().logical_voice_indicator == containment


def test_Parentage_logical_voice_indicator_02():
    r'''A named staff and its contained unvoiced leaves share 
    the same signature.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff.name = 'foo'

    containment = more(staff).select_parentage().logical_voice_indicator
    for component in iterationtools.iterate_components_in_expr(staff):
        assert more(component).select_parentage().logical_voice_indicator == containment

def test_Parentage_logical_voice_indicator_03():
    r'''Leaves inside equally named sequential voices inside a staff
    share the same signature.
    '''

    staff = Staff(Voice("c'8 d'8 e'8 f'8") * 2)
    staff[0].name = 'foo'
    staff[1].name = 'foo'

    containment = more(staff[0][0]).select_parentage().logical_voice_indicator
    for leaf in staff.select_leaves():
        assert more(leaf).select_parentage().logical_voice_indicator == containment


def test_Parentage_logical_voice_indicator_04():
    r'''Return LogicalVoiceIndicator giving the root and
    first voice, staff and score in the parentage of component.
    '''

    voice = Voice(notetools.make_repeated_notes(4))
    voice.insert(2, Container(Voice(notetools.make_repeated_notes(2)) * 2))
    voice[2].is_simultaneous = True
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(
        voice)
    voice.override.note_head.color = 'red'

    assert testtools.compare(
        voice,
        r'''
        \new Voice \with {
            \override NoteHead #'color = #red
        } {
            c'8
            d'8
            <<
                \new Voice {
                    e'8
                    f'8
                }
                \new Voice {
                    g'8
                    a'8
                }
            >>
            b'8
            c''8
        }
        '''
        )

    signatures = [more(leaf).select_parentage().logical_voice_indicator 
        for leaf in voice.select_leaves(allow_discontiguous_leaves=True)]

    assert signatures[0] == signatures[1]
    assert signatures[0] != signatures[2]
    assert signatures[0] != signatures[4]
    assert signatures[0] == signatures[6]

    assert signatures[2] == signatures[3]
    assert signatures[2] != signatures[4]


def test_Parentage_logical_voice_indicator_05():
    r'''Return LogicalVoiceIndicator giving the root and
    first voice, staff and score in parentage of component.
    '''

    voice = Voice(notetools.make_repeated_notes(4))
    voice.name = 'foo'
    voice.insert(2, Container(Voice(notetools.make_repeated_notes(2)) * 2))
    voice[2].is_simultaneous = True
    voice[2][0].name = 'foo'
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(
        voice)
    voice.override.note_head.color = 'red'

    assert testtools.compare(
        voice,
        r'''
        \context Voice = "foo" \with {
            \override NoteHead #'color = #red
        } {
            c'8
            d'8
            <<
                \context Voice = "foo" {
                    e'8
                    f'8
                }
                \new Voice {
                    g'8
                    a'8
                }
            >>
            b'8
            c''8
        }
        '''
        )

    signatures = [more(leaf).select_parentage().logical_voice_indicator 
        for leaf in voice.select_leaves(allow_discontiguous_leaves=True)]

    signatures[0] == signatures[1]
    signatures[0] == signatures[2]
    signatures[0] != signatures[4]
    signatures[0] == signatures[6]

    signatures[2] == signatures[0]
    signatures[2] == signatures[3]
    signatures[2] == signatures[4]
    signatures[2] == signatures[6]

    signatures[4] != signatures[0]
    signatures[4] != signatures[2]
    signatures[4] == signatures[5]
    signatures[4] == signatures[6]


def test_Parentage_logical_voice_indicator_06():
    r'''Return LogicalVoiceIndicator giving the root and
    first voice, staff and score in parentage of component.
    '''

    container = Container(Staff([Voice("c'8 d'8")]) * 2)
    container[0].name = 'staff1'
    container[1].name = 'staff2'
    container[0][0].name = 'voicefoo'
    container[1][0].name = 'voicefoo'
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(
        container)
    assert py.test.raises(
        AssertionError, 'spannertools.BeamSpanner(container.select_leaves())')
    leaves = container.select_leaves(allow_discontiguous_leaves=True)
    spannertools.BeamSpanner(leaves[:2])
    spannertools.BeamSpanner(leaves[2:])

    assert testtools.compare(
        container,
        r'''
        {
            \context Staff = "staff1" {
                \context Voice = "voicefoo" {
                    c'8 [
                    d'8 ]
                }
            }
            \context Staff = "staff2" {
                \context Voice = "voicefoo" {
                    e'8 [
                    f'8 ]
                }
            }
        }
        '''
        )

    signatures = [more(leaf).select_parentage().logical_voice_indicator 
        for leaf in leaves]

    signatures[0] == signatures[1]
    signatures[0] != signatures[2]

    signatures[2] != signatures[2]
    signatures[2] == signatures[3]


def test_Parentage_logical_voice_indicator_07():
    r'''Return LogicalVoiceIndicator giving the root and
    first voice, staff and score in parentage of component.
    '''

    container = Container(notetools.make_repeated_notes(2))
    container[1:1] = Container(
        Voice(notetools.make_repeated_notes(1)) * 2) * 2
    container[1].is_simultaneous = True
    container[1][0].name = 'alto'
    container[1][1].name = 'soprano'
    container[2][0].name = 'alto'
    container[2][1].name = 'soprano'
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(
        container)
    container[1][1].override.note_head.color = 'red'
    container[2][1].override.note_head.color = 'red'

    assert testtools.compare(
        container,
        r'''
        {
            c'8
            <<
                \context Voice = "alto" {
                    d'8
                }
                \context Voice = "soprano" \with {
                    \override NoteHead #'color = #red
                } {
                    e'8
                }
            >>
            {
                \context Voice = "alto" {
                    f'8
                }
                \context Voice = "soprano" \with {
                    \override NoteHead #'color = #red
                } {
                    g'8
                }
            }
            a'8
        }
        '''
        )

    signatures = [more(leaf).select_parentage().logical_voice_indicator 
        for leaf in container.select_leaves(allow_discontiguous_leaves=True)]

    signatures[0] != signatures[1]
    signatures[0] != signatures[2]
    signatures[0] != signatures[3]
    signatures[0] != signatures[4]
    signatures[0] == signatures[5]

    signatures[1] != signatures[0]
    signatures[1] != signatures[2]
    signatures[1] == signatures[3]
    signatures[1] != signatures[4]
    signatures[1] != signatures[5]

    signatures[2] != signatures[0]
    signatures[2] != signatures[1]
    signatures[2] != signatures[3]
    signatures[2] == signatures[4]
    signatures[2] != signatures[5]


def test_Parentage_logical_voice_indicator_08():
    r'''Unicorporated leaves carry equivalent containment signatures.
    '''

    note_1 = Note(0, (1, 8))
    note_2 = Note(0, (1, 8))

    signature_1 = more(note_1).select_parentage().logical_voice_indicator
    signature_2 = more(note_2).select_parentage().logical_voice_indicator
    assert signature_1 == signature_2


def test_Parentage_logical_voice_indicator_09():
    r'''Notes appear in the same logical voice.
    '''

    t1 = Staff([Voice([Note(0, (1, 8))])])
    t1.name = 'staff'
    t1[0].name = 'voice'

    t2 = Staff([Voice([Note(0, (1, 8))])])
    t2.name = 'staff'
    t2[0].name = 'voice'

    t1_leaf_signature = more(t1.select_leaves()[0]).select_parentage().logical_voice_indicator
    t2_leaf_signature = more(t2.select_leaves()[0]).select_parentage().logical_voice_indicator
    assert t1_leaf_signature == t2_leaf_signature


def test_Parentage_logical_voice_indicator_10():
    r'''Measure and leaves must carry same logical voice signature.
    '''

    staff = Staff([Measure((2, 8), "c'8 d'8")] +
        notetools.make_repeated_notes(2))
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(
        staff)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            e'8
            f'8
        }
        '''
        )

    assert more(staff[0]).select_parentage().logical_voice_indicator == \
        more(staff[-1]).select_parentage().logical_voice_indicator
    assert more(staff[0]).select_parentage().logical_voice_indicator == \
        more(staff[0][0]).select_parentage().logical_voice_indicator
    assert more(staff[0][0]).select_parentage().logical_voice_indicator == \
        more(staff[-1]).select_parentage().logical_voice_indicator


def test_Parentage_logical_voice_indicator_11():
    r'''Leaves inside different staves have different logical voice 
    signatures, even when the staves have the same name.
    '''

    container = Container(Staff(notetools.make_repeated_notes(2)) * 2)
    container[0].name = container[1].name = 'staff'
    
    assert testtools.compare(
        container,
        r'''
        {
            \context Staff = "staff" {
                c'8
                c'8
            }
            \context Staff = "staff" {
                c'8
                c'8
            }
        }
        '''
        )

    leaves = container.select_leaves(allow_discontiguous_leaves=True)
    assert more(leaves[0]).select_parentage().logical_voice_indicator == \
        more(leaves[1]).select_parentage().logical_voice_indicator
    assert more(leaves[0]).select_parentage().logical_voice_indicator != \
        more(leaves[2]).select_parentage().logical_voice_indicator
    assert more(leaves[2]).select_parentage().logical_voice_indicator == \
        more(leaves[3]).select_parentage().logical_voice_indicator
    assert more(leaves[2]).select_parentage().logical_voice_indicator != \
        more(leaves[0]).select_parentage().logical_voice_indicator
