import abjad
import pytest


def test_scoretools_Container_extend_01():
    r'''Extend container with list of leaves.
    '''

    voice = abjad.Voice("c'8 d'8")
    beam = abjad.Beam()
    abjad.attach(beam, voice[:])
    voice.extend([abjad.Note("c'8"), abjad.Note("d'8")])

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8 ]
            c'8
            d'8
        }
        '''
        )

    assert abjad.inspect(voice).is_well_formed()


def test_scoretools_Container_extend_02():
    r'''Extend container with contents of other container.
    '''

    voice_1 = abjad.Voice("c'8 d'8")
    beam = abjad.Beam()
    abjad.attach(beam, voice_1[:])

    voice_2 = abjad.Voice("e'8 f'8")
    beam = abjad.Beam()
    abjad.attach(beam, voice_2[:])
    voice_1.extend(voice_2)

    assert format(voice_1) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8 ]
            e'8 [
            f'8 ]
        }
        '''
        )

    assert abjad.inspect(voice_1).is_well_formed()


def test_scoretools_Container_extend_03():
    r'''Extending container with empty list leaves container unchanged.
    '''

    voice = abjad.Voice("c'8 d'8")
    beam = abjad.Beam()
    abjad.attach(beam, voice[:])
    voice.extend([])

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8 ]
        }
        '''
        )

    assert abjad.inspect(voice).is_well_formed()


def test_scoretools_Container_extend_04():
    r'''Extending one container with empty second container leaves both
    containers unchanged.
    '''

    voice = abjad.Voice("c'8 d'8")
    beam = abjad.Beam()
    abjad.attach(beam, voice[:])
    voice.extend(abjad.Voice([]))

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8 ]
        }
        '''
        )

    assert abjad.inspect(voice).is_well_formed()


def test_scoretools_Container_extend_05():
    r'''Trying to extend container with noncomponent raises TypeError.
    '''

    voice = abjad.Voice("c'8 d'8")
    beam = abjad.Beam()
    abjad.attach(beam, voice[:])

    assert pytest.raises(Exception, 'voice.extend(7)')
    assert pytest.raises(Exception, "voice.extend('foo')")


def test_scoretools_Container_extend_06():
    r'''Trying to extend container with noncontainer raises exception.
    '''

    voice = abjad.Voice("c'8 d'8")
    beam = abjad.Beam()
    abjad.attach(beam, voice[:])

    statement = 'voice.extend(abjad.Note(4, (1, 4)))'
    assert pytest.raises(AttributeError, statement)

    statement = 'voice.extend(abjad.Chord([2, 3, 5], (1, 4)))'
    assert pytest.raises(AttributeError, statement)


def test_scoretools_Container_extend_07():
    r'''Extend container with partial and spanned contents of other container.
    '''

    voice_1 = abjad.Voice("c'8 d'8")
    beam = abjad.Beam()
    abjad.attach(beam, voice_1[:])

    voice_2 = abjad.Voice("c'8 d'8 e'8 f'8")
    beam = abjad.Beam()
    abjad.attach(beam, voice_2[:])

    voice_1.extend(voice_2[-2:])

    assert format(voice_1) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8 ]
            e'8
            f'8
        }
        '''
        )

    assert abjad.inspect(voice_1).is_well_formed()

    assert format(voice_2) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8 ]
        }
        '''
        )

    assert abjad.inspect(voice_2).is_well_formed()


def test_scoretools_Container_extend_08():
    r'''Extend container with partial and spanned contents of other container.
    Covered span comes with components from donor container.
    '''

    voice_1 = abjad.Voice("c'8 d'8")
    beam = abjad.Beam()
    abjad.attach(beam, voice_1[:])

    voice_2 = abjad.Voice("c'8 d'8 e'8 f'8")
    beam = abjad.Beam()
    abjad.attach(beam, voice_2[:])
    slur = abjad.Slur()
    abjad.attach(slur, voice_2[-2:])

    assert format(voice_2) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8
            e'8 (
            f'8 ] )
        }
        '''
        )

    voice_1.extend(voice_2[-2:])

    assert format(voice_1) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8 ]
            e'8 (
            f'8 )
        }
        '''
        )

    assert abjad.inspect(voice_1).is_well_formed()

    assert format(voice_2) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8 ]
        }
        '''
        )

    assert abjad.inspect(voice_2).is_well_formed()


def test_scoretools_Container_extend_09():
    r'''Extend container with LilyPond input string.
    '''

    container = abjad.Container([])
    container.extend("c'4 ( d'4 e'4 f'4 )")

    assert format(container) == abjad.String.normalize(
        r'''
        {
            c'4 (
            d'4
            e'4
            f'4 )
        }
        '''
        )

    assert abjad.inspect(container).is_well_formed()


def test_scoretools_Container_extend_10():
    r'''Selections are stripped out.
    '''

    maker = abjad.NoteMaker()
    selection_1 = maker([0, 2], [abjad.Duration(1, 4)])
    selection_2 = maker([4, 5], [abjad.Duration(1, 4)])
    selection_3 = maker([7, 9], [abjad.Duration(1, 4)])
    selection_4 = maker([11, 12], [abjad.Duration(1, 4)])
    selections = [selection_1, selection_2, selection_3, selection_4]
    container = abjad.Container()
    container.extend(selections)

    assert format(container) == abjad.String.normalize(
        r'''
        {
            c'4
            d'4
            e'4
            f'4
            g'4
            a'4
            b'4
            c''4
        }
        '''
        )

    assert abjad.inspect(container).is_well_formed()
