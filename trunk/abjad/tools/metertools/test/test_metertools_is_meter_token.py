from abjad import *


def test_metertools_is_meter_token_01( ):

   assert metertools.is_meter_token(metertools.Meter(3, 8))
   assert metertools.is_meter_token(Fraction(3, 8))
   assert metertools.is_meter_token((3, 8))


def test_metertools_is_meter_token_02( ):

   assert not metertools.is_meter_token('text')
