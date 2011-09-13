from abjad import *


def test_MetricGridSpanner_split_on_bar_01():
    '''MetricGrid splits notes on bar lines.
    '''

    t = Staff(Note(0, (1,8)) * 8)
    m = spannertools.MetricGridSpanner(t.leaves, [(3, 16)])
    m.split_on_bar()

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\t\\time 3/16\n\tc'8\n\tc'16 ~\n\tc'16\n\tc'8\n\tc'8\n\tc'16 ~\n\tc'16\n\tc'8\n\tc'8\n\tc'16 ~\n\tc'16\n}"

    r'''
    \new Staff {
        \time 3/16
        c'8
        c'16 ~
        c'16
        c'8
        c'8
        c'16 ~
        c'16
        c'8
        c'8
        c'16 ~
        c'16
    }
    '''


def test_MetricGridSpanner_split_on_bar_02():
    '''MetricGrid splits notes on bar lines.
    '''

    t = Staff(Note(0, (1,8))*8)
    m = spannertools.MetricGridSpanner(t.leaves, [(3, 16), (2, 8)])
    m.split_on_bar()

    assert t.format == "\\new Staff {\n\t\\time 3/16\n\tc'8\n\tc'16 ~\n\t\\time 2/8\n\tc'16\n\tc'8\n\tc'16 ~\n\t\\time 3/16\n\tc'16\n\tc'8\n\t\\time 2/8\n\tc'8\n\tc'8\n\t\\time 3/16\n\tc'8\n}"

    r'''
    \new Staff {
        \time 3/16
        c'8
        c'16 ~
        \time 2/8
        c'16
        c'8
        c'16 ~
        \time 3/16
        c'16
        c'8
        \time 2/8
        c'8
        c'8
        \time 3/16
        c'8
    }
    '''


def test_MetricGridSpanner_split_on_bar_03():
    '''MetricGrid split works with tuplets.
    '''

    t = Voice([Tuplet(Fraction(2,3), Note(0, (1,8)) * 6)])
    m = spannertools.MetricGridSpanner(t.leaves, [(1, 8)])
    m.split_on_bar()

    assert t.format == "\\new Voice {\n\t\\times 2/3 {\n\t\t\\time 1/8\n\t\tc'8\n\t\tc'16 ~\n\t\tc'16\n\t\tc'8\n\t\tc'8\n\t\tc'16 ~\n\t\tc'16\n\t\tc'8\n\t}\n}"

    r'''
    \new Voice {
        \times 2/3 {
            \time 1/8
            c'8
            c'16 ~
            c'16
            c'8
            c'8
            c'16 ~
            c'16
            c'8
        }
    }
    '''


def test_MetricGridSpanner_split_on_bar_04():
    '''MetricGrid split works with nested tuplets.
    '''

    t = Voice([Tuplet(Fraction(2,3), [Note(0, (1,8)),
            Tuplet(Fraction(3,2), Note(0, (1,8)) *4)])])
    m = spannertools.MetricGridSpanner(t.leaves, [(1, 8)])
    m.split_on_bar()

    assert t.format =="\\new Voice {\n\t\\times 2/3 {\n\t\t\\time 1/8\n\t\tc'8\n\t\t\\fraction \\times 3/2 {\n\t\t\t\\times 2/3 {\n\t\t\t\tc'16 ~\n\t\t\t}\n\t\t\t\\times 2/3 {\n\t\t\t\tc'8\n\t\t\t}\n\t\t\t\\times 2/3 {\n\t\t\t\tc'16 ~\n\t\t\t}\n\t\t\t\\times 2/3 {\n\t\t\t\tc'8\n\t\t\t}\n\t\t\t\\times 2/3 {\n\t\t\t\tc'16 ~\n\t\t\t}\n\t\t\t\\times 2/3 {\n\t\t\t\tc'8\n\t\t\t}\n\t\t\t\\times 2/3 {\n\t\t\t\tc'16 ~\n\t\t\t}\n\t\t\t\\times 2/3 {\n\t\t\t\tc'8\n\t\t\t}\n\t\t}\n\t}\n}"

    r'''
    \new Voice {
        \times 2/3 {
            \time 1/8
            c'8
            \fraction \times 3/2 {
                \times 2/3 {
                    c'16 ~
                }
                \times 2/3 {
                    c'8
                }
                \times 2/3 {
                    c'16 ~
                }
                \times 2/3 {
                    c'8
                }
                \times 2/3 {
                    c'16 ~
                }
                \times 2/3 {
                    c'8
                }
                \times 2/3 {
                    c'16 ~
                }
                \times 2/3 {
                    c'8
                }
            }
        }
    }
    '''


def test_MetricGridSpanner_split_on_bar_05():
    '''MetricGrid can split conditionally.
    '''

    v = Voice([Note(1, (1, 4)), Rest((1, 4)), Note(1, (1, 4))])
    def cond(leaf):
        if not isinstance(leaf, Rest): return True
        else: return False
    m = spannertools.MetricGridSpanner(v.leaves, [(1, 8)])
    m.splitting_condition = cond
    m.split_on_bar()

    assert componenttools.is_well_formed_component(v)
    assert len(v) == 5
    assert v[0].written_duration == v[1].written_duration == Duration(1, 8)
    assert v[3].written_duration == v[3].written_duration == Duration(1, 8)
    assert v[2].written_duration == Duration(1, 4)
    ties = spannertools.get_spanners_attached_to_any_improper_child_of_component(v, tietools.TieSpanner)
    assert len(ties) == 2
