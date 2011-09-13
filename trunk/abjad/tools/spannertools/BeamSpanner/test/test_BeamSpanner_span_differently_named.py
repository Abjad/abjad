from abjad import *
import py.test


def test_BeamSpanner_span_differently_named_01():
    '''Abjad does NOT let you span across differently named Voices.'''

    v1 = Voice(notetools.make_repeated_notes(4))
    v1.name = 'foo'
    v2 = Voice(notetools.make_repeated_notes(4))
    v2.name = 'bar'
    t = Staff([v1, v2])
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)

    r'''
    \new Staff {
        \context Voice = "foo" {
            c'8
            cs'8
            d'8
            ef'8
        }
        \context Voice = "bar" {
            e'8
            f'8
            fs'8
            g'8
        }
    }
    '''

    assert py.test.raises(AssertionError, 'p = spannertools.BeamSpanner(t)')

    p = spannertools.BeamSpanner(t[0])

    r'''
    \new Staff {
        \context Voice = "foo" {
            c'8 [
            cs'8
            d'8
            ef'8 ]
        }
        \context Voice = "bar" {
            e'8
            f'8
            fs'8
            g'8
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == '\\new Staff {\n\t\\context Voice = "foo" {\n\t\tc\'8 [\n\t\tcs\'8\n\t\td\'8\n\t\tef\'8 ]\n\t}\n\t\\context Voice = "bar" {\n\t\te\'8\n\t\tf\'8\n\t\tfs\'8\n\t\tg\'8\n\t}\n}'


def test_BeamSpanner_span_differently_named_02():
    '''Abjad does NOT let you span across Staves, even if they and
    all its sub-contexts are equally named.'''

    t = Container(Staff(Voice(notetools.make_repeated_notes(4)) * 2) * 2)
    t[0].is_parallel = True
    t[1].is_parallel = True
    t[0].name, t[1].name = 'foo', 'foo'
    t[0][0].name, t[1][0].name = 'first', 'first'
    t[0][1].name, t[1][1].name = 'second', 'second'
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)

    r'''
    {
        \context Staff = "foo" <<
            \context Voice = "first" {
                c'8
                cs'8
                d'8
                ef'8
            }
            \context Voice = "second" {
                e'8
                f'8
                fs'8
                g'8
            }
        >>
        \context Staff = "foo" <<
            \context Voice = "first" {
                af'8
                a'8
                bf'8
                b'8
            }
            \context Voice = "second" {
                c''8
                cs''8
                d''8
                ef''8
            }
        >>
    }
    '''

    assert py.test.raises(AssertionError, 'p = spannertools.BeamSpanner([t[0][0], t[1][0]])')
