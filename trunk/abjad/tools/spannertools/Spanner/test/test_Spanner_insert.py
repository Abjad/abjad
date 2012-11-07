from abjad import *


def test_Spanner_insert_01():
    '''Insert component in spanner at index i.
        Add spanner to component's aggregator.
        Component then knows about spanner and vice versa.
        Not composer-safe.
        Inserting into middle of spanner may leave discontiguous spanner.'''

    t = Voice("c'8 d'8 e'8 f'8")
    p = beamtools.BeamSpanner(t[:2])

    r'''
    \new Voice {
        c'8 [
        d'8 ]
        e'8
        f'8
    }
    '''

    p._insert(1, t.leaves[-1])

    "Interior insert leaves discontiguous spanner: beamtools.BeamSpanner(c'8, f'8, d'8)."

    assert not wellformednesstools.is_well_formed_component(t)


def test_Spanner_insert_02():
    '''Insert component at index zero in spanner.
        This operation does not mangle spanner.
        Operation is still not composer-safe, however.
        Note that p.append() and p.append_left() are composer-safe.'''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    p = beamtools.BeamSpanner(t[1])

    r'''
    \new Voice {
        {
            c'8
            d'8
        }
        {
            e'8 [
            f'8 ]
        }
        {
            g'8
            a'8
        }
    }
    '''

    p._insert(0, t[0][1])

    r'''
    \new Voice {
        {
            c'8
            d'8 [
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

    assert t.lilypond_format == "\\new Voice {\n\t{\n\t\tc'8\n\t\td'8 [\n\t}\n\t{\n\t\te'8\n\t\tf'8 ]\n\t}\n\t{\n\t\tg'8\n\t\ta'8\n\t}\n}"
