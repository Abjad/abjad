from abjad import *
import py.test


def test_Container___setitem___slice_01():
    '''Containers set single leaves correctly in an unspanned structure.'''

    t = Staff("c'8 d'8 e'8 f'8")
    t[2:2] = [Note(7, (1, 8))]

    r'''
    \new Staff {
        c'8
        d'8
        g'8
        e'8
        f'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc'8\n\td'8\n\tg'8\n\te'8\n\tf'8\n}"


def test_Container___setitem___slice_02():
    '''Set single leaf between spanned components.'''

    t = Staff("c'8 d'8 e'8 f'8")
    p = spannertools.BeamSpanner(t[:])
    note = Note(7, (1, 8))
    t[2:2] = [note]

    r'''
    \new Staff {
        c'8 [
        d'8
        g'8
        e'8
        f'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc'8 [\n\td'8\n\tg'8\n\te'8\n\tf'8 ]\n}"


def test_Container___setitem___slice_03():
    '''Containers set sequence of leaves
        between spanned components.'''

    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8"), Note("g'8"), Note("a'8")]

    beginning = notes[:2]
    middle = notes[2:4]
    end = notes[4:]

    t = Staff(beginning + end)
    p = spannertools.BeamSpanner(t[:])

    r'''
    \new Staff {
        c'8 [
        d'8
        g'8
        a'8 ]
    }
    '''

    t[2:2] = middle

    r'''
    \new Staff {
        c'8 [
        d'8
        e'8
        f'8
        g'8
        a'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc'8 [\n\td'8\n\te'8\n\tf'8\n\tg'8\n\ta'8 ]\n}"


def test_Container___setitem___slice_04():
    '''Replace sequence of spanned components with a single leaf.'''

    t = Staff("c'8 d'8 e'8 f'8")
    p = spannertools.BeamSpanner(t[:])
    note = Note(12, (1, 8))
    t[1:3] = [note]

    r'''
    \new Staff {
        c'8 [
        c''8
        f'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc'8 [\n\tc''8\n\tf'8 ]\n}"


def test_Container___setitem___slice_05():
    '''Replace a sequence of multiple components with
        a different sequence of multiple components.'''

    t = Staff("c'8 d'8 e'8 f'8")
    p = spannertools.BeamSpanner(t[:])
    notes = [Note(11, (1, 8)), Note(9, (1, 8)), Note(7, (1, 8))]
    t[1:3] = notes

    r'''
    \new Staff {
        c'8 [
        b'8
        a'8
        g'8
        f'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc'8 [\n\tb'8\n\ta'8\n\tg'8\n\tf'8 ]\n}"


def test_Container___setitem___slice_06():
    '''Donor and recipient container are the same.'''

    t = Staff(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.BeamSpanner(t.leaves)

    r'''
    \new Staff {
        {
            c'8 [
            d'8
        }
        {
            e'8
            f'8 ]
        }
    }
    '''

    sequential = t[0]
    t[0:1] = sequential.leaves

    r'''
    \new Staff {
        c'8 [
        d'8
        {
            e'8
            f'8 ]
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert len(sequential) == 0
    assert t.format == "\\new Staff {\n\tc'8 [\n\td'8\n\t{\n\t\te'8\n\t\tf'8 ]\n\t}\n}"


def test_Container___setitem___slice_07():
    '''Donor and recipient container are the same.'''

    t = Staff(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.BeamSpanner(t.leaves)

    r'''
    \new Staff {

        {
            c'8 [
            d'8
        }
        {
            e'8
            f'8 ]
        }
    }
    '''

    t[0:0] = t[0][:1]

    r'''
    \new Staff {
        c'8
        {
            d'8 [
        }
        {
            e'8
            f'8 ]
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc'8\n\t{\n\t\td'8 [\n\t}\n\t{\n\t\te'8\n\t\tf'8 ]\n\t}\n}"


def test_Container___setitem___slice_08():
    '''Donor and recipient container are the same.'''

    t = Staff(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.BeamSpanner(t.leaves)

    r'''
    \new Staff {
        {
            c'8 [
            d'8
        }
        {
            e'8
            f'8 ]
        }
    }
    '''

    t[0:0] = t[0][:]

    r'''
    \new Staff {
        c'8
        d'8
        {
        }
        {
            e'8 [
            f'8 ]
        }
    }
    '''

    assert t.format == "\\new Staff {\n\tc'8\n\td'8\n\t{\n\t}\n\t{\n\t\te'8 [\n\t\tf'8 ]\n\t}\n}"


def test_Container___setitem___slice_09():
    '''Donor and recipient container are the same.'''

    t = Staff(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.BeamSpanner(t.leaves)

    r'''
    \new Staff {
        {
            c'8 [
            d'8
        }
        {
            e'8
            f'8 ]
        }
    }
    '''

    sequential = t[0]
    t[0:0] = sequential[:]
    sequential[0:0] = t[-1][:1]

    r'''
    \new Staff {
        c'8
        d'8
        {
            e'8
        }
        {
            f'8 [ ]
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc'8\n\td'8\n\t{\n\t\te'8\n\t}\n\t{\n\t\tf'8 [ ]\n\t}\n}"


def test_Container___setitem___slice_10():
    '''Donor and recipient container are the same.'''

    t = Staff(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.BeamSpanner(t.leaves)

    r'''
    \new Staff {
        {
            c'8 [
            d'8
        }
        {
            e'8
            f'8 ]
        }
    }
    '''

    t[0:0] = t[0][:1]
    t[len(t):len(t)] = t[-1][-1:]

    r'''
    \new Staff {
        c'8
        {
            d'8 [
        }
        {
            e'8 ]
        }
        f'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc'8\n\t{\n\t\td'8 [\n\t}\n\t{\n\t\te'8 ]\n\t}\n\tf'8\n}"


def test_Container___setitem___slice_11():
    '''Extremely small coequal indices act as zero.'''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])
    t[-1000:-1000] = [Rest((1, 8))]

    r'''
    \new Voice {
        r8
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tr8\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"


def test_Container___setitem___slice_12():
    '''Extremely large, coequal indices work correctly.'''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])
    t[1000:1000] = [Rest((1, 8))]

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8
        f'8 ]
        r'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n\tr8\n}"


def test_Container___setitem___slice_13():
    '''You can use the slice for of setitem to empty the contents
    of a container. When you do this, emptied components withdraw
    from absolutely all spanners.

    On the other hand, if you want to empty a container and
    allow the emptied components to remain embedded within spanners,
    use containertools.delete_contents_of_container() instead.'''

    t = Staff("c'8 d'8 e'8 f'8")
    inner = Container(t[1:3])
    outer = Container([inner])
    beam = spannertools.BeamSpanner(inner[:])

    r'''
    \new Staff {
        c'8
        {
            {
                d'8 [
                e'8 ]
            }
        }
        f'8
    }
    '''

    # set outer container contents to empty
    outer[:] = []

    r'''
    \new Staff {
        c'8
        {
        }
        f'8
    }
    '''

    assert t.format == "\\new Staff {\n\tc'8\n\t{\n\t}\n\tf'8\n}"

    r'''
    {
        d'8
        e'8
    }
    '''

    # inner container leaves DO withdraw from all spanners
    assert inner.format == "{\n\td'8\n\te'8\n}"

    # ALTERNATIVE: use containertools.delete_contents_of_container()

    t = Staff("c'8 d'8 e'8 f'8")
    inner = Container(t[1:3])
    outer = Container([inner])
    beam = spannertools.BeamSpanner(inner[:])

    containertools.delete_contents_of_container(outer)

    r'''
    \new Staff {
        c'8
        {
        }
        f'8
    }
    '''

    r'''
    {
        d'8 [
        e'8 ]
    }
    '''

    # inner container leaves DO NOT withdraw from spanners
    assert inner.format == "{\n\td'8 [\n\te'8 ]\n}"
