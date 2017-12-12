import abjad
import pytest


def test_lilypondparsertools_LilyPondParser__spanners__Slur_01():
    r'''Successful slurs, showing single leaf overlap.
    '''

    maker = abjad.NoteMaker()
    target = abjad.Container(maker([0] * 4, [(1, 4)]))
    slur = abjad.Slur()
    abjad.attach(slur, target[2:])
    slur = abjad.Slur()
    abjad.attach(slur, target[:3])

    assert format(target) == abjad.String.normalize(
        r'''
        {
            c'4 (
            c'4
            c'4 ) (
            c'4 )
        }
        '''
        )

    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__spanners__Slur_02():
    r'''Swapped start and stop.
    '''

    maker = abjad.NoteMaker()
    target = abjad.Container(maker([0] * 4, [(1, 4)]))
    slur = abjad.Slur()
    abjad.attach(slur, target[2:])
    slur = abjad.Slur()
    abjad.attach(slur, target[:3])

    assert format(target) == abjad.String.normalize(
        r'''
        {
            c'4 (
            c'4
            c'4 ) (
            c'4 )
        }
        '''
        )

    string = r"\relative c' { c ( c c () c ) }"

    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__spanners__Slur_03():
    r'''Single leaf.
    '''

    string = '{ c () c c c }'
    assert pytest.raises(Exception, 'LilyPondParser()(string)')


def test_lilypondparsertools_LilyPondParser__spanners__Slur_04():
    r'''Unterminated.
    '''

    string = '{ c ( c c c }'
    assert pytest.raises(Exception, 'LilyPondParser()(string)')


def test_lilypondparsertools_LilyPondParser__spanners__Slur_05():
    r'''Unstarted.
    '''

    string = '{ c c c c ) }'
    assert pytest.raises(Exception, 'LilyPondParser()(string)')


def test_lilypondparsertools_LilyPondParser__spanners__Slur_06():
    r'''Nested.
    '''

    string = '{ c ( c ( c ) c ) }'
    assert pytest.raises(Exception, 'LilyPondParser()(string)')


def test_lilypondparsertools_LilyPondParser__spanners__Slur_07():
    r'''With direction.
    '''

    maker = abjad.NoteMaker()
    target = abjad.Container(maker([0] * 4, [(1, 4)]))
    slur = abjad.Slur(direction=abjad.Down)
    abjad.attach(slur, target[:3])
    slur = abjad.Slur(direction=abjad.Up)
    abjad.attach(slur, target[2:])

    assert format(target) == abjad.String.normalize(
        r'''
        {
            c'4 _ (
            c'4
            c'4 ) ^ (
            c'4 )
        }
        '''
        )

    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
