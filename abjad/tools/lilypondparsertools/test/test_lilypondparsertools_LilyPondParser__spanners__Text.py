import abjad
import pytest


def test_lilypondparsertools_LilyPondParser__spanners__Text_01():
    r'''Successful text spanners, showing single leaf overlap.
    '''

    maker = abjad.NoteMaker()
    target = abjad.Container(maker([0] * 4, [(1, 4)]))
    text_spanner = abjad.TextSpanner()
    abjad.attach(text_spanner, target[2:])
    text_spanner = abjad.TextSpanner()
    abjad.attach(text_spanner, target[:3])

    assert format(target) == abjad.String.normalize(
        r'''
        {
            c'4 \startTextSpan
            c'4
            c'4 \stopTextSpan \startTextSpan
            c'4 \stopTextSpan
        }
        '''
        )

    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__spanners__Text_02():
    r'''Swapped start and stop.
    '''

    maker = abjad.NoteMaker()
    target = abjad.Container(maker([0] * 4, [(1, 4)]))
    text_spanner = abjad.TextSpanner()
    abjad.attach(text_spanner, target[2:])
    text_spanner = abjad.TextSpanner()
    abjad.attach(text_spanner, target[:3])

    assert format(target) == abjad.String.normalize(
        r'''
        {
            c'4 \startTextSpan
            c'4
            c'4 \stopTextSpan \startTextSpan
            c'4 \stopTextSpan
        }
        '''
        )

    string = r"\relative c' { c \startTextSpan c c \startTextSpan \stopTextSpan c \stopTextSpan }"

    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__spanners__Text_03():
    r'''Single leaf.
    '''

    string = r'{ c \startTextSpan \stopTextSpan c c c }'
    assert pytest.raises(Exception, 'LilyPondParser()(string)')


def test_lilypondparsertools_LilyPondParser__spanners__Text_04():
    r'''Unterminated.
    '''

    string = r'{ c \startTextSpan c c c }'
    assert pytest.raises(Exception, 'LilyPondParser()(string)')


def test_lilypondparsertools_LilyPondParser__spanners__Text_05():
    r'''Unstarted.
    '''

    string = r'{ c c c c \stopTextSpan }'
    assert pytest.raises(Exception, 'LilyPondParser()(string)')


def test_lilypondparsertools_LilyPondParser__spanners__Text_06():
    r'''Nested.
    '''

    string = r'{ c \startTextSpan c \startTextSpan c \stopTextSpan c \stopTextSpan }'
    assert pytest.raises(Exception, 'LilyPondParser()(string)')
