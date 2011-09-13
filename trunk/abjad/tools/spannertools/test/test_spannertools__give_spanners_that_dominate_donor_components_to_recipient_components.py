from abjad import *
from abjad.tools.spannertools._give_spanners_that_dominate_donor_components_to_recipient_components import _give_spanners_that_dominate_donor_components_to_recipient_components


def test_spannertools__give_spanners_that_dominate_donor_components_to_recipient_components_01():
    '''Find spanners that dominate donor_components.
    Apply dominant spanners to recipient_components.
    Withdraw donor_components from spanners.
    The operation can mangle spanners.
    Remove donor_components from parentage immediately after.'''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.CrescendoSpanner(t[:])
    spannertools.BeamSpanner(t[:2])
    spannertools.SlurSpanner(t[1:3])

    r'''
    \new Voice {
        c'8 [ \<
        d'8 ] (
        e'8 )
        f'8 \!
    }
    '''

    recipient = Voice(notetools.make_repeated_notes(3, Duration(1, 16)))
    spannertools.BeamSpanner(recipient)

    r'''
    \new Voice {
        c'16 [
        c'16
        c'16 ]
    }
    '''

    _give_spanners_that_dominate_donor_components_to_recipient_components(t[1:3], recipient[:])

    "Voice t is now ..."

    r'''
    \new Voice {
        c'8 [ \<
        d'8 ]
        e'8
        f'8 \!
    }
    '''

    "Both crescendo and beam are now discontiguous."

    assert not componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8 [ \\<\n\td'8 ]\n\te'8\n\tf'8 \\!\n}"

    "Recipient is now ..."

    r'''
    \new Voice {
        c'16 [ (
        c'16
        c'16 ] )
    }
    '''

    "Slur is contiguous but recipient participates in discont. cresc."

    assert not componenttools.is_well_formed_component(recipient)
    assert recipient.format == "\\new Voice {\n\tc'16 [ (\n\tc'16\n\tc'16 ] )\n}"


def test_spannertools__give_spanners_that_dominate_donor_components_to_recipient_components_02():
    '''Not composer-safe.
    '''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.BeamSpanner(t[:])

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
    }
    '''

    donor = t[0]
    recipient = Voice("c'8 d'8 e'8 f'8")
    _give_spanners_that_dominate_donor_components_to_recipient_components([donor], [recipient])

    "Container t is now ..."

    r'''
    \new Voice {
        {
            c'8
            d'8
        }
        {
            e'8
            f'8 ]
        }
    }
    '''

    assert t.format == "\\new Voice {\n\t{\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8 ]\n\t}\n}"

    "Recipient container is now ..."

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8
        f'8
    }
    '''

    assert recipient.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8\n}"

    "Both container t and recipient container carry discontiguous spanners."

    assert not componenttools.is_well_formed_component(t)
    assert not componenttools.is_well_formed_component(recipient)
