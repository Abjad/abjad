from abjad import *


def test_SequentialSelection__give_dominant_spanners_to_components_01():
    r'''Find spanners that dominate donor_components.
    Apply dominant spanners to recipient_components.
    Withdraw donor_components from spanners.
    The operation can mangle spanners.
    Remove donor_components from parentage immediately after.
    '''

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

    t[1:3]._give_dominant_spanners_to_components(recipient[:])

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

    assert not select(t).is_well_formed()
    assert t.lilypond_format == "\\new Voice {\n\tc'8 [ \\<\n\td'8 ]\n\te'8\n\tf'8 \\!\n}"

    "Recipient is now ..."

    r'''
    \new Voice {
        c'16 [ (
        c'16
        c'16 ] )
    }
    '''

    "Slur is contiguous but recipient participates in discont. cresc."

    assert not select(recipient).is_well_formed()
    assert recipient.lilypond_format == "\\new Voice {\n\tc'16 [ (\n\tc'16\n\tc'16 ] )\n}"


def test_SequentialSelection__give_dominant_spanners_to_components_02():
    r'''Not composer-safe.
    '''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
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
    t[:1]._give_dominant_spanners_to_components([recipient])

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

    assert t.lilypond_format == "\\new Voice {\n\t{\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8 ]\n\t}\n}"

    "Recipient container is now ..."

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8
        f'8
    }
    '''

    assert recipient.lilypond_format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8\n}"

    "Both container t and recipient container carry discontiguous spanners."

    assert not select(t).is_well_formed()
    assert not select(recipient).is_well_formed()
