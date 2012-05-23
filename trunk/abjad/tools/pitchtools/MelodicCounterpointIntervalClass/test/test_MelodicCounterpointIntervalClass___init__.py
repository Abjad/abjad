from abjad import *


def test_MelodicCounterpointIntervalClass___init___01():
    '''Works with numbers 1 - 8.'''

    mcpic = pitchtools.MelodicCounterpointIntervalClass(1)
    assert mcpic.number == 1

    mcpic = pitchtools.MelodicCounterpointIntervalClass(2)
    assert mcpic.number == 2

    mcpic = pitchtools.MelodicCounterpointIntervalClass(3)
    assert mcpic.number == 3

    mcpic = pitchtools.MelodicCounterpointIntervalClass(4)
    assert mcpic.number == 4

    mcpic = pitchtools.MelodicCounterpointIntervalClass(5)
    assert mcpic.number == 5

    mcpic = pitchtools.MelodicCounterpointIntervalClass(6)
    assert mcpic.number == 6

    mcpic = pitchtools.MelodicCounterpointIntervalClass(7)
    assert mcpic.number == 7

    mcpic = pitchtools.MelodicCounterpointIntervalClass(8)
    assert mcpic.number == 8


def test_MelodicCounterpointIntervalClass___init___02():
    '''Works with numbers -1 to -8.'''

    mcpic = pitchtools.MelodicCounterpointIntervalClass(-1)
    assert mcpic.number == 1

    mcpic = pitchtools.MelodicCounterpointIntervalClass(-2)
    assert mcpic.number == -2

    mcpic = pitchtools.MelodicCounterpointIntervalClass(-3)
    assert mcpic.number == -3

    mcpic = pitchtools.MelodicCounterpointIntervalClass(-4)
    assert mcpic.number == -4

    mcpic = pitchtools.MelodicCounterpointIntervalClass(-5)
    assert mcpic.number == -5

    mcpic = pitchtools.MelodicCounterpointIntervalClass(-6)
    assert mcpic.number == -6

    mcpic = pitchtools.MelodicCounterpointIntervalClass(-7)
    assert mcpic.number == -7

    mcpic = pitchtools.MelodicCounterpointIntervalClass(-8)
    assert mcpic.number == -8


def test_MelodicCounterpointIntervalClass___init___03():
    '''Works with numbers greater than 8.'''

    mcpic = pitchtools.MelodicCounterpointIntervalClass(9)
    assert mcpic.number == 2

    mcpic = pitchtools.MelodicCounterpointIntervalClass(10)
    assert mcpic.number == 3

    mcpic = pitchtools.MelodicCounterpointIntervalClass(11)
    assert mcpic.number == 4

    mcpic = pitchtools.MelodicCounterpointIntervalClass(12)
    assert mcpic.number == 5

    mcpic = pitchtools.MelodicCounterpointIntervalClass(13)
    assert mcpic.number == 6

    mcpic = pitchtools.MelodicCounterpointIntervalClass(14)
    assert mcpic.number == 7

    mcpic = pitchtools.MelodicCounterpointIntervalClass(15)
    assert mcpic.number == 8


def test_MelodicCounterpointIntervalClass___init___04():
    '''Works with numbers less than -8.'''

    mcpic = pitchtools.MelodicCounterpointIntervalClass(-9)
    assert mcpic.number == -2

    mcpic = pitchtools.MelodicCounterpointIntervalClass(-10)
    assert mcpic.number == -3

    mcpic = pitchtools.MelodicCounterpointIntervalClass(-11)
    assert mcpic.number == -4

    mcpic = pitchtools.MelodicCounterpointIntervalClass(-12)
    assert mcpic.number == -5

    mcpic = pitchtools.MelodicCounterpointIntervalClass(-13)
    assert mcpic.number == -6

    mcpic = pitchtools.MelodicCounterpointIntervalClass(-14)
    assert mcpic.number == -7

    mcpic = pitchtools.MelodicCounterpointIntervalClass(-15)
    assert mcpic.number == -8
