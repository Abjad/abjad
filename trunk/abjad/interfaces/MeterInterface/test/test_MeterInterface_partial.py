from abjad import *
import py.test


## TODO: FIXME ##
def test_MeterInterface_partial_01( ):

   pass

#   t = Staff(macros.scale(4))
#   t.meter.forced = metertools.Meter(2, 8)
#   t.meter.partial = Rational(1, 8)
#
#   r'''
#   \new Staff {
#           \time 2/8
#           \partial 8
#           c'8
#           d'8
#           e'8
#           f'8
#   }   
#   '''
#
#   assert componenttools.is_well_formed_component(t)
#   assert t.format == "\\new Staff {\n\t\\time 2/8\n\t\\partial 8\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
