from abjad import *
import py.test


def test_measuretools_scale_measure_by_multiplier_and_adjust_meter_01():
    '''Scale binary to nonbinary.
        No note_head rewriting necessary.'''

    t = Measure((3, 8), "c'8 d'8 e'8")
    measuretools.scale_measure_by_multiplier_and_adjust_meter(t, Duration(2, 3))

    r'''
    {
        \time 3/12
        \scaleDurations #'(2 . 3) {
            c'8
            d'8
            e'8
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 3/12\n\t\\scaleDurations #'(2 . 3) {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t}\n}"



def test_measuretools_scale_measure_by_multiplier_and_adjust_meter_02():
    '''Scale nonbinary meter to binary.
        No note_head rewriting necessary.'''

    t = Measure((3, 12), "c'8 d'8 e'8")
    measuretools.scale_measure_by_multiplier_and_adjust_meter(t, Duration(3, 2))

    r'''
    {
        \time 3/8
        c'8
        d'8
        e'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 3/8\n\tc'8\n\td'8\n\te'8\n}"


def test_measuretools_scale_measure_by_multiplier_and_adjust_meter_03():
    '''Scale binary meter to binary meter.
        Noteheads rewrite with dots.'''

    t = Measure((3, 8), "c'8 d'8 e'8")
    measuretools.scale_measure_by_multiplier_and_adjust_meter(t, Duration(3, 2))

    r'''
    {
        \time 9/16
        c'8.
        d'8.
        e'8.
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 9/16\n\tc'8.\n\td'8.\n\te'8.\n}"


def test_measuretools_scale_measure_by_multiplier_and_adjust_meter_04():
    '''Scale binary meter to binary meter.
        Noteheads rewrite without dots.'''

    t = Measure((9, 16), "c'8. d'8. e'8.")
    measuretools.scale_measure_by_multiplier_and_adjust_meter(t, Duration(2, 3))

    r'''
    {
        \time 3/8
        c'8
        d'8
        e'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 3/8\n\tc'8\n\td'8\n\te'8\n}"


def test_measuretools_scale_measure_by_multiplier_and_adjust_meter_05():
    '''Scale binary meter to nonbinary meter.
        No note_head rewriting necessary.'''

    t = Measure((9, 16), "c'16 d'16 e'16 f'16 g'16 a'16 b'16 c''16 d''16")
    measuretools.scale_measure_by_multiplier_and_adjust_meter(t, Duration(2, 3))

    r'''
    {
        \time 9/24
        \scaleDurations #'(2 . 3) {
            c'16
            d'16
            e'16
            f'16
            g'16
            a'16
            b'16
            c''16
            d''16
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 9/24\n\t\\scaleDurations #'(2 . 3) {\n\t\tc'16\n\t\td'16\n\t\te'16\n\t\tf'16\n\t\tg'16\n\t\ta'16\n\t\tb'16\n\t\tc''16\n\t\td''16\n\t}\n}"


def test_measuretools_scale_measure_by_multiplier_and_adjust_meter_06():
    '''Scale nonbinary meter to binary meter.
        Noteheads rewrite with double duration.'''

    t = Measure((3, 12), "c'8 d'8 e'8")
    measuretools.scale_measure_by_multiplier_and_adjust_meter(t, Duration(3))

    r'''
    {
        \time 3/4
        c'4
        d'4
        e'4
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 3/4\n\tc'4\n\td'4\n\te'4\n}"


def test_measuretools_scale_measure_by_multiplier_and_adjust_meter_07():
    '''Scale binary meter by one half.
        Noteheads rewrite with half duration.
        Time signature rewrites with double denominator.'''

    t = Measure((6, 16), "c'16 d'16 e'16 f'16 g'16 a'16")
    measuretools.scale_measure_by_multiplier_and_adjust_meter(t, Duration(1, 2))

    r'''
    {
        \time 6/32
        c'32
        d'32
        e'32
        f'32
        g'32
        a'32
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 6/32\n\tc'32\n\td'32\n\te'32\n\tf'32\n\tg'32\n\ta'32\n}"


def test_measuretools_scale_measure_by_multiplier_and_adjust_meter_08():
    '''Scale binary meter by one quarter.
        Noteheads rewrite with quarter duration.
        Time signature rewrites with quadruple denominator.'''

    t = Measure((6, 16), "c'16 d'16 e'16 f'16 g'16 a'16")
    measuretools.scale_measure_by_multiplier_and_adjust_meter(t, Duration(1, 4))

    r'''
    {
        \time 6/64
        c'64
        d'64
        e'64
        f'64
        g'64
        a'64
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 6/64\n\tc'64\n\td'64\n\te'64\n\tf'64\n\tg'64\n\ta'64\n}"


def test_measuretools_scale_measure_by_multiplier_and_adjust_meter_09():
    '''Scale binary meter by two.
        Noteheads rewrite with double duration.
        Time signature rewrites with half denominator.'''

    t = Measure((6, 16), "c'16 d'16 e'16 f'16 g'16 a'16")
    measuretools.scale_measure_by_multiplier_and_adjust_meter(t, Duration(2))

    r'''
    {
        \time 6/8
        c'8
        d'8
        e'8
        f'8
        g'8
        a'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 6/8\n\tc'8\n\td'8\n\te'8\n\tf'8\n\tg'8\n\ta'8\n}"


def test_measuretools_scale_measure_by_multiplier_and_adjust_meter_10():
    '''Scale binary meter by four.
        Noteheads rewrite with quadruple duration.
        Time signature rewrites with quarter denominator.'''

    t = Measure((6, 16), "c'16 d'16 e'16 f'16 g'16 a'16")
    measuretools.scale_measure_by_multiplier_and_adjust_meter(t, Duration(4))

    r'''
    {
        \time 6/4
        c'4
        d'4
        e'4
        f'4
        g'4
        a'4
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 6/4\n\tc'4\n\td'4\n\te'4\n\tf'4\n\tg'4\n\ta'4\n}"


def test_measuretools_scale_measure_by_multiplier_and_adjust_meter_11():
    '''Raise ZeroDivisionError when multiplier equals zero.'''

    t = Measure((6, 16), "c'16 d'16 e'16 f'16 g'16 a'16")
    py.test.raises(ZeroDivisionError, 'measuretools.scale_measure_by_multiplier_and_adjust_meter(t, 0)')
