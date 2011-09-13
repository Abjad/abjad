from abjad import *
import py.test


def test_MetricGridSpanner_01():
    t = Staff(Note(0, (1, 8)) * 8)
    m = spannertools.MetricGridSpanner(t.leaves, [(2, 8)])

    assert t.format == "\\new Staff {\n\t\\time 2/8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n}"

    r'''
    \new Staff {
        \time 2/8
        c'8
        c'8
        c'8
        c'8
        c'8
        c'8
        c'8
        c'8
    }
    '''


def test_MetricGridSpanner_02():
    t = Staff(Note(0, (1,8)) * 8)
    m = spannertools.MetricGridSpanner(t.leaves, [(3, 16)])

    assert t.format == "\\new Staff {\n\t\\time 3/16\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n}"

    r'''
    \new Staff {
        \time 3/16
        c'8
        c'8
        c'8
        c'8
        c'8
        c'8
        c'8
        c'8
    }
    '''


def test_MetricGridSpanner_03():
    '''MetricGrid cycles throught given meters to cover spanner's duration.'''

    t = Staff(Note(0, (1,8)) * 8)
    m = spannertools.MetricGridSpanner(t.leaves, [(1, 8), (1, 4)])

    assert t.format == "\\new Staff {\n\t\\time 1/8\n\tc'8\n\t\\time 1/4\n\tc'8\n\tc'8\n\t\\time 1/8\n\tc'8\n\t\\time 1/4\n\tc'8\n\tc'8\n\t\\time 1/8\n\tc'8\n\t\\time 1/4\n\tc'8\n}"

    r'''
    \new Staff {
        \time 1/8
        c'8
        \time 1/4
        c'8
        c'8
        \time 1/8
        c'8
        \time 1/4
        c'8
        c'8
        \time 1/8
        c'8
        \time 1/4
        c'8
    }
    '''


def test_MetricGridSpanner_04():
    '''MetricGrid knows how to draw itself in the middle of a note. '''

    t = Staff(notetools.make_repeated_notes(8))
    m = spannertools.MetricGridSpanner(t.leaves, [(3, 16), (2, 8)])

    r'''
    \new Staff {
        \time 3/16
        c'8
        <<
        {
            \time 2/8
            s1 * 1/16
        }
        c'8
        >>
        c'8
        <<
        {
            \time 3/16
            s1 * 1/16
        }
        c'8
        >>
        c'8
        \time 2/8
        c'8
        c'8
        \time 3/16
        c'8
    }
    '''

    assert t.format == "\\new Staff {\n\t\\time 3/16\n\tc'8\n\t<<\n\t{\n\t\t\\time 2/8\n\t\ts1 * 1/16\n\t}\n\tc'8\n\t>>\n\tc'8\n\t<<\n\t{\n\t\t\\time 3/16\n\t\ts1 * 1/16\n\t}\n\tc'8\n\t>>\n\tc'8\n\t\\time 2/8\n\tc'8\n\tc'8\n\t\\time 3/16\n\tc'8\n}"


def test_MetricGridSpanner_05():
    '''MetricGrid knows how to draw itself in the middle of a note. '''

    t = Staff(Note(0, (1,2)) * 2)
    m = spannertools.MetricGridSpanner(t.leaves, [(1, 8), (1, 4)])

    r'''
    \new Staff {
        \time 1/8
        <<
        {
            \time 1/4
            s1 * 1/8
        }
        {
            \time 1/8
            s1 * 3/8
        }
        c'2
        >>
        \time 1/4
        <<
        {
            \time 1/8
            s1 * 1/4
        }
        {
            \time 1/4
            s1 * 3/8
        }
        c'2
        >>
    }
    '''


    assert t.format == "\\new Staff {\n\t\\time 1/8\n\t<<\n\t{\n\t\t\\time 1/4\n\t\ts1 * 1/8\n\t}\n\t{\n\t\t\\time 1/8\n\t\ts1 * 3/8\n\t}\n\tc'2\n\t>>\n\t\\time 1/4\n\t<<\n\t{\n\t\t\\time 1/8\n\t\ts1 * 1/4\n\t}\n\t{\n\t\t\\time 1/4\n\t\ts1 * 3/8\n\t}\n\tc'2\n\t>>\n}"
