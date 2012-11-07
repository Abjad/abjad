from abjad import *


def test_Container_pop_01():
    '''Containers pop leaves correctly.
        Popped leaves detach from parent.
        Popped leaves withdraw from crossing spanners.
        Popped leaves carry covered spanners forward.'''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.SlurSpanner(t[:])
    beamtools.BeamSpanner(t[1])

    r'''
    \new Voice {
        c'8 (
        d'8 [ ]
        e'8
        f'8 )
    }
    '''

    result = t.pop(1)

    r'''
    \new Voice {
        c'8 (
        e'8
        f'8 )
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Voice {\n\tc'8 (\n\te'8\n\tf'8 )\n}"

    "Result is now d'8 [ ]"

    assert wellformednesstools.is_well_formed_component(result)
    assert result.lilypond_format == "d'8 [ ]"


def test_Container_pop_02():
    '''Containers pop nested containers correctly.
        Popped containers detach from both parent and spanners.'''

    t = Staff(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    p = beamtools.BeamSpanner(t[:])

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

    sequential = t.pop()

    r'''
    \new Staff {
        {
            c'8 [
            d'8 ]
        }
    }
    '''

    assert t.lilypond_format == "\\new Staff {\n\t{\n\t\tc'8 [\n\t\td'8 ]\n\t}\n}"
    assert wellformednesstools.is_well_formed_component(t)

    r'''
    {
        e'8
        f'8
    }
    '''

    assert sequential.lilypond_format == "{\n\te'8\n\tf'8\n}"
    assert wellformednesstools.is_well_formed_component(sequential)
