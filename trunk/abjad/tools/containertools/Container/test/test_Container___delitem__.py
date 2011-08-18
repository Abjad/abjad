from abjad import *



def test_Container___delitem___01():
    '''Delete spanned component.
    Component withdraws crossing spanners.
    Component carries covered spanners forward.
    Operation always leaves all expressions in tact.
    '''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.BeamSpanner(t[:])
    spannertools.SlurSpanner(t[0][:])
    spannertools.SlurSpanner(t[1][:])

    r'''
    \new Voice {
        {
            c'8 [ (
            d'8 )
        }
        {
            e'8 (
            f'8 ] )
        }
    }
    '''

    old = t[0]
    del(t[0])

    "Container t is now ..."

    r'''
    \new Voice {
        {
            e'8 [ (
            f'8 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\t{\n\t\te'8 [ (\n\t\tf'8 ] )\n\t}\n}"

    "Deleted component is now ..."

    r'''
    {
        c'8 (
        d'8 )
    }
    '''

    assert componenttools.is_well_formed_component(old)
    assert old.format == "{\n\tc'8 (\n\td'8 )\n}"


def test_Container___delitem___02():
    '''Delete 1 leaf in container.
    Spanner structure is preserved.'''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])

    del(t[1])

    r'''
    \new Voice {
        c'8 [
        e'8
        f'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8 [\n\te'8\n\tf'8 ]\n}"


def test_Container___delitem___03():
    '''Delete slice in middle of container.'''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])

    del(t[1:3])

    r'''
    \new Voice {
        c'8 [
        f'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8 [\n\tf'8 ]\n}"


def test_Container___delitem___04():
    '''Delete slice from beginning to middle of container.'''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])

    del(t[:2])

    r'''
    \new Voice {
        e'8 [
        f'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\te'8 [\n\tf'8 ]\n}"


def test_Container___delitem___05():
    '''Delete slice from middle to end of container.'''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])

    del(t[2:])

    r'''
    \new Voice {
        c'8 [
        d'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8 [\n\td'8 ]\n}"


def test_Container___delitem___06():
    '''Delete slice from beginning to end of container.'''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])

    del(t[:])

    r'''
    \new Voice {
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == '\\new Voice {\n}'


def test_Container___delitem___07():
    '''Detach leaf from tuplet and spanner.'''

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    spannertools.BeamSpanner(t[:])

    del(t[1])

    r'''
    {
        c'8 [
        e'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\tc'8 [\n\te'8 ]\n}"
