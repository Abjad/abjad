from abjad import *
from abjad.tools.componenttools._give_music_from_donor_components_to_recipient_components import _give_music_from_donor_components_to_recipient_components
import py.test


def test_componenttools__give_music_from_donor_components_to_recipient_components_01():
    '''Give spanned music from donor to recipient.
    Helper is not composer-safe and results here in bad spanners.
    '''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.BeamSpanner(t.leaves)

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
    recipient = Voice([])
    _give_music_from_donor_components_to_recipient_components([donor], recipient)

    "Container t is now ..."

    r'''
    \new Voice {
        {
        }
        {
            e'8
            f'8 ]
        }
    }
    '''

    "Container t carries discontiguous spanners."

    assert not componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\t{\n\t}\n\t{\n\t\te'8\n\t\tf'8 ]\n\t}\n}"

    "Recipient container is now ..."

    r'''
    \new Voice {
        c'8 [
        d'8
    }
    '''

    "Recipient container carries discontiguous spanners."

    assert not componenttools.is_well_formed_component(recipient)
    assert recipient.format == "\\new Voice {\n\tc'8 [\n\td'8\n}"


def test_componenttools__give_music_from_donor_components_to_recipient_components_02():
    '''When donor is leaf do nothing.
    '''

    donor = Note(0, (1, 8))
    recipient = Voice([])

    _give_music_from_donor_components_to_recipient_components([donor], recipient)

    assert componenttools.is_well_formed_component(donor)
    assert donor.format == "c'8"

    assert componenttools.is_well_formed_component(recipient)
    assert recipient.format == '\\new Voice {\n}'


def test_componenttools__give_music_from_donor_components_to_recipient_components_03():
    '''When recipient is unable to accept donated music raise music contents error.
    '''

    donor = Voice("c'8 d'8 e'8 f'8")
    recipient = Voice("c'8 d'8 e'8 f'8")

    assert py.test.raises(
        MusicContentsError, '_give_music_from_donor_components_to_recipient_components([donor], recipient)')
