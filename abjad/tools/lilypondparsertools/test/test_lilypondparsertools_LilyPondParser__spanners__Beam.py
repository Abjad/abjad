import abjad
import pytest


def test_lilypondparsertools_LilyPondParser__spanners__Beam_01():

    maker = abjad.NoteMaker()
    target = abjad.Container(maker([0] * 4, [(1, 4)]))
    beam = abjad.Beam()
    abjad.attach(beam, target[0:3])
    beam = abjad.Beam()
    abjad.attach(beam, target[3:])

    assert format(target) == abjad.String.normalize(
        r'''
        {
            c'4 [
            c'4
            c'4 ]
            c'4 [ ]
        }
        '''
        )

    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__spanners__Beam_02():
    r'''With start and stop reversed.
    '''

    maker = abjad.NoteMaker()
    target = abjad.Container(maker([0] * 4, [(1, 4)]))
    beam = abjad.Beam()
    abjad.attach(beam, target[0:3])
    beam = abjad.Beam()
    abjad.attach(beam, target[3:])

    assert format(target) == abjad.String.normalize(
        r'''
        {
            c'4 [
            c'4
            c'4 ]
            c'4 [ ]
        }
        '''
        )

    string = r'''\relative c' { c [ c c ] c ] [ }'''
    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__spanners__Beam_03():

    maker = abjad.NoteMaker()
    target = abjad.Container(maker([0] * 4, [(1, 4)]))
    beam = abjad.Beam()
    abjad.attach(beam, target[:])
    beam = abjad.Beam()
    abjad.attach(beam, target[1:3])

    assert format(target) == abjad.String.normalize(
        r'''
        {
            c'4 [
            c'4 [
            c'4 ]
            c'4 ]
        }
        '''
        )

    assert pytest.raises(Exception, "LilyPondParser()(format(target))")


def test_lilypondparsertools_LilyPondParser__spanners__Beam_04():

    maker = abjad.NoteMaker()
    target = abjad.Container(maker([0] * 4, [(1, 4)]))
    beam = abjad.Beam()
    abjad.attach(beam, target[:3])
    beam = abjad.Beam()
    abjad.attach(beam, target[2:])

    assert format(target) == abjad.String.normalize(
        r'''
        {
            c'4 [
            c'4
            c'4 ] [
            c'4 ]
        }
        '''
        )

    assert pytest.raises(Exception, "LilyPondParser()(format(target))")


def test_lilypondparsertools_LilyPondParser__spanners__Beam_05():

    string = "{ c'4 [ c'4 c'4 c'4 }"
    assert pytest.raises(Exception, "LilyPondParser()(string)")


def test_lilypondparsertools_LilyPondParser__spanners__Beam_06():

    string = "{ c'4 c'4 c'4 c'4 ] }"
    result = abjad.lilypondparsertools.LilyPondParser()(string)
    assert not abjad.inspect(result[-1]).get_spanners()


def test_lilypondparsertools_LilyPondParser__spanners__Beam_07():
    r'''With direction.
    '''

    maker = abjad.NoteMaker()
    target = abjad.Container(maker([0] * 4, [(1, 4)]))
    beam = abjad.Beam(direction=abjad.Up)
    abjad.attach(beam, target[0:3])
    beam = abjad.Beam(direction=abjad.Down)
    abjad.attach(beam, target[3:])

    assert format(target) == abjad.String.normalize(
        r'''
        {
            c'4 ^ [
            c'4
            c'4 ]
            c'4 _ [ ]
        }
        '''
        )

    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
