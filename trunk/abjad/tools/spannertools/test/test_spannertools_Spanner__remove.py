# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_spannertools_Spanner__remove_01():
    r'''Remove interior component from spanner.
    Remove spanner from component's aggregator.
    Spanner is left discontiguous and score no longer checks.
    Not composer-safe.
    Follow immediately with operation to remove component from score.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner()
    attach(beam, voice[:])

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            d'8
            e'8
            f'8 ]
        }
        '''
        )

    beam._remove(beam.components[1])

    "Spanner is now discontiguous: c'8, e'8, f'8 but no d'8."

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            d'8
            e'8
            f'8 ]
        }
        '''
        )

    assert not inspect(voice).is_well_formed()


def test_spannertools_Spanner__remove_02():
    r'''Remove last component from spanner.
    Remove spanner from component's aggregator.
    Here an end element removes from spanner.
    So spanner is not left discontiguous and score checks.
    Still not composer-safe.
    Note spanner.pop() and spanner.pop_left() are composer-safe.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    beam = spannertools.BeamSpanner()
    attach(beam, voice[:])

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8 ]
            }
        }
        '''
        )

    result = beam._remove(beam.components[2])

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [
                d'8
            }
            {
                e'8
                f'8 ]
            }
            {
                g'8
                a'8
            }
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_spannertools_Spanner__remove_03():
    r'''Remove works only on references and not on equality.
    '''

    class MockSpanner(spannertools.Spanner):
        def __init__(self, components=None):
            spannertools.Spanner.__init__(self, components)
        def _copy_keyword_args(self, new):
            pass

    note = Note("c'4")
    spanner = MockSpanner()
    spanner.attach(Note("c'4"))

    assert py.test.raises(Exception, 'spanner._remove(note)')
