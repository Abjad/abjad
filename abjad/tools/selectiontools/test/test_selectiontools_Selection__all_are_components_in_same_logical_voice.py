# -*- coding: utf-8 -*-
from abjad import *
Component = scoretools.Component
Selection = selectiontools.Selection
selector = select().by_leaf(flatten=True)


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_01():
    r'''Unincorporated leaves do not share a logical voice.
    Unicorporated leaves do not share a root component.
    False if not allow orphans; True if allow orphans.
    '''

    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]
    assert Selection._all_are_components_in_same_logical_voice(notes)
    assert not Selection._all_are_components_in_same_logical_voice(
        notes, allow_orphans=False)


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_02():
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
        select(container).by_class())


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_03():
    r'''Tuplet and leaves all logical voice.
    '''

    tuplet = scoretools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")

    r'''
    \times 2/3 {
        c'8
        d'8
        e'8
    }
    '''

    assert Selection._all_are_components_in_same_logical_voice(
        select(tuplet).by_class())


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_04():
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
        select(voice).by_class())


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_05():
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
        select(staff).by_class())


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_06():
    r'''Voice, sequential and leaves all appear in same logical voice.
    '''

    voice = Voice(r'''
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
        ''')

    assert format(voice) == stringtools.normalize(
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
        select(voice).by_class())


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_07():
    r'''Anonymous voice, tuplets and leaves all appear in same logical voice.
    '''

    voice = Voice(r'''
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
        ''')

    assert format(voice) == stringtools.normalize(
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
        select(voice).by_class())


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_08():
    r'''Logical voice does not extend across anonymous voices.
    '''

    staff = Staff(r'''
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
        ''')

    assert format(staff) == stringtools.normalize(
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

    leaves = selector(staff)
    assert Selection._all_are_components_in_same_logical_voice(leaves[:4])
    assert Selection._all_are_components_in_same_logical_voice(leaves[4:])
    assert not Selection._all_are_components_in_same_logical_voice(leaves)
    assert not Selection._all_are_components_in_same_logical_voice(staff[:])


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_09():
    r'''Logical voice encompasses across like-named voices.
    '''

    staff = Staff(r'''
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
        ''')

    assert format(staff) == stringtools.normalize(
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

    leaves = selector(staff)
    assert Selection._all_are_components_in_same_logical_voice(leaves)


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_10():
    r'''Logical voice does not extend across differently named voices.
    '''

    staff = Staff(r'''
        \context Voice = "foo" {
            c'8
            d'8
        }
        \context Voice = "bar" {
            e'8
            f'8
        }
        ''')

    assert format(staff) == stringtools.normalize(
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

    leaves = selector(staff)
    assert not Selection._all_are_components_in_same_logical_voice(leaves)


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_11():
    r'''Logical voice does not across anonymous voices.
    Logical voice does not extend across anonymous staves.
    '''

    container = Container(r'''
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
        ''')

    assert format(container) == stringtools.normalize(
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

    leaves = selector(container)
    assert not Selection._all_are_components_in_same_logical_voice(leaves)


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_12():
    r'''Logical voice does not extend across anonymous voices.
    Logical voice does not extend across anonymous staves.
    '''

    container = Container(r'''
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
        ''')

    assert format(container) == stringtools.normalize(
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

    leaves = selector(container)
    assert not Selection._all_are_components_in_same_logical_voice(leaves[:4])


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_13():
    r'''Anonymous voice, sequentials and leaves all appear in same
    logical voice.
    '''

    voice = Voice(r'''
        {
            c'8
            d'8
        }
        {
            e'8
            f'8
        }
        ''')

    assert format(voice) == stringtools.normalize(
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

    leaves = selector(voice)
    assert Selection._all_are_components_in_same_logical_voice(leaves)


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_14():
    r'''Logical voice can extend across like-named staves.
    Logical voice can not extend across differently named implicit voices.
    '''

    container = Container(r'''
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
        ''')

    assert format(container) == stringtools.normalize(
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

    leaves = selector(container)
    assert Selection._all_are_components_in_same_logical_voice(leaves[:4])
    assert not Selection._all_are_components_in_same_logical_voice(leaves)


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_15():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    container = Container(r'''
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
        ''')

    assert format(container) == stringtools.normalize(
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

    leaves = selector(container)
    assert Selection._all_are_components_in_same_logical_voice(leaves[:4])
    assert Selection._all_are_components_in_same_logical_voice(leaves[4:])
    assert not Selection._all_are_components_in_same_logical_voice(leaves)


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_16():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    container = Container(r'''
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
        ''')

    assert format(container) == stringtools.normalize(
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

    leaves = selector(container)
    assert Selection._all_are_components_in_same_logical_voice(leaves[:4])
    assert Selection._all_are_components_in_same_logical_voice(leaves[4:])
    assert not Selection._all_are_components_in_same_logical_voice(leaves)


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_17():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    container = Container(r'''
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
        ''')

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

    leaves = selector(container)
    assert Selection._all_are_components_in_same_logical_voice(leaves[:4])
    assert Selection._all_are_components_in_same_logical_voice(leaves[4:])
    assert not Selection._all_are_components_in_same_logical_voice(leaves)


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_18():
    r'''Logical voice can not extend acrossdifferently named implicit voices.
    '''

    container = Container(r'''
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
        ''')

    assert format(container) == stringtools.normalize(
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

    leaves = selector(container)
    assert Selection._all_are_components_in_same_logical_voice(leaves[:4])
    assert Selection._all_are_components_in_same_logical_voice(leaves[4:])
    assert not Selection._all_are_components_in_same_logical_voice(leaves)


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_19():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    container = Container(r'''
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
        ''')

    assert format(container) == stringtools.normalize(
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

    leaves = selector(container)
    assert Selection._all_are_components_in_same_logical_voice(leaves[:4])
    assert Selection._all_are_components_in_same_logical_voice(leaves[4:])
    assert not Selection._all_are_components_in_same_logical_voice(leaves)


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_20():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    container = Container(r'''
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
        ''')

    assert format(container) == stringtools.normalize(
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

    leaves = selector(container)
    assert Selection._all_are_components_in_same_logical_voice(leaves[:4])
    assert Selection._all_are_components_in_same_logical_voice(leaves[4:])
    assert not Selection._all_are_components_in_same_logical_voice(leaves)


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_21():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    container = Container(r'''
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
        ''')

    assert format(container) == stringtools.normalize(
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

    leaves = selector(container)
    assert Selection._all_are_components_in_same_logical_voice(leaves[:4])
    assert Selection._all_are_components_in_same_logical_voice(leaves[4:])
    assert not Selection._all_are_components_in_same_logical_voice(leaves)


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_22():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    container = Container(r'''
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
        ''')

    assert format(container) == stringtools.normalize(
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

    leaves = selector(container)
    assert Selection._all_are_components_in_same_logical_voice(leaves[:4])
    assert Selection._all_are_components_in_same_logical_voice(leaves[4:])
    assert not Selection._all_are_components_in_same_logical_voice(leaves)


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_23():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    container = Container(r'''
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
        ''')

    assert format(container) == stringtools.normalize(
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

    leaves = selector(container)
    assert Selection._all_are_components_in_same_logical_voice(leaves[:4])
    assert Selection._all_are_components_in_same_logical_voice(leaves[4:])
    assert not Selection._all_are_components_in_same_logical_voice(leaves)


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_24():
    r'''Logical voice can not extend across differently named implicit voices.
    NOTE: THIS IS THE LILYPOND LACUNA.
    LilyPond *does* extend logical voice in this case.
    Abjad does not.
    '''

    container = Container(r'''
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
        ''')

    assert format(container) == stringtools.normalize(
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

    leaves = selector(container)
    assert Selection._all_are_components_in_same_logical_voice(leaves[:4])
    assert Selection._all_are_components_in_same_logical_voice(leaves[4:])
    assert not Selection._all_are_components_in_same_logical_voice(leaves)


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_25():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    container = Container(r'''
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
        ''')

    assert format(container) == stringtools.normalize(
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

    leaves = selector(container)
    assert Selection._all_are_components_in_same_logical_voice(leaves[:4])
    assert Selection._all_are_components_in_same_logical_voice(leaves[4:])
    assert not Selection._all_are_components_in_same_logical_voice(leaves)


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_26():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    container = Container(r'''
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
        ''')

    assert format(container) == stringtools.normalize(
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

    leaves = selector(container)
    assert Selection._all_are_components_in_same_logical_voice(leaves[:4])
    assert Selection._all_are_components_in_same_logical_voice(leaves[4:])
    assert not Selection._all_are_components_in_same_logical_voice(leaves)


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_27():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    voice = Voice([Note(n, (1, 8)) for n in range(4)])
    container = Container([voice])
    notes = [Note(n, (1, 8)) for n in range(4, 8)]
    container = Container([container] + notes)

    assert format(container) == stringtools.normalize(
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

    leaves = selector(container)
    assert Selection._all_are_components_in_same_logical_voice(leaves[:4])
    assert Selection._all_are_components_in_same_logical_voice(leaves[4:])
    assert not Selection._all_are_components_in_same_logical_voice(leaves)


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_28():
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

    leaves = selector(container)
    assert Selection._all_are_components_in_same_logical_voice(leaves[:4])
    assert Selection._all_are_components_in_same_logical_voice(leaves[4:])
    assert not Selection._all_are_components_in_same_logical_voice(leaves)


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_29():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    voice_1 = Voice([Note(n, (1, 8)) for n in range(4)])
    voice_1.name = 'foo'
    voice_2 = Voice([voice_1])
    voice_2.name = 'bar'
    notes = [Note(n, (1, 8)) for n in range(4, 8)]
    container = Container([voice_2] + notes)

    assert format(container) == stringtools.normalize(
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

    leaves = selector(container)
    assert Selection._all_are_components_in_same_logical_voice(leaves[:4])
    assert Selection._all_are_components_in_same_logical_voice(leaves[4:])
    assert not Selection._all_are_components_in_same_logical_voice(leaves)


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_30():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    voice_1 = Voice([Note(n, (1, 8)) for n in range(4)])
    voice_2 = Voice([voice_1])
    notes = [Note(n, (1, 8)) for n in range(4, 8)]
    container = Container([voice_2] + notes)

    assert format(container) == stringtools.normalize(
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

    leaves = selector(container)
    assert Selection._all_are_components_in_same_logical_voice(leaves[:4])
    assert Selection._all_are_components_in_same_logical_voice(leaves[4:])
    assert not Selection._all_are_components_in_same_logical_voice(leaves)


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_31():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    notes = [Note(n, (1, 8)) for n in range(4)]
    voice_1 = Voice(Note(12, (1, 8)) * 4)
    voice_2 = Voice(Note(0, (1, 8)) * 4)
    container = Container([voice_1, voice_2])
    container.is_simultaneous = True
    container = Container(notes + [container])

    assert format(container) == stringtools.normalize(
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

    leaves = selector(container)
    assert not Selection._all_are_components_in_same_logical_voice(leaves[:8])
    assert not Selection._all_are_components_in_same_logical_voice(leaves[4:])


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_32():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    container = Container(r'''
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
        ''')

    assert format(container) == stringtools.normalize(
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

    leaves = selector(container)
    assert not Selection._all_are_components_in_same_logical_voice(leaves[:8])
    assert not Selection._all_are_components_in_same_logical_voice(leaves[4:])


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_33():
    r'''Logical voice does extend across gaps.
    Logical voice can not extend across differently named voices.
    '''

    container = Container(r'''
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
        ''')

    outer = (0, 1, 10, 11)
    middle = (2, 3, 8, 9)
    inner = (4, 5, 6, 7)

    assert format(container) == stringtools.normalize(
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

    leaves = selector(container)
    assert Selection._all_are_components_in_same_logical_voice(
        [leaves[i] for i in outer])
    assert Selection._all_are_components_in_same_logical_voice(
        [leaves[i] for i in middle])
    assert Selection._all_are_components_in_same_logical_voice(
        [leaves[i] for i in inner])
    assert not Selection._all_are_components_in_same_logical_voice(leaves[:4])


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_34():
    r'''Logical voice does extend across gaps.
    Logical voice can not extend across differently named implicit voices.
    '''

    staff = Staff(r'''
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
        ''')

    outer = (0, 1, 10, 11)
    middle = (2, 3, 8, 9)
    inner = (4, 5, 6, 7)

    assert format(staff) == stringtools.normalize(
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

    leaves = selector(staff)
    assert Selection._all_are_components_in_same_logical_voice(
        [leaves[i] for i in outer])
    assert Selection._all_are_components_in_same_logical_voice(
        [leaves[i] for i in middle])
    assert Selection._all_are_components_in_same_logical_voice(
        [leaves[i] for i in inner])
    assert not Selection._all_are_components_in_same_logical_voice(leaves[:4])


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_35():
    r'''Containers and leaves all appear in same logical voice.
    '''

    container = Container(r'''
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
        ''')

    assert format(container) == stringtools.normalize(
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
        select(container).by_class())


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_36():
    r'''Tuplets and leaves all appear in same logical voice.
    '''

    a = scoretools.FixedDurationTuplet(
        Duration(3, 8), "e'8 f'8 fs'8 g'8")
    b = scoretools.FixedDurationTuplet(
        Duration(3, 8), "d'8 ef'8 af'8 a'8")
    t = scoretools.FixedDurationTuplet(
        Duration(3, 8), "c'8 cs'8 bf'8 b'8")
    b.insert(2, a)
    t.insert(2, b)
    b.target_duration = Duration(6, 8)
    t.target_duration = Duration(9, 8)

    assert format(t) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 9/10 {
            c'8
            cs'8
            \tweak text #tuplet-number::calc-fraction-text
            \times 6/7 {
                d'8
                ef'8
                \tweak text #tuplet-number::calc-fraction-text
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
        select(t).by_class())


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_37():
    r'''Logical voice can not extend across differently named voices.
    '''

    container = Container(r'''
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
        ''')

    assert format(container) == stringtools.normalize(
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

    leaves = selector(container)
    assert Selection._all_are_components_in_same_logical_voice(
        [leaves[i] for i in outer])
    assert Selection._all_are_components_in_same_logical_voice(
        [leaves[i] for i in inner])
    assert not Selection._all_are_components_in_same_logical_voice(leaves)


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_38():
    r'''Logical voice does not extend over differently named voices.
    '''

    container = Container(r'''
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
        ''')

    assert format(container) == stringtools.normalize(
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

    leaves = selector(container)
    assert Selection._all_are_components_in_same_logical_voice(leaves[:4])
    assert Selection._all_are_components_in_same_logical_voice(leaves[4:])
    assert not Selection._all_are_components_in_same_logical_voice(leaves)


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_39():
    r'''Can not nest across differently named implicit voices.
    '''

    container = Voice(
        r'''
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
        ''')

    assert format(container) == stringtools.normalize(
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

    leaves = selector(container)
    assert Selection._all_are_components_in_same_logical_voice(
        [leaves[i] for i in outer])
    assert Selection._all_are_components_in_same_logical_voice(
        [leaves[i] for i in inner])
    assert not Selection._all_are_components_in_same_logical_voice(leaves)


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_40():
    r'''Logical voice can not extend across differently named voices.
    '''

    voice = Voice(r'''
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
        ''')
    voice.name = 'foo'

    assert format(voice) == stringtools.normalize(
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

    leaves = selector(voice)
    assert Selection._all_are_components_in_same_logical_voice(
        [leaves[i] for i in outer])
    assert Selection._all_are_components_in_same_logical_voice(
        [leaves[i] for i in inner])
    assert not Selection._all_are_components_in_same_logical_voice(leaves)


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_41():
    r'''Logical voice can not extend across differently named anonymous voices.
    '''

    container = Container(r'''
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
        ''')

    assert format(container) == stringtools.normalize(
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

    leaves = selector(container)
    assert Selection._all_are_components_in_same_logical_voice(leaves[:4])
    assert Selection._all_are_components_in_same_logical_voice(leaves[4:8])
    assert Selection._all_are_components_in_same_logical_voice(leaves[8:])
    assert not Selection._all_are_components_in_same_logical_voice(leaves[:8])
    assert not Selection._all_are_components_in_same_logical_voice(leaves[4:])
    assert not Selection._all_are_components_in_same_logical_voice(leaves)


def test_selectiontools_Selection__all_are_components_in_same_logical_voice_42():
    r'''Logical voice can not extend across differently named anonymous voices.
    '''

    container = Container(r'''
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
        ''')

    assert format(container) == stringtools.normalize(
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

    leaves = selector(container)
    assert Selection._all_are_components_in_same_logical_voice(
        [leaves[i] for i in outer])
    assert Selection._all_are_components_in_same_logical_voice(leaves[2:6])
    assert Selection._all_are_components_in_same_logical_voice(leaves[6:10])
    assert not Selection._all_are_components_in_same_logical_voice(leaves[:6])
    assert not Selection._all_are_components_in_same_logical_voice(leaves)
