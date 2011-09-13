from abjad import *
import py.test


def test_BeamSpanner_span_anonymous_01():
    '''Spanned empty sequential container;
        container formats no beam indications.'''

    t = Container([])
    p = spannertools.BeamSpanner(t)

    r'''
    {
    }
    '''

    assert len(p.components) == 1
    assert isinstance(p.components[0], Container)
    assert len(p.leaves) == 0
    assert t.format == '{\n}'


def test_BeamSpanner_span_anonymous_02():
    '''Nonempty spanned sequential container;
        container formats beam indications on first and last leaves.'''

    t = Container(Note(0, (1, 8)) * 8)
    p = spannertools.BeamSpanner(t)

    r'''
    {
        c'8 [
        c'8
        c'8
        c'8
        c'8
        c'8
        c'8
        c'8 ]
    }
    '''

    assert len(p.components) == 1
    assert isinstance(p.components[0], Container)
    assert len(p.leaves) == 8
    assert t.format == "{\n\tc'8 [\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8 ]\n}"


def test_BeamSpanner_span_anonymous_03():
    '''Contiguous nonempty spanned containers;
        first and last leaves in contiguity chain format
        beam indications.'''

    t = Staff(Container(Note(0, (1, 8)) * 4) * 2)
    p = spannertools.BeamSpanner(t[:])

    r'''
    \new Staff {
        {
            c'8 [
            c'8
            c'8
            c'8
        }
        {
            c'8
            c'8
            c'8
            c'8 ]
        }
    }
    '''

    assert len(p.components) == 2
    assert isinstance(p.components[0], Container)
    assert isinstance(p.components[1], Container)
    assert len(p.leaves) == 8
    "\\new Staff {\n\t{\n\t\tc'8 [\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t}\n\t{\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8 ]\n\t}\n}"


def test_BeamSpanner_span_anonymous_04():
    '''Contiguous nonempty containers and leaves;
        top-level attachment;
        first and last leaves in contiguity chain format
        beam indications.'''

    t = Staff([Container(notetools.make_repeated_notes(4)), Note(0, (1, 8)), Note(0, (1, 8))])
    p = spannertools.BeamSpanner(t)

    r'''
    \new Staff {
        {
            c'8 [
            c'8
            c'8
            c'8
        }
        c'8
        c'8 ]
    }
    '''

    assert len(p.components) == 1
    assert isinstance(p.components[0], Staff)
    assert len(p.leaves) == 6
    assert t.format == "\\new Staff {\n\t{\n\t\tc'8 [\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t}\n\tc'8\n\tc'8 ]\n}"


def test_BeamSpanner_span_anonymous_05():
    '''Contiguous nonempty containers and leaves;
        intermediate attachment;
        first and last leaves in contiguity chain format beam indications.'''

    t = Staff([Container(notetools.make_repeated_notes(4)), Note(0, (1, 8)), Note(0, (1, 8))])
    p = spannertools.BeamSpanner(t[:])

    r'''
    \new Staff {
        {
            c'8 [
            c'8
            c'8
            c'8
        }
        c'8
        c'8 ]
    }
    '''

    assert len(p.components) == 3
    assert isinstance(p.components[0], Container)
    assert isinstance(p.components[1], Note)
    assert isinstance(t[2], Note)
    assert len(p.leaves) == 6
    assert t.format == "\\new Staff {\n\t{\n\t\tc'8 [\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t}\n\tc'8\n\tc'8 ]\n}"


def test_BeamSpanner_span_anonymous_06():
    '''Contiguous nonempty containers and leaves;
        leaf-level attachment;
        first and last leaves in contiguity chain format beam indications.'''

    t = Staff([Container(notetools.make_repeated_notes(4)), Note(0, (1, 8)), Note(0, (1, 8))])
    p = spannertools.BeamSpanner(t.leaves)

    r'''
    \new Staff {
        {
            c'8 [
            c'8
            c'8
            c'8
        }
        c'8
        c'8 ]
    }
    '''

    assert len(p.components) == 6
    for x in p.components:
        assert isinstance(x, Note)
    assert len(p.leaves) == 6
    assert t.format == "\\new Staff {\n\t{\n\t\tc'8 [\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t}\n\tc'8\n\tc'8 ]\n}"


def test_BeamSpanner_span_anonymous_07():
    '''Contiguous empty containers are OK;
        no beams appear at format-time.'''

    t = Staff(Container([]) * 3)
    p = spannertools.BeamSpanner(t[:])

    assert len(p.components) == 3
    for x in p.components:
        assert isinstance(x, Container)
    assert len(p.leaves) == 0

    r'''
    \new Staff {
        {
        }
        {
        }
        {
        }
    }
    '''


def test_BeamSpanner_span_anonymous_08():
    '''Intervening empty containers are OK.'''

    t = Staff(Container(Note(0, (1, 8)) * 4) * 2)
    t.insert(1, Container([]))
    p = spannertools.BeamSpanner(t[:])

    assert len(p.components) == 3
    for x in p.components:
        assert isinstance(x, Container)
    assert len(p.leaves) == 8
    assert t.format == "\\new Staff {\n\t{\n\t\tc'8 [\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t}\n\t{\n\t}\n\t{\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8 ]\n\t}\n}"

    r'''
    \new Staff {
        {
            c'8 [
            c'8
            c'8
            c'8
        }
        {
        }
        {
            c'8
            c'8
            c'8
            c'8 ]
        }
    }
    '''


def test_BeamSpanner_span_anonymous_09():
    '''Empty containers at edges are OK.'''

    t = Staff(Container([]) * 2)
    t.insert(1, Container(Note(0, (1, 8)) * 4))
    p = spannertools.BeamSpanner(t[:])

    assert len(p.components) == 3
    for x in p.components:
        assert isinstance(x, Container)
    assert len(p.leaves) == 4
    assert t.format == "\\new Staff {\n\t{\n\t}\n\t{\n\t\tc'8 [\n\t\tc'8\n\t\tc'8\n\t\tc'8 ]\n\t}\n\t{\n\t}\n}"

    r'''
    \new Staff {
        {
        }
        {
            c'8 [
            c'8
            c'8
            c'8 ]
        }
        {
        }
    }
    '''


def test_BeamSpanner_span_anonymous_10():
    '''Spanners group anonymous containers at
        completely different depths just fine;
        the only requirement is that the *leaves* of all
        arguments passed to spannertools.BeamSpanner() be *temporarly contiguous*.
        Ie, there's a *leaf temporal contiguity* requirement.'''

    s1 = Container([Note(i, (1,8)) for i in range(4)])
    s1 = Container([s1])
    s2 = Container([Note(i, (1,8)) for i in range(4,8)])
    s2 = Container([s2])
    t = Voice([s1, s2])
    p = spannertools.BeamSpanner(t)
    assert len(p.components) == 1
    assert len(p.leaves) == 8

    p.clear()
    p = spannertools.BeamSpanner([t[0], t[1]])
    assert len(p.components) == 2
    assert len(p.leaves) == 8

    p.clear()
    p = spannertools.BeamSpanner([t[0][0], t[1][0]])
    assert len(p.components) == 2
    assert len(p.leaves) == 8

    p.clear()
    p = spannertools.BeamSpanner([t[0], t[1][0]])
    assert len(p.components) == 2
    assert len(p.leaves) == 8

    p.clear()
    p = spannertools.BeamSpanner([t[0][0], t[1]])
    assert len(p.components) == 2
    assert len(p.leaves) == 8

    r'''
    \new Voice {
        {
            {
                c'8
                cs'8
                d'8
                ef'8
            }
        }
        {
            {
                e'8
                f'8
                fs'8
                g'8
            }
        }
    }
    '''


def test_BeamSpanner_span_anonymous_11():
    '''Asymmetric structure;
        but otherwise same as immediately above.'''

    s1 = Container([Note(i, (1,8)) for i in range(4)])
    s1 = Container([s1])
    s1 = Container([s1])
    s2 = Container([Note(i, (1,8)) for i in range(4,8)])
    t = Voice([s1, s2])

    p = spannertools.BeamSpanner(t)
    assert len(p.components) == 1
    assert len(p.leaves) == 8
    p.clear()

    p = spannertools.BeamSpanner([t[0], t[1]])
    assert len(p.components) == 2
    assert len(p.leaves) == 8
    p.clear()

    p = spannertools.BeamSpanner([t[0][0], t[1]])
    assert len(p.components) == 2
    assert len(p.leaves) == 8
    p.clear()

    p = spannertools.BeamSpanner([t[0][0][0], t[1]])
    assert len(p.components) == 2
    assert len(p.leaves) == 8
    p.clear()

    r'''
    \new Voice {
        {
            {
                {
                    c'8
                    cs'8
                    d'8
                    ef'8
                }
            }
        }
        {
            e'8
            f'8
            fs'8
            g'8
        }
    }
    '''


def test_BeamSpanner_span_anonymous_12():
    '''Docs.'''

    s1 = Container([Note(i, (1, 8)) for i in range(2)])
    s2 = Container([Note(i, (1, 8)) for i in range(3, 5)])
    v = Voice([s1, Note(2, (1, 8)), s2])

    p = spannertools.BeamSpanner(v)
    assert len(p.components) == 1
    assert len(p.leaves) == 5
    p.clear()

    p = spannertools.BeamSpanner(v[:])
    assert len(p.components) == 3
    assert len(p.leaves) == 5
    p.clear()

    r'''
    \new Voice {
        {
            c'8
            cs'8
        }
        d'8
        {
            ef'8
            e'8
        }
    }
    '''


def test_BeamSpanner_span_anonymous_13():
    '''Alternating sequences of tuplets and notes span correctly.'''

    t1 = tuplettools.FixedDurationTuplet(Duration(1,4), [Note(i, (1,8)) for i in range(3)])
    t2 = tuplettools.FixedDurationTuplet(Duration(1,4), [Note(i, (1,8)) for i in range(4,7)])
    v = Voice([t1, Note(3, (1,8)), t2])

    r'''
    \new Voice {
        \times 2/3 {
            c'8
            cs'8
            d'8
        }
        ef'8
        \times 2/3 {
            e'8
            f'8
            fs'8
        }
    }
    '''

    p = spannertools.BeamSpanner(v)
    assert len(p.components) == 1
    assert len(p.leaves) == 7
    p.clear()

    p = spannertools.BeamSpanner(v[:])
    assert len(p.components) == 3
    assert len(p.leaves) == 7
    p.clear()


def test_BeamSpanner_span_anonymous_14():
    '''Asymmetrically nested tuplets span correctly.'''

    tinner = tuplettools.FixedDurationTuplet(Duration(1, 4), Note(0, (1, 8)) * 3)
    t = tuplettools.FixedDurationTuplet(Duration(2, 4), [Note("c'4"), tinner, Note("c'4")])

    r'''
    \times 2/3 {
        c'4
        \times 2/3 {
            c'8
            c'8
            c'8
        }
        c'4
    }
    '''

    p = spannertools.BeamSpanner(t)
    assert len(p.components) == 1
    assert len(p.leaves) == 5
    p.clear()

    p = spannertools.BeamSpanner(t[:])
    assert len(p.components) == 3
    assert len(p.leaves) == 5


def test_BeamSpanner_span_anonymous_15():
    '''Parent asymmetric structures DO NOT allow spanning.
        LilyPond will correspondingly not render the beam
        through two different anonymous voices.'''

    v1 = Voice([Note(i , (1, 8)) for i in range(3)])
    n = Note(3, (1,8))
    v2 = Voice([Note(i , (1, 8)) for i in range(4, 8)])
    t = Staff([v1, n, v2])

    r'''
    \new Staff {
        \new Voice {
            c'8
            cs'8
            d'8
        }
        ef'8
        \new Voice {
            e'8
            f'8
            fs'8
            g'8
        }
    }
    '''

    assert py.test.raises(AssertionError, 'p = spannertools.BeamSpanner([t[0], t[1]])')
    assert py.test.raises(AssertionError, 'p = spannertools.BeamSpanner([t[1], t[2]])')
