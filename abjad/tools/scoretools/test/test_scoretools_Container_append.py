import abjad
import pytest


def test_scoretools_Container_append_01():
    r'''Append sequential to voice.
    '''

    voice = abjad.Voice("c'8 d'8")
    beam = abjad.Beam()
    abjad.attach(beam, voice[:])
    voice.append(abjad.Container("e'8 f'8"))

    assert format(voice) == abjad.String.normalize(
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
        )

    assert abjad.inspect(voice).is_well_formed()


def test_scoretools_Container_append_02():
    r'''Append leaf to tuplet.
    '''

    tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
    beam = abjad.Beam()
    abjad.attach(beam, tuplet[:])
    tuplet.append(abjad.Note(5, (1, 16)), preserve_duration=True)

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \times 4/7 {
            c'8 [
            d'8
            e'8 ]
            f'16
        }
        '''
        )

    assert abjad.inspect(tuplet).is_well_formed()


def test_scoretools_Container_append_03():
    r'''Trying to append noncomponent to container raises TypeError.
    '''

    voice = abjad.Voice("c'8 d'8 e'8")
    beam = abjad.Beam()
    abjad.attach(beam, voice[:])

    assert pytest.raises(Exception, "voice.append('foo')")
    assert pytest.raises(Exception, "voice.append(99)")
    assert pytest.raises(Exception, "voice.append([])")
    assert pytest.raises(Exception, "voice.append([abjad.Note(0, (1, 8))])")


def test_scoretools_Container_append_04():
    r'''Append spanned leaf from donor container to recipient container.
    '''

    voice_1 = abjad.Voice("c'8 d'8 e'8")
    beam = abjad.Beam()
    abjad.attach(beam, voice_1[:])

    assert format(voice_1) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8
            e'8 ]
        }
        '''
        )

    voice_2 = abjad.Voice("c'8 d'8 e'8 f'8")
    beam = abjad.Beam()
    abjad.attach(beam, voice_2[:])

    assert format(voice_2) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8
            e'8
            f'8 ]
        }
        '''
        )

    voice_1.append(voice_2[-1])

    assert format(voice_1) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8
            e'8 ]
            f'8
        }
        '''
        )

    assert abjad.inspect(voice_1).is_well_formed()

    assert format(voice_2) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8
            e'8 ]
        }
        '''
        )

    assert abjad.inspect(voice_2).is_well_formed()


def test_scoretools_Container_append_05():
    r'''Append spanned leaf from donor container to recipient container.
    Donor and recipient containers are the same.
    '''

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    beam = abjad.Beam()
    abjad.attach(beam, voice[:])

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8
            e'8
            f'8 ]
        }
        '''
        )

    voice.append(voice[1])

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8 [
            e'8
            f'8 ]
            d'8
        }
        '''
        )

    assert abjad.inspect(voice).is_well_formed()


def test_scoretools_Container_append_06():
    r'''Can not insert grace container into container.
    '''

    staff = abjad.Staff("c' d' e'")
    grace_container = abjad.GraceContainer("f'16 g'")

    assert pytest.raises(Exception, 'staff.append(grace_container)')
