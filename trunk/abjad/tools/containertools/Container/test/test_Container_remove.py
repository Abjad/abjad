from abjad import *
import py.test


def test_Container_remove_01():
    '''Containers remove leaves correctly.
    Leaf detaches from parentage.
    Leaf withdraws from crossing spanners.
    Leaf carries covered spanners forward.
    Leaf returns after removal.
    '''

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

    #result = t.remove(t[1])
    note = t[1]
    t.remove(note)

    r'''
    \new Voice {
        c'8 (
        e'8
        f'8 )
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Voice {\n\tc'8 (\n\te'8\n\tf'8 )\n}"

    "Note is now d'8 [ ]"

    #assert wellformednesstools.is_well_formed_component(result)
    assert wellformednesstools.is_well_formed_component(note)
    #assert result.lilypond_format == "d'8 [ ]"
    assert note.lilypond_format == "d'8 [ ]"


def test_Container_remove_02():
    '''Containers remove nested containers correctly.
    Container detaches from parentage.
    Container withdraws from crossing spanners.
    Container carries covered spanners forward.
    Container returns after removal.
    '''

    t = Staff(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    sequential = t[0]
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

    t.remove(sequential)

    r'''
    \new Staff {
        {
            e'8 [
            f'8 ]
        }
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Staff {\n\t{\n\t\te'8 [\n\t\tf'8 ]\n\t}\n}"

    r'''
    {
        c'8
        d'8
    }
    '''

    assert wellformednesstools.is_well_formed_component(sequential)
    assert sequential.lilypond_format == "{\n\tc'8\n\td'8\n}"


def test_Container_remove_03():
    '''Container remove works on identity and not equality.
    '''

    note = Note("c'4")
    container = Container([Note("c'4")])

    assert py.test.raises(Exception, 'container.remove(note)')
