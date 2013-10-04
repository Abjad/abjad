# -*- encoding: utf-8 -*-
import py.test
from abjad import *
Component = componenttools.Component
Selection = selectiontools.Selection


def test_Selection__all_are_components_in_same_logical_voice_01():
    r'''Unincorporated leaves do not share a logical voice.
    Unicorporated leaves do not share a root component.
    False if not allow orphans; True if allow orphans.
    '''

    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]
    assert Selection._all_are_components_in_same_logical_voice(notes)
    assert not Selection._all_are_components_in_same_logical_voice(
        notes, allow_orphans=False)


def test_Selection__all_are_components_in_same_logical_voice_02():
    r'''Container and leaves all logical voice.
    '''

    container = Container("c'8 d'8 e'8 f'8")

    r'''
    {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert Selection._all_are_components_in_same_logical_voice(
        list(iterationtools.iterate_components_in_expr(container, Component)))


def test_Selection__all_are_components_in_same_logical_voice_03():
    r'''Tuplet and leaves all logical voice.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")

    r'''
    \times 2/3 {
        c'8
        d'8
        e'8
    }
    '''

    assert Selection._all_are_components_in_same_logical_voice(
        list(iterationtools.iterate_components_in_expr(tuplet, Component)))


def test_Selection__all_are_components_in_same_logical_voice_04():
    r'''Voice and leaves all appear in same logical voice.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")

    r'''
    \new Voice {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert Selection._all_are_components_in_same_logical_voice(
        list(iterationtools.iterate_components_in_expr(voice, Component)))


def test_Selection__all_are_components_in_same_logical_voice_05():
    r'''Anonymous staff and leaves all appear in same logical voice.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")

    r'''
    \new Staff {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert Selection._all_are_components_in_same_logical_voice(
        list(iterationtools.iterate_components_in_expr(staff, Component)))


def test_Selection__all_are_components_in_same_logical_voice_06():
    r'''Voice, sequential and leaves all appear in same logical voice.
    '''

    voice = Voice(Container(notetools.make_repeated_notes(4)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(
        voice)

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8
                d'8
                e'8
                f'8
            }
            {
                g'8
                a'8
                b'8
                c''8
            }
        }
        '''
        )

    assert Selection._all_are_components_in_same_logical_voice(
        list(iterationtools.iterate_components_in_expr(voice, Component)))


def test_Selection__all_are_components_in_same_logical_voice_07():
    r'''Anonymous voice, tuplets and leaves all appear in same logical voice.
    '''

    voice = Voice(tuplettools.FixedDurationTuplet(
        Duration(2, 8), notetools.make_repeated_notes(3)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(
        voice)

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            \times 2/3 {
                c'8
                d'8
                e'8
            }
            \times 2/3 {
                f'8
                g'8
                a'8
            }
        }
        '''
        )

    assert Selection._all_are_components_in_same_logical_voice(
        list(iterationtools.iterate_components_in_expr(voice, Component)))


def test_Selection__all_are_components_in_same_logical_voice_08():
    r'''Logical voice does not extend across anonymous voices.
    '''

    staff = Staff(Voice(notetools.make_repeated_notes(4)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(
        staff)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \new Voice {
                c'8
                d'8
                e'8
                f'8
            }
            \new Voice {
                g'8
                a'8
                b'8
                c''8
            }
        }
        '''
        )

    assert Selection._all_are_components_in_same_logical_voice(
        staff.select_leaves(allow_discontiguous_leaves=True)[:4])
    assert Selection._all_are_components_in_same_logical_voice(
        staff.select_leaves(allow_discontiguous_leaves=True)[4:])
    assert not Selection._all_are_components_in_same_logical_voice(
        staff.select_leaves(allow_discontiguous_leaves=True))
    assert not Selection._all_are_components_in_same_logical_voice(
        staff[:])


def test_Selection__all_are_components_in_same_logical_voice_09():
    r'''Logical voice encompasses across like-named voices.
    '''

    staff = Staff(Voice(notetools.make_repeated_notes(4)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(
        staff)
    staff[0].name = 'foo'
    staff[1].name = 'foo'

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \context Voice = "foo" {
                c'8
                d'8
                e'8
                f'8
            }
            \context Voice = "foo" {
                g'8
                a'8
                b'8
                c''8
            }
        }
        '''
        )

    assert Selection._all_are_components_in_same_logical_voice(
        staff.select_leaves(allow_discontiguous_leaves=True))


def test_Selection__all_are_components_in_same_logical_voice_10():
    r'''Logical voice does not extend across differently named voices.
    '''

    staff = Staff(Voice(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(
        staff)
    staff[0].name = 'foo'
    staff[1].name = 'bar'

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \context Voice = "foo" {
                c'8
                d'8
            }
            \context Voice = "bar" {
                e'8
                f'8
            }
        }
        '''
        )

    assert not Selection._all_are_components_in_same_logical_voice(
        staff.select_leaves(allow_discontiguous_leaves=True))


def test_Selection__all_are_components_in_same_logical_voice_11():
    r'''Logical voice does not across anonymous voices.
    Logical voice does not extend across anonymous staves.
    '''

    container = Container(Staff([Voice(notetools.make_repeated_notes(2))]) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(
        container)

    assert testtools.compare(
        container,
        r'''
        {
            \new Staff {
                \new Voice {
                    c'8
                    d'8
                }
            }
            \new Staff {
                \new Voice {
                    e'8
                    f'8
                }
            }
        }
        '''
        )

    assert not Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True))


def test_Selection__all_are_components_in_same_logical_voice_12():
    r'''Logical voice does not extend across anonymous voices.
    Logical voice does not extend across anonymous staves.
    '''

    container = Container(
        Staff(Voice(notetools.make_repeated_notes(2)) * 2) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(
        container)
    container[0].is_simultaneous = True
    container[1].is_simultaneous = True

    assert testtools.compare(
        container,
        r'''
        {
            \new Staff <<
                \new Voice {
                    c'8
                    d'8
                }
                \new Voice {
                    e'8
                    f'8
                }
            >>
            \new Staff <<
                \new Voice {
                    g'8
                    a'8
                }
                \new Voice {
                    b'8
                    c''8
                }
            >>
        }
        '''
        )

    assert not Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[:4])


def test_Selection__all_are_components_in_same_logical_voice_13():
    r'''Anonymous voice, sequentials and leaves all appear in same 
    logical voice.
    '''

    voice = Voice(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(
        voice)

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8
                d'8
            }
            {
                e'8
                f'8
            }
        }
        '''
        )

    assert Selection._all_are_components_in_same_logical_voice(
        voice.select_leaves(allow_discontiguous_leaves=True))


def test_Selection__all_are_components_in_same_logical_voice_14():
    r'''Logical voice can extend across like-named staves.
    Logical voice can not extend across differently named implicit voices.
    '''

    container = Container(Staff(Note(0, (1, 8)) * 4) * 2)
    pitchtools.set_ascending_named_pitches_on_tie_chains_in_expr(
        container)
    container[0].name = 'foo'
    container[1].name = 'foo'

    assert testtools.compare(
        container,
        r'''
        {
            \context Staff = "foo" {
                c'8
                cs'8
                d'8
                ef'8
            }
            \context Staff = "foo" {
                e'8
                f'8
                fs'8
                g'8
            }
        }
        '''
        )

    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[:4])
    assert not Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True))


def test_Selection__all_are_components_in_same_logical_voice_15():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    container = Container([
        Container(notetools.make_repeated_notes(4)), 
        Voice(notetools.make_repeated_notes(4)),
        ])
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(
        container)

    assert testtools.compare(
        container,
        r'''
        {
            {
                c'8
                d'8
                e'8
                f'8
            }
            \new Voice {
                g'8
                a'8
                b'8
                c''8
            }
        }
        '''
        )

    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[:4])
    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[4:])
    assert not Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True))


def test_Selection__all_are_components_in_same_logical_voice_16():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    container = Container(
        [Voice(notetools.make_repeated_notes(4)), 
        Container(notetools.make_repeated_notes(4))])
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(
        container)

    assert testtools.compare(
        container,
        r'''
        {
            \new Voice {
                c'8
                d'8
                e'8
                f'8
            }
            {
                g'8
                a'8
                b'8
                c''8
            }
        }
        '''
        )

    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[:4])
    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[4:])
    assert not Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True))


def test_Selection__all_are_components_in_same_logical_voice_17():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    container = Container([
        Container(notetools.make_repeated_notes(4)), 
        Voice(notetools.make_repeated_notes(4)),
        ])
    container[1].name = 'foo'
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(
        container)

    r'''
    {
        {
            c'8
            d'8
            e'8
            f'8
        }
        \context Voice = "foo" {
            g'8
            a'8
            b'8
            c''8
        }
    }
    '''

    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[:4])
    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[4:])
    assert not Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True))


def test_Selection__all_are_components_in_same_logical_voice_18():
    r'''Logical voice can not extend acrossdifferently named implicit voices.
    '''

    container = Container([
        Voice(notetools.make_repeated_notes(4)), 
        Container(notetools.make_repeated_notes(4)),
        ])
    container[0].name = 'foo'
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(
        container)

    assert testtools.compare(
        container,
        r'''
        {
            \context Voice = "foo" {
                c'8
                d'8
                e'8
                f'8
            }
            {
                g'8
                a'8
                b'8
                c''8
            }
        }
        '''
        )

    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[:4])
    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[4:])
    assert not Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True))


def test_Selection__all_are_components_in_same_logical_voice_19():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    container = Container(
        [Container(notetools.make_repeated_notes(4)), 
        Staff(notetools.make_repeated_notes(4))])
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(
        container)

    assert testtools.compare(
        container,
        r'''
        {
            {
                c'8
                d'8
                e'8
                f'8
            }
            \new Staff {
                g'8
                a'8
                b'8
                c''8
            }
        }
        '''
        )

    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[:4])
    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[4:])
    assert not Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True))


def test_Selection__all_are_components_in_same_logical_voice_20():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    container = Container(
        [Staff(Note(0, (1, 8)) * 4), Container(Note(0, (1, 8)) * 4)])
    pitchtools.set_ascending_named_pitches_on_tie_chains_in_expr(
        container)

    assert testtools.compare(
        container,
        r'''
        {
            \new Staff {
                c'8
                cs'8
                d'8
                ef'8
            }
            {
                e'8
                f'8
                fs'8
                g'8
            }
        }
        '''
        )

    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[:4])
    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[4:])
    assert not Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True))


def test_Selection__all_are_components_in_same_logical_voice_21():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    container = Container(Note(0, (1, 8)) * 4 + [Voice(Note(0, (1, 8)) * 4)])
    pitchtools.set_ascending_named_pitches_on_tie_chains_in_expr(
        container)

    assert testtools.compare(
        container,
        r'''
        {
            c'8
            cs'8
            d'8
            ef'8
            \new Voice {
                e'8
                f'8
                fs'8
                g'8
            }
        }
        '''
        )

    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[:4])
    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[4:])
    assert not Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True))


def test_Selection__all_are_components_in_same_logical_voice_22():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    container = Container([Voice(Note(0, (1, 8)) * 4)] + Note(0, (1, 8)) * 4)
    pitchtools.set_ascending_named_pitches_on_tie_chains_in_expr(
        container)

    assert testtools.compare(
        container,
        r'''
        {
            \new Voice {
                c'8
                cs'8
                d'8
                ef'8
            }
            e'8
            f'8
            fs'8
            g'8
        }
        '''
        )

    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[:4])
    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[4:])
    assert not Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True))


def test_Selection__all_are_components_in_same_logical_voice_23():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    container = Container(Note(0, (1, 8)) * 4 + [Voice(Note(0, (1, 8)) * 4)])
    container[4].name = 'foo'
    pitchtools.set_ascending_named_pitches_on_tie_chains_in_expr(
        container)

    assert testtools.compare(
        container,
        r'''
        {
            c'8
            cs'8
            d'8
            ef'8
            \context Voice = "foo" {
                e'8
                f'8
                fs'8
                g'8
            }
        }
        '''
        )

    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[:4])
    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[4:])
    assert not Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True))


def test_Selection__all_are_components_in_same_logical_voice_24():
    r'''Logical voice can not extend across differently named implicit voices.
    NOTE: THIS IS THE LILYPOND LACUNA.
    LilyPond *does* extend logical voice in this case.
    Abjad does not.
    '''

    container = Container([Voice(Note(0, (1, 8)) * 4)] + Note(0, (1, 8)) * 4)
    pitchtools.set_ascending_named_pitches_on_tie_chains_in_expr(
        container)
    container[0].name = 'foo'

    assert testtools.compare(
        container,
        r'''
        {
            \context Voice = "foo" {
                c'8
                cs'8
                d'8
                ef'8
            }
            e'8
            f'8
            fs'8
            g'8
        }
        '''
        )

    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[:4])
    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[4:])
    assert not Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True))


def test_Selection__all_are_components_in_same_logical_voice_25():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    container = Container(Note(0, (1, 8)) * 4 + [Voice(Note(0, (1, 8)) * 4)])
    pitchtools.set_ascending_named_pitches_on_tie_chains_in_expr(
        container)

    assert testtools.compare(
        container,
        r'''
        {
            c'8
            cs'8
            d'8
            ef'8
            \new Voice {
                e'8
                f'8
                fs'8
                g'8
            }
        }
        '''
        )

    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[:4])
    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[4:])
    assert not Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True))


def test_Selection__all_are_components_in_same_logical_voice_26():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    container = Container(notetools.make_repeated_notes(4))
    container.insert(0, Staff(notetools.make_repeated_notes(4)))
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(
        container)

    assert testtools.compare(
        container,
        r'''
        {
            \new Staff {
                c'8
                d'8
                e'8
                f'8
            }
            g'8
            a'8
            b'8
            c''8
        }
        '''
        )

    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[:4])
    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[4:])
    assert not Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True))


def test_Selection__all_are_components_in_same_logical_voice_27():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    voice = Voice([Note(n, (1, 8)) for n in range(4)])
    container = Container([voice])
    notes = [Note(n, (1, 8)) for n in range(4, 8)]
    container = Container([container] + notes)

    assert testtools.compare(
        container,
        r'''
        {
            {
                \new Voice {
                    c'8
                    cs'8
                    d'8
                    ef'8
                }
            }
            e'8
            f'8
            fs'8
            g'8
        }
        '''
        )

    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[:4])
    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[4:])
    assert not Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True))


def test_Selection__all_are_components_in_same_logical_voice_28():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    voice = Voice([Note(n, (1, 8)) for n in range(4)])
    voice.name = 'foo'
    q = Container([voice])
    notes = [Note(n, (1, 8)) for n in range(4, 8)]
    container = Container([q] + notes)

    r'''
    {
        {
            \context Voice = "foo" {
                c'8
                cs'8
                d'8
                ef'8
            }
        }
        e'8
        f'8
        fs'8
        g'8
    }
    '''

    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[:4])
    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[4:])
    assert not Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True))


def test_Selection__all_are_components_in_same_logical_voice_29():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    voice_1 = Voice([Note(n, (1, 8)) for n in range(4)])
    voice_1.name = 'foo'
    voice_2 = Voice([voice_1])
    voice_2.name = 'bar'
    notes = [Note(n, (1, 8)) for n in range(4, 8)]
    container = Container([voice_2] + notes)

    assert testtools.compare(
        container,
        r'''
        {
            \context Voice = "bar" {
                \context Voice = "foo" {
                    c'8
                    cs'8
                    d'8
                    ef'8
                }
            }
            e'8
            f'8
            fs'8
            g'8
        }
        '''
        )

    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[:4])
    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[4:])
    assert not Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True))


def test_Selection__all_are_components_in_same_logical_voice_30():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    voice_1 = Voice([Note(n, (1, 8)) for n in range(4)])
    voice_2 = Voice([voice_1])
    notes = [Note(n, (1, 8)) for n in range(4, 8)]
    container = Container([voice_2] + notes)

    assert testtools.compare(
        container,
        r'''
        {
            \new Voice {
                \new Voice {
                    c'8
                    cs'8
                    d'8
                    ef'8
                }
            }
            e'8
            f'8
            fs'8
            g'8
        }
        '''
        )

    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[:4])
    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[4:])
    assert not Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True))


def test_Selection__all_are_components_in_same_logical_voice_31():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    notes = [Note(n, (1, 8)) for n in range(4)]
    voice_1 = Voice(Note(12, (1, 8)) * 4)
    voice_2 = Voice(Note(0, (1, 8)) * 4)
    container = Container([voice_1, voice_2])
    container.is_simultaneous = True
    container = Container(notes + [container])

    assert testtools.compare(
        container,
        r'''
        {
            c'8
            cs'8
            d'8
            ef'8
            <<
                \new Voice {
                    c''8
                    c''8
                    c''8
                    c''8
                }
                \new Voice {
                    c'8
                    c'8
                    c'8
                    c'8
                }
            >>
        }
        '''
        )

    assert not Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[:8])
    assert not Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[4:])


def test_Selection__all_are_components_in_same_logical_voice_32():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    container = Container(
        [Container(Voice(Note(0, (1, 8)) * 4) * 2)] + Note(0, (1, 8)) * 4)
    container[0].is_simultaneous = True
    pitchtools.set_ascending_named_pitches_on_tie_chains_in_expr(
        container)

    assert testtools.compare(
        container,
        r'''
        {
            <<
                \new Voice {
                    c'8
                    cs'8
                    d'8
                    ef'8
                }
                \new Voice {
                    e'8
                    f'8
                    fs'8
                    g'8
                }
            >>
            af'8
            a'8
            bf'8
            b'8
        }
        '''
        )

    assert not Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[:8])
    assert not Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[4:])


def test_Selection__all_are_components_in_same_logical_voice_33():
    r'''Logical voice does extend across gaps.
    Logical voice can not extend across differently named voices.
    '''

    container = Container(Note(0, (1, 8)) * 4)
    a, b = Voice(Note(0, (1, 8)) * 4) * 2
    a.insert(2, b)
    container.insert(2, a)
    pitchtools.set_ascending_named_pitches_on_tie_chains_in_expr(
        container)

    outer = (0, 1, 10, 11)
    middle = (2, 3, 8, 9)
    inner = (4, 5, 6, 7)

    assert testtools.compare(
        container,
        r'''
        {
            c'8
            cs'8
            \new Voice {
                d'8
                ef'8
                \new Voice {
                    e'8
                    f'8
                    fs'8
                    g'8
                }
                af'8
                a'8
            }
            bf'8
            b'8
        }
        '''
        )

    assert Selection._all_are_components_in_same_logical_voice(
        [container.select_leaves(allow_discontiguous_leaves=True)[i] 
        for i in outer])
    assert Selection._all_are_components_in_same_logical_voice(
        [container.select_leaves(allow_discontiguous_leaves=True)[i] 
        for i in middle])
    assert Selection._all_are_components_in_same_logical_voice(
        [container.select_leaves(allow_discontiguous_leaves=True)[i] 
        for i in inner])
    assert not Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[:4])


def test_Selection__all_are_components_in_same_logical_voice_34():
    r'''Logical voice does extend across gaps.
    Logical voice can not extend across differently named implicit voices.
    '''

    staff = Staff(Note(0, (1, 8)) * 4)
    a, b = staff * 2
    a.insert(2, b)
    staff.insert(2, a)
    pitchtools.set_ascending_named_pitches_on_tie_chains_in_expr(
        staff)

    outer = (0, 1, 10, 11)
    middle = (2, 3, 8, 9)
    inner = (4, 5, 6, 7)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8
            cs'8
            \new Staff {
                d'8
                ef'8
                \new Staff {
                    e'8
                    f'8
                    fs'8
                    g'8
                }
                af'8
                a'8
            }
            bf'8
            b'8
        }
        '''
        )

    assert Selection._all_are_components_in_same_logical_voice(
        [staff.select_leaves(allow_discontiguous_leaves=True)[i] 
        for i in outer])
    assert Selection._all_are_components_in_same_logical_voice(
        [staff.select_leaves(allow_discontiguous_leaves=True)[i] 
        for i in middle])
    assert Selection._all_are_components_in_same_logical_voice(
        [staff.select_leaves(allow_discontiguous_leaves=True)[i] 
        for i in inner])
    assert not Selection._all_are_components_in_same_logical_voice(
        staff.select_leaves(allow_discontiguous_leaves=True)[:4])


def test_Selection__all_are_components_in_same_logical_voice_35():
    r'''Containers and leaves all appear in same logical voice.
    '''

    a, b, container = Container(Note(0, (1, 8)) * 4) * 3
    a.insert(2, b)
    container.insert(2, a)
    pitchtools.set_ascending_named_pitches_on_tie_chains_in_expr(
        container)

    assert testtools.compare(
        container,
        r'''
        {
            c'8
            cs'8
            {
                d'8
                ef'8
                {
                    e'8
                    f'8
                    fs'8
                    g'8
                }
                af'8
                a'8
            }
            bf'8
            b'8
        }
        '''
        )

    assert Selection._all_are_components_in_same_logical_voice(
        list(iterationtools.iterate_components_in_expr(container, Component)))


def test_Selection__all_are_components_in_same_logical_voice_36():
    r'''Tuplets and leaves all appear in same logical voice.
    '''

    a, b, t = tuplettools.FixedDurationTuplet(
        Duration(3, 8), Note(0, (1, 8)) * 4) * 3
    b.insert(2, a)
    t.insert(2, b)
    b.target_duration = Duration(6, 8)
    t.target_duration = Duration(9, 8)
    pitchtools.set_ascending_named_pitches_on_tie_chains_in_expr(t)

    assert testtools.compare(
        t,
        r'''
        \tweak #'text #tuplet-number::calc-fraction-text
        \times 9/10 {
            c'8
            cs'8
            \tweak #'text #tuplet-number::calc-fraction-text
            \times 6/7 {
                d'8
                ef'8
                \tweak #'text #tuplet-number::calc-fraction-text
                \times 3/4 {
                    e'8
                    f'8
                    fs'8
                    g'8
                }
                af'8
                a'8
            }
            bf'8
            b'8
        }
        '''
        )

    assert Selection._all_are_components_in_same_logical_voice(
        list(iterationtools.iterate_components_in_expr(t, Component)))


def test_Selection__all_are_components_in_same_logical_voice_37():
    r'''Logical voice can not extend across differently named voices.
    '''

    container = Container(Note(0, (1, 8)) * 4)
    container.insert(2, Container([Container([Voice(Note(0, (1, 8)) * 4)])]))
    container[2][0][0].name = 'foo'
    pitchtools.set_ascending_named_pitches_on_tie_chains_in_expr(
        container)

    assert testtools.compare(
        container,
        r'''
        {
            c'8
            cs'8
            {
                {
                    \context Voice = "foo" {
                        d'8
                        ef'8
                        e'8
                        f'8
                    }
                }
            }
            fs'8
            g'8
        }
        '''
        )

    outer = (0, 1, 6, 7)
    inner = (2, 3, 4, 5)

    assert Selection._all_are_components_in_same_logical_voice(
        [container.select_leaves(allow_discontiguous_leaves=True)[i] 
        for i in outer])
    assert Selection._all_are_components_in_same_logical_voice(
        [container.select_leaves(allow_discontiguous_leaves=True)[i] 
        for i in inner])
    assert not Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True))


def test_Selection__all_are_components_in_same_logical_voice_38():
    r'''Logical voice does not extend over differently named voices.
    '''

    container = Container(Note(0, (1, 8)) * 4)
    container.insert(0, Container([Container([Voice(Note(0, (1, 8)) * 4)])]))
    container[0][0][0].name = 'foo'
    pitchtools.set_ascending_named_pitches_on_tie_chains_in_expr(
        container)

    assert testtools.compare(
        container,
        r'''
        {
            {
                {
                    \context Voice = "foo" {
                        c'8
                        cs'8
                        d'8
                        ef'8
                    }
                }
            }
            e'8
            f'8
            fs'8
            g'8
        }
        '''
        )

    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[:4])
    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[4:])
    assert not Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True))


def test_Selection__all_are_components_in_same_logical_voice_39():
    r'''Can not nest across differently named implicit voices.
    '''

    container = Container(Note(0, (1, 8)) * 4)
    container.insert(2, Voice(Note(0, (1, 8)) * 4))
    container = Container([container])
    container = Container([container])
    container = Voice([container])
    pitchtools.set_ascending_named_pitches_on_tie_chains_in_expr(
        container)

    assert testtools.compare(
        container,
        r'''
        \new Voice {
            {
                {
                    {
                        c'8
                        cs'8
                        \new Voice {
                            d'8
                            ef'8
                            e'8
                            f'8
                        }
                        fs'8
                        g'8
                    }
                }
            }
        }
        '''
        )

    outer = (0, 1, 6, 7)
    inner = (2, 3, 4, 5)

    assert Selection._all_are_components_in_same_logical_voice(
        [container.select_leaves( allow_discontiguous_leaves=True)[i] 
        for i in outer])
    assert Selection._all_are_components_in_same_logical_voice(
        [container.select_leaves(allow_discontiguous_leaves=True)[i] 
        for i in inner])
    assert not Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True))


def test_Selection__all_are_components_in_same_logical_voice_40():
    r'''Logical voice can not extend across differently named voices.
    '''

    voice = Voice(Note(0, (1, 8)) * 4)
    voice.name = 'bar'
    q = Container(Note(0, (1, 8)) * 4)
    q.insert(2, voice)
    qq = Container(Note(0, (1, 8)) * 4)
    qq.insert(2, q)
    voice = Voice(Note(0, (1, 8)) * 4)
    voice.insert(2, qq)
    voice.name = 'foo'
    pitchtools.set_ascending_named_pitches_on_tie_chains_in_expr(
        voice)

    assert testtools.compare(
        voice,
        r'''
        \context Voice = "foo" {
            c'8
            cs'8
            {
                d'8
                ef'8
                {
                    e'8
                    f'8
                    \context Voice = "bar" {
                        fs'8
                        g'8
                        af'8
                        a'8
                    }
                    bf'8
                    b'8
                }
                c''8
                cs''8
            }
            d''8
            ef''8
        }
        '''
        )

    outer = (0, 1, 2, 3, 4, 5, 10, 11, 12, 13, 14, 15)
    inner = (6, 7, 8, 9)

    assert Selection._all_are_components_in_same_logical_voice(
        [voice.select_leaves(allow_discontiguous_leaves=True)[i] 
        for i in outer])
    assert Selection._all_are_components_in_same_logical_voice(
        [voice.select_leaves(allow_discontiguous_leaves=True)[i] 
        for i in inner])
    assert not Selection._all_are_components_in_same_logical_voice(
        voice.select_leaves(allow_discontiguous_leaves=True))


def test_Selection__all_are_components_in_same_logical_voice_41():
    r'''Logical voice can not extend across differently named anonymous voices.
    '''

    container = Container(notetools.make_repeated_notes(4))
    container[0:0] = Voice(notetools.make_repeated_notes(4)) * 2
    pitchtools.set_ascending_named_pitches_on_tie_chains_in_expr(
        container)

    assert testtools.compare(
        container,
        r'''
        {
            \new Voice {
                c'8
                cs'8
                d'8
                ef'8
            }
            \new Voice {
                e'8
                f'8
                fs'8
                g'8
            }
            af'8
            a'8
            bf'8
            b'8
        }
        '''
        )

    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[:4])
    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[4:8])
    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[8:])
    assert not Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[:8])
    assert not Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[4:])
    assert not Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True))


def test_Selection__all_are_components_in_same_logical_voice_42():
    r'''Logical voice can not extend across differently named anonymous voices.
    '''

    simultaneous_container = Container(Voice(Note(0, (1, 8)) * 4) * 2)
    simultaneous_container.is_simultaneous = True
    container = Container(Note(0, (1, 8)) * 4)
    container.insert(2, simultaneous_container)
    pitchtools.set_ascending_named_pitches_on_tie_chains_in_expr(
        container)

    assert testtools.compare(
        container,
        r'''
        {
            c'8
            cs'8
            <<
                \new Voice {
                    d'8
                    ef'8
                    e'8
                    f'8
                }
                \new Voice {
                    fs'8
                    g'8
                    af'8
                    a'8
                }
            >>
            bf'8
            b'8
        }
        '''
        )

    outer = (0, 1, 10, 11)

    assert Selection._all_are_components_in_same_logical_voice(
        [container.select_leaves(allow_discontiguous_leaves=True)[i] 
        for i in outer])
    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[2:6])
    assert Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[6:10])
    assert not Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True)[:6])
    assert not Selection._all_are_components_in_same_logical_voice(
        container.select_leaves(allow_discontiguous_leaves=True))
