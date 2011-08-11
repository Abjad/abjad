from abjad import *
from abjad.tools import metertools


def test_metertools_get_nonbinary_factor_from_meter_denominator_01( ):
    '''Return nonbinary factor in denominator of meter, else 1.'''

    assert metertools.get_nonbinary_factor_from_meter_denominator(contexttools.TimeSignatureMark(3, 12)) == 3
    assert metertools.get_nonbinary_factor_from_meter_denominator(contexttools.TimeSignatureMark(3, 18)) == 9
    assert metertools.get_nonbinary_factor_from_meter_denominator(contexttools.TimeSignatureMark(3, 19)) == 19
    assert metertools.get_nonbinary_factor_from_meter_denominator(contexttools.TimeSignatureMark(3, 20)) == 5
    assert metertools.get_nonbinary_factor_from_meter_denominator(contexttools.TimeSignatureMark(3, 21)) == 21
    assert metertools.get_nonbinary_factor_from_meter_denominator(contexttools.TimeSignatureMark(3, 24)) == 3
    assert metertools.get_nonbinary_factor_from_meter_denominator(contexttools.TimeSignatureMark(3, 28)) == 7


def test_metertools_get_nonbinary_factor_from_meter_denominator_02( ):
    '''Return nonbinary factor in denominator of meter, else 1.'''

    assert metertools.get_nonbinary_factor_from_meter_denominator(contexttools.TimeSignatureMark(3, 8)) == 1


