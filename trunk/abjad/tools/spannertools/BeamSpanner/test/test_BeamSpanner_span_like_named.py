from abjad import *
import py.test


def test_BeamSpanner_span_like_named_01():
    '''Abjad lets you span liked named voices.'''

    t = Staff(Voice(notetools.make_repeated_notes(4)) * 2)
    t[0].name = 'foo'
    t[1].name = 'foo'
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)

    p = spannertools.BeamSpanner(t)
    assert len(p.components) == 1
    assert isinstance(p.components[0], Staff)
    assert len(p.leaves) == 8
    assert t.format == '\\new Staff {\n\t\\context Voice = "foo" {\n\t\tc\'8 [\n\t\tcs\'8\n\t\td\'8\n\t\tef\'8\n\t}\n\t\\context Voice = "foo" {\n\t\te\'8\n\t\tf\'8\n\t\tfs\'8\n\t\tg\'8 ]\n\t}\n}'
    p.clear()

    p = spannertools.BeamSpanner(t[:])
    assert len(p.components) == 2
    for x in p.components:
        assert isinstance(x, Voice)
    assert len(p.leaves) == 8
    assert t.format == '\\new Staff {\n\t\\context Voice = "foo" {\n\t\tc\'8 [\n\t\tcs\'8\n\t\td\'8\n\t\tef\'8\n\t}\n\t\\context Voice = "foo" {\n\t\te\'8\n\t\tf\'8\n\t\tfs\'8\n\t\tg\'8 ]\n\t}\n}'

    r'''
    \new Staff {
        \context Voice = "foo" {
            c'8 [
            cs'8
            d'8
            ef'8
        }
        \context Voice = "foo" {
            e'8
            f'8
            fs'8
            g'8 ]
        }
    }
    '''


def test_BeamSpanner_span_like_named_02():
    '''
    Abjad does NOT lets you span over liked named staves.
    '''

    t = Container(Staff([Voice(notetools.make_repeated_notes(4))]) * 2)
    t[0].name, t[1].name = 'foo', 'foo'
    t[0][0].name, t[1][0].name = 'bar', 'bar'
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)

    assert py.test.raises(AssertionError, 'p = spannertools.BeamSpanner(t)')

    assert py.test.raises(AssertionError, 'p = spannertools.BeamSpanner(t[:])')

    assert py.test.raises(AssertionError, 'p = spannertools.BeamSpanner([t[0][0], t[1][0]])')


def test_BeamSpanner_span_like_named_03():
    '''
    Like-named containers need not be lexically contiguous.
    '''

    t = Container(Container(Voice(notetools.make_repeated_notes(4)) * 2) * 2)
    t[0].is_parallel = True
    t[1].is_parallel = True
    t[0][0].name, t[1][1].name = 'first', 'first'
    t[0][1].name, t[1][0].name = 'second', 'second'
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)

    p = spannertools.BeamSpanner([t[0][0], t[1][1]])
    assert len(p.components) == 2
    assert isinstance(p.components[0], Voice)
    assert isinstance(p.components[1], Voice)
    assert len(p.leaves) == 8
    p.clear()

    r'''
    {
        <<
            \context Voice = "first" {
                c'8 [
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
        <<
            \context Voice = "second" {
                af'8
                a'8
                bf'8
                b'8
            }
            \context Voice = "first" {
                c''8
                cs''8
                d''8
                ef''8 ]
            }
        >>
    }
    '''


def test_BeamSpanner_span_like_named_04():
    '''
    Asymmetric structures are no problem.
    '''

    t = Container(Container(Voice(notetools.make_repeated_notes(4)) * 2) * 2)
    t[0].is_parallel = True
    t[1].is_parallel = True
    t[0][0].name, t[1][0].name = 'first', 'first'
    t[0][1].name, t[1][1].name = 'second', 'second'
    del(t[1][1])
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)
    p = spannertools.BeamSpanner([t[0][0], t[1][0]])

    assert len(p.components) == 2
    assert len(p.leaves) == 8

    assert t.format == '{\n\t<<\n\t\t\\context Voice = "first" {\n\t\t\tc\'8 [\n\t\t\tcs\'8\n\t\t\td\'8\n\t\t\tef\'8\n\t\t}\n\t\t\\context Voice = "second" {\n\t\t\te\'8\n\t\t\tf\'8\n\t\t\tfs\'8\n\t\t\tg\'8\n\t\t}\n\t>>\n\t<<\n\t\t\\context Voice = "first" {\n\t\t\taf\'8\n\t\t\ta\'8\n\t\t\tbf\'8\n\t\t\tb\'8 ]\n\t\t}\n\t>>\n}'

    r'''
    {
        <<
            \context Voice = "first" {
                c'8 [
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
        <<
            \context Voice = "first" {
                af'8
                a'8
                bf'8
                b'8 ]
            }
        >>
    }
    '''
