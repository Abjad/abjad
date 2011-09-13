from abjad import *
import py.test


def test_Spanner__remove_01():
    '''Remove interior component from spanner.
    Remove spanner from component's aggregator.
    Spanner is left discontiguous and score no longer checks.
    Not composer-safe.
    Follow immediately with operation to remove component from score.
    '''

    t = Voice("c'8 d'8 e'8 f'8")
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    p = spannertools.BeamSpanner(t[:])

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    p._remove(p.components[1])

    "Spanner is now discontiguous: spannertools.BeamSpanner(c'8, e'8, f'8)."

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    assert not componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"


def test_Spanner__remove_02():
    '''Remove last component from spanner.
    Remove spanner from component's aggregator.
    Here an end element removes from spanner.
    So spanner is not left discontiguous and score checks.
    Still not composer-safe.
    Note spanner.pop() and spanner.pop_left() are composer-safe.
    '''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    p = spannertools.BeamSpanner(t[:])

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

    result = p._remove(p.components[2])

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

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8 ]\n\t}\n\t{\n\t\tg'8\n\t\ta'8\n\t}\n}"


def test_Spanner__remove_03():
    '''Remove works only on references and not on equality.
    '''

    note = Note("c'4")
    spanner = spannertools.Spanner([Note("c'4")])

    assert py.test.raises(Exception, 'spanner._remove(note)')
