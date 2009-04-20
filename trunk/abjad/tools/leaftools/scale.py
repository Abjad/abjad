## TODO: leaftools.scale( ) completely deprecated.    ##
## TODO: Use leaftools.duration_change( ) instead.    ##


#from abjad.exceptions.exceptions import AssignabilityError
#from abjad.leaf.leaf import _Leaf
#from abjad.rational.rational import Rational
#from abjad.tools import clone
#from abjad.tools import iterate
#from abjad.tools import mathtools
#from abjad.tuplet.fd.tuplet import FixedDurationTuplet
#
#
### NOTE: (or rather questions) 
### - would this be better named leaf_reset_duration( )?... 
###   we are not really scaling.
### - should multipliers be retained in setting of new duration ?
#
#def scale(leaf, dur):
#   '''Example:
#      
#      >>> leaftools.scale(Note(0, (1, 8)), Rational(5, 13))
#      FixedDurationTuplet((5, 13), [Note(0, (1, 4))])'''
#
#   assert isinstance(leaf, _Leaf) 
#   assert isinstance(dur, Rational)
#   assert dur > 0
#   try:
#      leaf.duration.written = dur
#      return leaf
#   except AssignabilityError:
#      leaf.duration.written = mathtools.converge_to_power_of_two(leaf.duration.written, dur)
#      result = FixedDurationTuplet(dur, [leaf])
#      return result
