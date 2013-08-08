# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_BeamSpanner_span_parallel_container_01():
    r'''Abjad spanners will not inspect the contents of parallel containers.
    '''

    container = Container([])
    container.is_simultaneous = True
    beam = spannertools.BeamSpanner(container)

    assert len(beam.components) == 1
    assert beam.components[0] is container
    assert len(beam.leaves) == 0
    assert testtools.compare(
        container.lilypond_format,
        r'''
        <<
        >>
        '''
        )


def test_BeamSpanner_span_parallel_container_02():
    r'''Nonempty spanned parallel container.
    '''

    container = Container(Voice(notetools.make_repeated_notes(4)) * 2)
    container.is_simultaneous = True
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(container)

    assert py.test.raises(AssertionError, 'beam = spannertools.BeamSpanner(container)')

#   assert len(beam.components) == 1
#   assert beam.components[0] is container
#   assert len(beam.leaves) == 0
#   assert container.lilypond_format == "<<\n\container{\n\container\tc'8\n\container\tcs'8\n\container\td'8\n\container\tef'8\n\container}\n\container{\n\container\te'8\n\container\tf'8\n\container\tfs'8\n\container\tg'8\n\container}\n>>"
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
    r'''Voice accepts spanner,
        even lodged within parallel parent container.'''

    container = Container(Voice(notetools.make_repeated_notes(4)) * 2)
    container.is_simultaneous = True
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(container)
    beam = spannertools.BeamSpanner(container[0])

    assert len(beam.components) == 1
    assert isinstance(beam.components[0], Container)
    assert testtools.compare(
        container.lilypond_format,
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
        )

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
    r'''Abjad forbids but LilyPond is happy.
    '''

    staff = Staff(notetools.make_repeated_notes(4))
    new = Container(Voice(notetools.make_repeated_notes(4)) * 2)
    new.is_simultaneous = True
    staff.insert(2, new)
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(staff)

    assert py.test.raises(AssertionError, 'beam = spannertools.BeamSpanner(staff)')


def test_BeamSpanner_span_parallel_container_05():
    r'''Abjad ignores empty parallel containers with no leaves.
        LilyPond is happy here.'''

    staff = Staff(notetools.make_repeated_notes(4))
    new = Container([])
    new.is_simultaneous = True
    staff.insert(2, new)
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(staff)
    beam = spannertools.BeamSpanner(staff)

    assert len(beam.components) == 1
    assert len(beam.leaves) == 4
    assert testtools.compare(
        staff.lilypond_format,
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
        )

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
    r'''This is the proper way to 'thread through' parallel containers.
        LilyPond is happy here again.'''

    staff = Staff(Voice(notetools.make_repeated_notes(4)) * 2)
    staff[0].name, staff[1].name = 'foo', 'foo'
    new = Container(Voice(notetools.make_repeated_notes(4)) * 2)
    new.is_simultaneous = True
    staff.insert(1, new)
    staff[1][0].name = 'foo'
    staff[1][1].name = 'bar'
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(staff)
    beam = spannertools.BeamSpanner([staff[0], staff[1][0], staff[2]])

    assert len(beam.components) == 3
    assert beam.components[0] is staff[0]
    assert beam.components[1] is staff[1][0]
    assert beam.components[2] is staff[2]
    assert len(beam.leaves) == 12
    assert testtools.compare(
        staff.lilypond_format,
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
        )

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
