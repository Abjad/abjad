from abjad import *
import py.test


def test_Container_append_01():
    '''Append sequential to voice.'''

    t = Voice(notetools.make_repeated_notes(2))
    beamtools.BeamSpanner(t[:])
    t.append(Container(notetools.make_repeated_notes(2)))
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)

    r'''
    \new Voice {
        c'8 [
        d'8 ]
        {
            e'8
            f'8
        }
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Voice {\n\tc'8 [\n\td'8 ]\n\t{\n\t\te'8\n\t\tf'8\n\t}\n}"


def test_Container_append_02():
    '''Append leaf to tuplet.'''

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    beamtools.BeamSpanner(t[:])
    t.append(Note(5, (1, 16)))

    r'''
    \times 4/7 {
        c'8 [
        d'8
        e'8 ]
        f'16
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == "\\times 4/7 {\n\tc'8 [\n\td'8\n\te'8 ]\n\tf'16\n}"


def test_Container_append_03():
    '''Trying to append noncomponent to container
        raises TypeError.'''

    t = Voice("c'8 d'8 e'8")
    beamtools.BeamSpanner(t[:])

    assert py.test.raises(Exception, "t.append('foo')")
    assert py.test.raises(Exception, "t.append(99)")
    assert py.test.raises(Exception, "t.append([])")
    assert py.test.raises(Exception, "t.append([Note(0, (1, 8))])")


def test_Container_append_04():
    '''Append spanned leaf from donor container to recipient container.'''

    t = Voice("c'8 d'8 e'8")
    beamtools.BeamSpanner(t[:])

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8 ]
    }
    '''

    u = Voice("c'8 d'8 e'8 f'8")
    beamtools.BeamSpanner(u[:])

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    t.append(u[-1])

    "Container t is now ..."

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8 ]
        f'8
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8 ]\n\tf'8\n}"

    "Container u is now ..."

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8 ]
    }
    '''

    assert wellformednesstools.is_well_formed_component(u)
    assert u.lilypond_format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8 ]\n}"


def test_Container_append_05():
    '''Append spanned leaf from donor container to recipient container.
        Donor and recipient containers are the same.'''

    t = Voice("c'8 d'8 e'8 f'8")
    beamtools.BeamSpanner(t[:])

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    t.append(t[1])

    r'''
    \new Voice {
        c'8 [
        e'8
        f'8 ]
        d'8
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Voice {\n\tc'8 [\n\te'8\n\tf'8 ]\n\td'8\n}"


def test_Container_append_06():
    '''Can not insert grace container into container.
    '''

    staff = Staff("c' d' e'")
    grace_container = gracetools.GraceContainer("f'16 g'")

    assert py.test.raises(GraceContainerError, 'staff.append(grace_container)')
