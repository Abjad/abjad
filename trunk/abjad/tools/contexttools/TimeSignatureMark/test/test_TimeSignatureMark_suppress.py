from abjad import *
import py.test


def test_TimeSignatureMark_suppress_01():
    '''Suppress binary meter at format-time.'''

    t = Measure((7, 8), "c'8 d'8 e'8 f'8 g'8 a'8 b'8")
    contexttools.get_effective_time_signature(t).suppress = True

    r'''
    {
        c'8
        d'8
        e'8
        f'8
        g'8
        a'8
        b'8
    }
    '''

    assert t.format == "{\n\tc'8\n\td'8\n\te'8\n\tf'8\n\tg'8\n\ta'8\n\tb'8\n}"


def test_TimeSignatureMark_suppress_02():
    '''Nonbinary meter suppression at format-time raises custom exception.'''

    t = Measure((8, 9), "c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    contexttools.get_effective_time_signature(t).suppress = True

    assert py.test.raises(NonbinaryTimeSignatureSuppressionError, 't.format')
