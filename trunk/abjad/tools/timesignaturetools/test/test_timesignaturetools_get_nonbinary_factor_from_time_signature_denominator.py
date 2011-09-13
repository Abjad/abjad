from abjad import *
from abjad.tools import timesignaturetools


def test_timesignaturetools_get_nonbinary_factor_from_time_signature_denominator_01():
    '''Return nonbinary factor in denominator of meter, else 1.'''

    assert timesignaturetools.get_nonbinary_factor_from_time_signature_denominator(contexttools.TimeSignatureMark((3, 12))) == 3
    assert timesignaturetools.get_nonbinary_factor_from_time_signature_denominator(contexttools.TimeSignatureMark((3, 18))) == 9
    assert timesignaturetools.get_nonbinary_factor_from_time_signature_denominator(contexttools.TimeSignatureMark((3, 19))) == 19
    assert timesignaturetools.get_nonbinary_factor_from_time_signature_denominator(contexttools.TimeSignatureMark((3, 20))) == 5
    assert timesignaturetools.get_nonbinary_factor_from_time_signature_denominator(contexttools.TimeSignatureMark((3, 21))) == 21
    assert timesignaturetools.get_nonbinary_factor_from_time_signature_denominator(contexttools.TimeSignatureMark((3, 24))) == 3
    assert timesignaturetools.get_nonbinary_factor_from_time_signature_denominator(contexttools.TimeSignatureMark((3, 28))) == 7


def test_timesignaturetools_get_nonbinary_factor_from_time_signature_denominator_02():
    '''Return nonbinary factor in denominator of meter, else 1.'''

    assert timesignaturetools.get_nonbinary_factor_from_time_signature_denominator(contexttools.TimeSignatureMark((3, 8))) == 1
