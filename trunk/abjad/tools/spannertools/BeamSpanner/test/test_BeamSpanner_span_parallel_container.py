from abjad import *
import py.test


def test_BeamSpanner_span_parallel_container_01():
    '''Abjad spanners will not inspect the contents of parallel containers.'''

    t = Container([])
    t.is_parallel = True
    p = spannertools.BeamSpanner(t)

    assert len(p.components) == 1
    assert p.components[0] is t
    assert len(p.leaves) == 0
    assert t.format == '<<\n>>'


def test_BeamSpanner_span_parallel_container_02():
    '''Nonempty spanned parallel container.'''

    t = Container(Voice(notetools.make_repeated_notes(4)) * 2)
    t.is_parallel = True
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)

    assert py.test.raises(AssertionError, 'p = spannertools.BeamSpanner(t)')

#   assert len(p.components) == 1
#   assert p.components[0] is t
#   assert len(p.leaves) == 0
#   assert t.format == "<<\n\t{\n\t\tc'8\n\t\tcs'8\n\t\td'8\n\t\tef'8\n\t}\n\t{\n\t\te'8\n\t\tf'8\n\t\tfs'8\n\t\tg'8\n\t}\n>>"
#
#   r'''<<
#      {
#         c'8
#         cs'8
#         d'8
#         ef'8
#      }
#      {
#         e'8
#         f'8
#         fs'8
#         g'8
#      }
#   >>'''


def test_BeamSpanner_span_parallel_container_03():
    '''Voice accepts spanner,
        even lodged within parallel parent container.'''

    t = Container(Voice(notetools.make_repeated_notes(4)) * 2)
    t.is_parallel = True
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)
    p = spannertools.BeamSpanner(t[0])

    assert len(p.components) == 1
    assert isinstance(p.components[0], Container)
    assert t.format == "<<\n\t\\new Voice {\n\t\tc'8 [\n\t\tcs'8\n\t\td'8\n\t\tef'8 ]\n\t}\n\t\\new Voice {\n\t\te'8\n\t\tf'8\n\t\tfs'8\n\t\tg'8\n\t}\n>>"

    r'''
    <<
        \new Voice {
            c'8 [
            cs'8
            d'8
            ef'8 ]
        }
        \new Voice {
            e'8
            f'8
            fs'8
            g'8
        }
    >>
    '''

def test_BeamSpanner_span_parallel_container_04():
    '''Abjad forbids but LilyPond is happy.'''

    t = Staff(notetools.make_repeated_notes(4))
    new = Container(Voice(notetools.make_repeated_notes(4)) * 2)
    new.is_parallel = True
    t.insert(2, new)
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)

    assert py.test.raises(AssertionError, 'p = spannertools.BeamSpanner(t)')


def test_BeamSpanner_span_parallel_container_05():
    '''Abjad ignores empty parallel containers with no leaves.
        LilyPond is happy here.'''

    t = Staff(notetools.make_repeated_notes(4))
    new = Container([])
    new.is_parallel = True
    t.insert(2, new)
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)
    p = spannertools.BeamSpanner(t)

    assert len(p.components) == 1
    assert len(p.leaves) == 4
    assert t.format == "\\new Staff {\n\tc'8 [\n\tcs'8\n\t<<\n\t>>\n\td'8\n\tef'8 ]\n}"

    r'''
    \new Staff {
        c'8 [
        cs'8
        <<
        >>
        d'8
        ef'8 ]
    }
    '''


def test_BeamSpanner_span_parallel_container_06():
    '''This is the proper way to 'thread through' parallel containers.
        LilyPond is happy here again.'''

    t = Staff(Voice(notetools.make_repeated_notes(4)) * 2)
    t[0].name, t[1].name = 'foo', 'foo'
    new = Container(Voice(notetools.make_repeated_notes(4)) * 2)
    new.is_parallel = True
    t.insert(1, new)
    t[1][0].name = 'foo'
    t[1][1].name = 'bar'
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)
    p = spannertools.BeamSpanner([t[0], t[1][0], t[2]])

    assert len(p.components) == 3
    assert p.components[0] is t[0]
    assert p.components[1] is t[1][0]
    assert p.components[2] is t[2]
    assert len(p.leaves) == 12
    assert t.format == '\\new Staff {\n\t\\context Voice = "foo" {\n\t\tc\'8 [\n\t\tcs\'8\n\t\td\'8\n\t\tef\'8\n\t}\n\t<<\n\t\t\\context Voice = "foo" {\n\t\t\te\'8\n\t\t\tf\'8\n\t\t\tfs\'8\n\t\t\tg\'8\n\t\t}\n\t\t\\context Voice = "bar" {\n\t\t\taf\'8\n\t\t\ta\'8\n\t\t\tbf\'8\n\t\t\tb\'8\n\t\t}\n\t>>\n\t\\context Voice = "foo" {\n\t\tc\'\'8\n\t\tcs\'\'8\n\t\td\'\'8\n\t\tef\'\'8 ]\n\t}\n}'

    r'''
    \new Staff {
        \context Voice = "foo" {
            c'8 [
            cs'8
            d'8
            ef'8
        }
        <<
            \context Voice = "foo" {
                e'8
                f'8
                fs'8
                g'8
            }
            \context Voice = "bar" {
                af'8
                a'8
                bf'8
                b'8
            }
        >>
        \context Voice = "foo" {
            c''8
            cs''8
            d''8
            ef''8 ]
        }
    }
    '''
