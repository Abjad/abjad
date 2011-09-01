from abjad import *
from abjad.tools.componenttools._Component import _Component
import py.test


def test_componenttools_all_are_components_in_same_thread_01():
    '''Unincorporated leaves do not thread.
    Unicorporated leaves do not share a root component.
    False if not allow orphans; True if allow orphans.
    '''

    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]
    assert componenttools.all_are_components_in_same_thread(notes)
    assert not componenttools.all_are_components_in_same_thread(notes, allow_orphans = False)


def test_componenttools_all_are_components_in_same_thread_02():
    '''Container and leaves all thread.
    '''

    t = Container("c'8 d'8 e'8 f'8")

    r'''
    {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert componenttools.all_are_components_in_same_thread(list(componenttools.iterate_components_forward_in_expr(t, _Component)))


def test_componenttools_all_are_components_in_same_thread_03():
    '''Tuplet and leaves all thread.
    '''

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")

    r'''
    \times 2/3 {
        c'8
        d'8
        e'8
    }
    '''

    assert componenttools.all_are_components_in_same_thread(list(componenttools.iterate_components_forward_in_expr(t, _Component)))


def test_componenttools_all_are_components_in_same_thread_04():
    '''Voice and leaves all thread.
    '''

    t = Voice("c'8 d'8 e'8 f'8")

    r'''
    \new Voice {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert componenttools.all_are_components_in_same_thread(
        list(componenttools.iterate_components_forward_in_expr(t, _Component)))


def test_componenttools_all_are_components_in_same_thread_05():
    '''Anonymous staff and leaves all thread.
    '''

    t = Staff("c'8 d'8 e'8 f'8")

    r'''
    \new Staff {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert componenttools.all_are_components_in_same_thread(list(componenttools.iterate_components_forward_in_expr(t, _Component)))


def test_componenttools_all_are_components_in_same_thread_06():
    '''Voice, sequential and leaves all thread.
    '''

    t = Voice(Container(notetools.make_repeated_notes(4)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

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

    assert componenttools.all_are_components_in_same_thread(
        list(componenttools.iterate_components_forward_in_expr(t, _Component)))


def test_componenttools_all_are_components_in_same_thread_07():
    '''Anonymous voice, tuplets and leaves all thread.
    '''

    t = Voice(tuplettools.FixedDurationTuplet(Duration(2, 8), notetools.make_repeated_notes(3)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

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

    assert componenttools.all_are_components_in_same_thread(list(componenttools.iterate_components_forward_in_expr(t, _Component)))


def test_componenttools_all_are_components_in_same_thread_08():
    '''Can not thread across anonymous voices.
    '''

    t = Staff(Voice(notetools.make_repeated_notes(4)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

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

    assert componenttools.all_are_components_in_same_thread(t.leaves[:4])
    assert componenttools.all_are_components_in_same_thread(t.leaves[4:])
    assert not componenttools.all_are_components_in_same_thread(t.leaves)
    assert not componenttools.all_are_components_in_same_thread(t[:])


def test_componenttools_all_are_components_in_same_thread_09():
    '''Can thread across like-named voices.
    '''

    t = Staff(Voice(notetools.make_repeated_notes(4)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    t[0].name = 'foo'
    t[1].name = 'foo'

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

    assert componenttools.all_are_components_in_same_thread(t.leaves)


def test_componenttools_all_are_components_in_same_thread_10():
    '''Can not thread across differently named voices.
    '''

    t = Staff(Voice(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    t[0].name = 'foo'
    t[1].name = 'bar'

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

    assert not componenttools.all_are_components_in_same_thread(t.leaves)


def test_componenttools_all_are_components_in_same_thread_11():
    '''Can not thread across anonymous voices.
    Can not thread across anonymous staves.
    '''

    t = Container(Staff([Voice(notetools.make_repeated_notes(2))]) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

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

    assert not componenttools.all_are_components_in_same_thread(t.leaves)


def test_componenttools_all_are_components_in_same_thread_12():
    '''Can not thread across anonymous voices.
    Can not thread across anonymous staves.
    '''

    t = Container(Staff(Voice(notetools.make_repeated_notes(2)) * 2) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    t[0].is_parallel = True
    t[1].is_parallel = True

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

    assert not componenttools.all_are_components_in_same_thread(t.leaves[:4])


def test_componenttools_all_are_components_in_same_thread_13():
    '''Anonymous voice, sequentials and leaves all thread.
    '''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

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

    assert componenttools.all_are_components_in_same_thread(t.leaves)


def test_componenttools_all_are_components_in_same_thread_14():
    '''Can thread across like-named staves.
    Can not thread across differently named IMPLICIT voices.
    '''

    t = Container(Staff(Note(0, (1, 8)) * 4) * 2)
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)
    t[0].name = 'foo'
    t[1].name = 'foo'

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

    assert componenttools.all_are_components_in_same_thread(t.leaves[:4])
    assert not componenttools.all_are_components_in_same_thread(t.leaves)


def test_componenttools_all_are_components_in_same_thread_15():
    '''Can not thread across differently named IMPLICIT voices.
    '''

    t = Container([Container(notetools.make_repeated_notes(4)), Voice(notetools.make_repeated_notes(4))])
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

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

    assert componenttools.all_are_components_in_same_thread(t.leaves[:4])
    assert componenttools.all_are_components_in_same_thread(t.leaves[4:])
    assert not componenttools.all_are_components_in_same_thread(t.leaves)


def test_componenttools_all_are_components_in_same_thread_16():
    '''Can not thread across differently named IMPLICIT voices.
    '''

    t = Container([Voice(notetools.make_repeated_notes(4)), Container(notetools.make_repeated_notes(4))])
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

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

    assert componenttools.all_are_components_in_same_thread(t.leaves[:4])
    assert componenttools.all_are_components_in_same_thread(t.leaves[4:])
    assert not componenttools.all_are_components_in_same_thread(t.leaves)


def test_componenttools_all_are_components_in_same_thread_17():
    '''Can not thread across differently named IMPLICIT voices.
    '''

    t = Container([Container(notetools.make_repeated_notes(4)), Voice(notetools.make_repeated_notes(4))])
    t[1].name = 'foo'
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

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

    assert componenttools.all_are_components_in_same_thread(t.leaves[:4])
    assert componenttools.all_are_components_in_same_thread(t.leaves[4:])
    assert not componenttools.all_are_components_in_same_thread(t.leaves)


def test_componenttools_all_are_components_in_same_thread_18():
    '''Can not thread over differently named IMPLICIT voices.
    '''

    t = Container([Voice(notetools.make_repeated_notes(4)), Container(notetools.make_repeated_notes(4))])
    t[0].name = 'foo'
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

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

    assert componenttools.all_are_components_in_same_thread(t.leaves[:4])
    assert componenttools.all_are_components_in_same_thread(t.leaves[4:])
    assert not componenttools.all_are_components_in_same_thread(t.leaves)


def test_componenttools_all_are_components_in_same_thread_19():
    '''Can not thread across differently named IMPLICIT voices.
    '''

    t = Container([Container(notetools.make_repeated_notes(4)), Staff(notetools.make_repeated_notes(4))])
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

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

    assert componenttools.all_are_components_in_same_thread(t.leaves[:4])
    assert componenttools.all_are_components_in_same_thread(t.leaves[4:])
    assert not componenttools.all_are_components_in_same_thread(t.leaves)


def test_componenttools_all_are_components_in_same_thread_20():
    '''Can not thread across differently named IMPLICIT voices.
    '''

    t = Container([Staff(Note(0, (1, 8)) * 4), Container(Note(0, (1, 8)) * 4)])
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)

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

    assert componenttools.all_are_components_in_same_thread(t.leaves[:4])
    assert componenttools.all_are_components_in_same_thread(t.leaves[4:])
    assert not componenttools.all_are_components_in_same_thread(t.leaves)


def test_componenttools_all_are_components_in_same_thread_21():
    '''Can not thread across differently named IMPLICIT voices.
    '''

    t = Container(Note(0, (1, 8)) * 4 + [Voice(Note(0, (1, 8)) * 4)])
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)

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

    assert componenttools.all_are_components_in_same_thread(t.leaves[:4])
    assert componenttools.all_are_components_in_same_thread(t.leaves[4:])
    assert not componenttools.all_are_components_in_same_thread(t.leaves)


def test_componenttools_all_are_components_in_same_thread_22():
    '''Can not thread across differently named IMPLICIT voices.
    '''

    t = Container([Voice(Note(0, (1, 8)) * 4)] + Note(0, (1, 8)) * 4)
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)


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

    assert componenttools.all_are_components_in_same_thread(t.leaves[:4])
    assert componenttools.all_are_components_in_same_thread(t.leaves[4:])
    assert not componenttools.all_are_components_in_same_thread(t.leaves)


def test_componenttools_all_are_components_in_same_thread_23():
    '''Can not thread across differently named IMPLICIT voices.
    '''

    t = Container(Note(0, (1, 8)) * 4 + [Voice(Note(0, (1, 8)) * 4)])
    t[4].name = 'foo'
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)

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

    assert componenttools.all_are_components_in_same_thread(t.leaves[:4])
    assert componenttools.all_are_components_in_same_thread(t.leaves[4:])
    assert not componenttools.all_are_components_in_same_thread(t.leaves)


def test_componenttools_all_are_components_in_same_thread_24():
    '''Can not thread across differently named IMPLICIT voices.
    NOTE: THIS IS THE LILYPOND LACUNA.
    LilyPond *does* thread in this case.
    Abjad does not.
    '''

    t = Container([Voice(Note(0, (1, 8)) * 4)] + Note(0, (1, 8)) * 4)
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)
    t[0].name = 'foo'

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

    assert componenttools.all_are_components_in_same_thread(t.leaves[:4])
    assert componenttools.all_are_components_in_same_thread(t.leaves[4:])
    assert not componenttools.all_are_components_in_same_thread(t.leaves)


def test_componenttools_all_are_components_in_same_thread_25():
    '''Can not thread across differently named IMPLICIT voices.
    '''

    t = Container(Note(0, (1, 8)) * 4 + [Voice(Note(0, (1, 8)) * 4)])
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)

    r'''
    {
        c'8
        cs'8
        d'8
        ef'8
        \new Staff {
            e'8
            f'8
            fs'8
            g'8
        }
    }
    '''

    assert componenttools.all_are_components_in_same_thread(t.leaves[:4])
    assert componenttools.all_are_components_in_same_thread(t.leaves[4:])
    assert not componenttools.all_are_components_in_same_thread(t.leaves)


def test_componenttools_all_are_components_in_same_thread_26():
    '''Can not thread across differently named IMPLICIT voices.
    '''

    t = Container(notetools.make_repeated_notes(4))
    t.insert(0, Staff(notetools.make_repeated_notes(4)))
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

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

    assert componenttools.all_are_components_in_same_thread(t.leaves[:4])
    assert componenttools.all_are_components_in_same_thread(t.leaves[4:])
    assert not componenttools.all_are_components_in_same_thread(t.leaves)


def test_componenttools_all_are_components_in_same_thread_27():
    '''Can not thread across differently named IMPLICIT voices.
    '''

    v = Voice([Note(n, (1, 8)) for n in range(4)])
    q = Container([v])
    notes = [Note(n, (1, 8)) for n in range(4, 8)]
    t = Container([q] + notes)

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

    assert componenttools.all_are_components_in_same_thread(t.leaves[:4])
    assert componenttools.all_are_components_in_same_thread(t.leaves[4:])
    assert not componenttools.all_are_components_in_same_thread(t.leaves)


def test_componenttools_all_are_components_in_same_thread_28():
    '''Can not thread across differently named IMPLICIT voices.
    '''

    v = Voice([Note(n, (1, 8)) for n in range(4)])
    v.name = 'foo'
    q = Container([v])
    notes = [Note(n, (1, 8)) for n in range(4, 8)]
    t = Container([q] + notes)

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

    assert componenttools.all_are_components_in_same_thread(t.leaves[:4])
    assert componenttools.all_are_components_in_same_thread(t.leaves[4:])
    assert not componenttools.all_are_components_in_same_thread(t.leaves)


def test_componenttools_all_are_components_in_same_thread_29():
    '''Can not thread across differently named IMPLICIT voices.
    '''

    v1 = Voice([Note(n, (1, 8)) for n in range(4)])
    v1.name = 'foo'
    v2 = Voice([v1])
    v2.name = 'bar'
    notes = [Note(n, (1, 8)) for n in range(4, 8)]
    t = Container([v2] + notes)

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

    assert componenttools.all_are_components_in_same_thread(t.leaves[:4])
    assert componenttools.all_are_components_in_same_thread(t.leaves[4:])
    assert not componenttools.all_are_components_in_same_thread(t.leaves)


def test_componenttools_all_are_components_in_same_thread_30():
    '''Can not thread across differently named IMPLICIT voices.
    '''

    v1 = Voice([Note(n, (1, 8)) for n in range(4)])
    v2 = Voice([v1])
    notes = [Note(n, (1, 8)) for n in range(4, 8)]
    t = Container([v2] + notes)

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

    assert componenttools.all_are_components_in_same_thread(t.leaves[:4])
    assert componenttools.all_are_components_in_same_thread(t.leaves[4:])
    assert not componenttools.all_are_components_in_same_thread(t.leaves)


def test_componenttools_all_are_components_in_same_thread_31():
    '''Can not thread across differently named IMPLICIT voices.
    '''

    notes = [Note(n, (1, 8)) for n in range(4)]
    vtop = Voice(Note(12, (1, 8)) * 4)
    vbottom = Voice(Note(0, (1, 8)) * 4)
    p = Container([vtop, vbottom])
    p.is_parallel = True
    t = Container(notes + [p])

    r'''
    {
        c'8
        cs'8
        d'8
        ef'8
        <<
            \new Voice {
                af'8
                a'8
                bf'8
                b'8
            }
            \new Voice {
                e'8
                f'8
                fs'8
                g'8
            }
        >>
    }
    '''

    assert not componenttools.all_are_components_in_same_thread(t.leaves[:8])
    assert not componenttools.all_are_components_in_same_thread(t.leaves[4:])


def test_componenttools_all_are_components_in_same_thread_32():
    '''Can not thread across differently named IMPLICIT voices.
    '''

    t = Container([Container(Voice(Note(0, (1, 8)) * 4) * 2)] + Note(0, (1, 8)) * 4)
    t[0].is_parallel = True
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)

    r'''
    {
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
        c'8
        cs'8
        d'8
        ef'8
    }
    '''

    assert not componenttools.all_are_components_in_same_thread(t.leaves[:8])
    assert not componenttools.all_are_components_in_same_thread(t.leaves[4:])


def test_componenttools_all_are_components_in_same_thread_33():
    '''Can thread across gaps.
    Can not thread across differently named voices.
    '''

    t = Container(Note(0, (1, 8)) * 4)
    a, b = Voice(Note(0, (1, 8)) * 4) * 2
    a.insert(2, b)
    t.insert(2, a)
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)

    outer = (0, 1, 10, 11)
    middle = (2, 3, 8, 9)
    inner = (4, 5, 6, 7)

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

    assert componenttools.all_are_components_in_same_thread([t.leaves[i] for i in outer])
    assert componenttools.all_are_components_in_same_thread([t.leaves[i] for i in middle])
    assert componenttools.all_are_components_in_same_thread([t.leaves[i] for i in inner])
    assert not componenttools.all_are_components_in_same_thread(t.leaves[:4])


def test_componenttools_all_are_components_in_same_thread_34():
    '''Can thread across gaps.
    Can not thread across differently named IMPLICIT voices.
    '''

    t = Staff(Note(0, (1, 8)) * 4)
    a, b = t * 2
    a.insert(2, b)
    t.insert(2, a)
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)

    outer = (0, 1, 10, 11)
    middle = (2, 3, 8, 9)
    inner = (4, 5, 6, 7)

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

    assert componenttools.all_are_components_in_same_thread([t.leaves[i] for i in outer])
    assert componenttools.all_are_components_in_same_thread([t.leaves[i] for i in middle])
    assert componenttools.all_are_components_in_same_thread([t.leaves[i] for i in inner])
    assert not componenttools.all_are_components_in_same_thread(t.leaves[:4])


def test_componenttools_all_are_components_in_same_thread_35():
    '''Containers and leaves all thread.
    '''

    a, b, t = Container(Note(0, (1, 8)) * 4) * 3
    a.insert(2, b)
    t.insert(2, a)
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)

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

    assert componenttools.all_are_components_in_same_thread(list(componenttools.iterate_components_forward_in_expr(t, _Component)))


def test_componenttools_all_are_components_in_same_thread_36():
    '''Tuplets and leaves all thread.
    '''

    a, b, t = tuplettools.FixedDurationTuplet(Duration(3, 8), Note(0, (1, 8)) * 4) * 3
    b.insert(2, a)
    t.insert(2, b)
    b.target_duration = Duration(6, 8)
    t.target_duration = Duration(9, 8)
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)

    r'''
    \fraction \times 9/10 {
        c'8
        cs'8
        \fraction \times 6/7 {
            d'8
            ef'8
            \fraction \times 3/4 {
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

    assert componenttools.all_are_components_in_same_thread(list(componenttools.iterate_components_forward_in_expr(t, _Component)))


def test_componenttools_all_are_components_in_same_thread_37():
    '''Can not thread across differently named voices.
    '''

    t = Container(Note(0, (1, 8)) * 4)
    t.insert(2, Container([Container([Voice(Note(0, (1, 8)) * 4)])]))
    t[2][0][0].name = 'foo'
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)

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

    outer = (0, 1, 6, 7)
    inner = (2, 3, 4, 5)

    assert componenttools.all_are_components_in_same_thread([t.leaves[i] for i in outer])
    assert componenttools.all_are_components_in_same_thread([t.leaves[i] for i in inner])
    assert not componenttools.all_are_components_in_same_thread(t.leaves)


def test_componenttools_all_are_components_in_same_thread_38():
    '''Can not thread over differently named voices.
    '''

    t = Container(Note(0, (1, 8)) * 4)
    t.insert(0, Container([Container([Voice(Note(0, (1, 8)) * 4)])]))
    t[0][0][0].name = 'foo'
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)

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

    assert componenttools.all_are_components_in_same_thread(t.leaves[:4])
    assert componenttools.all_are_components_in_same_thread(t.leaves[4:])
    assert not componenttools.all_are_components_in_same_thread(t.leaves)


def test_componenttools_all_are_components_in_same_thread_39():
    '''Can not nest across differently named implicit voices.
    '''

    t = Container(Note(0, (1, 8)) * 4)
    t.insert(2, Voice(Note(0, (1, 8)) * 4))
    t = Container([t])
    t = Container([t])
    t = Voice([t])
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)

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

    outer = (0, 1, 6, 7)
    inner = (2, 3, 4, 5)

    assert componenttools.all_are_components_in_same_thread([t.leaves[i] for i in outer])
    assert componenttools.all_are_components_in_same_thread([t.leaves[i] for i in inner])
    assert not componenttools.all_are_components_in_same_thread(t.leaves)


def test_componenttools_all_are_components_in_same_thread_40():
    '''Can not thread across differently named voices.
    '''

    v = Voice(Note(0, (1, 8)) * 4)
    v.name = 'bar'
    q = Container(Note(0, (1, 8)) * 4)
    q.insert(2, v)
    qq = Container(Note(0, (1, 8)) * 4)
    qq.insert(2, q)
    t = Voice(Note(0, (1, 8)) * 4)
    t.insert(2, qq)
    t.name = 'foo'
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)

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

    outer = (0, 1, 2, 3, 4, 5, 10, 11, 12, 13, 14, 15)
    inner = (6, 7, 8, 9)

    assert componenttools.all_are_components_in_same_thread([t.leaves[i] for i in outer])
    assert componenttools.all_are_components_in_same_thread([t.leaves[i] for i in inner])
    assert not componenttools.all_are_components_in_same_thread(t.leaves)


def test_componenttools_all_are_components_in_same_thread_41():
    '''Can not thread across differently named anonymous voices.
    '''

    t = Container(notetools.make_repeated_notes(4))
    t[0:0] = Voice(notetools.make_repeated_notes(4)) * 2
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)

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

    assert componenttools.all_are_components_in_same_thread(t.leaves[:4])
    assert componenttools.all_are_components_in_same_thread(t.leaves[4:8])
    assert componenttools.all_are_components_in_same_thread(t.leaves[8:])
    assert not componenttools.all_are_components_in_same_thread(t.leaves[:8])
    assert not componenttools.all_are_components_in_same_thread(t.leaves[4:])
    assert not componenttools.all_are_components_in_same_thread(t.leaves)


def test_componenttools_all_are_components_in_same_thread_42():
    '''Can not thread across differently named anonymous voices.
    '''

    p = Container(Voice(Note(0, (1, 8)) * 4) * 2)
    p.is_parallel = True
    t = Container(Note(0, (1, 8)) * 4)
    t.insert(2, p)
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)

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

    outer = (0, 1, 10, 11)

    assert componenttools.all_are_components_in_same_thread([t.leaves[i] for i in outer])
    assert componenttools.all_are_components_in_same_thread(t.leaves[2:6])
    assert componenttools.all_are_components_in_same_thread(t.leaves[6:10])
    assert not componenttools.all_are_components_in_same_thread(t.leaves[:6])
    assert not componenttools.all_are_components_in_same_thread(t.leaves)
